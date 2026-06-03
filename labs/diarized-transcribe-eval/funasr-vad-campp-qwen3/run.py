"""FunASR VAD + cam++ clustering + Qwen3-ASR transcription evaluation."""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

EVAL_DIR = Path(__file__).parent
DEFAULT_AUDIO = EVAL_DIR.parent / "test-audio.m4a"
ASR_MODEL = str(Path("~/Models/Qwen3-ASR-1.7B-4bit").expanduser())
MAX_SPEAKERS = 6


def prepare_wav(audio_path: str) -> str:
    if audio_path.endswith(".wav"):
        return audio_path
    wav_path = str(EVAL_DIR / "input_16k.wav")
    subprocess.run(
        ["ffmpeg", "-i", audio_path, "-ar", "16000", "-ac", "1", "-y", wav_path],
        capture_output=True, check=True,
    )
    return wav_path


def get_vad_segments(wav_path: str) -> list[dict]:
    from funasr import AutoModel

    print("  [1/4] FunASR VAD: detecting speech segments...")
    vad_model = AutoModel(
        model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        disable_update=True,
    )
    res = vad_model.generate(input=wav_path, cache={})
    segments = []
    for interval in res[0]["value"]:
        segments.append({"start_ms": interval[0], "end_ms": interval[1]})
    print(f"  VAD done: {len(segments)} segments")
    return segments


def extract_embeddings(wav_path: str, segments: list[dict]) -> np.ndarray:
    from funasr import AutoModel
    import torch

    print(f"  [2/4] cam++: extracting speaker embeddings for {len(segments)} segments...")
    spk_model = AutoModel(model="iic/speech_campplus_sv_zh-cn_16k-common", disable_update=True)

    embeddings = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, seg in enumerate(segments):
            seg_path = os.path.join(tmpdir, f"seg_{i:04d}.wav")
            duration_ms = seg["end_ms"] - seg["start_ms"]

            if duration_ms < 300:
                embeddings.append(np.zeros(192))
                continue

            start_s = seg["start_ms"] / 1000.0
            duration_s = duration_ms / 1000.0
            subprocess.run(
                ["ffmpeg", "-i", wav_path, "-ss", str(start_s), "-t", str(duration_s),
                 "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", "-y", seg_path],
                capture_output=True, check=True,
            )

            res = spk_model.generate(input=seg_path)
            emb = res[0]["spk_embedding"].squeeze().numpy()
            embeddings.append(emb)

            if (i + 1) % 100 == 0:
                print(f"    Embeddings: {i + 1}/{len(segments)}...")

    return np.array(embeddings)


def cluster_speakers(embeddings: np.ndarray, max_speakers: int) -> list[int]:
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.preprocessing import normalize

    print(f"  [3/4] Clustering into max {max_speakers} speakers...")
    valid_mask = np.any(embeddings != 0, axis=1)
    valid_embeddings = normalize(embeddings[valid_mask])

    clustering = AgglomerativeClustering(
        n_clusters=max_speakers,
        metric="cosine",
        linkage="average",
    )
    valid_labels = clustering.fit_predict(valid_embeddings)

    labels = np.full(len(embeddings), -1, dtype=int)
    labels[valid_mask] = valid_labels

    unique_speakers = len(set(valid_labels))
    print(f"  Clustering done: {unique_speakers} speakers")
    return labels.tolist()


def transcribe_segments(wav_path: str, segments: list[dict]) -> list[dict]:
    from mlx_audio.stt.utils import load_model

    print(f"  [4/4] Loading Qwen3-ASR model...")
    model = load_model(ASR_MODEL)

    print(f"  Transcribing {len(segments)} segments...")
    results = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, seg in enumerate(segments):
            seg_path = os.path.join(tmpdir, f"seg_{i:04d}.wav")
            duration_ms = seg["end_ms"] - seg["start_ms"]

            if duration_ms < 300:
                results.append("")
                continue

            start_s = seg["start_ms"] / 1000.0
            duration_s = duration_ms / 1000.0
            cmd_result = subprocess.run(
                ["ffmpeg", "-i", wav_path, "-ss", str(start_s), "-t", str(duration_s),
                 "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", "-y", seg_path],
                capture_output=True,
            )
            if cmd_result.returncode != 0:
                results.append("")
                continue

            result = model.generate(seg_path, language="zh")
            results.append(result.text.strip())

            if (i + 1) % 50 == 0:
                print(f"    Transcribed: {i + 1}/{len(segments)}...")

    return results


def main():
    audio_path = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT_AUDIO)
    max_speakers = int(sys.argv[2]) if len(sys.argv) > 2 else MAX_SPEAKERS
    output_txt = EVAL_DIR / "transcript.txt"
    output_json = EVAL_DIR / "result.json"

    print(f"=== FunASR VAD + cam++ + Qwen3-ASR Evaluation ===")
    print(f"Audio: {audio_path}")
    print(f"Max speakers: {max_speakers}")
    start = time.time()

    wav_path = prepare_wav(audio_path)
    print(f"  Prepared WAV: {wav_path}")

    segments = get_vad_segments(wav_path)
    embeddings = extract_embeddings(wav_path, segments)
    labels = cluster_speakers(embeddings, max_speakers)
    texts = transcribe_segments(wav_path, segments)

    elapsed = time.time() - start

    results = []
    for seg, label, text in zip(segments, labels, texts):
        results.append({
            "speaker": int(label),
            "start_ms": seg["start_ms"],
            "end_ms": seg["end_ms"],
            "text": text,
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
