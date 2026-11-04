#!/usr/bin/env python3
"""Isolated pyannote worker used by transcribe_speakers.py."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--speakers", type=int)
    args = parser.parse_args()

    import soundfile as sf
    import torch
    from pyannote.audio import Pipeline

    audio, sample_rate = sf.read(args.audio, dtype="float32", always_2d=True)
    waveform = torch.from_numpy(audio.T.copy())
    pipeline = Pipeline.from_pretrained(Path(args.model))
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    if device == "mps":
        pipeline.to(torch.device("mps"))

    kwargs = {"num_speakers": args.speakers} if args.speakers else {}
    result = pipeline(
        {"waveform": waveform, "sample_rate": sample_rate},
        **kwargs,
    )
    annotation = getattr(result, "speaker_diarization", result)
    segments = [
        {
            "start": round(turn.start, 3),
            "end": round(turn.end, 3),
            "speaker": speaker,
        }
        for turn, _, speaker in annotation.itertracks(yield_label=True)
    ]
    Path(args.output).write_text(
        json.dumps(segments, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Diarization: device={device}, segments={len(segments)}", flush=True)


if __name__ == "__main__":
    main()
