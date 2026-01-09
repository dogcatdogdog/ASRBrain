import unittest
import sys
import os

# 路径挂载
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ConfigTool import ConfigTool
from core.AsrService import AsrService
from core.BatchProcessor import BatchProcessor
from utils.LogTool import LogTool

class TestDatasetBatch(unittest.TestCase):
    def setUp(self):
        ConfigTool.load("appDev.yaml")
        ConfigTool.load("models.yaml")
        # 初始化模型
        AsrService.initModel()
        # 确保数据集目录存在
        self.datasetDir = "app/data/dataset"
        if not os.path.exists(self.datasetDir):
            os.makedirs(self.datasetDir)

    def test_batch_logic(self):
        """
        集成测试: 验证 BatchProcessor 能否正常生成目录结构和 CSV
        """
        LogTool.info("Running BatchProcessor integration test...")
        
        # 运行批量处理器
        resultDir = BatchProcessor.run(self.datasetDir)
        
        if resultDir:
            # 验证结果文件夹结构
            self.assertTrue(os.path.exists(resultDir))
            self.assertTrue(os.path.exists(os.path.join(resultDir, "summary.csv")))
            self.assertTrue(os.path.isdir(os.path.join(resultDir, "details")))
            LogTool.info(f"Test Success: Batch results generated at {resultDir}")
        else:
            LogTool.info("Test Finished: No files to process in dataset dir.")

if __name__ == '__main__':
    unittest.main()