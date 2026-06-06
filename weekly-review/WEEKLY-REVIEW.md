# Weekly Review — 周记&月结归档

个人周记和月结的归档模块。记录每周/每月在投资、学习、工作、生活方面的回顾与反思。

## Structure

```
weekly-review/
├── WEEKLY-REVIEW.md          # 本文件（模块入口）
├── YYYY-MM-DD~MM-DD.md       # 各期周记/月结
└── assets/                   # 图片等附件
```

## 文件命名

- 格式：`YYYY-MM-DD~MM-DD.md`（起始日期带年份，结束日期只写月-日）
- 跨年：`2025-12-29~2026-01-23.md`（结束日期带年份）
- 子页面：`YYYY-MM-DD~MM-DD_标题.md`

## 内容结构

每篇周记通常包含以下章节（可灵活调整）：

### 本周完成
- 列出本周 done 的 task，用 task-id 引用（如 `- [x] task-20260314-001 整理《预测》读书笔记`）
- 来源：`operations/tasks/tasks.jsonl` 中本周状态变为 done 的条目

### 投资
- 本周交易记录（标的、方向、价格、数量）
- 各资产类别的下一步计划（黄金/白银、BTC/ETH、A股、港股、外汇）

### 修行&内观
- 工作：沟通方式、协作反思
- 交易：交易心理、策略复盘
- 生活：日常观察与感悟

### 学习
- 在读书籍/课程及进度（用 checkbox 标记完成状态）

### 接下来的调整
- 方向性意图和反思（不需要追踪完成状态的）
- 具体可追踪的 TODO **必须**同步创建 task，周记里用 task-id 引用：
  `- [ ] task-20260606-001 阅读知识星球文章`

## 与其他模块的关联

- **operations/tasks/** — TODO 的唯一 source of truth；周记通过 task-id 引用，不独立维护 TODO 状态
- **investment/** — 投资章节的交易记录与投资日志互补
- **knowledge/learning/** — 学习章节的书籍/课程与 learning 模块关联

## 写作流程

1. 回顾 `operations/tasks/tasks.jsonl` 中本周完成的 task，填入「本周完成」
2. 撰写投资/修行/学习等回顾章节
3. 写「接下来的调整」时，如果某条足够具体、可追踪 → 创建 task → 周记里引用 task-id

## Usage

| 操作 | 方法 |
|------|------|
| 查看某期周记 | 按日期找到对应 .md 文件 |
| 新建周记 | 创建 `YYYY-MM-DD~MM-DD.md`，参考上述内容结构 |
| 搜索历史 | `grep -r "关键词" weekly-review/` |
