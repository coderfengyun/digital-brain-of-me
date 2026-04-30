# Sources — 外部输入来源账本

所有需要处理的外部输入（论文、文章、研报、播客、讲座录音等）统一注册在 `sources/sources.jsonl`，遵循 **source (输入) → processing (处理) → output (领域归属)** 模型。

`sources/` 只负责记录来源和处理结果位置，不决定内容归属。最终产物应放在真实语境目录里，例如 `investment/洪灏/半导体超级周期/notes.md` 或 `knowledge/ai/autoharness/notes.md`。

## Structure

```
sources/
├── SOURCES.md          ← 本文件
├── sources.jsonl       ← 注册表（所有 paper + podcast）
├── paper-XXX.pdf       ← 文件类输入
├── paper-XXX.docx
└── pod-XXX.ogg
```

输出分布在对应领域目录：

```
investment/作者/文章主题/      ← 投资研报、宏观、地缘、资产配置
knowledge/ai/文章主题/         ← AI、agent、context engineering、AI 产品、developer tools、persona
knowledge/organizations/主题/   ← 组织管理、决策机制、协作方式
```

`paper` 和 `podcast` 都是处理类型，不是存储目录。处理完成后，`output` 指向最终领域目录中的 `.md` 文件。

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
  "output": "investment/洪灏/文章主题/notes.md | knowledge/ai/文章主题/notes.md"
}
```

### 字段语义

| 字段 | 含义 | 规则 |
|------|------|------|
| `id` | 唯一标识 | `paper-YYYYMMDD-XXX` 或 `pod-YYYYMMDD-XXX`，序号从 001 起 |
| `type` | 处理类型 | `paper`（长文本阅读）或 `podcast`（转录） |
| `source` | 输入来源 | URL 原样存；本地文件放 `sources/{id}.ext` |
| `title` | 标题 | 必填 |
| `tags` | 检索标签 | 可选，`[]` 表示无标签 |
| `added_at` | 添加日期 | `YYYY-MM-DD` |
| `output` | 处理结果路径 | 空 = 待处理，有值 = 已完成 |

### 不在 jsonl 中记录的内容

- 处理中间产物（下载的 HTML、转换的 WAV、音频文件等）
- 处理参数（模板、whisper 模型、语言、RSS feed URL 等）
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

**Step 3: 判断输出归属**

先判断材料未来最可能在哪个语境下被再次调用：

| 内容类型 | 输出位置 |
|---------|----------|
| 投资、宏观、地缘、能源、货币、资产配置、研报 | `investment/{作者或机构}/{文章主题}/notes.md` |
| AI、agent、context engineering、AI 产品、developer tools、persona | `knowledge/ai/{文章主题}/notes.md` |
| 组织管理、决策机制、协作方式 | `knowledge/organizations/{主题}/notes.md` |
| 课程、书籍、系统学习 | `knowledge/learning/` |
| 尚未成熟的探索性主题 | `knowledge/research/`（临时缓冲，后续迁出） |

投资类文章优先按作者/机构归档。无明确作者时使用机构名；确实无法识别时暂放 `investment/unknown/{文章主题}/`，后续补充来源信息。

**Step 4: 处理**

根据 type 路由到对应的处理流程：

- **paper** → 使用 `paper-reading` skill，按 Phase 0 → Phase 1 → Phase 2 → Phase 3 执行
- **podcast** → 使用 `podcast-transcribe` skill（运行 `.claude/skills/podcast-transcribe/transcribe_podcast.py --output-dir <目标目录>`）

**Step 5: 更新 output**

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
```

## Integration with Other Modules

| 模块 | 关系 |
|------|------|
| `paper-reading` skill | paper 类型的处理流程；输出到领域目录 |
| `investment/` | 投资、宏观、地缘、能源、研报的主要归属地 |
| `knowledge/ai/` | AI、agent、context engineering、AI 产品与工具的归属地 |
| `knowledge/organizations/` | 组织管理、决策机制、协作方式的归属地 |
| `knowledge/bookmarks/` | 纯链接收藏，不经过处理流程，独立管理 |
| `content/ideas/` | 阅读笔记和转录文本可以启发内容创意 |
| `podcast-transcribe` skill | 独立 skill，完成 podcast 的转录+注册+更新 output |

## 设计原则

1. **输入统一**：无论 URL 还是文件，都是 source，注册在同一个 jsonl
2. **处理类型不等于内容归属**：`paper` 表示长文本阅读流程，不表示输出到 `knowledge/papers/`
3. **输出统一**：所有类型的最终产物都是 .md 文件
4. **输出归属语境**：最终产物放到未来最可能被调用的领域目录
5. **Bookmark 不属于 sources**：没有处理流程的纯链接收藏，独立管理在 `knowledge/bookmarks/bookmarks.jsonl`
