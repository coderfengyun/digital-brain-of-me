#!/usr/bin/env bash
#
# Digital Brain Python 环境初始化
# 用法: bash setup.sh
#
# 功能:
#   1. 确保 Python 3.13 存在（没有则通过 homebrew/apt 安装）
#   2. 创建项目 .venv（基于 3.13）
#   3. 安装 requirements.txt 中的依赖
#
set -euo pipefail

REQUIRED_PYTHON="3.13"
VENV_DIR=".venv"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# --- Step 1: Locate or install Python 3.13 ---

find_python313() {
    for candidate in python${REQUIRED_PYTHON} python3.13; do
        if command -v "$candidate" &>/dev/null; then
            local ver
            ver=$("$candidate" --version 2>&1 | grep -oE '3\.13\.[0-9]+')
            if [[ -n "$ver" ]]; then
                echo "$candidate"
                return 0
            fi
        fi
    done
    return 1
}

PYTHON_BIN=""
if PYTHON_BIN=$(find_python313); then
    echo "✓ 找到 Python $REQUIRED_PYTHON: $(command -v "$PYTHON_BIN") ($($PYTHON_BIN --version))"
else
    echo "Python $REQUIRED_PYTHON 未安装，正在安装..."
    if command -v brew &>/dev/null; then
        brew install python@3.13
    elif command -v apt-get &>/dev/null; then
        sudo apt-get update && sudo apt-get install -y python3.13 python3.13-venv python3.13-dev
    else
        echo "ERROR: 无法自动安装 Python 3.13（未检测到 brew 或 apt-get）"
        echo "请手动安装后重新运行此脚本"
        exit 1
    fi

    if ! PYTHON_BIN=$(find_python313); then
        echo "ERROR: 安装后仍找不到 Python $REQUIRED_PYTHON"
        exit 1
    fi
    echo "✓ 已安装 Python $REQUIRED_PYTHON: $($PYTHON_BIN --version)"
fi

# --- Step 2: Create venv ---

if [[ -d "$VENV_DIR" ]]; then
    # Verify existing venv uses 3.13
    VENV_VER=$("$VENV_DIR/bin/python3" --version 2>&1 | grep -oE '3\.13\.[0-9]+' || true)
    if [[ -z "$VENV_VER" ]]; then
        echo "现有 .venv 不是 Python 3.13，重建..."
        rm -rf "$VENV_DIR"
    else
        echo "✓ .venv 已存在 (Python $VENV_VER)"
    fi
fi

if [[ ! -d "$VENV_DIR" ]]; then
    echo "创建 .venv (Python $REQUIRED_PYTHON)..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
    echo "✓ .venv 已创建"
fi

# --- Step 3: Install dependencies ---

echo "安装依赖..."
"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -r requirements.txt -q
echo "✓ 依赖安装完成"

# --- Done ---

echo ""
echo "=========================================="
echo "  环境就绪！"
echo "  Python: $("$VENV_DIR/bin/python3" --version)"
echo "  路径:   $SCRIPT_DIR/$VENV_DIR/bin/python3"
echo "=========================================="
