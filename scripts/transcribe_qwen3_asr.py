#!/usr/bin/env python3
"""使用 Qwen3-ASR 1.7B MLX 模型转写音频。"""

from __future__ import annotations

import argparse
from pathlib import Path

from qwen3_asr_mlx import Qwen3ASR


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe audio with Qwen3-ASR 1.7B")
    parser.add_argument("audio", type=Path, help="音频文件路径（WAV/MP3/FLAC 等）")
    parser.add_argument(
        "--model",
        default="mlx-community/Qwen3-ASR-1.7B-bf16",
        help="Hugging Face 模型名或本地模型目录",
    )
    parser.add_argument("--language", default=None, help="可选语言提示，例如 Chinese 或 English")
    parser.add_argument("--context", default=None, help="可选热词/上下文")
    args = parser.parse_args()

    if not args.audio.is_file():
        raise SystemExit(f"找不到音频文件：{args.audio}")

    print(f"正在加载模型：{args.model}")
    model = Qwen3ASR.from_pretrained(args.model)
    print(f"正在转写：{args.audio}")
    result = model.transcribe(
        str(args.audio),
        language=args.language,
        context=args.context,
    )

    print("\n--- 转写结果 ---")
    print(result.text)
    print(f"语言：{result.language}")
    print(f"时长：{result.duration:.2f} 秒")


if __name__ == "__main__":
    main()
