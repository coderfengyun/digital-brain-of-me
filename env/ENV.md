# 环境与依赖

项目所有依赖通过 `bash env/setup.sh` 一键安装（幂等，新机器从零开始只需 `git clone && bash env/setup.sh`）。

## 依赖分层

| 层级 | 管理方式 | 配置文件 |
|------|---------|---------|
| Python 包 | uv | `pyproject.toml` + `uv.lock` |
| Node.js 包 | npm | `package.json` |
| 系统工具 | brew / apt | `env/setup.sh` 中声明 |
| 模型文件 | curl / huggingface-cli | `env/models.toml` |

### 模型文件

本地推理用的预训练模型权重，统一存放在 `.env` 中 `MODELS_DIR` 指向的根目录。

- 清单文件：`env/models.toml`（列出所有模型的相对路径、大小、下载地址、是否必需）
- `setup.sh` 自动下载 `required = true` 的模型
- 其余模型按需手动下载（`huggingface-cli download` 或 `wget`）

## 日常操作

- 执行 Python 脚本：`uv run <script.py>`（不使用系统 `python3`）
- 新增 Python 依赖：`uv add <package>`
- 新增系统工具：在 `env/setup.sh` 的"系统工具"段落添加检测+安装逻辑
