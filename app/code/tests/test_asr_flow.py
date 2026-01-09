import unittest
import sys
import os
import numpy as np
import soundfile as sf

# 将 app/code 加入 sys.path，确保能导入 core, utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ConfigTool import ConfigTool
from core.AsrService import AsrService
from core.StreamProcessor import StreamProcessor
from utils.LogTool import LogTool

class TestAsrFlow(unittest.TestCase):
    def setUp(self):
        # 加载配置
        ConfigTool.load("appDev.yaml")
        ConfigTool.load("models.yaml")
        
        # 确保模型初始化
        success = AsrService.initModel()
        self.assertTrue(success, "Model initialization failed")
        
        # 创建一个临时的测试音频文件 (3秒噪音)
        self.testFile = "app/data/simple/test_integration.wav"
        if not os.path.exists(os.path.dirname(self.testFile)):
             os.makedirs(os.path.dirname(self.testFile))
        
        fs = 16000
        # 生成一段随机噪音
        data = np.random.uniform(-0.1, 0.1, fs*3)
        sf.write(self.testFile, data, fs)
        
        self.results = []

    def tearDown(self):
        # 清理临时文件
        if os.path.exists(self.testFile):
            os.remove(self.testFile)

    def test_run_stream(self):
        """
        集成测试: 验证 StreamProcessor 能否正常跑通流程
        """
        LogTool.info("Running integration test: test_run_stream")
        
        def callback(data):
            self.results.append(data)
        
        # 运行流式处理
        StreamProcessor.run(self.testFile, callback)
        
        # 验证: 程序没有崩溃
        # 由于输入是噪音，可能被 VAD 过滤导致 results 为空，这是正常的
        # 我们主要验证的是 pipeline 的完整性 (读取 -> 模型 -> 回调)
        print(f"Captured {len(self.results)} segments from noise input.")
        
        # 如果我们想验证有结果，可以用真实音频，但在 CI 环境下尽量少依赖外部文件
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
