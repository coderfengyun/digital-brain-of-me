# Spec Coding：规约驱动的 AI 编程范式

**研究日期**: 2026-03-27
**研究动机**: 阅读阿里云《打造高可靠 AI 助手》一文时，Spec Coding 概念被多次提及但定义模糊，需深入理解

---

## 概念起源

**Sean Grove**（OpenAI 研究员），2025 年 6 月在 AI Engineer World's Fair 2025 发表主题演讲 **"The New Code"**。

核心口号：**"Prompt Engineering is Dead — Everything is A Spec!"**

核心论断：**"The person who communicates most effectively is the most valuable programmer."**（最能有效沟通的人，就是最有价值的程序员）

Sean Grove 的观察：开发者实际编写代码只占工作的 10-20%，另外 80% 是结构化沟通（理解用户、规划方案、测试结果）。AI 越来越擅长"写代码"，但在理解"你到底想要什么"上还很差。**Spec 就是弥补这个鸿沟的桥梁。**

他以 OpenAI 的 Model Spec 为例：这份用英语写的规约文档定义了模型的行为，具有版本控制、变更日志、协作编辑。修复模型的"过度谄媚"问题时，不是重新训练模型，而是**更新 Spec**，变更自动传播到整个系统。

> 演讲视频：https://www.youtube.com/watch?v=8rABwKRsec4

---

## Spec 到底是什么？

Spec（Specification，规约）是一份**结构化的、可机读的文档**，完整描述软件的意图（intent）、行为（behavior）、架构（architecture）和实现计划。

**关键定义：Spec 捕获的是 intent（意图），不是 instructions（指令）。代码只是 Spec 的一种可能的实现产物。**

Sean Grove 的类比：
- 高级语言 → 编译器 → 二进制产物
- Spec → AI → 代码

同一份 Spec 可以生成 Web 应用、移动应用、API、文档，甚至播客。

---

## Spec 的具体形态

### Kiro IDE（AWS）的实现 — 最成熟

每个 Spec 生成三个 Markdown 文件，存放在 `.kiro/specs/<feature-name>/` 目录下：

**`requirements.md`** — 使用 EARS（Easy Approach to Requirements Syntax）格式：

```
WHEN a user submits a form with invalid data
THE SYSTEM SHALL display validation errors next to the relevant fields

WHEN there are more than 10 reviews
THE SYSTEM SHALL paginate results with 10 reviews per page
```

**`design.md`** — 技术架构文档：
- 系统架构与组件设计
- 序列图和数据流（Mermaid 语法）
- 接口定义和数据模型
- 错误处理策略
- 单元测试策略

**`tasks.md`** — 离散的、可跟踪的实现任务列表，带实时状态更新。

### "黄叔"的 Claude Code 实践

Spec 形态是一份 `Prd.md`，包含：
- 核心目标 (Mission)：一句话产品愿景
- 用户画像 (Persona)：为谁设计？核心痛点？
- V1 MVP 功能列表 / V2+ 后续版本功能
- 关键业务逻辑 (Business Rules)
- 数据契约 (Data Contract)
- ASCII 原型图（3 个不同设计理念）
- 架构蓝图：Mermaid 序列图/流程图 + 组件交互 + 技术选型与风险

---

## Spec Coding 的工作流

### 通用三阶段（Kiro）

```
Phase 1: Requirements（需求定义）
  输入：自然语言描述（"添加一个产品评价系统"）
  输出：requirements.md（EARS 格式）
  人工：审查、修改、补充边界条件

Phase 2: Design（技术设计）
  输入：已确认的 requirements.md + 现有代码库
  输出：design.md（架构、序列图、API、测试策略）
  人工：审查架构合理性

Phase 3: Implementation（实现）
  输入：requirements.md + design.md
  输出：tasks.md → 逐个执行 → 生成代码
  人工：监控进度、验收
```

### Claude Code 上的实践（"黄叔"方案）

**产品 0→1**：
1. 输入 Spec Prompt（定义 AI 扮演首席产品设计师）
2. AI 主动提问追问，直到完成完整的 `Prd.md`
3. AI 根据 `Prd.md` + Context7 MCP 开始开发

