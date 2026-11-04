---
name: transcribe
description: "Audio/video transcription and local speaker diarization (Qwen3-ASR default, whisper.cpp fallback, pyannote speaker separation). Use when the user wants to transcribe spoken content or distinguish speakers in a recording, including podcasts, meetings, audio, video, Spotify episodes, and RSS feeds."
---

# Transcribe

将音频/视频转录为文字的独立工具。

输入 Spotify URL、RSS feed、本地音频或视频文件，输出 Markdown 格式的转录文本。

多人对话可额外使用本地 pyannote 声纹聚类，将音频拆成带时间戳的说话人轮次，再逐段交给 Qwen3-ASR 转录。模型权重必须预先存在，本 Skill 不自动下载模型。

## 引擎优先级

**Qwen3-ASR 0.6B > whisper.cpp**。脚本只在本地已有 Qwen3-ASR 0.6B 模型时使用它，否则 fallback 到 whisper.cpp，不会为了自动选择引擎而下载模型。可通过 `--engine whisper` 强制使用 whisper。

## 核心流程

```
Spotify URL → 查 RSS feed → 下载音频 → Qwen3-ASR/whisper 转录 → Markdown
RSS URL → 下载音频 → Qwen3-ASR/whisper 转录 → Markdown
本地音频 → Qwen3-ASR/whisper 转录 → Markdown
```

## 使用方式

### 方式一：从 Spotify 链接转录

Spotify 没有公开的播客音频下载或转录 API。核心路径：**Spotify URL → 查 RSS feed → 下载音频 → whisper.cpp 转录**。

**Step 1: 从 Spotify URL 找到 Show Name**

访问 Spotify episode 页面（`https://open.spotify.com/episode/<ID>`），提取播客节目名称。

**Step 2: 通过 iTunes Search API 查 RSS Feed**

```
https://itunes.apple.com/search?term=<Show+Name>&entity=podcast&limit=5
```

返回 JSON 中的 `feedUrl` 字段即为 RSS feed URL。这是最可靠的免费方式，无需 API key。

备选查询方式：Listen Notes、Podchaser、PodcastIndex.org。

**Step 3: 运行转录脚本**

```bash
python .codex/skills/transcribe/transcribe_podcast.py --rss "<RSS_URL>" --count 1 --model base --output-dir investment/洪灏/
```

### 方式二：通过 RSS Feed 转录

```bash
# 转录最新 1 集，输出到指定目录
python .codex/skills/transcribe/transcribe_podcast.py --rss "https://example.com/feed.xml" --count 1 --output-dir investment/洪灏/

# 转录最新 3 集，使用 small 模型（更高质量）
python .codex/skills/transcribe/transcribe_podcast.py --rss "https://example.com/feed.xml" --count 3 --model small --output-dir investment/洪灏/

# 指定语言
python .codex/skills/transcribe/transcribe_podcast.py --rss "https://example.com/feed.xml" --language zh --output-dir knowledge/research/
```

### 方式三：通过本地音频/视频文件转录

`--audio` 接受音频（.mp3, .wav, .m4a）和视频（.mp4, .webm）文件，ffmpeg 自动提取音频。

```bash
# 转录本地音频文件
python .codex/skills/transcribe/transcribe_podcast.py --audio ~/Downloads/episode.mp3 --title "Episode Title" --show "Show Name" --output-dir investment/卢麒元/

# 转录本地视频文件（自动提取音频）
python .codex/skills/transcribe/transcribe_podcast.py --audio ~/Downloads/video.mp4 --title "视频标题" --show "作者名" --url "https://weibo.com/..." --tags "标签1,标签2" --language zh --output-dir investment/洪灏/视频主题/

# 指定模型和语言
python .codex/skills/transcribe/transcribe_podcast.py --audio ~/Downloads/episode.mp3 --title "Title" --show "Show" --model base --language en --output-dir knowledge/research/
```

### 方式四：区分多人对话的说话人

使用 `transcribe_speakers.py` 在本机完成两阶段处理：

1. pyannote 生成说话人时间轴；
2. Qwen3-ASR 0.6B 按说话人轮次重新转录并输出时间戳。

两阶段必须使用隔离的 Python 环境：新版 `qwen3-asr-mlx` 与 pyannote 间接依赖的 `transformers` 对 `huggingface-hub` / `tokenizers` 的版本要求冲突。统一入口会用 `.venv-diarize/bin/python` 跑 pyannote、用 `.venv/bin/python` 跑 Qwen，不能把两套依赖强行装进同一个环境。

首次设置 diarization 环境：

```bash
uv venv --python 3.12 .venv-diarize
uv pip install --python .venv-diarize/bin/python \
  -r .codex/skills/transcribe/requirements-diarization.txt
```

