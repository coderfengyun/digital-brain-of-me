#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"
REQUIREMENTS="$SKILL_DIR/requirements-asr.txt"

models_dir="${MODELS_DIR:-$HOME/Models}"
if [[ -f "$PROJECT_ROOT/.env" ]]; then
    configured="$(sed -n 's/^MODELS_DIR=//p' "$PROJECT_ROOT/.env" | tail -1)"
    if [[ -n "$configured" ]]; then
        models_dir="${configured/#\~/$HOME}"
    fi
fi

wheelhouse="$models_dir/python-wheels/qwen3-asr-mlx"
runtime="$models_dir/.venvs/qwen3-asr-mlx"
model="$models_dir/Qwen3-ASR-0.6B-MLX"
python_bin="${PYTHON_BIN:-$(command -v python3.13 || true)}"

if [[ -z "$python_bin" ]]; then
    echo "Error: Python 3.13 is required. Set PYTHON_BIN explicitly." >&2
    exit 1
fi

if [[ "${1:-}" == "--download" ]]; then
    mkdir -p "$wheelhouse"
    env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY \
        -u http_proxy -u https_proxy -u all_proxy \
        NO_PROXY='*' no_proxy='*' \
        "$python_bin" -m pip download --dest "$wheelhouse" -r "$REQUIREMENTS"
fi

if ! compgen -G "$wheelhouse/qwen3_asr_mlx-*.whl" >/dev/null; then
    echo "Error: local ASR wheel cache is empty: $wheelhouse" >&2
    echo "Run this script once with --download to populate it without a proxy." >&2
    exit 1
fi

"$python_bin" -m venv "$runtime"
"$runtime/bin/python" -m pip install \
    --no-index --find-links "$wheelhouse" -r "$REQUIREMENTS"

if [[ ! -f "$model/model.safetensors" ]]; then
    echo "Warning: local model weights not found at $model" >&2
fi

echo "ASR runtime: $runtime/bin/python"
echo "ASR model:   $model"
echo "Wheel cache: $wheelhouse"
