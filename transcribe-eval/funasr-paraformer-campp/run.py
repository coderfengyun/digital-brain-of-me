"""FunASR Paraformer + cam++ transcription with speaker diarization."""

from funasr import AutoModel
import json
import time
import sys

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/yangdoudou/Downloads/新录音 2.m4a'
    output_txt = sys.argv[2] if len(sys.argv) > 2 else 'transcript.txt'
    output_json = sys.argv[3] if len(sys.argv) > 3 else 'result.json'

    print("Loading models...")
    start = time.time()

    model = AutoModel(
        model='iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
        vad_model='fsmn-vad',
        vad_kwargs={'max_single_segment_time': 30000},
        spk_model='cam++',
        punc_model='ct-punc',
        device='cpu',
    )

    print(f"Models loaded in {time.time()-start:.1f}s")
    print(f"Transcribing: {input_file}")

    res = model.generate(
        input=input_file,
        cache={},
        batch_size_s=60,
    )

    elapsed = time.time() - start
    print(f"Transcription done in {elapsed:.1f}s")

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    with open(output_txt, 'w', encoding='utf-8') as f:
        total = 0
        for item in res:
            if 'sentence_info' in item:
                for sent in item['sentence_info']:
                    spk = sent.get('spk', '?')
                    start_ms = sent.get('start', 0)
                    end_ms = sent.get('end', 0)
                    text = sent.get('text', '')
                    f.write(f"[Speaker {spk}] {start_ms}ms-{end_ms}ms: {text}\n")
                    total += 1
        f.write(f"\n--- Total: {total} sentences, elapsed: {elapsed:.1f}s ---\n")

    print(f"Saved {total} sentences to {output_txt}")
    print(f"Saved raw JSON to {output_json}")


if __name__ == '__main__':
    main()
