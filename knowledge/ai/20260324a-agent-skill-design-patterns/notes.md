# 5 Agent Skill Design Patterns Every ADK Developer Should Know

**类型**: 方法

---

## 📖 核心叙事 (Narrative)

### 一句话概括
> SKILL.md 的格式已被 30+ 工具标准化，真正的挑战是内容设计——本文从生态实践中提炼出 5 种 Skill 设计模式，帮助开发者构建可靠的 Agent。

### 叙事结构

```
问题: SKILL.md 格式已标准化，但开发者不知道如何设计 Skill 内部的逻辑内容
↓
观察: 不同用途的 Skill（如封装框架约定 vs. 多步文档流程）内部逻辑截然不同，但外部格式完全相同
↓
假设: 存在可复用的设计模式，能指导 Skill 内容的结构化设计
↓
方法: 研究 Anthropic、Vercel、Google 等生态中的 Skill 构建实践，提炼出 5 种模式
↓
验证: 每种模式提供完整的 ADK 代码示例 + 决策树帮助选择
↓
结论: 将复杂指令拆解为结构化模式，而非塞入单一 system prompt
```

---

## 📊 数据证据层 (Evidence)

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| 格式已不再是问题 | 将焦点从格式转向内容设计 | **例子**: 30+ agent 工具（Claude Code, Gemini CLI, Cursor）已采用相同的 SKILL.md 布局 | 文章开头 | ⭐⭐ 中（数字未验证，但趋势明确） |
| Tool Wrapper: 按需加载库知识 | 将框架约定打包为可触发的 Skill，而非硬编码到 system prompt | **例子**: FastAPI 技能仅在检测到相关关键词时加载 conventions.md | Pattern 1 代码示例 | ⭐⭐⭐ 强（模式清晰，代码可运行） |
| Generator: 模板驱动一致输出 | 用 assets/ + references/ 分离模板与风格指南，Skill 充当"项目经理"协调填充 | **例子**: 技术报告生成器按 5 步流程加载模板、收集变量、填充文档 | Pattern 2 代码示例 | ⭐⭐⭐ 强（解决了 LLM 输出不一致的痛点） |
| Reviewer: 分离"查什么"与"怎么查" | 外部化评审标准为 checklist 文件，同一 Skill 基础设施可服务不同审计场景 | **例子**: 将 Python 风格 checklist 替换为 OWASP 安全 checklist 即可变成安全审计 | Pattern 3 代码示例 | ⭐⭐⭐ 强（模块化程度高，复用性好） |
| Inversion: Agent 先采访再行动 | 用"不可协商的闸门指令"强制 Agent 收集完整上下文后才开始生成 | **例子**: 项目规划器在 6 个问题全部回答后才进入 Synthesis 阶段 | Pattern 4 代码示例 | ⭐⭐⭐ 强（直击 Agent 盲目生成的顽疾） |
| Pipeline: 硬性检查点防止跳步 | 菱形门控条件（diamond gate）确保 Agent 不能绕过验证步骤 | **例子**: 文档管道要求用户确认 docstring 后才进入组装阶段 | Pattern 5 代码示例 | ⭐⭐⭐ 强（解决复杂任务中 Agent 跳步的问题） |
| 模式可组合 | Pipeline 可包含 Reviewer 步骤；Generator 可以 Inversion 开头 | **例子**: 描述了组合场景，但无具体代码 | 文章结尾 | ⭐⭐ 中（缺少组合示例代码） |

---

## 🤔 批判性思考 (Critical Thinking)

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | 假设: SKILL.md 是 Agent 技能的标准载体，且 30+ 工具已统一格式<br>失效场景: 如果各工具的 Skill 运行时行为差异大（如对 references/ 目录的处理不同），则同一 Skill 在不同工具间不可移植，模式的普适性会打折 |
| 关键局限 | - 所有示例都是单一 Skill 场景，缺少多 Skill 协作/冲突的讨论<br>- 未讨论模式选择的灰色地带（例如一个 Skill 同时需要 Inversion + Reviewer 时的优先级）<br>- 没有性能数据：不同模式对 context window 的消耗对比<br>- "30+ 工具"的说法缺少具体来源引证 |
| 实验充分性 | 缺失验证: 没有 A/B 对比数据证明使用这些模式后 Agent 质量提升；代码示例是 skeleton 级别，未展示实际运行效果或评测 |

---

## 💡 与我的 digital-brain 系统的关联

回看自己的 `digital-brain` skill，可以识别出多种模式的组合运用：
- **Tool Wrapper**: 各模块入口文档充当按需加载的领域知识（如 AI.md、INVESTMENT.md）
- **Generator**: Paper 阅读使用模板驱动（TEMPLATE-METHOD.md 等）
- **Pipeline**: Paper 阅读流程的 Phase 0 → Phase 1 → Phase 2 就是带检查点的管道
- **Inversion**: 尚未显式使用，但可以考虑在内容创作前加入结构化采访步骤

这验证了文章的核心观点：好的 Skill 设计是模式的有意识组合，而非随意堆砌指令。
