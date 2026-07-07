#!/usr/bin/env python3
"""
AssemblyAI transcription with speaker diarization.

Usage:
    uv run .claude/skills/transcribe/transcribe_gcp.py \
        --audio ~/Downloads/podcast.mp3 \
        --title "对话标题" \
        --show "节目名" \
        --output-dir investment/洪灏/ \
        --speakers 2
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import assemblyai as aai
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


def format_diarized_transcript(utterances: list) -> str:
    """Format AssemblyAI utterances into readable markdown."""
    lines = []
    for utt in utterances:
        lines.append(f"**Speaker {utt.speaker}:** {utt.text}")
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
    content += f"**Model:** assemblyai\n"
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
        description='Transcribe audio with AssemblyAI (speaker diarization)'
    )
    parser.add_argument('--audio', required=True, help='Path to local audio/video file')
    parser.add_argument('--title', required=True, help='Episode/recording title')
    parser.add_argument('--show', required=True, help='Show or author name')
    parser.add_argument('--output-dir', required=True, help='Output directory for transcript')
    parser.add_argument('--language', default='zh', help='Language code (default: zh). Use "auto" for auto-detection.')
    parser.add_argument('--speakers', type=int, default=None, help='Expected number of speakers (auto-detect if not specified)')
    parser.add_argument('--url', default=None, help='Source URL (optional)')
    parser.add_argument('--tags', default='', help='Comma-separated tags')

    args = parser.parse_args()

    audio_path = Path(args.audio).resolve()
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)

    api_key = os.environ.get('ASSEMBLYAI_API_KEY')
    if not api_key:
        print("Error: ASSEMBLYAI_API_KEY not set in .env or environment.")
        sys.exit(1)

    aai.settings.api_key = api_key

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir

    tags = [t.strip() for t in args.tags.split(',') if t.strip()] if args.tags else []

    print(f"Transcribing: {audio_path.name}")
    print(f"  Language: {args.language}, Speakers: {args.speakers or 'auto-detect'}")

    config = aai.TranscriptionConfig(
        speech_models=["universal-3-pro", "universal-2"],
        speaker_labels=True,
    )
    if args.speakers:
        config.speakers_expected = args.speakers

    if args.language == "auto":
        config.language_detection = True
    else:
        config.language_code = args.language

    transcriber = aai.Transcriber(config=config)

    print("  Uploading and transcribing (this may take a while for long audio)...")
    transcript = transcriber.transcribe(str(audio_path))

    if transcript.status == aai.TranscriptStatus.error:
        print(f"  Error: Transcription failed: {transcript.error}")
        sys.exit(1)

    if not transcript.utterances:
        print("  Warning: No utterances returned.")
        sys.exit(1)

    actual_speakers = len(set(u.speaker for u in transcript.utterances))
    print(f"  Transcription complete: {len(transcript.utterances)} utterances, {actual_speakers} speakers detected")

    formatted = format_diarized_transcript(transcript.utterances)

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
