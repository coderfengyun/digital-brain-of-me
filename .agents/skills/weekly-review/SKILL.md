---
name: weekly-review
description: "创建、定位、续写和整理 Digital Brain 周记。提到‘周记’、‘weekly review’、‘本周复盘’、‘继续写周记’、‘录入周记’或要把近期想法整理进周记时触发。"
---

# Weekly Review

负责把周记内容写入本仓库既定位置，并遵守周记模块已有规则。

## 开始前

完整读取 [`weekly-review/WEEKLY-REVIEW.md`](../../../weekly-review/WEEKLY-REVIEW.md)。章节结构以 [`weekly-review/TEMPLATE.md`](../../../weekly-review/TEMPLATE.md) 为唯一来源，不在本 Skill 复制模板内容。

## 定位与创建

1. 周记只能放在 `weekly-review/`。
2. 用户给出日期范围时，按模块命名规则定位对应文件。
3. 用户只说“本周”“这周”或“weekly review”时：
   - 先列出 `weekly-review/` 中已有的日期文件；
   - 若已有文件的日期范围覆盖当前日期，继续写该文件；
   - 若没有，按当前自然周的周一至周日确定日期范围，从 `TEMPLATE.md` 创建新文件。
4. 创建前检查目标是否存在；存在时读取并续写，绝不以模板覆盖。
5. 实际文件名和文件链接中的 `~` 是普通字符，不要写成 `\~`。

## 写入原则

- 用户提供的原文、截图转写或口述内容，默认保持原意和原有措辞；不确定处先保留或询问，不推断补写。
- 用户要求整理时，可以调整归类与顺序，但不要把推断写成用户观点。
- 具体、可追踪的 TODO 遵守模块规则：先记录到 `operations/tasks/tasks.jsonl`，再在周记中引用 task-id。
- 若内容触发投资、OCR 等其他 Skill，按对应 Skill 完成其专属步骤，再回到周记写入。

## 完成检查

- 文件位于 `weekly-review/`，名称符合日期规则。
- 没有创建同一日期范围的重复文件。
- 未覆盖已有内容。
- 返回可点击的正确文件路径，路径中不转义 `~`。
