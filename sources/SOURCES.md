# Sources — 外部输入统一管理

所有需要处理的外部输入（论文、文章、播客、讲座录音等）统一注册在 `sources/sources.jsonl`，遵循 **source (输入) → processing (处理) → output (输出)** 模型。

## Structure

```
sources/
├── SOURCES.md          ← 本文件
├── sources.jsonl       ← 注册表（所有 paper + podcast）
├── paper-XXX.pdf       ← 文件类输入
├── paper-XXX.docx
└── pod-XXX.ogg
```

处理产物和输出分布在对应模块目录：

```
papers/                 ← paper 的处理产物 + 输出
└── paper-XXX/
    ├── source.*        ← 处理产物（下载的 HTML/转换的文本）
    └── notes.md        ← 输出
podcasts/               ← podcast 的处理产物 + 输出
├── audio/              ← 处理产物（下载的音频）
└── transcripts/        ← 输出
    └── xxx.md
```

## Data Schema

所有类型共享同一 schema，没有类型特有字段。

```json
{
  "id": "paper-YYYYMMDD-XXX | pod-YYYYMMDD-XXX",
  "type": "paper | podcast",
  "source": "https://... | sources/{id}.ext",
  "title": "标题",
  "tags": [],
  "added_at": "YYYY-MM-DD",
  "output": "papers/{id}/notes.md | podcasts/transcripts/xxx.md"
}
```

### 字段语义

| 字段 | 含义 | 规则 |
|------|------|------|
| `id` | 唯一标识 | `paper-YYYYMMDD-XXX` 或 `pod-YYYYMMDD-XXX`，序号从 001 起 |
| `type` | 处理类型 | `paper`（阅读）或 `podcast`（转录） |
| `source` | 输入来源 | URL 原样存；本地文件放 `sources/{id}.ext` |
| `title` | 标题 | 必填 |
| `tags` | 检索标签 | 可选，`[]` 表示无标签 |
| `added_at` | 添加日期 | `YYYY-MM-DD` |
| `output` | 处理结果路径 | 空 = 待处理，有值 = 已完成 |

### 不在 jsonl 中记录的内容

- 处理中间产物（下载的 HTML、转换的 WAV、音频文件等）
- 处理参数（whisper 模型、语言、RSS feed URL 等）
- 状态字段（由 `output` 是否为空推导）

这些信息要么是临时的（处理完即无用），要么写在 output 的 .md header 中。

## Usage

### 添加新来源

**Step 1: 判断类型**

| 输入 | type | 判断依据 |
|------|------|----------|
| 文章/论文 URL | `paper` | arxiv、博客、Twitter thread、微信公众号等文字内容 |
| PDF/DOCX 文件 | `paper` | 文档类文件 |
| Spotify/播客 URL | `podcast` | 音频平台链接 |
| 音频文件（mp3/ogg/wav） | `podcast` | 音频类文件 |

**Step 2: 注册**

1. 生成 ID：`paper-YYYYMMDD-XXX` 或 `pod-YYYYMMDD-XXX`（检查当日已有序号，递增）
2. 如果 source 是文件：复制到 `sources/{id}.ext`
3. 追加一行到 `sources/sources.jsonl`：

```json
{"id": "paper-20260413-001", "type": "paper", "source": "https://example.com/article", "title": "文章标题", "tags": [], "added_at": "2026-04-13", "output": ""}
```

**Step 3: 处理**

根据 type 路由到对应的处理流程：

- **paper** → 读 `papers/PAPERS.md`，按 Phase 0 → Phase 1 → Phase 2 执行
- **podcast** → 运行 `scripts/transcribe_podcast.py` 或按 `podcasts/PODCASTS.md` 手动处理

**Step 4: 更新 output**

处理完成后，将 output 路径写回 `sources.jsonl` 中对应条目。

### 查询

```bash
# 查看所有未处理的来源
python3 -c "
import json
with open('sources/sources.jsonl') as f:
    for line in f:
        e = json.loads(line.strip())
        if not e.get('output'):
            print(f'{e[\"id\"]}  {e[\"title\"][:50]}')
"

# 按类型筛选
python3 -c "
import json
with open('sources/sources.jsonl') as f:
    for line in f:
        e = json.loads(line.strip())
        if e['type'] == 'paper':
            status = 'done' if e.get('output') else 'pending'
            print(f'[{status}] {e[\"id\"]}  {e[\"title\"][:50]}')
"

# 搜索内容（在 output 文件中 grep）
grep -r "关键词" papers/*/notes.md podcasts/transcripts/
```

## Integration with Other Modules

| 模块 | 关系 |
|------|------|
| `papers/` | paper 类型的处理流程和输出目录，详见 `papers/PAPERS.md` |
| `podcasts/` | podcast 类型的处理流程和输出目录，详见 `podcasts/PODCASTS.md` |
| `knowledge/bookmarks/` | 纯链接收藏，不经过处理流程，独立管理 |
| `content/ideas/` | 阅读笔记和转录文本可以启发内容创意 |
| `scripts/` | `transcribe_podcast.py` 自动完成 podcast 的注册+转录+更新 output |

## 设计原则

1. **输入统一**：无论 URL 还是文件，都是 source，注册在同一个 jsonl
2. **处理临时**：中间产物不进 jsonl，处理参数写进 output 的 .md header
3. **输出统一**：所有类型的最终产物都是 .md 文件
4. **按约定组织**：文件位置可从 ID 推导，减少需要显式记录的路径
5. **Bookmark 不属于 sources**：没有处理流程的纯链接收藏，独立管理在 `knowledge/bookmarks/bookmarks.jsonl`
