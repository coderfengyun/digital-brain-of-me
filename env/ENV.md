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

本地推理用的预训练模型权重，体积大（百MB级）且不入 git，按工具存放在各自的缓存目录。

| 模型 | 用途 | 存放路径 | 大小 |
|------|------|---------|------|
| `ggml-base.bin` | whisper.cpp 语音转文字（transcribe skill 使用） | `~/.cache/whisper-cpp/` | ~141MB |

`setup.sh` 会自动检测并下载缺失的模型。如需更高质量转录，可手动下载 `ggml-small.bin`（244MB）或 `ggml-large.bin`（1.5GB）到同一目录，转录时通过 `--model small/large` 指定。

## 日常操作

- 执行 Python 脚本：`uv run <script.py>`（不使用系统 `python3`）
- 新增 Python 依赖：`uv add <package>`
- 新增系统工具：在 `env/setup.sh` 的"系统工具"段落添加检测+安装逻辑
