#!/usr/bin/env python3
"""
GCP Speech-to-Text v2 transcription with speaker diarization.

Usage:
    uv run .claude/skills/transcribe/transcribe_gcp.py \
        --audio ~/Downloads/podcast.mp3 \
        --title "对话标题" \
        --show "节目名" \
        --output-dir investment/洪灏/ \
        --language zh-CN \
        --speakers 2
"""

import argparse
import json
import os
import re
import shutil
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


def convert_to_flac(audio_path: str, flac_path: str) -> bool:
    """Convert audio/video to 16kHz mono FLAC using ffmpeg."""
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-ar", "16000", "-ac", "1",
        "-c:a", "flac",
        "-y", flac_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ffmpeg error: {result.stderr[:500]}")
    return result.returncode == 0


def upload_to_gcs(local_path: str, bucket_name: str, blob_name: str) -> str:
    """Upload file to GCS and return gs:// URI."""
    from google.cloud import storage

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    print(f"  Uploading to gs://{bucket_name}/{blob_name}...")
    blob.upload_from_filename(local_path)
    return f"gs://{bucket_name}/{blob_name}"


def delete_from_gcs(bucket_name: str, blob_name: str):
    """Delete a file from GCS."""
    from google.cloud import storage

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()


def batch_recognize(
    gcs_uri: str,
    project_id: str,
    language: str,
    min_speakers: int,
    max_speakers: int,
    location: str = "global",
) -> list[dict]:
    """Run GCP Speech-to-Text v2 batch recognize with speaker diarization.

    Returns list of {word, speaker_label} dicts.
    """
    from google.cloud.speech_v2 import SpeechClient
    from google.cloud.speech_v2.types import cloud_speech

    client = SpeechClient()

    recognizer_name = f"projects/{project_id}/locations/{location}/recognizers/_"

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[language],
        model="long",
        features=cloud_speech.RecognitionFeatures(
            enable_word_time_offsets=True,
            diarization_config=cloud_speech.SpeakerDiarizationConfig(
                min_speaker_count=min_speakers,
                max_speaker_count=max_speakers,
            ),
        ),
    )

    file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=gcs_uri)

    request = cloud_speech.BatchRecognizeRequest(
        recognizer=recognizer_name,
        config=config,
        files=[file_metadata],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )

    print("  Starting batch recognition...")
    operation = client.batch_recognize(request=request)

    print("  Waiting for transcription to complete (polling every 15s)...")
    while not operation.done():
        time.sleep(15)
        print("    Still processing...")

    response = operation.result()

    words_with_speakers = []
    for file_uri, file_result in response.results.items():
        for result in file_result.transcript.results:
            if not result.alternatives:
                continue
            alt = result.alternatives[0]
            for word_info in alt.words:
                words_with_speakers.append({
                    "word": word_info.word,
                    "speaker": word_info.speaker_label or "0",
                })

    return words_with_speakers


def aggregate_speakers(words: list[dict]) -> list[dict]:
    """Aggregate word-level speaker labels into speaker segments.

    Returns list of {speaker, text} dicts.
    """
    if not words:
        return []

    segments = []
    current_speaker = words[0]["speaker"]
    current_words = []

    for w in words:
        if w["speaker"] != current_speaker:
            segments.append({
                "speaker": current_speaker,
                "text": "".join(current_words).strip(),
            })
            current_speaker = w["speaker"]
            current_words = []
        current_words.append(w["word"])

    if current_words:
        segments.append({
            "speaker": current_speaker,
            "text": "".join(current_words).strip(),
        })

    return segments


def format_diarized_transcript(segments: list[dict]) -> str:
    """Format speaker segments into readable markdown."""
    lines = []
    for seg in segments:
        if seg["text"]:
            lines.append(f"**Speaker {seg['speaker']}:** {seg['text']}")
    return "\n\n".join(lines)


