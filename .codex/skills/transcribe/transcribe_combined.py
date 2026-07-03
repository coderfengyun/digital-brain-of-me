#!/usr/bin/env python3
"""
Combined transcription: AssemblyAI (speaker diarization) + Qwen3-ASR (text quality).

Plan A: Use AssemblyAI for speaker time segments, then cut audio by those segments
and transcribe each segment with Qwen3-ASR for higher quality text.

Usage:
    uv run .codex/skills/transcribe/transcribe_combined.py \
        --audio ~/Downloads/podcast.mp3 \
        --title "对话标题" \
        --show "节目名" \
        --output-dir investment/洪灏/

    # Reuse saved speaker segments (skip AssemblyAI):
    uv run .codex/skills/transcribe/transcribe_combined.py \
        --audio ~/Downloads/podcast.mp3 \
        --speaker-json /tmp/speakers.json \
        --title "对话标题" \
        --show "节目名" \
        --output-dir investment/洪灏/
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv


def _find_project_root() -> Path:
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / ".git").exists():
            return p
        p = p.parent
    return Path(__file__).resolve().parent


PROJECT_ROOT = _find_project_root()
SOURCES_JSONL = PROJECT_ROOT / "sources" / "sources.jsonl"

load_dotenv(PROJECT_ROOT / ".env")


def sanitize_filename(name: str, max_len: int = 50) -> str:
    safe = re.sub(r'[^\w\s-]', '', name)
    safe = re.sub(r'[\s-]+', '-', safe).strip('-')
    return safe[:max_len]


def generate_id() -> str:
    date_str = datetime.now().strftime('%Y%m%d')
    existing = set()
    if SOURCES_JSONL.exists():
        with open(SOURCES_JSONL, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    if entry['id'].startswith(f'pod-{date_str}'):
                        existing.add(entry['id'])
    seq = 1
    while f'pod-{date_str}-{seq:03d}' in existing:
        seq += 1
    return f'pod-{date_str}-{seq:03d}'


# --- Step 1: AssemblyAI speaker diarization ---

def get_speaker_segments(audio_path: str, speakers: int | None) -> list[dict]:
    """Get speaker-labeled time segments from AssemblyAI.

    Returns list of {speaker, start, end} dicts (times in seconds).
    """
    import assemblyai as aai

    api_key = os.environ.get('ASSEMBLYAI_API_KEY')
    if not api_key:
        print("Error: ASSEMBLYAI_API_KEY not set.")
        sys.exit(1)

    aai.settings.api_key = api_key

    config = aai.TranscriptionConfig(
        speech_models=["universal-3-pro", "universal-2"],
        speaker_labels=True,
    )
    if speakers:
        config.speakers_expected = speakers

    transcriber = aai.Transcriber(config=config)
    print("  [Step 1/2] AssemblyAI: getting speaker segments...")
    transcript = transcriber.transcribe(audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        print(f"  Error: AssemblyAI failed: {transcript.error}")
        sys.exit(1)

    segments = []
    for utt in transcript.utterances:
        segments.append({
            "speaker": utt.speaker,
            "start": utt.start / 1000.0,
            "end": utt.end / 1000.0,
        })

    actual_speakers = len(set(s["speaker"] for s in segments))
    print(f"  AssemblyAI done: {len(segments)} utterances, {actual_speakers} speakers")
    return segments


# --- Step 2: Cut audio + Qwen3-ASR per segment ---

def cut_audio_segment(audio_path: str, start: float, end: float, output_path: str) -> bool:
    """Cut a segment from audio using ffmpeg."""
    duration = end - start
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-ss", str(start), "-t", str(duration),
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        "-y", output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def transcribe_segments_qwen3(
    audio_path: str, speaker_segments: list[dict], model_path: str, language: str
) -> list[dict]:
    """Transcribe each speaker segment with Qwen3-ASR.

    Returns list of {speaker, text} dicts.
    """
    from mlx_audio.stt.utils import load_model

    print(f"  [Step 2/2] Qwen3-ASR: transcribing {len(speaker_segments)} segments...")
    model = load_model(model_path)

    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, seg in enumerate(speaker_segments):
            seg_path = os.path.join(tmpdir, f"seg_{i:04d}.wav")

            if not cut_audio_segment(audio_path, seg["start"], seg["end"], seg_path):
                print(f"    Warning: ffmpeg failed for segment {i}, skipping")
                continue

            duration = seg["end"] - seg["start"]
            if duration < 0.3:
                results.append({"speaker": seg["speaker"], "text": ""})
                continue

            result = model.generate(seg_path, language=language)
            text = result.text.strip()
            results.append({"speaker": seg["speaker"], "text": text})

            if (i + 1) % 50 == 0:
                print(f"    Processed {i + 1}/{len(speaker_segments)} segments...")

    print(f"  Qwen3-ASR done: {len(results)} segments transcribed")
    return results


# --- Output ---

def format_diarized_transcript(segments: list[dict]) -> str:
    lines = []
    for seg in segments:
        if seg["text"].strip():
            lines.append(f"**Speaker {seg['speaker']}:** {seg['text']}")
    return "\n\n".join(lines)


def save_transcript_md(
    formatted_transcript: str,
    episode_data: dict,
    output_dir: Path,
    show: str,
    language: str,
    num_speakers: int,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_show = sanitize_filename(show)
    safe_title = sanitize_filename(episode_data.get('title', 'Untitled'))
    episode_id = episode_data['id']
    filename = f"{safe_show}_{safe_title}_{episode_id}.md"
    output_path = output_dir / filename

    content = f"# {episode_data.get('title', 'Untitled')}\n\n"
    content += f"**Show:** {show}\n"
    content += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n"
    if episode_data.get('source'):
        content += f"**Source:** [{episode_data['source']}]({episode_data['source']})\n"
    content += f"**Language:** {language}\n"
    content += f"**Model:** qwen3-asr + assemblyai-diarization\n"
    content += f"**Speakers:** {num_speakers}\n\n"
    content += f"## Transcript\n\n{formatted_transcript}\n"

    output_path.write_text(content, encoding='utf-8')
    return output_path


def append_jsonl(episode_data: dict):
    SOURCES_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(SOURCES_JSONL, 'a') as f:
        f.write(json.dumps(episode_data, ensure_ascii=False) + '\n')


def main():
    parser = argparse.ArgumentParser(
        description='Combined transcription: AssemblyAI speakers + Qwen3-ASR text'
    )
    parser.add_argument('--audio', required=True, help='Path to local audio/video file')
    parser.add_argument('--title', required=True, help='Recording title')
    parser.add_argument('--show', required=True, help='Show or author name')
    parser.add_argument('--output-dir', required=True, help='Output directory')
    parser.add_argument('--language', default='zh', help='Language code (default: zh)')
    parser.add_argument('--speakers', type=int, default=None, help='Expected speakers (auto if omitted)')
    parser.add_argument('--asr-model', default='~/Models/Qwen3-ASR-1.7B-4bit',
                        help='Qwen3-ASR model path')
    parser.add_argument('--speaker-json', default=None,
                        help='Path to saved speaker segments JSON (skip AssemblyAI)')
    parser.add_argument('--save-speakers', default=None,
                        help='Save AssemblyAI speaker segments to this JSON path')
    parser.add_argument('--url', default=None, help='Source URL (optional)')
    parser.add_argument('--tags', default='', help='Comma-separated tags')

    args = parser.parse_args()

    audio_path = Path(args.audio).expanduser().resolve()
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir

    tags = [t.strip() for t in args.tags.split(',') if t.strip()] if args.tags else []
    asr_model = str(Path(args.asr_model).expanduser())

    print(f"Combined transcription: {audio_path.name}")
    print(f"  Language: {args.language}, Speakers: {args.speakers or 'auto'}")
    print()

    start_time = time.time()

    # Step 1: Get speaker segments
    if args.speaker_json:
        print(f"  Loading speaker segments from {args.speaker_json}...")
        with open(args.speaker_json, 'r') as f:
            speaker_segments = json.load(f)
        actual_speakers = len(set(s["speaker"] for s in speaker_segments))
        print(f"  Loaded: {len(speaker_segments)} utterances, {actual_speakers} speakers")
    else:
        speaker_segments = get_speaker_segments(str(audio_path), args.speakers)

    # Save speaker segments if requested
    if args.save_speakers:
        with open(args.save_speakers, 'w') as f:
            json.dump(speaker_segments, f, ensure_ascii=False, indent=2)
        print(f"  Speaker segments saved to {args.save_speakers}")

    # Step 2: Transcribe each segment with Qwen3-ASR
    results = transcribe_segments_qwen3(str(audio_path), speaker_segments, asr_model, args.language)

    actual_speakers = len(set(r["speaker"] for r in results if r["text"]))
    elapsed = time.time() - start_time
    print(f"\n  Total: {actual_speakers} speakers, {elapsed:.1f}s elapsed")

    # Output
    formatted = format_diarized_transcript(results)
    episode_id = generate_id()
    episode_data = {
        'id': episode_id,
        'type': 'podcast',
        'source': args.url or '',
        'title': args.title,
        'tags': tags,
        'added_at': datetime.now().strftime('%Y-%m-%d'),
        'output': '',
    }

    output_path = save_transcript_md(
        formatted, episode_data, output_dir,
        show=args.show, language=args.language,
        num_speakers=actual_speakers,
    )
    episode_data['output'] = str(output_path.relative_to(PROJECT_ROOT))
    append_jsonl(episode_data)

    print(f"  Saved: {output_path.relative_to(PROJECT_ROOT)}")
    print("Done!")


if __name__ == '__main__':
    main()
