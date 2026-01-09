from faster_whisper import WhisperModel
from utils.LogTool import LogTool
from utils.ConfigTool import ConfigTool
import os

class AsrService:
    _model = None

    @staticmethod
    def initModel():
        """
        根据配置加载 Whisper 模型
        """
        if AsrService._model is not None:
            return True
            
        try:
            modelSize = ConfigTool.get("modelConfig.modelSize", "base")
            device = ConfigTool.get("modelConfig.device", "cpu")
            computeType = ConfigTool.get("modelConfig.computeType", "int8")
            
            # 使用 ConfigTool 获取路径，默认为 app/models
            modelPath = ConfigTool.get("modelConfig.modelPath", "app/models")
            
            # 确保目录存在
            if not os.path.exists(modelPath):
                os.makedirs(modelPath)

            LogTool.info(f"Loading Whisper model: {modelSize} from {modelPath} on {device} ({computeType})...")
            
            AsrService._model = WhisperModel(
                modelSize, 
                device=device, 
                compute_type=computeType,
                download_root=modelPath
            )
            
            LogTool.info("Model loaded successfully.")
            return True
        except Exception as e:
            LogTool.error("Failed to load Whisper model", e)
            return False

    @staticmethod
    def transcribe(audioData):
        """
        对音频 numpy 数组进行识别
        返回: list of dict [{'text': str, 'start': float, 'end': float}, ...]
        """
        if AsrService._model is None:
            if not AsrService.initModel():
                return []

        try:
            beamSize = ConfigTool.get("asrParams.beamSize", 5)
            language = ConfigTool.get("asrParams.language", "zh")
            
            # 读取配置中的提示语
            initialPrompt = ConfigTool.get("asrParams.initialPrompt", "")
            
            segments, info = AsrService._model.transcribe(
                audioData, 
                beam_size=beamSize, 
                language=language,
                vad_filter=ConfigTool.get("asrParams.vadFilter", True),
                vad_parameters=dict(min_silence_duration_ms=ConfigTool.get("asrParams.vadMinSilenceDurationMs", 500)),
                initial_prompt=initialPrompt
            )

            # faster-whisper 的 segments 是一个生成器，必须遍历才能触发推理
            resultSegments = []
            for segment in segments:
                resultSegments.append({
                    "text": segment.text,
                    "start": segment.start,
                    "end": segment.end
                })
            
            return resultSegments
        except Exception as e:
            LogTool.error("Transcription error", e)
            return []