def save_transcript_md(
    formatted_transcript: str,
    episode_data: dict,
    output_dir: Path,
    show: str,
    language: str,
    num_speakers: int,
    description: str = "",
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
    content += f"**Model:** gcp-speech-v2\n"
    content += f"**Speakers:** {num_speakers}\n\n"
    if description:
        content += f"## Description\n\n{description}\n\n"
    content += f"## Transcript\n\n{formatted_transcript}\n"

    output_path.write_text(content, encoding='utf-8')
    return output_path


def append_jsonl(episode_data: dict):
    SOURCES_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(SOURCES_JSONL, 'a') as f:
        f.write(json.dumps(episode_data, ensure_ascii=False) + '\n')


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe audio with GCP Speech-to-Text v2 (speaker diarization)'
    )
    parser.add_argument('--audio', required=True, help='Path to local audio/video file')
    parser.add_argument('--title', required=True, help='Episode/recording title')
    parser.add_argument('--show', required=True, help='Show or author name')
    parser.add_argument('--output-dir', required=True, help='Output directory for transcript')
    parser.add_argument('--language', default='zh-CN', help='BCP-47 language code (default: zh-CN)')
    parser.add_argument('--speakers', type=int, default=2, help='Expected number of speakers (default: 2)')
    parser.add_argument('--gcs-bucket', default=None, help='GCS bucket name (or set GCP_SPEECH_BUCKET env var)')
    parser.add_argument('--project', default=None, help='GCP project ID (or set GCP_PROJECT_ID env var)')
    parser.add_argument('--url', default=None, help='Source URL (optional)')
    parser.add_argument('--tags', default='', help='Comma-separated tags')

    args = parser.parse_args()

    audio_path = Path(args.audio).resolve()
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)

    bucket_name = args.gcs_bucket or os.environ.get('GCP_SPEECH_BUCKET')
    if not bucket_name:
        print("Error: GCS bucket not specified. Use --gcs-bucket or set GCP_SPEECH_BUCKET env var.")
        sys.exit(1)

    project_id = args.project or os.environ.get('GCP_PROJECT_ID')
    if not project_id:
        print("Error: GCP project ID not specified. Use --project or set GCP_PROJECT_ID env var.")
        sys.exit(1)

    if not shutil.which("ffmpeg"):
        print("Error: ffmpeg not found. Install with: brew install ffmpeg")
        sys.exit(1)

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir

    tags = [t.strip() for t in args.tags.split(',') if t.strip()] if args.tags else []

    print(f"Transcribing: {audio_path.name}")
    print(f"  Language: {args.language}, Speakers: {args.speakers}")

    episode_id = generate_id()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    blob_name = f"transcribe-tmp/{timestamp}_{audio_path.stem}.flac"

    with tempfile.TemporaryDirectory() as tmpdir:
        flac_path = os.path.join(tmpdir, "audio.flac")

        print("  Converting to FLAC (16kHz mono)...")
        if not convert_to_flac(str(audio_path), flac_path):
            print("  Error: ffmpeg conversion failed")
            sys.exit(1)

        gcs_uri = upload_to_gcs(flac_path, bucket_name, blob_name)

    try:
        words = batch_recognize(
            gcs_uri=gcs_uri,
            project_id=project_id,
            language=args.language,
            min_speakers=max(1, args.speakers - 1),
            max_speakers=args.speakers + 2,
        )

        if not words:
            print("  Warning: No transcription results returned.")
            sys.exit(1)

        print(f"  Transcription complete: {len(words)} words detected")

        segments = aggregate_speakers(words)
        formatted = format_diarized_transcript(segments)

    finally:
        print("  Cleaning up GCS temporary file...")
        try:
            delete_from_gcs(bucket_name, blob_name)
        except Exception as e:
            print(f"  Warning: Failed to delete GCS file: {e}")

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
        num_speakers=args.speakers,
    )
    episode_data['output'] = str(output_path.relative_to(PROJECT_ROOT))
    append_jsonl(episode_data)

    print(f"  Saved: {output_path.relative_to(PROJECT_ROOT)}")
    print("Done!")


if __name__ == '__main__':
    main()
