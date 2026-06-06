# 环境与依赖

项目所有依赖通过 `bash env/setup.sh` 一键安装（幂等，新机器从零开始只需 `git clone && bash env/setup.sh`）。

## 依赖分层

| 层级 | 管理方式 | 配置文件 |
|------|---------|---------|
| Python 包 | uv | `pyproject.toml` + `uv.lock` |
| Node.js 包 | npm | `package.json` |
| 系统工具 | brew / apt | `env/setup.sh` 中声明 |
| 模型文件 | curl 下载到本地缓存 | `env/setup.sh` 中声明 |

### 模型文件

本地推理用的预训练模型权重，体积大（GB级）且不入 git。分两类存放：

**1. Whisper.cpp 模型（`~/.cache/whisper-cpp/`）**

`transcribe_podcast.py` 使用的轻量语音转文字模型，由 `setup.sh` 自动下载。

| 模型 | 大小 | 质量 | 用途 |
|------|------|------|------|
| `ggml-base.bin`（默认） | 141MB | 良好 | 日常单人转录 |
| `ggml-small.bin` | 244MB | 很好 | 正式转录 |
| `ggml-large.bin` | 1.5GB | 最佳 | 高质量需求 |

转录时通过 `--model base/small/large` 切换。

**2. ASR 大模型（`~/Models/`，由 `.env` 中 `MODELS_DIR` 指向）**

`transcribe_combined.py`（AssemblyAI 说话人分离 + 本地 ASR 高质量转录）使用的模型。适合多人对话、需要区分说话人的场景。

| 模型 | 大小 | 说明 |
|------|------|------|
| `Qwen3-ASR-0.6B` | 1.8GB | 通义千问 ASR，52语言，速度优先 |
| `Qwen3-ASR-1.7B-4bit` | 1.5GB | 同上 4bit 量化版，精度/速度平衡（默认） |
| `MiMo-V2.5-ASR-MLX` | 5.1GB | 小米 MiMo，MLX 格式，中英双语，复杂声学场景鲁棒 |

这些模型需手动从 HuggingFace（或 hf-mirror）下载，`setup.sh` 不自动管理。

## 日常操作

- 执行 Python 脚本：`uv run <script.py>`（不使用系统 `python3`）
- 新增 Python 依赖：`uv add <package>`
- 新增系统工具：在 `env/setup.sh` 的"系统工具"段落添加检测+安装逻辑
