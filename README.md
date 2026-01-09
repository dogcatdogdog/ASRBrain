# ASRBrain (Project Gemini)

**离线、高性能、隐私优先的智能语音识别底座**

ASRBrain 是一个旨在构建本地化智能交互核心的工程项目。它集成了 OpenAI 的 Whisper 模型（通过 faster-whisper 优化），实现了在纯 CPU 环境下的高效流式语音转文字能力。

本项目严格遵循工程化规范，为构建下一代离线 AI 助手（Agent + ASR + TTS）奠定基础。

---

## ✨ 核心特性 (Features)

*   **🔒 纯离线运行**: 所有模型和依赖均部署在本地，无需联网，保障数据隐私。
*   **🚀 高性能推理**: 基于 `faster-whisper` (CTranslate2) 和 `int8` 量化技术，在普通 CPU 上即可实现 0.3x ~ 0.5x 实时率的转写。
*   **🌊 模拟流式处理**: 内置 VAD (语音活动检测) 和流式切片逻辑，支持长音频的实时分段输出。
*   **🛠️ 强大的 CLI 工具**:
    *   支持单文件实时识别与控制台输出。
    *   支持目录级批量扫描，自动生成 CSV 汇总报表和 JSONL 详情。
*   **🇨🇳 中文优化**: 针对简体中文输出进行了专门的 Prompt 调优，解决了 Whisper 常见的繁简混杂问题。

---

## 🚀 快速开始 (Quick Start)

### 1. 环境准备

推荐使用 Python 3.10+。

```bash
# 1. 克隆项目
git clone https://github.com/your-username/ASRBrain.git
cd ASRBrain

# 2. 创建虚拟环境 (可选但推荐)
python -m venv venv
# Windows 激活:
venv\Scripts\activate
# Linux/Mac 激活:
source venv/bin/activate

# 3. 安装依赖
pip install -r app/code/requirements.txt
```

### 2. 模型准备

项目配置默认使用 `small` 模型。首次运行时，程序会自动下载模型到 `app/models/` 目录。
如果您在离线环境，请预先下载模型并手动放入该目录。

### 3. 使用 CLI 工具

#### 单文件识别
适合测试效果，结果会实时打印并保存到 `app/out/`。

```bash
# Windows 用户建议先切换代码页以避免乱码
chcp 65001

# 运行识别
python app/code/main.py -i "path/to/your/audio.wav"
```

#### 批量处理
适合大规模回归测试，会自动扫描目录下的所有 `.wav` 文件。

```bash
python app/code/main.py --batch "path/to/audio/folder"
```
运行结束后，您将在 `app/out/batch_YYYYMMDD_HHMMSS/` 下找到：
*   `summary.csv`: 所有文件的识别文本汇总。
*   `details/*.jsonl`: 每个文件带时间戳的详细切片数据。

---

## 📂 目录结构

```text
app/
├── code/                # 源代码
│   ├── core/            # 核心业务 (AsrService, StreamProcessor)
│   ├── utils/           # 通用工具 (Log, Config, File)
│   ├── tests/           # 测试套件
│   └── main.py          # CLI 入口
├── config/              # 配置文件 (appDev.yaml, models.yaml)
├── models/              # 模型存储目录
├── data/                # 本地测试数据
├── logs/                # 运行时日志
└── out/                 # 识别结果输出 (JSONL, CSV)
```

---

## 🐛 已知问题 (Known Issues)

*   **Windows 控制台乱码**: 在部分 Windows 终端（cmd/PowerShell）中，实时打印的中文可能会显示为乱码或方框。
    *   *Workaround*: 请直接查看 `app/out/` 下生成的 `.jsonl` 文件，文件内容的编码是正常的 UTF-8。或者运行 `chcp 65001` 尝试修复显示。
*   **VAD 阈值**: 当前的能量 VAD 对背景音乐较敏感。如果您的音频背景噪声明确，可能需要调整 `appDev.yaml` 中的 `silenceThreshold`。

---

## 🗺️ 路线图 (Roadmap)

### Phase 1: Python Sidecar (进行中)
- [x] 核心 ASR 引擎 (faster-whisper集成)
- [x] 流式切片与 VAD 逻辑
- [x] CLI 命令行工具 (单文件/批量)
- [ ] **Next**: 构建 FastAPI WebSocket 接口，为前端提供实时服务
- [ ] **Next**: 接入 LLM (本地大模型)，实现对识别结果的语义理解


---

## 📄 License

MIT
