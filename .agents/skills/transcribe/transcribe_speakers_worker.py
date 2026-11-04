#!/usr/bin/env python3
"""Isolated Qwen3-ASR worker used by transcribe_speakers.py."""

import argparse
import json
from pathlib import Path

from transcribe_speakers import (
    asr_token_budget,
    merge_turns,
    render_markdown,
    speaker_mapping,
    split_turns,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True)
    parser.add_argument("--segments", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--show", required=True)
    parser.add_argument("--language", required=True)
    parser.add_argument("--source")
    parser.add_argument("--speaker-names")
    parser.add_argument("--context")
    parser.add_argument("--min-segment-duration", type=float, default=0.2)
    parser.add_argument("--merge-gap", type=float, default=1.0)
    parser.add_argument("--max-segment-duration", type=float, default=30.0)
    args = parser.parse_args()

    import numpy as np
    import soundfile as sf
    from qwen3_asr_mlx import Qwen3ASR

    raw_segments = json.loads(Path(args.segments).read_text(encoding="utf-8"))
    segments = split_turns(
        merge_turns(
            raw_segments,
            min_duration=args.min_segment_duration,
            max_gap=args.merge_gap,
        ),
        max_duration=args.max_segment_duration,
    )
    requested_names = (
        [name.strip() for name in args.speaker_names.split(",") if name.strip()]
        if args.speaker_names
        else None
    )
    names = speaker_mapping(segments, requested_names)

    audio, sample_rate = sf.read(args.audio, dtype="float32", always_2d=True)
    mono = audio.mean(axis=1)
    duration = len(mono) / sample_rate
    model = Qwen3ASR.from_pretrained(args.model)

    turns = []
    for index, segment in enumerate(segments, start=1):
        start = max(0.0, segment["start"] - 0.08)
        end = min(duration, segment["end"] + 0.08)
        chunk = np.asarray(
            mono[int(start * sample_rate) : int(end * sample_rate)], dtype=np.float32
        )
        context = args.context if args.context and end - start >= 2.0 else None
        result = model.transcribe(
            chunk,
            language=args.language,
            context=context,
            max_tokens=asr_token_budget(end - start),
            chunk_duration=args.max_segment_duration,
        )
        text = result.text.strip()
        if context and text == context.strip():
            text = ""
        if text:
            turns.append({**segment, "text": text})
        if index % 20 == 0 or index == len(segments):
            print(f"Transcription: {index}/{len(segments)}", flush=True)

    Path(args.output).write_text(
        render_markdown(
            args.title,
            args.show,
            args.language,
            turns,
            names,
            args.source,
        ),
        encoding="utf-8",
    )
    print(f"Speaker transcript: turns={len(turns)}", flush=True)


if __name__ == "__main__":
    main()
