# Weekly Review — 周记&月结归档

个人周记和月结的归档模块。记录每周/每月在投资、学习、工作、生活方面的回顾与反思。

## Structure

```
weekly-review/
├── WEEKLY-REVIEW.md          # 本文件（模块入口）
├── TEMPLATE.md               # 周记内容模板
├── YYYY-MM-DD~MM-DD.md       # 各期周记/月结
└── assets/                   # 图片等附件
```

## 文件命名

- 格式：`YYYY-MM-DD~MM-DD.md`（起始日期带年份，结束日期只写月-日）
- 跨年：`2025-12-29~2026-01-23.md`（结束日期带年份）
- 子页面：`YYYY-MM-DD~MM-DD_标题.md`

## 内容模板

新建周记时直接复制 [`TEMPLATE.md`](./TEMPLATE.md)。周记的章节与初始格式以该模板为唯一来源；需要调整默认内容结构时，直接修改模板，不在本文件重复维护。

## 与其他模块的关联

- **operations/tasks/** — TODO 的唯一 source of truth；周记通过 task-id 引用，不独立维护 TODO 状态
- **investment/** — 投资章节的交易记录与投资日志互补
- **knowledge/learning/** — 学习章节的书籍/课程与 learning 模块关联

## 写作流程

1. 复制 [`TEMPLATE.md`](./TEMPLATE.md)，按文件命名规则创建本期周记。
2. 回顾 `operations/tasks/tasks.jsonl` 中本周完成的 task，并在周记中用 task-id 引用。
3. 如果回顾中出现具体、可追踪的 TODO，先创建 task，再在周记中引用 task-id。

## Usage

| 操作 | 方法 |
|------|------|
| 查看某期周记 | 按日期找到对应 .md 文件 |
| 新建周记 | 复制 `TEMPLATE.md` 为 `YYYY-MM-DD~MM-DD.md` |
| 搜索历史 | `grep -r "关键词" weekly-review/` |
