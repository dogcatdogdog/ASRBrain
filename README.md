# ASRBrain (Project Gemini) - 离线智能语音底座

**Building the Auditory Cortex for Offline AI Agents**

ASRBrain 是一个专为 **离线环境 (Air-gapped)** 设计的高性能语音识别引擎。它不仅是一个语音转文字工具，更是为本地化 AI Agent 打造的“听觉中枢”。

---

## 🧠 技术架构 (Technical Architecture)

本项目采用 **Python Sidecar** 模式，核心技术栈如下：

*   **推理引擎**: `faster-whisper`
    *   基于 [CTranslate2](https://github.com/OpenNMT/CTranslate2) (C++ 推理库)，比原始 OpenAI Whisper 快 4 倍，内存占用更少。
    *   默认启用 **INT8 量化**，确保在普通 CPU 上也能实现接近实时的推理速度。
*   **流式处理**: `StreamProcessor`
    *   自研流式逻辑，采用 **滑动窗口 + VAD (语音活动检测)** 策略。
    *   能够自动将连续音频流切分为独立句子，并保留精确的绝对时间戳。
*   **工程规范**:
    *   严格的 MVC 分层设计。
    *   静态工具类封装 (`LogTool`, `ConfigTool`)，便于未来向 C++ 迁移。

---

## 🚀 用户指南 (User Guide)

### 1. 环境安装 (Installation)

推荐使用 Conda 进行环境隔离：

```bash
# 1. 克隆代码
git clone https://github.com/dogcatdogdog/ASRBrain.git
cd ASRBrain

# 2. 创建环境 (Python 3.10)
conda create -n asr_brain python=3.10
conda activate asr_brain

# 3. 安装依赖
# 包含 torch, faster-whisper, soundfile 等核心库
pip install -r app/code/requirements.txt
```

### 2. 模型准备 (Model Setup)

无需手动下载！ASRBrain 具有**自动模型管理**功能。

*   **自动下载**: 首次运行程序时，它会自动检测 `app/models/` 目录。如果模型不存在，会自动从 HuggingFace 镜像下载 `small` 模型（约 480MB）。
*   **手动切换**: 如果您的机器配置较低，或者需要更高精度，请修改 `app/config/models.yaml`：
    ```yaml
    modelConfig:
      # 可选: tiny, base, small, medium, large-v3
      modelSize: "small" 
      # 显式指定 INT8 量化以加速 CPU 推理
      computeType: "int8"
    ```

### 3. 数据准备 (Data Preparation)

为了测试效果，您需要准备一些音频文件：
*   **格式**: 推荐 `.wav` 格式。
*   **采样率**: 16000Hz (最佳) 或 24000Hz+ (程序会自动读取，但 16k 最原生)。
*   **存放位置**: 建议放入 `app/data/dataset/` 目录（需自行创建）。

### 4. 运行测试 (Usage)

#### 场景 A: 快速测试单个文件
想看看某个录音识别准不准？使用单文件模式。

```bash
# Windows 用户推荐命令 (防止控制台乱码)
chcp 65001

# 运行命令 (-i 指定输入文件)
python app/code/main.py -i "app/data/dataset/story.wav"
```
*   **效果**: 屏幕上会像字幕一样逐句打印识别结果。
*   **结果**: 完整的时间轴数据会保存到 `app/out/session_xxx.jsonl`。

#### 场景 B: 批量回归测试
想一次性测试 100 个文件？使用批量模式。

```bash
# 运行命令 (--batch 指定目录)
python app/code/main.py --batch "app/data/dataset"
```
*   **效果**: 自动扫描目录下所有 wav 文件。
*   **报告**: 在 `app/out/batch_xxx/` 下生成 `summary.csv` (汇总表) 和 `details/` (详细时间轴)。

---

## ⚠️ 当前局限 (Current Limitations)

**注意：本项目目前处于 Phase 1 中期。**

1.  **仿真流式**: 目前通过读取文件模拟流式输入，**尚未接入真实麦克风**。无法对着电脑说话直接出字。
2.  **延迟**: 采用“静音后识别”策略，长句需要说完才能上屏，缺乏即时的“中间结果”反馈。

---

## 📅 近期计划 (Coming Soon)

1.  **真实流式接入**: 开发 WebSocket 接口，对接前端麦克风实时流。
2.  **Interim Results**: 实现“边说边出字”的实时反馈效果。
3.  **Neural VAD**: 引入神经网络 VAD 替代能量检测，提升抗噪能力。

---

## 📄 License

MIT License