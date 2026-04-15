---
name: podcast-transcribe
description: "Podcast audio transcription tool using whisper.cpp. Use when: user wants to transcribe a podcast episode, convert audio to text, get a transcript from Spotify/RSS/local audio file. Trigger on phrases like 'transcribe podcast', 'podcast transcript', '转录播客', '播客转文字', 'transcribe this episode', 'whisper transcribe', or any request involving converting spoken audio content to text. Also trigger when the user provides a Spotify episode URL or mentions RSS feed transcription."
---

# Podcast Transcribe

将播客/音频转录为文字的独立工具。

输入 Spotify URL、RSS feed 或本地音频文件，输出 Markdown 格式的转录文本。

## 核心流程

```
Spotify URL → 查 RSS feed → 下载音频 → whisper.cpp 转录 → Markdown
RSS URL → 下载音频 → whisper.cpp 转录 → Markdown
本地音频 → whisper.cpp 转录 → Markdown
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
python .claude/skills/podcast-transcribe/transcribe_podcast.py --rss "<RSS_URL>" --count 1 --model base --output-dir investment/洪灏/
```

### 方式二：通过 RSS Feed 转录

```bash
# 转录最新 1 集，输出到指定目录
python .claude/skills/podcast-transcribe/transcribe_podcast.py --rss "https://example.com/feed.xml" --count 1 --output-dir investment/洪灏/

# 转录最新 3 集，使用 small 模型（更高质量）
python .claude/skills/podcast-transcribe/transcribe_podcast.py --rss "https://example.com/feed.xml" --count 3 --model small --output-dir investment/洪灏/

# 指定语言
python .claude/skills/podcast-transcribe/transcribe_podcast.py --rss "https://example.com/feed.xml" --language zh --output-dir knowledge/research/
```

### 方式三：通过本地音频文件转录

```bash
# 转录本地音频文件
python .claude/skills/podcast-transcribe/transcribe_podcast.py --audio ~/Downloads/episode.mp3 --title "Episode Title" --show "Show Name" --output-dir investment/卢麒元/

# 指定模型和语言
python .claude/skills/podcast-transcribe/transcribe_podcast.py --audio ~/Downloads/episode.mp3 --title "Title" --show "Show" --model base --language en --output-dir knowledge/research/
```

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

## Whisper 模型选择

| 模型 | 大小 | 速度 | 质量 | 建议场景 |
|------|------|------|------|----------|
| `tiny` | 74MB | 最快 | 一般 | 快速预览 |
| `base` | 141MB | 快 | 良好 | 日常使用（默认） |
| `small` | 244MB | 中等 | 很好 | 正式转录 |
| `large` | 1550MB | 慢 | 最佳 | 高质量需求 |

## 已验证的 RSS Feed

| Show | RSS Feed | 备注 |
|------|----------|------|
| Moving Markets (Julius Baer) | `https://feeds.transistor.fm/moving-markets` | 英文财经播客，单集约 10-15 分钟 |

## Prerequisites

```bash
# macOS
brew install whisper-cpp ffmpeg

# 下载 Whisper 模型（目前已安装 base 模型）
mkdir -p ~/.cache/whisper-cpp
curl -L -o ~/.cache/whisper-cpp/ggml-base.bin \
  "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin"

# Python 依赖
python3 -m pip install feedparser requests
```

## 技术备忘

- whisper-cpp 安装后的命令是 `whisper-cli`（不是 `whisper-cpp`）
- 模型文件存放在 `~/.cache/whisper-cpp/ggml-<model>.bin`
- ffmpeg 会将音频预处理为 16kHz 单声道 WAV（whisper.cpp 的输入要求）
- 用户机器上有多个 Python 版本，安装依赖用 `python3 -m pip install` 确保一致
