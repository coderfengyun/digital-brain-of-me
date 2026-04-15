# How Noah Keeps Generative UI and LLM Conversations in Sync

**类型**: 方法

---

## 核心叙事 (Narrative)

### 一句话概括
> 在生成式 UI + LLM 的聊天应用中，将所有 UI 状态变化作为结构化消息写入对话历史，使对话成为 UI 和 LLM 的唯一事实来源（single source of truth）。

### 叙事结构

```
问题: 生成式 UI 应用中，UI 状态和 LLM 对话是两个割裂的系统——用户在 UI 上点击/选择，LLM 完全不知道
↓
观察: 现有方案各有缺陷——TUI 模式（AskUserQuestion）会锁定输入框，不适合 GUI；Prompt 注入模式（sentPrompt）能传状态但无法持久化，刷新页面后 UI 状态丢失
↓
假设: 如果把 UI 状态变化作为正式的用户消息写入对话历史，就能同时解决 LLM 感知和 UI 持久化两个问题
↓
方法: 将每个 UI 状态变化打包为 tagged union 结构 { "state": "clicked|selected...", "message": "..." }，作为完整用户消息发送给 LLM
↓
验证: 在 Noah 产品中实际落地，实现了 LLM 同步 + UI 重载后状态恢复
↓
结论: 对话历史成为 LLM 和 UI 的唯一事实来源；核心洞见是不要把 UI 和对话当作独立渠道
```

---

## 数据证据层 (Evidence)

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| 现有 UI+LLM 方案存在状态割裂 | 系统性归纳了两类现有方案的不足 | **例子**: (1) Claude Code 的 AskUserQuestion 工具在终端有效，但 GUI 中会锁定聊天框；(2) Pi/Claude 使用 `sentPrompt(text)` 可传状态，但页面刷新后无法重建之前的选择 | 正文 "Why Existing Patterns Fall Short" | ⭐⭐⭐ 强——两个具体产品对比，问题描述清晰 |
| 将 UI 状态变化作为结构化消息写入对话 | 用 tagged union 统一 UI 事件格式，写入对话历史 | **例子**: `{ "state": "clicked\|selected...", "message": "Review AI model" }`——每个 UI 操作都变成一条用户消息 | 正文 "What We Did in Noah" | ⭐⭐ 中——方案描述清晰但缺少技术细节（如何处理高频交互、消息膨胀等） |
| 对话历史成为唯一事实来源 | 一个数据源同时服务 LLM 上下文和 UI 状态恢复 | **例子**: (1) LLM 接收状态变化作为上下文，继续 agentic loop；(2) 重载会话时，UI harness 从对话历史中的 state 字段重建 UI 状态 | 正文 "This does two things at once" | ⭐⭐ 中——逻辑自洽但无定量数据（延迟、token 开销、用户体验指标） |

---

## 批判性思考 (Critical Thinking)

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | 假设: UI 交互频率足够低，可以逐一写入对话历史而不会导致 context 爆炸<br>失效场景: 高频交互（如拖拽、实时滑块调整）会产生大量消息，迅速耗尽 LLM context window |
| 关键局限 | - 没有讨论 token 成本：每个 UI 操作都变成一条消息，长会话的 token 开销可能很高<br>- 没有讨论消息合并/压缩策略：连续快速操作如何处理？<br>- 没有对比其他方案（如独立状态存储 + 摘要注入），只对比了 TUI 和 prompt injection<br>- 缺少用户体验数据（延迟、满意度等） |
| 实验充分性 | 缺失验证: 仅展示了设计思路和产品截图，没有 A/B 测试、用户研究或性能基准测试。作为一篇产品技术博文而非学术论文，这是可以理解的，但降低了方案的普适性论证力 |
