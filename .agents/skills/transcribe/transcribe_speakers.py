#!/usr/bin/env python3
"""Local speaker diarization plus Qwen3-ASR transcription.

pyannote produces the speaker timeline. Qwen3-ASR 0.6B transcribes each
speaker turn. Both models must already be available locally; this script never
downloads model weights.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


QWEN_MODEL_NAME = "Qwen3-ASR-0.6B"
QWEN_REPO_ID = "mlx-community/Qwen3-ASR-0.6B-bf16"
DIARIZATION_REPO_ID = "pyannote/speaker-diarization-community-1"


def find_project_root() -> Path:
    path = Path(__file__).resolve().parent
    while path != path.parent:
        if (path / ".git").exists():
            return path
        path = path.parent
    return Path.cwd()


PROJECT_ROOT = find_project_root()
SOURCES_JSONL = PROJECT_ROOT / "sources" / "sources.jsonl"


def load_project_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass


def cached_hf_snapshot(repo_id: str) -> Path | None:
    """Return an already-downloaded Hugging Face snapshot without networking."""
    hf_home = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface"))
    repo_dir = hf_home / "hub" / f"models--{repo_id.replace('/', '--')}"
    ref = repo_dir / "refs" / "main"
    if ref.exists():
        snapshot = repo_dir / "snapshots" / ref.read_text(encoding="utf-8").strip()
        if snapshot.exists():
            return snapshot
    snapshots = repo_dir / "snapshots"
    if snapshots.exists():
        candidates = sorted(
            (path for path in snapshots.iterdir() if path.is_dir()),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        if candidates:
            return candidates[0]
    return None


def resolve_model_path(explicit: str | None, kind: str) -> Path:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if path.exists():
            return path
        raise FileNotFoundError(f"Model path does not exist: {path}")

    models_dir = Path(os.environ.get("MODELS_DIR", "~/Models")).expanduser()
    if kind == "asr":
        candidates = [
            models_dir / f"{QWEN_MODEL_NAME}-MLX",
            models_dir / QWEN_MODEL_NAME,
            cached_hf_snapshot(QWEN_REPO_ID),
        ]
        label = "Qwen3-ASR 0.6B MLX"
    else:
        candidates = [
            models_dir / "speaker-diarization-community-1",
            models_dir / "pyannote" / "speaker-diarization-community-1",
            cached_hf_snapshot(DIARIZATION_REPO_ID),
        ]
        label = "pyannote speaker-diarization-community-1"

    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(
        f"Local {label} model not found. Download it first or pass the model path explicitly."
    )


def convert_to_wav(audio_path: Path, wav_path: Path) -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required but was not found")
    result = subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(audio_path),
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            "-y",
            str(wav_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg conversion failed: {result.stderr.strip()}")


def merge_turns(
    segments: list[dict], min_duration: float = 0.2, max_gap: float = 1.0
) -> list[dict]:
    """Remove noise-sized detections and merge adjacent turns from one speaker."""
    filtered = sorted(
        (
            dict(segment)
            for segment in segments
            if segment["end"] - segment["start"] >= min_duration
        ),
        key=lambda segment: (segment["start"], segment["end"]),
    )
    merged: list[dict] = []
    for segment in filtered:
        if (
            merged
            and segment["speaker"] == merged[-1]["speaker"]
            and segment["start"] - merged[-1]["end"] <= max_gap
        ):
            merged[-1]["end"] = max(merged[-1]["end"], segment["end"])
        else:
            merged.append(segment)
    return merged


def speaker_mapping(segments: list[dict], names: list[str] | None) -> dict[str, str]:
    labels: list[str] = []
    for segment in segments:
        label = segment["speaker"]
        if label not in labels and segment["end"] - segment["start"] >= 0.5:
            labels.append(label)
    for segment in segments:
        if segment["speaker"] not in labels:
            labels.append(segment["speaker"])

    if names:
        if len(names) != len(labels):
            raise ValueError(
                f"--speaker-names contains {len(names)} names, but diarization found "
                f"{len(labels)} speakers"
            )
        return dict(zip(labels, names, strict=True))

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return {
        label: f"说话人 {alphabet[index] if index < len(alphabet) else index + 1}"
        for index, label in enumerate(labels)
    }


def timestamp(seconds: float) -> str:
    total = max(0, int(math.floor(seconds)))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def sanitize_filename(name: str, max_len: int = 50) -> str:
    safe = re.sub(r"[^\w\s-]", "", name)
    safe = re.sub(r"[\s-]+", "-", safe).strip("-")
    return safe[:max_len]


def generate_id() -> str:
    date_str = datetime.now().strftime("%Y%m%d")
    existing: set[str] = set()
    if SOURCES_JSONL.exists():
        for line in SOURCES_JSONL.read_text(encoding="utf-8").splitlines():
            if line.strip():
                source_id = json.loads(line)["id"]
                if source_id.startswith(f"pod-{date_str}"):
                    existing.add(source_id)
    sequence = 1
    while f"pod-{date_str}-{sequence:03d}" in existing:
        sequence += 1
    return f"pod-{date_str}-{sequence:03d}"


def render_markdown(
    title: str,
    show: str,
    language: str,
    turns: list[dict],
    names: dict[str, str],
    source: str | None,
) -> str:
    lines = [
        f"# {title}（按说话人拆分）",
        "",
        f"**Show:** {show}",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
    ]
    if source:
        lines.append(f"**Source:** [{source}]({source})")
    lines.extend(
        [
            f"**Language:** {language}",
            "**Model:** Qwen3-ASR-0.6B + pyannote speaker-diarization-community-1",
            "**Note:** 说话人标签按首次主要发言排序；短促或重叠发言可能存在边界误差。",
            "",
            "## Transcript",
            "",
        ]
    )
    for turn in turns:
        lines.extend(
            [
                f"**[{timestamp(turn['start'])}–{timestamp(turn['end'])}] "
                f"{names[turn['speaker']]}：**",
                "",
                turn["text"],
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def append_source(entry: dict) -> None:
    SOURCES_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with SOURCES_JSONL.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")


def resolve_python(explicit: str | None, env_name: str, default: Path) -> Path:
    value = explicit or os.environ.get(env_name) or str(default)
    expanded = Path(value).expanduser()
    if expanded.exists():
        # Do not call Path.resolve() here: venv Python executables are often
        # symlinks to the base interpreter. Dereferencing that symlink drops
        # the virtual environment and therefore all of its installed packages.
        return Path(os.path.abspath(expanded))
    executable = shutil.which(value)
    if executable:
        return Path(executable).resolve()
    raise FileNotFoundError(
        f"Python interpreter not found: {value}. Pass it explicitly or set {env_name}."
    )


def default_asr_python() -> Path:
    """Prefer the persistent ASR runtime stored beside local model weights."""
    models_dir = Path(os.environ.get("MODELS_DIR", "~/Models")).expanduser()
    persistent = models_dir / ".venvs" / "qwen3-asr-mlx" / "bin" / "python"
    if persistent.exists():
        return persistent
    return PROJECT_ROOT / ".venv" / "bin" / "python"


def run_worker(command: list[str], cache_dir: Path) -> None:
    environment = os.environ.copy()
    environment["HF_HUB_OFFLINE"] = "1"
    environment["MPLCONFIGDIR"] = str(cache_dir / "matplotlib")
    environment["XDG_CACHE_HOME"] = str(cache_dir / "xdg")
    Path(environment["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    Path(environment["XDG_CACHE_HOME"]).mkdir(parents=True, exist_ok=True)
    result = subprocess.run(command, env=environment)
    if result.returncode != 0:
        raise RuntimeError(f"Worker failed with exit code {result.returncode}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local speaker diarization with pyannote and Qwen3-ASR"
    )
    parser.add_argument("--audio", required=True, help="Local audio/video path")
    parser.add_argument("--title", required=True, help="Recording title")
    parser.add_argument("--show", default="Unknown", help="Show or author name")
    parser.add_argument("--output-dir", required=True, help="Transcript output directory")
    parser.add_argument("--language", default="Chinese", help="Qwen language name")
    parser.add_argument("--speakers", type=int, default=None, help="Expected speakers")
    parser.add_argument(
        "--speaker-names",
        help="Comma-separated names ordered by first substantial appearance",
    )
    parser.add_argument("--context", help="Optional ASR vocabulary/topic hint")
    parser.add_argument("--asr-model", help="Local Qwen3-ASR MLX model directory")
    parser.add_argument(
        "--diarization-model", help="Local pyannote pipeline directory"
    )
    parser.add_argument(
        "--asr-python",
        help="Python with qwen3-asr-mlx (default: .venv/bin/python)",
    )
    parser.add_argument(
        "--diarization-python",
        help="Python with pyannote-audio (default: .venv-diarize/bin/python)",
    )
    parser.add_argument("--save-segments", help="Optional raw speaker JSON output")
    parser.add_argument("--min-segment-duration", type=float, default=0.2)
    parser.add_argument("--merge-gap", type=float, default=1.0)
    parser.add_argument("--url", help="Source URL")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument(
        "--no-register-source",
        action="store_true",
        help="Do not append an entry to sources/sources.jsonl",
    )
    args = parser.parse_args()

    load_project_env()
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    audio_path = Path(args.audio).expanduser().resolve()
    if not audio_path.exists():
        parser.error(f"Audio file not found: {audio_path}")
    output_dir = Path(args.output_dir).expanduser()
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    asr_model = resolve_model_path(args.asr_model, "asr")
    diarization_model = resolve_model_path(args.diarization_model, "diarization")
    asr_python = resolve_python(
        args.asr_python,
        "ASR_PYTHON",
        default_asr_python(),
    )
    diarization_python = resolve_python(
        args.diarization_python,
        "DIARIZATION_PYTHON",
        PROJECT_ROOT / ".venv-diarize" / "bin" / "python",
    )

    episode_id = generate_id()
    filename = (
        f"{sanitize_filename(args.show)}_{sanitize_filename(args.title)}_"
        f"{episode_id}_speakers.md"
    )
    output_path = output_dir / filename
    skill_dir = Path(__file__).resolve().parent

    with tempfile.TemporaryDirectory(prefix="speaker-transcribe-") as tmpdir:
        temporary_dir = Path(tmpdir)
        wav_path = temporary_dir / "audio.wav"
        segments_path = temporary_dir / "segments.json"
        convert_to_wav(audio_path, wav_path)
        diarization_command = [
            str(diarization_python),
            str(skill_dir / "diarize_speakers_worker.py"),
            "--audio",
            str(wav_path),
            "--model",
            str(diarization_model),
            "--output",
            str(segments_path),
        ]
        if args.speakers:
            diarization_command.extend(["--speakers", str(args.speakers)])
        run_worker(diarization_command, temporary_dir / "cache-diarization")

        if args.save_segments:
            segment_path = Path(args.save_segments).expanduser()
            segment_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(segments_path, segment_path)

        transcription_command = [
            str(asr_python),
            str(skill_dir / "transcribe_speakers_worker.py"),
            "--audio",
            str(wav_path),
            "--segments",
            str(segments_path),
            "--model",
            str(asr_model),
            "--output",
            str(output_path),
            "--title",
            args.title,
            "--show",
            args.show,
            "--language",
            args.language,
            "--min-segment-duration",
            str(args.min_segment_duration),
            "--merge-gap",
            str(args.merge_gap),
        ]
        if args.speaker_names:
            transcription_command.extend(["--speaker-names", args.speaker_names])
        if args.context:
            transcription_command.extend(["--context", args.context])
        if args.url:
            transcription_command.extend(["--source", args.url])
        run_worker(transcription_command, temporary_dir / "cache-asr")

    if not args.no_register_source:
        try:
            output_value = str(output_path.relative_to(PROJECT_ROOT))
        except ValueError:
            output_value = str(output_path)
        append_source(
            {
                "id": episode_id,
                "type": "podcast",
                "source": args.url or "",
                "title": args.title,
                "tags": [tag.strip() for tag in args.tags.split(",") if tag.strip()],
                "added_at": datetime.now().strftime("%Y-%m-%d"),
                "output": output_value,
            }
        )
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
