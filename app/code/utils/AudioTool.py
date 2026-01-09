import numpy as np
import soundfile as sf
from utils.LogTool import LogTool

class AudioTool:
    @staticmethod
    def readFileGenerator(filePath, chunkSize=16000):
        """
        生成器：按 Chunk 读取音频文件，模拟流式输入
        filePath: 文件路径
        chunkSize: 每次读取的采样点数 (16000 表示 1秒音频)
        """
        try:
            with sf.SoundFile(filePath) as f:
                # 获取音频属性
                sampleRate = f.samplerate
                LogTool.info(f"Start reading file: {filePath}, SampleRate: {sampleRate}")
                
                # 如果不是 16k，Whisper 需要重采样，这里简单起见假设输入是 16k
                # 生产环境建议在此处加入 resample 逻辑
                while f.tell() < f.frames:
                    data = f.read(chunkSize, dtype='float32')
                    # 如果是多声道，转单声道
                    if len(data.shape) > 1:
                        data = data.mean(axis=1)
                    yield data
        except Exception as e:
            LogTool.error(f"Error reading audio file: {filePath}", e)
            return None

    @staticmethod
    def getRms(audioData):
        """
        计算音频块的均方根能量 (Root Mean Square)
        用于判断是否有声音
        """
        if len(audioData) == 0:
            return 0
        return np.sqrt(np.mean(np.square(audioData)))

    @staticmethod
    def isSilent(audioData, threshold=0.01):
        """
        判断当前音频块是否为静音
        """
        return AudioTool.getRms(audioData) < threshold
