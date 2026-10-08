#!/usr/bin/env python3
"""可断点续跑地转录固定时长音频分段。"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import torch
from qwen_asr import Qwen3ASRModel


MODEL_PATH = "/Users/chentienan/Models/Qwen3-ASR-0.6B"
WORK_DIR = Path("tmp/transcriptions/标准录音11")
CHUNKS_DIR = WORK_DIR / "chunks"
RESULTS_PATH = WORK_DIR / "segments.jsonl"
OUTPUT_PATH = Path("content/transcripts/标准录音11.md")
CHUNK_SECONDS = 300


def timestamp(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def read_completed() -> dict[int, dict]:
    completed: dict[int, dict] = {}
    if RESULTS_PATH.exists():
        for line in RESULTS_PATH.read_text(encoding="utf-8").splitlines():
            if line.strip():
                item = json.loads(line)
                completed[item["index"]] = item
    return completed


def write_markdown(results: dict[int, dict]) -> None:
    lines = [
        "# 标准录音 11 转录稿",
        "",
        "> 使用 Qwen3-ASR-0.6B 本地转录；时间为分段起点，机器转录可能存在错漏。",
        "",
    ]
    for index in sorted(results):
        item = results[index]
        lines.extend([f"## {timestamp(item['start_seconds'])}", "", item["text"].strip(), ""])
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    chunks = sorted(CHUNKS_DIR.glob("chunk-*.wav"))
    if not chunks:
        raise SystemExit(f"没有找到音频分段：{CHUNKS_DIR}")

    completed = read_completed()
    print(f"共 {len(chunks)} 段，已完成 {len(completed)} 段", flush=True)
    print("正在加载模型……", flush=True)
    load_started = time.time()
    model = Qwen3ASRModel.from_pretrained(
        MODEL_PATH,
        dtype=torch.float32,
        device_map="cpu",
        max_inference_batch_size=1,
        max_new_tokens=2048,
    )
    print(f"模型加载完成：{time.time() - load_started:.1f}s", flush=True)

    for index, chunk in enumerate(chunks):
        if index in completed:
            continue
        started = time.time()
        print(
            f"[{index + 1}/{len(chunks)}] {timestamp(index * CHUNK_SECONDS)} {chunk.name}",
            flush=True,
        )
        try:
            result = model.transcribe(audio=str(chunk), language="Chinese")[0]
        except Exception as exc:
            print(f"分段 {index} 失败：{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
            raise
        item = {
            "index": index,
            "start_seconds": index * CHUNK_SECONDS,
            "language": result.language,
            "elapsed_seconds": round(time.time() - started, 2),
            "text": result.text.strip(),
        }
        with RESULTS_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")
            handle.flush()
        completed[index] = item
        write_markdown(completed)
        print(f"完成，用时 {item['elapsed_seconds']:.1f}s，字符数 {len(item['text'])}", flush=True)

    write_markdown(completed)
    print(f"全部完成：{OUTPUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
