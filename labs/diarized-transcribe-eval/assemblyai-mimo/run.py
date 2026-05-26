"""AssemblyAI (speaker diarization) + MiMo-V2.5-ASR-MLX (transcription) evaluation."""

import json
import os
import subprocess
import sys
import tempfile
import time
from functools import partial
from pathlib import Path

print = partial(print, flush=True)

from dotenv import load_dotenv

EVAL_DIR = Path(__file__).parent
PROJECT_ROOT = EVAL_DIR.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DEFAULT_AUDIO = EVAL_DIR.parent / "test-audio.m4a"
ASR_MODEL = str(Path("~/Models/MiMo-V2.5-ASR-MLX").expanduser())


def get_speaker_segments(audio_path: str) -> list[dict]:
    import assemblyai as aai

    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        print("Error: ASSEMBLYAI_API_KEY not set in .env")
        sys.exit(1)

    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(
        speech_models=["universal-3-pro", "universal-2"],
        speaker_labels=True,
    )

    transcriber = aai.Transcriber(config=config)
    print("  [1/3] AssemblyAI: uploading and processing...")
    transcript = transcriber.transcribe(audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        print(f"  Error: {transcript.error}")
        sys.exit(1)

    segments = []
    for utt in transcript.utterances:
        segments.append({
            "speaker": utt.speaker,
            "start_ms": utt.start,
            "end_ms": utt.end,
        })

    speakers = len(set(s["speaker"] for s in segments))
    print(f"  AssemblyAI done: {len(segments)} utterances, {speakers} speakers")
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
    from mlx_audio.stt import load

    print(f"  [2/3] Loading MiMo-V2.5-ASR model...")
    model = load(ASR_MODEL)

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
            text = result.text.strip()
            results.append({**seg, "text": text})
            print(f"    [{i + 1}/{len(segments)}] Speaker {seg['speaker']} ({duration_ms}ms): {text[:60]}")

    return results


def main():
    audio_path = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT_AUDIO)
    output_txt = EVAL_DIR / "transcript.txt"
    output_json = EVAL_DIR / "result.json"

    print(f"=== AssemblyAI + MiMo-V2.5-ASR Evaluation ===")
    print(f"Audio: {audio_path}")
    start = time.time()

    # Try to reuse speaker segments (own cache first, then assemblyai-qwen3)
    own_speakers = EVAL_DIR / "speakers.json"
    reuse_path = EVAL_DIR.parent / "assemblyai-qwen3" / "speakers.json"
    cached = own_speakers if own_speakers.exists() else (reuse_path if reuse_path.exists() else None)
    if cached:
        print(f"  Reusing speaker segments from {cached.relative_to(EVAL_DIR.parent)}")
        with open(cached, encoding="utf-8") as f:
            segments = json.load(f)
        speakers = len(set(s["speaker"] for s in segments))
        print(f"  Loaded: {len(segments)} utterances, {speakers} speakers")
    else:
        segments = get_speaker_segments(audio_path)
        speakers_json = EVAL_DIR / "speakers.json"
        with open(speakers_json, "w", encoding="utf-8") as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)
        print(f"  Speaker segments saved to speakers.json")

    results = transcribe_segments(audio_path, segments)
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
