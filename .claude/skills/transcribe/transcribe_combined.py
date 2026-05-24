#!/usr/bin/env python3
"""
Combined transcription: AssemblyAI (speaker diarization) + Qwen3-ASR (text quality) + Forced Aligner (alignment).

Flow:
1. AssemblyAI → speaker segments with timestamps
2. Qwen3-ASR → high-quality full transcript text
3. Qwen3 Forced Aligner → character-level timestamps for the transcript
4. Merge: assign each character to a speaker based on time overlap

Usage:
    python3 .claude/skills/transcribe/transcribe_combined.py \
        --audio ~/Downloads/podcast.mp3 \
        --title "对话标题" \
        --show "节目名" \
        --output-dir investment/洪灏/
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
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
    print("  [Step 1/3] AssemblyAI: uploading and getting speaker segments...")
    transcript = transcriber.transcribe(audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        print(f"  Error: AssemblyAI failed: {transcript.error}")
        sys.exit(1)

    segments = []
    for utt in transcript.utterances:
        segments.append({
            "speaker": utt.speaker,
            "start": utt.start / 1000.0,  # ms -> seconds
            "end": utt.end / 1000.0,
        })

    actual_speakers = len(set(s["speaker"] for s in segments))
    print(f"  AssemblyAI done: {len(segments)} utterances, {actual_speakers} speakers")
    return segments


# --- Step 2: Qwen3-ASR full transcription ---

def transcribe_qwen3(audio_path: str, model_path: str, language: str) -> str:
    """Get full transcript text from Qwen3-ASR."""
    from mlx_audio.stt.utils import load_model

    print(f"  [Step 2/3] Qwen3-ASR: transcribing full audio...")
    model = load_model(model_path)
    result = model.generate(audio_path, language=language)
    print(f"  Qwen3-ASR done: {len(result.text)} chars")
    return result.text


# --- Step 3: Forced Aligner ---

def align_text(audio_path: str, text: str, aligner_model_path: str, language: str) -> list[dict]:
    """Get character-level timestamps via forced aligner.

    Returns list of {text, start_time, end_time} dicts.
    """
    from mlx_audio.stt.utils import load_model

    print(f"  [Step 3/3] Forced Aligner: aligning {len(text)} chars to audio...")
    model = load_model(aligner_model_path)

    lang_map = {"zh": "Chinese", "en": "English", "ja": "Japanese", "ko": "Korean"}
    lang_name = lang_map.get(language, "Chinese")

    result = model.generate(audio_path, text=text, language=lang_name)

    items = [{"text": item.text, "start": item.start_time, "end": item.end_time}
             for item in result.items]
    print(f"  Aligner done: {len(items)} aligned tokens")
    return items


# --- Step 4: Merge ---

def merge_speakers_and_text(speaker_segments: list[dict], aligned_chars: list[dict]) -> list[dict]:
    """Assign each aligned character to a speaker based on time overlap.

    Returns list of {speaker, text} segments (consecutive same-speaker chars merged).
    """
    if not aligned_chars or not speaker_segments:
        return []

    def find_speaker(char_start: float, char_end: float) -> str:
        char_mid = (char_start + char_end) / 2
        for seg in speaker_segments:
            if seg["start"] <= char_mid <= seg["end"]:
                return seg["speaker"]
        # Fallback: find closest segment
        min_dist = float('inf')
        closest = speaker_segments[0]["speaker"]
        for seg in speaker_segments:
            dist = min(abs(seg["start"] - char_mid), abs(seg["end"] - char_mid))
            if dist < min_dist:
                min_dist = dist
                closest = seg["speaker"]
        return closest

    # Assign speaker to each char
    labeled_chars = []
    for ch in aligned_chars:
        speaker = find_speaker(ch["start"], ch["end"])
        labeled_chars.append({"speaker": speaker, "text": ch["text"]})

    # Merge consecutive same-speaker chars into segments
    merged = []
    current_speaker = labeled_chars[0]["speaker"]
    current_text = []

    for lc in labeled_chars:
        if lc["speaker"] != current_speaker:
            merged.append({"speaker": current_speaker, "text": "".join(current_text)})
            current_speaker = lc["speaker"]
            current_text = []
        current_text.append(lc["text"])

    if current_text:
        merged.append({"speaker": current_speaker, "text": "".join(current_text)})

    return merged


# --- Output ---

def format_diarized_transcript(segments: list[dict]) -> str:
    lines = []
    for seg in segments:
        if seg["text"].strip():
            lines.append(f"**Speaker {seg['speaker']}:** {seg['text'].strip()}")
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
        description='Combined transcription: Qwen3-ASR text + AssemblyAI speakers'
    )
    parser.add_argument('--audio', required=True, help='Path to local audio/video file')
    parser.add_argument('--title', required=True, help='Recording title')
    parser.add_argument('--show', required=True, help='Show or author name')
    parser.add_argument('--output-dir', required=True, help='Output directory')
    parser.add_argument('--language', default='zh', help='Language code (default: zh)')
    parser.add_argument('--speakers', type=int, default=None, help='Expected speakers (auto if omitted)')
    parser.add_argument('--asr-model', default='~/Models/Qwen3-ASR-1.7B-4bit',
                        help='Qwen3-ASR model path')
    parser.add_argument('--aligner-model', default='mlx-community/Qwen3-ForcedAligner-0.5B-4bit',
                        help='Forced aligner model path or HF repo')
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

    # Step 1: AssemblyAI speaker segments
    speaker_segments = get_speaker_segments(str(audio_path), args.speakers)

    # Step 2: Qwen3-ASR transcription
    transcript_text = transcribe_qwen3(str(audio_path), asr_model, args.language)

    # Step 3: Forced alignment
    aligned_chars = align_text(str(audio_path), transcript_text, args.aligner_model, args.language)

    # Step 4: Merge
    print("  Merging speaker labels with aligned text...")
    merged = merge_speakers_and_text(speaker_segments, aligned_chars)

    actual_speakers = len(set(s["speaker"] for s in merged))
    elapsed = time.time() - start_time
    print(f"  Merge done: {len(merged)} segments, {actual_speakers} speakers ({elapsed:.1f}s total)")

    # Output
    formatted = format_diarized_transcript(merged)
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

    print(f"\n  Saved: {output_path.relative_to(PROJECT_ROOT)}")
    print("Done!")


if __name__ == '__main__':
    main()
