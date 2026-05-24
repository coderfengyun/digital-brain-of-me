#!/usr/bin/env bash
#
# Digital Brain 全量环境初始化
# 用法: bash setup.sh
#
# 一键安装所有依赖：
#   1. uv → Python 3.13 + .venv + Python 包
#   2. Node.js + npm 包
#   3. 系统工具：ffmpeg, whisper-cpp
#   4. Whisper 模型文件
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

WHISPER_MODEL_DIR="$HOME/.cache/whisper-cpp"
WHISPER_MODEL="ggml-base.bin"

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

info()  { echo "  ✓ $1"; }
warn()  { echo "  ⚠ $1"; }
step()  { echo ""; echo "[$1]"; }

install_brew_pkg() {
    local pkg="$1"
    if command -v brew &>/dev/null; then
        brew install "$pkg"
    elif command -v apt-get &>/dev/null; then
        sudo apt-get update -qq && sudo apt-get install -y "$pkg"
    else
        echo "ERROR: 无法自动安装 $pkg（未检测到 brew 或 apt-get）"
        echo "请手动安装后重新运行此脚本"
        exit 1
    fi
}

# ─────────────────────────────────────────────
# 1. Python (uv)
# ─────────────────────────────────────────────

step "Python"

if ! command -v uv &>/dev/null; then
    if [[ -x "$HOME/.local/bin/uv" ]]; then
        export PATH="$HOME/.local/bin:$PATH"
    else
        echo "  安装 uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi
info "uv $(uv --version | awk '{print $2}')"

uv sync --quiet
info "Python $(.venv/bin/python3 --version | awk '{print $2}') + 依赖已同步"

# ─────────────────────────────────────────────
# 2. Node.js
# ─────────────────────────────────────────────

step "Node.js"

if ! command -v node &>/dev/null; then
    echo "  安装 Node.js..."
    install_brew_pkg node
fi
info "node $(node --version)"

if [[ -f package.json ]]; then
    if [[ ! -d node_modules ]]; then
        npm install --silent
    fi
    info "npm 依赖已就绪"
fi

# ─────────────────────────────────────────────
# 3. 系统工具
# ─────────────────────────────────────────────

step "系统工具"

if ! command -v ffmpeg &>/dev/null; then
    echo "  安装 ffmpeg..."
    install_brew_pkg ffmpeg
fi
info "ffmpeg $(ffmpeg -version 2>&1 | head -1 | awk '{print $3}')"

if ! command -v whisper-cli &>/dev/null; then
    echo "  安装 whisper-cpp..."
    install_brew_pkg whisper-cpp
fi
info "whisper-cli 已就绪"

# ─────────────────────────────────────────────
# 4. Whisper 模型
# ─────────────────────────────────────────────

step "Whisper 模型"

if [[ ! -f "$WHISPER_MODEL_DIR/$WHISPER_MODEL" ]]; then
    echo "  下载 $WHISPER_MODEL..."
    mkdir -p "$WHISPER_MODEL_DIR"
    curl -L -o "$WHISPER_MODEL_DIR/$WHISPER_MODEL" \
        "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/$WHISPER_MODEL"
fi
info "$WHISPER_MODEL ($(du -h "$WHISPER_MODEL_DIR/$WHISPER_MODEL" | awk '{print $1}'))"

# ─────────────────────────────────────────────
# 5. 本地配置 (.env)
# ─────────────────────────────────────────────

step "本地配置"

if [[ ! -f .env ]]; then
    cp .env.example .env
    info "已从 .env.example 创建 .env"
fi

if ! grep -q "^MODELS_DIR=" .env; then
    echo ""
    echo "  请指定本机模型文件目录（用于 whisper 等本地模型）"
    printf "  路径 [默认: ~/models]: "
    read -r models_dir
    models_dir="${models_dir:-$HOME/models}"
    # Expand ~ for validation but store as-is
    eval expanded_dir="$models_dir"
    if [[ ! -d "$expanded_dir" ]]; then
        warn "目录 $models_dir 不存在，将在首次使用时查找"
    fi
    echo "" >> .env
    echo "# Local paths (machine-specific, set during setup)" >> .env
    echo "MODELS_DIR=$models_dir" >> .env
    info "MODELS_DIR=$models_dir 已写入 .env"
else
    info "MODELS_DIR 已配置: $(grep '^MODELS_DIR=' .env | cut -d= -f2)"
fi

# ─────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────

echo ""
echo "=========================================="
echo "  Digital Brain 环境就绪！"
echo ""
echo "  Python:  uv run <script.py>"
echo "  Node:    npx defuddle <url>"
echo "  Audio:   whisper-cli / ffmpeg"
echo "=========================================="
