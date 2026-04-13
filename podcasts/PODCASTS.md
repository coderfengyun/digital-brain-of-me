# Podcasts - 播客转录与笔记

将播客音频转录为文字，建立可检索的播客知识库。

## Structure

```
podcasts/
├── transcripts/                # 转录文本存放目录
│   └── show-name_episode-title_ID.md
├── PODCASTS.md                 # 本文件
└── TEMPLATE.md                 # 转录笔记模板
```

## Data Schema

Podcast metadata lives in `sources/sources.jsonl` (type: `"podcast"`).

```json
{
  "id": "pod-YYYYMMDD-XXX",
  "type": "podcast",
  "source": "https://open.spotify.com/episode/... | sources/pod-XXX.ogg",
  "title": "Episode title",
  "tags": ["topic1", "topic2"],
  "added_at": "YYYY-MM-DD",
  "output": "podcasts/transcripts/show-name_episode-title_pod-YYYYMMDD-XXX.md"
}
```

### Fields
- `source` - URL 或本地文件路径（文件输入放 `sources/{id}.ext`）
- `output` - 转录 Markdown 文件路径（相对于项目根目录）

### Status
- `output` empty = 未转录
- `output` filled = 转录完成

### Processing Artifacts (not tracked in sources.jsonl)
- 音频文件: `podcasts/audio/` 目录下
- show name, language, rss_feed 等处理参数写入转录 .md header，不在 jsonl 中记录

<a id="transcription-workflow"></a>
## Transcription Workflow

### 从 Spotify 链接转录（完整流程）

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
python scripts/transcribe_podcast.py --rss "<RSS_URL>" --count 1 --model base
```

### 方式一：通过 RSS Feed 转录

```bash
# 转录最新 1 集
python scripts/transcribe_podcast.py --rss "https://example.com/feed.xml" --count 1

# 转录最新 3 集，使用 small 模型（更高质量）
python scripts/transcribe_podcast.py --rss "https://example.com/feed.xml" --count 3 --model small

# 指定语言
python scripts/transcribe_podcast.py --rss "https://example.com/feed.xml" --language zh
```

### 方式二：通过本地音频文件转录

```bash
# 转录本地音频文件
python scripts/transcribe_podcast.py --audio ~/Downloads/episode.mp3 --title "Episode Title" --show "Show Name"

# 指定模型和语言
python scripts/transcribe_podcast.py --audio ~/Downloads/episode.mp3 --title "Title" --show "Show" --model base --language en
```

### Whisper 模型选择

| 模型 | 大小 | 速度 | 质量 | 建议场景 |
|------|------|------|------|----------|
| `tiny` | 74MB | 最快 | 一般 | 快速预览 |
| `base` | 141MB | 快 | 良好 | 日常使用（默认） |
| `small` | 244MB | 中等 | 很好 | 正式转录 |
| `large` | 1550MB | 慢 | 最佳 | 高质量需求 |

## Usage

### 添加播客

```bash
python scripts/transcribe_podcast.py --rss "RSS_URL" --count 1
```

### 搜索转录内容

```bash
# 在转录文本中搜索关键词
grep -r "keyword" podcasts/transcripts/
```

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

# 下载其他模型（按需）
curl -L -o ~/.cache/whisper-cpp/ggml-tiny.bin \
  "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin"
curl -L -o ~/.cache/whisper-cpp/ggml-small.bin \
  "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin"

# Python 依赖（注意安装到 python3 对应的版本）
python3 -m pip install feedparser requests
```

## 技术备忘

- whisper-cpp 安装后的命令是 `whisper-cli`（不是 `whisper-cpp`）
- 模型文件存放在 `~/.cache/whisper-cpp/ggml-<model>.bin`
- ffmpeg 会将音频预处理为 16kHz 单声道 WAV（whisper.cpp 的输入要求）
- 用户机器上有多个 Python 版本，安装依赖用 `python3 -m pip install` 确保一致
