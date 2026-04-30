---
name: module-toolkit
description: "Digital Brain 系统模块创建与集成工具。Use when: user wants to create a new module, extend the digital brain system, check module integration, or asks about module creation conventions. Trigger on phrases like 'create module', 'add module', 'new module', 'extend system', '创建模块', '新增模块', '添加模块', '检查集成', 'check integration', 'module creation guide'. Also use when the user mentions adding a new data type or subsystem to the digital brain."
---

# Module Toolkit

Digital Brain 系统的模块创建与集成工具包。负责新建模块、验证集成完整性、维护模块创建规范。

## When to Activate

- 用户要创建新模块或扩展 digital-brain 系统
- 用户要检查某个模块的集成完整性
- 用户问如何创建模块、模块命名规范、集成要求等

## Skill Structure

```
.claude/skills/module-toolkit/
├── skill.md                              # This file
├── scripts/
│   ├── create_module.py                  # Automated module creator
│   └── check_module_integration.py       # Integration checker
└── references/
    └── MODULE_CREATION_GUIDE.md          # Complete 5-phase creation guide
```

## 核心工具

### 1. 自动创建模块

```bash
# knowledge/ 子目录下创建（默认）
python .claude/skills/module-toolkit/scripts/create_module.py <module_name> <keyword>

# 顶级目录创建
python .claude/skills/module-toolkit/scripts/create_module.py <module_name> <keyword> --top-level
```

自动完成:
- 创建 `<MODULE>.md` 模板文档
- 更新 3 个系统集成文件（CLAUDE.md, README.md, KNOWLEDGE.md）

### 2. 检查集成完整性

```bash
python .claude/skills/module-toolkit/scripts/check_module_integration.py <module_name> <keyword>
```

检查项:
- 3 个系统文档中是否有足够的关键词引用
- 模块主文档和数据文件是否存在
- 脚本文件是否存在

目标: 100% (所有文件通过)

## 创建流程

### 自动化创建（推荐）

1. 运行 `create_module.py`
2. 编辑生成的 `<MODULE>.md`，定义数据模型
3. 如需 JSONL，创建数据文件
4. 运行 `check_module_integration.py` 验证
5. 手动检查自动更新的内容是否合理，按需调整

### 手动创建（高级）

完整的 5 阶段流程见 `references/MODULE_CREATION_GUIDE.md`:
1. 需求分析 — 数据模型、工作流、标签体系
2. 核心文件 — `<MODULE>.md` + 可选 `.jsonl`
3. 系统集成 — 更新 4 个系统文件
4. 跨模块集成 — 定义数据流和关联
5. 质量保证 — 运行检查脚本

## 关键规范

### 命名规则
- 模块主文档: `<MODULE>.md`（全大写）
- 数据文件: `<module>.jsonl`（全小写）
- 模块名: 小写字母开头，可用小写字母、数字、连字符

### 目录选择
- `knowledge/` — 知识管理类模块（bookmarks, research, learning）
- 顶级目录 — 独立功能模块（operations, network, identity, content）

### 集成要求
每个模块必须在以下文件中有引用:
1. `CLAUDE.md` (≥3 次, 包含 Module Navigation 表)
2. `README.md` (≥3 次)
3. `knowledge/KNOWLEDGE.md` (≥2 次)

### 入口文件职责
- 只说明如何使用模块（数据格式、使用方法、目录结构）
- 不包含开发指南、系统架构等内容

## Quick Reference

| Task | Command |
|------|---------|
| Create module (auto) | `python .claude/skills/module-toolkit/scripts/create_module.py <name> <keyword>` |
| Create module (manual) | Read `references/MODULE_CREATION_GUIDE.md` |
| Check integration | `python .claude/skills/module-toolkit/scripts/check_module_integration.py <name> <keyword>` |

## 参考

- 完整创建指南: `references/MODULE_CREATION_GUIDE.md`
- 成功案例: `knowledge/papers/` 模块
