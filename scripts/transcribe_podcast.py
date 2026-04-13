#!/usr/bin/env python3
"""
Podcast transcription script using whisper.cpp.

Supports two modes:
1. RSS feed: Download audio from podcast RSS feed and transcribe
2. Local audio: Transcribe a local audio file directly

Usage:
    # From RSS feed
    python scripts/transcribe_podcast.py --rss "https://example.com/feed.xml" --count 1

    # From local audio file
    python scripts/transcribe_podcast.py --audio ~/Downloads/episode.mp3 --title "Episode Title" --show "Show Name"
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PODCASTS_DIR = PROJECT_ROOT / "podcasts"
TRANSCRIPTS_DIR = PODCASTS_DIR / "transcripts"
SOURCES_JSONL = PROJECT_ROOT / "sources" / "sources.jsonl"

# Whisper model search paths
MODEL_SEARCH_PATHS = [
    Path.home() / ".cache" / "whisper-cpp",
    Path("/opt/homebrew/share/whisper-cpp"),
    Path("/usr/local/share/whisper-cpp"),
    PROJECT_ROOT / "models",
]

# whisper-cli binary
WHISPER_CLI = shutil.which("whisper-cli") or "whisper-cli"


def find_model(model_name: str) -> str | None:
    """Find whisper model file in known locations."""
    filename = f"ggml-{model_name}.bin"
    for search_path in MODEL_SEARCH_PATHS:
        model_path = search_path / filename
        if model_path.exists():
            return str(model_path)
    return None


def sanitize_filename(name: str, max_len: int = 50) -> str:
    """Create a safe filename from a string."""
    safe = re.sub(r'[^\w\s-]', '', name)
    safe = re.sub(r'[\s-]+', '-', safe).strip('-')
    return safe[:max_len]


def convert_to_wav(audio_path: str, wav_path: str) -> bool:
    """Convert audio file to 16kHz mono WAV using ffmpeg."""
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        "-y", wav_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def transcribe_audio(wav_path: str, model_name: str, language: str | None = None) -> str | None:
    """Run whisper-cli on a WAV file and return transcript text."""
    model_path = find_model(model_name)
    if not model_path:
        print(f"Error: Model ggml-{model_name}.bin not found.")
        print(f"Download it: curl -L -o ~/.cache/whisper-cpp/ggml-{model_name}.bin "
              f"https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-{model_name}.bin")
        return None

    cmd = [WHISPER_CLI, "-m", model_path, "-f", wav_path, "--no-timestamps"]
    if language:
        cmd.extend(["-l", language])

    print(f"  Transcribing with whisper-cpp ({model_name} model)...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

    if result.returncode != 0:
        print(f"  Error: whisper-cli failed: {result.stderr[:500]}")
        return None

    # Parse output: skip lines starting with [ (timestamp lines) and blank lines
    lines = []
    for line in result.stdout.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith('['):
            lines.append(line)

    return '\n\n'.join(lines) if lines else result.stdout.strip()


def format_transcript(text: str) -> str:
    """Format raw transcript into readable paragraphs."""
    # Split into sentences and group ~3 per paragraph
    sentences = re.split(r'(?<=[.!?])\s+', text)
    paragraphs = []
    for i in range(0, len(sentences), 3):
        paragraph = ' '.join(sentences[i:i+3])
        if paragraph.strip():
            paragraphs.append(paragraph.strip())
    return '\n\n'.join(paragraphs)


def generate_id() -> str:
    """Generate a podcast episode ID."""
    date_str = datetime.now().strftime('%Y%m%d')
    # Find existing IDs for today
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


def save_transcript_md(transcript: str, episode_data: dict, model_name: str,
                       show: str = 'Unknown', language: str = 'auto',
                       description: str = '') -> Path:
    """Save transcript as markdown file.

    show/language/description are processing-time metadata written into the .md
    header but NOT stored in sources.jsonl.
    """
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    safe_show = sanitize_filename(show)
    safe_title = sanitize_filename(episode_data.get('title', 'Untitled'))
    episode_id = episode_data['id']
    filename = f"{safe_show}_{safe_title}_{episode_id}.md"
    output_path = TRANSCRIPTS_DIR / filename

    formatted = format_transcript(transcript)

    content = f"# {episode_data.get('title', 'Untitled')}\n\n"
    content += f"**Show:** {show}\n"
    content += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n"
    if episode_data.get('source'):
        content += f"**Source:** [{episode_data['source']}]({episode_data['source']})\n"
    content += f"**Language:** {language}\n"
    content += f"**Model:** whisper-{model_name}\n\n"
    if description:
        content += f"## Description\n\n{description}\n\n"
    content += f"## Transcript\n\n{formatted}\n"

    output_path.write_text(content, encoding='utf-8')
    return output_path


def append_jsonl(episode_data: dict):
    """Append episode metadata to sources.jsonl."""
    with open(SOURCES_JSONL, 'a') as f:
        f.write(json.dumps(episode_data, ensure_ascii=False) + '\n')


def transcribe_from_rss(rss_url: str, count: int, model: str, language: str | None):
    """Download and transcribe episodes from RSS feed."""
    try:
        import feedparser
    except ImportError:
        print("Error: feedparser not installed. Run: pip install feedparser")
        sys.exit(1)

    try:
        import requests
    except ImportError:
        print("Error: requests not installed. Run: pip install requests")
        sys.exit(1)

    print(f"Fetching RSS feed: {rss_url}")
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        print("Error: No episodes found in RSS feed.")
        return

    show_name = feed.feed.get('title', 'Unknown Show')
    print(f"Show: {show_name}")
    print(f"Episodes available: {len(feed.entries)}")
    print(f"Transcribing latest {count} episode(s)...\n")

    for i, entry in enumerate(feed.entries[:count]):
        title = entry.get('title', f'Episode {i+1}')
        description = entry.get('summary', '')
        link = entry.get('link', '')
        published = entry.get('published', '')

        # Find audio URL from enclosures
        audio_url = None
        for enclosure in entry.get('enclosures', []):
            if 'audio' in enclosure.get('type', ''):
                audio_url = enclosure.get('href')
                break

        # Fallback: check links
        if not audio_url:
            for link_entry in entry.get('links', []):
                if 'audio' in link_entry.get('type', ''):
                    audio_url = link_entry.get('href')
                    break

        if not audio_url:
            print(f"  [{i+1}/{count}] Skipping '{title}' - no audio URL found")
            continue

        print(f"  [{i+1}/{count}] {title}")
        print(f"  Audio: {audio_url[:80]}...")

        episode_id = generate_id()

        # Download audio to temp file
        with tempfile.TemporaryDirectory() as tmpdir:
            ext = Path(audio_url.split('?')[0]).suffix or '.mp3'
            audio_path = os.path.join(tmpdir, f"episode{ext}")
            wav_path = os.path.join(tmpdir, "episode.wav")

            print(f"  Downloading audio...")
            response = requests.get(audio_url, stream=True, timeout=60)
            response.raise_for_status()
            with open(audio_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"  Converting to WAV (16kHz mono)...")
            if not convert_to_wav(audio_path, wav_path):
                print(f"  Error: ffmpeg conversion failed")
                continue

            transcript = transcribe_audio(wav_path, model, language)
            if not transcript:
                continue

        # Save results
        episode_data = {
            'id': episode_id,
            'type': 'podcast',
            'source': link,
            'title': title,
            'tags': [],
            'added_at': datetime.now().strftime('%Y-%m-%d'),
            'output': '',
        }

        output_path = save_transcript_md(
            transcript, episode_data, model,
            show=show_name, language=language or 'auto', description=description)
        episode_data['output'] = str(output_path.relative_to(PROJECT_ROOT))
        append_jsonl(episode_data)

        print(f"  Saved: {output_path.relative_to(PROJECT_ROOT)}")
        print()

    print("Done!")


def transcribe_from_file(audio_path: str, title: str, show: str, model: str,
                         language: str | None, url: str | None, tags: list[str]):
    """Transcribe a local audio file."""
    audio_path = Path(audio_path).resolve()
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)

    print(f"Transcribing: {audio_path.name}")
    episode_id = generate_id()

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = os.path.join(tmpdir, "episode.wav")

        print(f"  Converting to WAV (16kHz mono)...")
        if not convert_to_wav(str(audio_path), wav_path):
            print("  Error: ffmpeg conversion failed")
            sys.exit(1)

        transcript = transcribe_audio(wav_path, model, language)
        if not transcript:
            sys.exit(1)

    episode_data = {
        'id': episode_id,
        'type': 'podcast',
        'source': url or '',
        'title': title,
        'tags': tags,
        'added_at': datetime.now().strftime('%Y-%m-%d'),
        'output': '',
    }

    output_path = save_transcript_md(
        transcript, episode_data, model,
        show=show, language=language or 'auto')
    episode_data['output'] = str(output_path.relative_to(PROJECT_ROOT))
    append_jsonl(episode_data)

    print(f"  Saved: {output_path.relative_to(PROJECT_ROOT)}")
    print("Done!")


def main():
    parser = argparse.ArgumentParser(description='Transcribe podcast episodes using whisper.cpp')

    # Input source (mutually exclusive)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--rss', help='RSS feed URL to download and transcribe episodes')
    source.add_argument('--audio', help='Path to local audio file')

    # RSS options
    parser.add_argument('--count', type=int, default=1, help='Number of episodes to transcribe from RSS (default: 1)')

    # Audio file options
    parser.add_argument('--title', default='Untitled Episode', help='Episode title (for local audio)')
    parser.add_argument('--show', default='Unknown Show', help='Show name (for local audio)')
    parser.add_argument('--url', help='Source URL (optional, for local audio)')
    parser.add_argument('--tags', default='', help='Comma-separated tags')

    # Whisper options
    parser.add_argument('--model', default='base', choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper model size (default: base)')
    parser.add_argument('--language', '-l', help='Language code (e.g., en, zh, ja). Auto-detect if not specified.')

    args = parser.parse_args()

    # Verify whisper-cli is available
    if not shutil.which("whisper-cli"):
        print("Error: whisper-cli not found. Install with: brew install whisper-cpp")
        sys.exit(1)

    # Verify ffmpeg is available
    if not shutil.which("ffmpeg"):
        print("Error: ffmpeg not found. Install with: brew install ffmpeg")
        sys.exit(1)

    # Ensure output directories exist
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    tags = [t.strip() for t in args.tags.split(',') if t.strip()] if args.tags else []

    if args.rss:
        transcribe_from_rss(args.rss, args.count, args.model, args.language)
    else:
        transcribe_from_file(args.audio, args.title, args.show, args.model,
                             args.language, args.url, tags)


if __name__ == '__main__':
    main()
