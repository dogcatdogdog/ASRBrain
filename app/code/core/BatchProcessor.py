import os
import glob
import csv
from datetime import datetime
from utils.LogTool import LogTool
from utils.FileTool import FileTool
from core.StreamProcessor import StreamProcessor

class BatchProcessor:
    @staticmethod
    def run(inputDir, outputBaseDir="app/out"):
        """
        批量处理指定目录下的所有音频文件
        :param inputDir: 输入包含 .wav 的目录
        :param outputBaseDir: 输出根目录
        """
        # 1. 扫描文件
        searchPath = os.path.join(inputDir, "*.wav")
        audioFiles = glob.glob(searchPath)
        
        if not audioFiles:
            LogTool.info(f"No .wav files found in {inputDir}.")
            return None

        LogTool.info(f"BatchProcessor started. Found {len(audioFiles)} files in {inputDir}")

        # 2. 创建本次批处理的唯一输出目录 (batch_时间戳)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batchOutDir = os.path.join(outputBaseDir, f"batch_{timestamp}")
        detailsOutDir = os.path.join(batchOutDir, "details")
        
        # 确保目录存在
        FileTool.ensureDir(os.path.join(detailsOutDir, "placeholder"))

        LogTool.info(f"Batch output directory: {batchOutDir}")

        # 3. 准备 CSV 汇总数据
        summaryData = []

        # 4. 循环处理每个文件
        for filePath in audioFiles:
            fileName = os.path.basename(filePath)
            LogTool.info(f"Batch processing file: {fileName}")
            
            # 详情 JSONL 路径 (放入子文件夹 details)
            detailJsonl = os.path.join(detailsOutDir, f"{fileName}.jsonl")
            
            # 用于汇总 CSV 的全文缓存
            fullTextParts = []

            def batchCallback(data):
                # A. 写入 JSONL 详情
                FileTool.appendJsonLine(detailJsonl, data)
                
                # B. 收集 Final 文本用于 CSV 汇总
                if data['type'] == 'final':
                    fullTextParts.append(data['text'])

            try:
                # 调用核心流式处理器 (模拟流式读取)
                StreamProcessor.run(filePath, batchCallback)
                
                # 记录汇总结果
                fullText = "".join(fullTextParts).strip()
                summaryData.append({
                    "filename": fileName,
                    "full_text": fullText,
                    "status": "success"
                })
            except Exception as e:
                LogTool.error(f"Failed to process {fileName}", e)
                summaryData.append({
                    "filename": fileName, 
                    "full_text": f"Error: {str(e)}",
                    "status": "error"
                })

        # 5. 生成 CSV 汇总报告 (带 BOM 确保 Excel 中文不乱码)
        csvFile = os.path.join(batchOutDir, "summary.csv")
        try:
            with open(csvFile, 'w', newline='', encoding='utf-8-sig') as f:
                fieldnames = ["filename", "full_text", "status"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(summaryData)
            
            LogTool.info(f"Batch processing complete. Report: {csvFile}")
            print(f"\n[Batch Complete]")
            print(f"Directory: {batchOutDir}")
            print(f"Summary CSV: summary.csv")
            return batchOutDir
        except Exception as e:
            LogTool.error("Failed to write summary CSV", e)
            return None
