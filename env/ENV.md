# 环境与依赖

项目所有依赖通过 `bash env/setup.sh` 一键安装（幂等，新机器从零开始只需 `git clone && bash env/setup.sh`）。

## 依赖分层

| 层级 | 管理方式 | 配置文件 |
|------|---------|---------|
| Python 包 | uv | `pyproject.toml` + `uv.lock` |
| Node.js 包 | npm | `package.json` |
| 系统工具 | brew / apt | `env/setup.sh` 中声明 |
| 模型文件 | curl 下载 | `env/setup.sh` 中声明 |

## 日常操作

- 执行 Python 脚本：`uv run <script.py>`（不使用系统 `python3`）
- 新增 Python 依赖：`uv add <package>`
- 新增系统工具：在 `env/setup.sh` 的"系统工具"段落添加检测+安装逻辑
