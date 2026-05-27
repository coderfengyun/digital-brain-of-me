"""从 diarization 结果中自动提取每个说话人最干净的参考音频片段。

选择策略：时长 3-8 秒 + 前后间隔大 + RMS 能量过滤（排除静音段）。
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

EVAL_DIR = Path(__file__).parent
DEFAULT_AUDIO = EVAL_DIR.parent / "test-audio.m4a"
SPEAKERS_JSON = EVAL_DIR / "speakers.json"
OUTPUT_DIR = EVAL_DIR / "references"


def get_rms(audio_path: str, start_ms: int, end_ms: int, source_audio: str) -> float:
    """用 ffmpeg 切片后计算 RMS 能量。"""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        cmd = [
            "ffmpeg", "-i", source_audio,
            "-ss", str(start_ms / 1000.0), "-t", str((end_ms - start_ms) / 1000.0),
            "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
            "-y", tmp.name,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return 0.0
        data = np.fromfile(tmp.name, dtype=np.int16, offset=44)  # skip WAV header
        if len(data) == 0:
            return 0.0
        return float(np.sqrt(np.mean(data.astype(np.float32) ** 2)))


def find_best_reference(speaker_segments: list[dict], source_audio: str, rms_threshold: float = 500.0) -> dict:
    """选择前后间隔最大、时长 3-8 秒、RMS 能量足够的片段。"""
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

    # 按间隔排序，逐个检查 RMS
    candidates.sort(key=lambda x: x["gap_before"] + x["gap_after"], reverse=True)

    for c in candidates:
        rms = get_rms(source_audio, c["start_ms"], c["end_ms"], source_audio)
        c["rms"] = rms
        if rms >= rms_threshold:
            return c

    # 全都低于阈值，选 RMS 最高的
    return max(candidates, key=lambda x: x.get("rms", 0))


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
        best = find_best_reference(by_speaker[spk], audio_path)
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
                  f"(gap_before={best['gap_before']}ms, gap_after={best['gap_after']}ms, "
                  f"rms={best.get('rms', 'N/A'):.0f}) → {out_path.name}")
        else:
            print(f"  Speaker {spk}: FAILED - {result.stderr[:100]}")

    print(f"\n参考音频已保存到 {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
