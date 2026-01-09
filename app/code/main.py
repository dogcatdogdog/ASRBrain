import sys
import os
import argparse
from datetime import datetime

# --- 修复 Windows 控制台乱码问题 ---
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.LogTool import LogTool
from utils.ConfigTool import ConfigTool
from utils.FileTool import FileTool
from core.AsrService import AsrService
from core.StreamProcessor import StreamProcessor
from core.BatchProcessor import BatchProcessor

def main():
    parser = argparse.ArgumentParser(description="ASRBrain CLI - Offline Speech Recognition")
    
    # 互斥组：单文件模式 vs 批量模式
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--input", help="Single input audio file path")
    group.add_argument("--batch", help="Batch input directory path (processes all .wav files)")
    
    parser.add_argument("-o", "--output", help="Output JSONL file path (only for single file mode)")
    
    args = parser.parse_args()

    LogTool.info("=== ASRBrain CLI Start ===")
    
    # 1. 加载配置
    ConfigTool.load("appDev.yaml")
    ConfigTool.load("models.yaml")

    # 2. 初始化模型
    if not AsrService.initModel():
        LogTool.error("Model init failed. Check models.yaml and app/models directory.")
        return

    # 3. 执行逻辑分支
    if args.batch:
        # --- 批量模式 ---
        inputDir = args.batch
        if not os.path.exists(inputDir):
            LogTool.error(f"Batch input directory not found: {inputDir}")
            return
        
        LogTool.info(f"Entering Batch Mode: {inputDir}")
        BatchProcessor.run(inputDir)

    else:
        # --- 单文件模式 (默认) ---
        inputFile = args.input
        if not inputFile:
            # 尝试从配置获取默认测试文件
            inputFile = ConfigTool.get("test.audioFile")
            if not inputFile or not os.path.exists(inputFile):
                parser.print_help()
                return
            LogTool.info(f"Using default input file: {inputFile}")

        if not os.path.exists(inputFile):
            LogTool.error(f"Input file not found: {inputFile}")
            return

        # 确定输出路径
        outputFile = args.output
        if not outputFile:
            sessionTime = datetime.now().strftime("%Y%m%d_%H%M%S")
            outputFile = os.path.join("app/out", f"session_{sessionTime}.jsonl")
        
        # 定义回调
        def onResult(data):
            print(f"\n[Result {data['audioTimeEnd']}s]: {data['text']}")
            FileTool.appendJsonLine(outputFile, data)

        # 运行识别
        chunkSize = ConfigTool.get("test.chunkSize", 8000)
        silenceThreshold = ConfigTool.get("test.silenceThreshold", 0.005)
        
        LogTool.info(f"Starting single file recognition: {inputFile}")
        StreamProcessor.run(inputFile, onResult, chunkSize=chunkSize, silenceThreshold=silenceThreshold)
        LogTool.info(f"Recognition finished. Saved to: {outputFile}")

    LogTool.info("=== ASRBrain CLI Finished ===")

if __name__ == "__main__":
    main()