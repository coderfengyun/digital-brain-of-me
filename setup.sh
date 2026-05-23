#!/usr/bin/env bash
#
# Digital Brain 环境初始化
# 用法: bash setup.sh
#
# 功能:
#   1. 确保 uv 已安装（没有则自动安装）
#   2. uv sync：自动下载 Python 3.13 + 创建 .venv + 按 lockfile 安装依赖
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# --- Step 1: Ensure uv is available ---

if ! command -v uv &>/dev/null; then
    # Check ~/.local/bin (uv default install location)
    if [[ -x "$HOME/.local/bin/uv" ]]; then
        export PATH="$HOME/.local/bin:$PATH"
    else
        echo "安装 uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi

echo "✓ uv $(uv --version | awk '{print $2}')"

# --- Step 2: uv sync (Python + venv + deps) ---

echo "同步环境..."
uv sync
echo ""
echo "=========================================="
echo "  环境就绪！"
echo "  Python: $(.venv/bin/python3 --version)"
echo "  路径:   $SCRIPT_DIR/.venv/bin/python3"
echo "  运行:   uv run <script.py>"
echo "=========================================="
