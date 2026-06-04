"""AssemblyAI standalone (ASR + diarization) evaluation."""

import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

EVAL_DIR = Path(__file__).parent
PROJECT_ROOT = EVAL_DIR.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DEFAULT_AUDIO = EVAL_DIR.parent / "test-audio.m4a"


def main():
    import assemblyai as aai

    audio_path = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT_AUDIO)
    output_txt = EVAL_DIR / "transcript.txt"
    output_json = EVAL_DIR / "result.json"

    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        print("Error: ASSEMBLYAI_API_KEY not set in .env")
        sys.exit(1)

    aai.settings.api_key = api_key

    print(f"=== AssemblyAI Standalone Evaluation ===")
    print(f"Audio: {audio_path}")
    start = time.time()

    config = aai.TranscriptionConfig(
        speech_models=["universal-3-pro", "universal-2"],
        speaker_labels=True,
        language_code="zh",
    )

    transcriber = aai.Transcriber(config=config)
    print("  Uploading and processing...")
    transcript = transcriber.transcribe(audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        print(f"  Error: {transcript.error}")
        sys.exit(1)

    elapsed = time.time() - start

    results = []
    for utt in transcript.utterances:
        results.append({
            "speaker": utt.speaker,
            "start_ms": utt.start,
            "end_ms": utt.end,
            "text": utt.text,
        })

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

    print(f"\nDone! {total} sentences, {speakers} speakers, {elapsed:.1f}s")
    print(f"  -> {output_txt.name}")
    print(f"  -> {output_json.name}")


if __name__ == "__main__":
    main()
