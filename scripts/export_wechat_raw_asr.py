from pathlib import Path
import subprocess


ROOT = Path("/private/tmp")
OUT = Path("investment/洪灏/2026-10-09-微信群视频/机器转录原文.md")
SETS = [
    ("一、洪灝：恒指目标、四季度机会和投资的要义", ROOT / "honghao-01-20s", False),
    ("二、洪灝：别人恐慌，我们贪婪", ROOT / "honghao-02-20s", False),
    ("三、洪灝：当下的情况", ROOT / "honghao-03-20s", False),
    ("四、洪灝：期待政策东风", ROOT / "honghao-04-true-20s", True),
]

header = """# 微信视频机器转录原文

生成日期：2026-10-10

说明：本文件逐段保留本地 ASR 的未经润色输出。每段约 20 秒；错别字、粤语同音字、断句、语言混杂和模型误识别均未修改。第四段录音存在系统串音，除英文采访片段外不能视为洪灝原话。

"""

with OUT.open("w", encoding="utf-8") as dst:
    dst.write(header)
    for title, folder, mixed in SETS:
        dst.write(f"## {title}\n\n")
        if mixed:
            dst.write("> ⚠️ 本段含明显后台串音；以下仅为录音文件的原始机器输出，不代表视频原声。\n\n")
        for wav in sorted(folder.glob("part-*.wav")):
            cmd = [
                "uv", "run", "python", "-c",
                "from qwen3_asr_mlx import Qwen3ASR; import sys; "
                "m=Qwen3ASR.from_pretrained('mlx-community/Qwen3-ASR-0.6B-bf16'); "
                "print(m.transcribe(sys.argv[1], language='zh').text, flush=True)",
                str(wav),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            text = result.stdout.strip()
            dst.write(f"### {wav.stem}\n\n{text}\n\n")

print(OUT)
