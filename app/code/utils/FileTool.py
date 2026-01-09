import os
import json
from utils.LogTool import LogTool

class FileTool:
    @staticmethod
    def ensureDir(filePath):
        """
        确保文件所在的目录存在
        """
        directory = os.path.dirname(filePath)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                LogTool.error(f"Failed to create directory: {directory}", e)

    @staticmethod
    def appendJsonLine(filePath, dataDict):
        """
        向文件追加一行 JSON 数据 (JSONL 格式)
        """
        try:
            FileTool.ensureDir(filePath)
            with open(filePath, 'a', encoding='utf-8') as f:
                jsonLine = json.dumps(dataDict, ensure_ascii=False)
                f.write(jsonLine + "\n")
            return True
        except Exception as e:
            LogTool.error(f"Failed to append to file: {filePath}", e)
            return False
