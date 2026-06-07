---
name: transcribe
description: "Audio/video transcription tool (Qwen3-ASR default, whisper.cpp fallback). Use when: user wants to transcribe a podcast episode, video, or any audio/video content to text. Trigger on phrases like 'transcribe podcast', 'podcast transcript', '转录播客', '播客转文字', 'transcribe this episode', 'whisper transcribe', '转录视频', 'transcribe video', or any request involving converting spoken content to text. Also trigger when the user provides a Spotify episode URL or mentions RSS feed transcription. Accepts both audio files (.mp3, .wav, .m4a) and video files (.mp4, .webm) — ffmpeg handles extraction automatically. Other skills (e.g. investment) may chain into this skill for transcription steps."
---

# Transcribe

将音频/视频转录为文字的独立工具。

输入 Spotify URL、RSS feed、本地音频或视频文件，输出 Markdown 格式的转录文本。

## 引擎优先级

**Qwen3-ASR > whisper.cpp**。脚本自动检测 Qwen3-ASR 模型是否存在（路径见 `env/models.toml`），存在则默认使用，否则 fallback 到 whisper.cpp。可通过 `--engine whisper` 强制使用 whisper。

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
python .claude/skills/transcribe/transcribe_podcast.py --rss "<RSS_URL>" --count 1 --model base --output-dir investment/洪灏/
```

### 方式二：通过 RSS Feed 转录

```bash
# 转录最新 1 集，输出到指定目录
python .claude/skills/transcribe/transcribe_podcast.py --rss "https://example.com/feed.xml" --count 1 --output-dir investment/洪灏/

# 转录最新 3 集，使用 small 模型（更高质量）
python .claude/skills/transcribe/transcribe_podcast.py --rss "https://example.com/feed.xml" --count 3 --model small --output-dir investment/洪灏/

# 指定语言
python .claude/skills/transcribe/transcribe_podcast.py --rss "https://example.com/feed.xml" --language zh --output-dir knowledge/research/
```

### 方式三：通过本地音频/视频文件转录

`--audio` 接受音频（.mp3, .wav, .m4a）和视频（.mp4, .webm）文件，ffmpeg 自动提取音频。

```bash
# 转录本地音频文件
python .claude/skills/transcribe/transcribe_podcast.py --audio ~/Downloads/episode.mp3 --title "Episode Title" --show "Show Name" --output-dir investment/卢麒元/

# 转录本地视频文件（自动提取音频）
python .claude/skills/transcribe/transcribe_podcast.py --audio ~/Downloads/video.mp4 --title "视频标题" --show "作者名" --url "https://weibo.com/..." --tags "标签1,标签2" --language zh --output-dir investment/洪灏/视频主题/

# 指定模型和语言
python .claude/skills/transcribe/transcribe_podcast.py --audio ~/Downloads/episode.mp3 --title "Title" --show "Show" --model base --language en --output-dir knowledge/research/
```

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

默认引擎 Qwen3-ASR 无需选择模型（使用 `$MODELS_DIR/Qwen3-ASR-1.7B-4bit`）。

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
uv add feedparser requests mlx-audio

# 模型：见 env/models.toml（位置、下载地址、是否 required 全在里面）
```

## 技术备忘

- 引擎优先级：Qwen3-ASR（`mlx_audio.stt.utils.load_model`）> whisper-cli
- whisper-cpp 安装后的命令是 `whisper-cli`（不是 `whisper-cpp`）
- 模型位置：统一查 `env/models.toml`
- ffmpeg 会将音频预处理为 16kHz 单声道 WAV（whisper/qwen3 的输入要求）
- 可通过 `--engine whisper` 强制使用 whisper 引擎
