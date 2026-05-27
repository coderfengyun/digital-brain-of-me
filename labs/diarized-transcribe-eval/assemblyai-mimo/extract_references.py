"""从 diarization 结果中自动提取每个说话人最干净的参考音频片段。"""

import json
import subprocess
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).parent
DEFAULT_AUDIO = EVAL_DIR.parent / "test-audio.m4a"
SPEAKERS_JSON = EVAL_DIR / "speakers.json"
OUTPUT_DIR = EVAL_DIR / "references"


def find_best_reference(segments: list[dict], speaker_segments: list[dict]) -> dict:
    """选择前后间隔最大、时长 3-8 秒的片段作为参考。"""
    candidates = [
        s for s in speaker_segments
        if 3000 <= s["duration_ms"] <= 8000
        and s["gap_before"] >= 200
        and s["gap_after"] >= 200
    ]
    if not candidates:
        candidates = [s for s in speaker_segments if 2000 <= s["duration_ms"] <= 12000]
    if not candidates:
        candidates = speaker_segments

    candidates.sort(key=lambda x: x["gap_before"] + x["gap_after"], reverse=True)
    return candidates[0]


def main():
    audio_path = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else str(DEFAULT_AUDIO)

    segments = json.load(open(SPEAKERS_JSON, encoding="utf-8"))

    by_speaker: dict[str, list] = {}
    for i, seg in enumerate(segments):
        spk = seg["speaker"]
        if spk not in by_speaker:
            by_speaker[spk] = []

        duration_ms = seg["end_ms"] - seg["start_ms"]
        gap_before = seg["start_ms"] - segments[i - 1]["end_ms"] if i > 0 else 1000
        gap_after = segments[i + 1]["start_ms"] - seg["end_ms"] if i < len(segments) - 1 else 1000

        by_speaker[spk].append({
            "idx": i,
            "start_ms": seg["start_ms"],
            "end_ms": seg["end_ms"],
            "duration_ms": duration_ms,
            "gap_before": gap_before,
            "gap_after": gap_after,
        })

    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"提取 {len(by_speaker)} 个说话人的参考音频")
    print(f"音频源: {audio_path}\n")

    for spk in sorted(by_speaker.keys()):
        best = find_best_reference(segments, by_speaker[spk])
        out_path = OUTPUT_DIR / f"speaker_{spk}.wav"

        start_s = best["start_ms"] / 1000.0
        duration_s = best["duration_ms"] / 1000.0

        cmd = [
            "ffmpeg", "-i", audio_path,
            "-ss", str(start_s), "-t", str(duration_s),
            "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
            "-y", str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"  Speaker {spk}: {best['duration_ms']}ms "
                  f"(gap_before={best['gap_before']}ms, gap_after={best['gap_after']}ms) "
                  f"→ {out_path.name}")
        else:
            print(f"  Speaker {spk}: FAILED - {result.stderr[:100]}")

    print(f"\n参考音频已保存到 {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
