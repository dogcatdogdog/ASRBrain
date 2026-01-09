import numpy as np
from datetime import datetime
from utils.LogTool import LogTool
from utils.AudioTool import AudioTool
from core.AsrService import AsrService

class StreamProcessor:
    @staticmethod
    def run(filePath, onResultCallback, chunkSize=8000, silenceThreshold=0.005, silenceCountTrigger=3):
        """
        运行流式识别主循环
        """
        LogTool.info(f"StreamProcessor started for: {filePath}")
        
        audioBuffer = []
        silenceCount = 0
        currentTime = 0.0
        sampleRate = 16000 # 假设 16k
        chunkDuration = chunkSize / sampleRate

        def processBuffer(buffer, isFinal=False):
            """内部函数：处理当前的 audioBuffer"""
            if len(buffer) == 0:
                return

            fullData = np.concatenate(buffer)
            bufferLen = len(fullData)
            bufferDuration = bufferLen / sampleRate
            
            # 计算这段 buffer 在整个流中的绝对起始时间
            bufferStartTime = currentTime - bufferDuration

            # 只有当 buffer 长度足够长才识别 (例如 0.5s)
            if bufferDuration > 0.5:
                segments = AsrService.transcribe(fullData)
                
                # 遍历所有识别出的片段 (Whisper 内部 VAD 切分出的句子)
                for seg in segments:
                    # 计算该句子的绝对时间
                    absStart = bufferStartTime + seg['start']
                    absEnd = bufferStartTime + seg['end']
                    
                    outData = {
                        "timestamp": datetime.now().isoformat(),
                        "audioTimeStart": round(absStart, 2),
                        "audioTimeEnd": round(absEnd, 2),
                        "text": seg['text'],
                        "type": "final" if isFinal else "interim" 
                        # 注: 在这种模拟流式中，VAD 切割后的处理通常都可视为这一段的 final
                        # 真正的 interim 是指 Whisper 的实时流式 partial result，这里暂不涉及
                    }
                    onResultCallback(outData)

        for chunk in AudioTool.readFileGenerator(filePath, chunkSize=chunkSize):
            audioBuffer.append(chunk)
            currentTime += chunkDuration
            
            # VAD 检测
            if AudioTool.isSilent(chunk, threshold=silenceThreshold):
                silenceCount += 1
            else:
                silenceCount = 0
            
            # 触发识别
            if silenceCount >= silenceCountTrigger and len(audioBuffer) > 0:
                processBuffer(audioBuffer, isFinal=True) # 切割点，视为 Final
                audioBuffer = []
                silenceCount = 0

        # 处理末尾残留
        if audioBuffer:
            processBuffer(audioBuffer, isFinal=True)
        
        LogTool.info("StreamProcessor finished.")