```bash
uv run .codex/skills/transcribe/transcribe_speakers.py \
  --audio ~/Downloads/meeting.m4a \
  --title "会议标题" \
  --show "语音备忘录" \
  --output-dir operations/meetings/ \
  --speakers 2 \
  --context "讨论中的专有名词或主题"
```

常用参数：

- `--speakers 2`：已知人数时固定说话人数；未知时省略，交给模型估计。
- `--speaker-names "付老师,我"`：按首次主要发言的先后顺序命名；跨录音的 A/B 标签不保证自动保持一致。
- `--save-segments /tmp/speakers.json`：保留 pyannote 原始时间段，方便复核或复用。
- `--asr-model`、`--diarization-model`：显式指定本地模型目录。
- `--asr-python`、`--diarization-python`：覆盖两个隔离环境的解释器；也可设置 `ASR_PYTHON`、`DIARIZATION_PYTHON`。
- `--no-register-source`：只生成文件，不向 `sources/sources.jsonl` 追加记录。

输出默认使用“说话人 A / B / C”并保留时间戳。短促插话、同时说话和环境噪声可能造成边界误差；不得仅凭声纹标签猜测真实身份。若用户确认身份，再用 `--speaker-names` 重新生成或批量改名。

## 翻译规则

**英文内容必须翻译为中文**。转录完成后，如果原始内容为英文（通过 `--language en` 指定或从转录结果判断），执行以下步骤：

1. 保留原始英文转录文件不变（作为原文留存）
2. 在同一目录生成中文翻译版本，文件名在原文件名后追加 `_zh`（如 `transcript.md` → `transcript_zh.md`）
3. 翻译要求：
   - 保持专业术语准确（金融/宏观/技术领域）
   - 人名、公司名保留英文原文并括注中文（如 Jensen Huang（黄仁勋））
   - 保持段落结构一致
   - 语言自然流畅，不要翻译腔
4. 翻译版的 Markdown header 中 `**Language:**` 改为 `zh (translated from en)`
5. 索引文件中链接指向翻译版（`_zh` 文件），原文作为参考保留

对于中文内容或中英混合（以中文为主）的内容，无需翻译。

## 输出

`--output-dir` 是必填参数，指定转录产物保存的目录。转录产物应放到内容所属的分类目录（如 `investment/洪灏/`），而非统一的转录目录。

转录结果为 Markdown 文件，格式如下：

```markdown
# Episode Title

**Show:** Show Name
**Date:** 2026-04-15
**Source:** [url](url)
**Language:** zh
**Model:** whisper-base

## Transcript

转录文本内容...
```

同时会在 `sources/sources.jsonl` 中注册一条记录，用于追踪处理过的外部输入。

## 模型选择

默认引擎 Qwen3-ASR 0.6B 无需选择模型（优先从 `MODELS_DIR` 加载，其次使用已有的 Hugging Face 缓存）。模型不存在时自动使用 whisper.cpp。

当使用 `--engine whisper` 时，通过 `--model` 指定 whisper 模型：

| 模型 | 大小 | 速度 | 质量 | 建议场景 |
|------|------|------|------|----------|
| `tiny` | 74MB | 最快 | 一般 | 快速预览 |
| `base` | 141MB | 快 | 良好 | whisper 默认 |
| `small` | 244MB | 中等 | 很好 | 正式转录 |
| `large` | 1550MB | 慢 | 最佳 | 高质量需求 |

## 已验证的 RSS Feed

| Show | RSS Feed | 备注 |
|------|----------|------|
| Moving Markets (Julius Baer) | `https://feeds.transistor.fm/moving-markets` | 英文财经播客，单集约 10-15 分钟 |

## Prerequisites

```bash
# 系统工具
brew install whisper-cpp ffmpeg

# Python 依赖（uv 管理）
uv add feedparser requests mlx-audio qwen3-asr-mlx soundfile

# 模型：见 env/models.toml（位置、下载地址、是否 required 全在里面）
```

说话人分离依赖由 `requirements-diarization.txt` 管理，并需要提前接受、下载 `pyannote/speaker-diarization-community-1`。脚本只查找 `MODELS_DIR` 和 Hugging Face 本地缓存；找不到时直接报错，不在执行过程中联网下载。

## 技术备忘

- 引擎优先级：本地 Qwen3-ASR 0.6B > whisper-cli
- whisper-cpp 安装后的命令是 `whisper-cli`（不是 `whisper-cpp`）
- 模型位置：统一查 `env/models.toml`
- ffmpeg 会将音频预处理为 16kHz 单声道 WAV（whisper/qwen3 的输入要求）
- 可通过 `--engine whisper` 强制使用 whisper 引擎
- 说话人脚本以预加载 waveform 的方式调用 pyannote，避免依赖 torchcodec 的 ffmpeg 动态库兼容性
- Apple Silicon 上 pyannote 优先使用 MPS；Qwen3-ASR MLX 使用 Metal。本机沙箱阻止 GPU 时，需要经用户授权在沙箱外离线运行