**产品迭代**：
1. 切到 **Plan Mode**（Opus 模型），口喷需求，AI 给方案 + ASCII 原型
2. 反复对齐方案
3. 切到执行模式，AI 在 `Prd.md` 顶部新增版本记录，按更新严格执行
4. AI 自切 todolist，按序执行，完毕自检

关键：**Opus 做规划和 Spec 生成，Sonnet 按 Spec 执行。** 类似需求评审会 + 研发执行的分工。

---

## 与"先规划再写代码"的本质区别

| 维度 | 传统规划 | Spec Coding |
|------|---------|-------------|
| 文档地位 | 辅助物，代码是主产物 | **Spec 就是新的源代码**，代码是衍生物 |
| 生命周期 | 写完就过时 | **Living Document**，随迭代同步更新 |
| 可执行性 | 人读的参考 | **机读的指令**，AI 直接按 Spec 生成代码 |
| 可恢复性 | 代码丢了就完了 | Spec 在，可以重新生成代码 |
| 可移植性 | 绑定技术栈 | 同一份 Spec 可生成多种产物 |
| Prompt vs Spec | — | **Prompt 是短暂的（ephemeral），Spec 是持久的、版本化的** |

Sean Grove 指出的第一个问题："PROMPTS ARE EPHEMERAL"——对话结束 Prompt 就消失了，Spec 是持久的、可回溯的。

---

## 工具生态

| 工具 | 类型 | 特点 |
|------|------|------|
| **Kiro IDE** (AWS) | 独立 IDE | 最成熟的内置 Spec-Driven 实现，三阶段工作流，$19/月 |
| **GitHub Spec Kit** | 开源 CLI | 四阶段（specify → plan → task → implement），MIT 许可 |
| **OpenSpec** | 开源框架 | 轻量，适合已有项目（brownfield） |
| **BMAD Method** | 方法论 | 模拟企业团队角色（PM、架构师、开发者），适合大型项目 |
| **GSD** | 开源框架 | 轻量级，专为 Claude Code 设计 |
| **Claude Code** | AI 编程助手 | 无内置 Spec 流程，通过 Plan Mode + CLAUDE.md 手动实现 |
| **Cursor** | AI IDE | 通过 `.cursorrules` + 手动 Spec 文档实现，更偏 Vibe Coding |

历史渊源：**GeneXus** 公司自 1988 年以来就在做规约驱动开发（确定性生成器，非 AI），已 35 年。

---

## 个人评价

Spec Coding 本质上是**把软件工程的经典流程（需求分析→系统设计→编码），重新定义为"人负责 Spec，AI 负责代码"的分工契约**。

它不是新发明，但在 AI 时代有了新意义：
1. **Spec 成为人与 AI 之间唯一的"源代码"** — 代码变成了可随时重新生成的中间产物
2. **结构化沟通能力取代编码能力** — 成为核心竞争力
3. **版本化的 Spec 比短暂的 Prompt 更可靠** — 可复现、可审计、可协作

未解决的问题：
- Spec 本身的质量仍然依赖人的表达能力和领域知识
- "从 Spec 重新生成代码"在复杂系统中的保真度存疑
- Spec 的维护成本可能不低于维护代码本身

---

## 参考来源

1. Sean Grove, "The New Code" - AIEWF 2025 Keynote, https://www.youtube.com/watch?v=8rABwKRsec4
2. 知乎 "Spec Coding：AI开发的新范式" - 科技狂宣子, https://zhuanlan.zhihu.com/p/1958256212194853636
3. Kiro IDE 官方文档, https://kiro.dev/docs/specs/
4. GitHub Spec Kit, https://github.com/github/spec-kit
5. Microsoft Developer Blog, "Diving Into Spec-Driven Development With GitHub Spec Kit", https://developer.microsoft.com/blog/spec-driven-development-spec-kit
6. Implicator.ai, "The End of Code: Why Specifications Are Eating Software", https://www.implicator.ai/the-end-of-coding-how-specifications-are-becoming-the-new-source-code/
7. Lunabase.ai, "Specification-Driven Development Complete Guide", https://lunabase.ai/blog/specification-driven-development-complete-guide-sdd-vs-tdd-vs-bdd-luna-base-2025
