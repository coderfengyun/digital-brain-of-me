---
name: paper-reading
description: "Systematic paper/article reading with narrative-driven approach. Use when: user wants to read a paper, article, blog post, Twitter thread, or any text-based external input. Trigger on phrases like 'read paper', 'read this', '读一下这篇', '这篇文章', 'add paper', 'paper reading', 'show unread papers', '读论文', '添加论文', 'add source' (for text content). Handles the full pipeline: obtain source → extract narrative → critical analysis → save notes."
---

# Paper Reading

系统化的论文/文章阅读流程，以叙事驱动——先理解作者要讲的**故事**，再用**数据**验证。

## Data Location

- 元数据注册：`sources/sources.jsonl`（type: `"paper"`）
- 阅读笔记：`knowledge/papers/paper-YYYYMMDD-XXX/notes.md`
- 源文件：`knowledge/papers/paper-YYYYMMDD-XXX/source.*`
- 模板文件：`.claude/skills/paper-reading/TEMPLATE-*.md`

## Paper Note Templates

根据论文类型选择对应模板：

| 类型 | 模板 | 适用场景 | 判断标准 |
|------|------|----------|----------|
| 方法 | [TEMPLATE-METHOD.md](./TEMPLATE-METHOD.md) | 提出新方法、实验验证 | 有实验、有 baseline 对比、有定量结果 |
| 叙事 | [TEMPLATE-NARRATIVE.md](./TEMPLATE-NARRATIVE.md) | 案例研究、故事性文章 | 以时间线或事件为主线，重在讲述过程 |
| 综述 | [TEMPLATE-SURVEY.md](./TEMPLATE-SURVEY.md) | 领域综述、文献回顾 | 梳理多篇工作，分类总结，指出趋势 |
| 理论 | [TEMPLATE-THEORY.md](./TEMPLATE-THEORY.md) | 数学证明、理论分析 | 核心是定理/命题及其证明 |

**默认选择**: 不确定时使用「方法」模板

## Reading Workflow

**Critical Rules**:
- ALWAYS obtain source document locally before reading
- ALWAYS read from local source, NOT from web fetch
- ALWAYS choose the appropriate template based on paper type
- ALWAYS update `sources.jsonl` after each phase

### Phase 0: Obtain Source Document

**Adding a new paper**:
1. Generate ID: `paper-YYYYMMDD-XXX`（检查当日已有序号，递增）
2. If source is a file: copy to `sources/{id}.ext`
3. Append to `sources/sources.jsonl`:
   ```json
   {"id": "paper-20260413-001", "type": "paper", "source": "https://example.com/article", "title": "文章标题", "tags": [], "added_at": "2026-04-13", "output": ""}
   ```

**Obtaining the source**:
1. For arxiv papers: Download HTML to `knowledge/papers/paper-YYYYMMDD-XXX/paper.html`
2. For web articles: Use Chrome MCP (navigate_page + take_snapshot) to save to `knowledge/papers/paper-YYYYMMDD-XXX/source.md`
3. For provided documents: Save to `knowledge/papers/paper-YYYYMMDD-XXX/source.pdf` or `source.md`

Source document is saved by convention — no need to update sources.jsonl at this phase.

### Phase 1: 全局扫描

**Goal**: 通读全文，产出段落分类和结构地图，为后续变速阅读做准备

**Process**:
1. 通读全文
2. 写一句话摘要——这篇文章在说什么
3. 对全文段落/章节做三类标记：
   - `[核心]` — 承载核心论点、关键创新、主要结论的段落
   - `[支撑]` — 展开论证的证据、例子、数据、实验细节
   - `[连接]` — 过渡、背景铺垫、相关工作综述
4. 画出结构地图（论证单元之间的关系），支持分支和对比，不限于线性流

段落分类写入笔记的"全局地图"区块，作为后续阅读的导航。

### Phase 2: 叙事提取 + 证据验证

**Goal**: 按段落分类的详略差异，提取叙事结构并验证关键论点

**变速阅读规则**：
- `[核心]` 段 → **精读**：完整提取论点、创新点，写入叙事结构和证据表
- `[支撑]` 段 → **扫读**：摘要式记录，标注"支撑了哪个核心论点"
- `[连接]` 段 → **跳读**：一句话带过（"从 A 过渡到 B"）

**叙事结构**：用垂直流或结构图呈现论证逻辑（可以有分支）：
```
问题: ...
↓
观察: ...
↓
假设: ...
├→ 方法A: ...
│   ↓ 验证: ...
└→ 方法B: ...
    ↓ 验证: ...
↓
结论: ...
```

**证据表**（仅针对 `[核心]` 段的论点）：

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|

- **支撑数据填写规则**: 优先使用定量数据；若论点无明确数据支撑，使用 `**例子**: 具体场景描述` 格式记录论文中的示例
- **具体例子引用规则**: 当论文通过具体真实例子来阐释一个概念或方法时（如 checklist 问题、prompt 片段、代码示例、配置项），在支撑数据中直接引用 2-3 个原文例子，帮助读者快速找到作者提出概念的「感觉」

### Phase 3: 批判性思考

**Goal**: 对核心论点做批判分析

**Process**:
1. Complete critical thinking section with 3 core questions
2. Update `output` field in sources.jsonl with notes.md path

## Querying

```bash
# 查看所有未读论文
python3 -c "
import json
with open('sources/sources.jsonl') as f:
    for line in f:
        e = json.loads(line.strip())
        if e['type'] == 'paper' and not e.get('output'):
            print(f'{e[\"id\"]}  {e[\"title\"][:50]}')
"
```

## Reference

- [EXAMPLE.md](./EXAMPLE.md) — Example: Attention Is All You Need
