"""pyannote-audio (speaker diarization) + Qwen3-ASR (transcription) evaluation."""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from dotenv import load_dotenv

EVAL_DIR = Path(__file__).parent
PROJECT_ROOT = EVAL_DIR.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DEFAULT_AUDIO = EVAL_DIR.parent / "test-audio.m4a"
ASR_MODEL = str(Path("~/Models/Qwen3-ASR-1.7B-4bit").expanduser())


def get_speaker_segments(audio_path: str) -> list[dict]:
    from pyannote.audio import Pipeline
    import torch

    hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not hf_token:
        print("Error: HF_TOKEN not set in .env")
        sys.exit(1)

    print("  [1/3] pyannote: loading pipeline...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        token=hf_token,
    )

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    pipeline.to(torch.device(device))
    print(f"  pyannote: running on {device}...")

    output = pipeline(audio_path, max_speakers=6)
    diarization = output.speaker_diarization

    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({
            "speaker": speaker,
            "start_ms": int(turn.start * 1000),
            "end_ms": int(turn.end * 1000),
        })

    speakers = len(set(s["speaker"] for s in segments))
    print(f"  pyannote done: {len(segments)} segments, {speakers} speakers")
    return segments


def cut_audio_segment(audio_path: str, start_ms: int, end_ms: int, output_path: str) -> bool:
    start_s = start_ms / 1000.0
    duration_s = (end_ms - start_ms) / 1000.0
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-ss", str(start_s), "-t", str(duration_s),
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        "-y", output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def transcribe_segments(audio_path: str, segments: list[dict]) -> list[dict]:
    from mlx_audio.stt.utils import load_model

    print(f"  [2/3] Loading Qwen3-ASR model...")
    model = load_model(ASR_MODEL)

    print(f"  [3/3] Transcribing {len(segments)} segments...")
    results = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, seg in enumerate(segments):
            seg_path = os.path.join(tmpdir, f"seg_{i:04d}.wav")
            duration_ms = seg["end_ms"] - seg["start_ms"]

            if duration_ms < 300:
                results.append({**seg, "text": ""})
                continue

            if not cut_audio_segment(audio_path, seg["start_ms"], seg["end_ms"], seg_path):
                print(f"    Warning: ffmpeg failed for segment {i}, skipping")
                results.append({**seg, "text": ""})
                continue

            result = model.generate(seg_path, language="zh")
            results.append({**seg, "text": result.text.strip()})

            if (i + 1) % 50 == 0:
                print(f"    Processed {i + 1}/{len(segments)}...")

    return results


def prepare_wav(audio_path: str) -> str:
    """Convert audio to 16kHz mono WAV for pyannote compatibility."""
    if audio_path.endswith(".wav"):
        return audio_path
    wav_path = str(EVAL_DIR / "input_16k.wav")
    cmd = ["ffmpeg", "-i", audio_path, "-ar", "16000", "-ac", "1", "-y", wav_path]
    subprocess.run(cmd, capture_output=True, check=True)
    return wav_path


def main():
    audio_path = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT_AUDIO)
    output_txt = EVAL_DIR / "transcript.txt"
    output_json = EVAL_DIR / "result.json"

    print(f"=== pyannote + Qwen3-ASR Evaluation ===")
    print(f"Audio: {audio_path}")
    start = time.time()

    wav_path = prepare_wav(audio_path)
    print(f"  Prepared WAV: {wav_path}")
    segments = get_speaker_segments(wav_path)

    # Save speaker segments for potential reuse
    speakers_json = EVAL_DIR / "speakers.json"
    with open(speakers_json, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)
    print(f"  Speaker segments saved to speakers.json")

    results = transcribe_segments(wav_path, segments)
    elapsed = time.time() - start

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    total = 0
    with open(output_txt, "w", encoding="utf-8") as f:
        for r in results:
            if r["text"]:
                f.write(f"[Speaker {r['speaker']}] {r['start_ms']}ms-{r['end_ms']}ms: {r['text']}\n")
                total += 1
        speakers = len(set(r["speaker"] for r in results if r["text"]))
        f.write(f"\n--- Total: {total} sentences, {speakers} speakers, elapsed: {elapsed:.1f}s ---\n")

    print(f"\nDone! {total} sentences, {elapsed:.1f}s")
    print(f"  -> {output_txt.name}")
    print(f"  -> {output_json.name}")


if __name__ == "__main__":
    main()
