# /canvas：不止是更漂亮的输出，而是下一代人机协作

**作者**: Phodal（Qoder 团队）  
**来源**: https://mp.weixin.qq.com/s/gYBMDqJm1g6iArB8POjAog  
**日期**: 2026-05-21  
**类型**: 叙事（产品理念）

---

## 🗺️ 全局地图

### 一句话摘要
> Agent 输出不应止于文本或孤立 HTML，而应是基于 Design System 和 recipe.md 构建的结构化 Canvas——每个节点既是结果展示，也是携带完整上下文的下一步行动入口。

### 段落分类

| 章节/段落 | 分类 | 一句话说明 |
|-----------|------|-----------|
| 文本输出变成负担 → HTML 趋势 | [连接] | 背景铺垫：从纯文本到 HTML 的演进 |
| HTML 太自由，需要 Canvas | [核心] | 问题定义：HTML 孤立一次性，Canvas 是有约束的 Design System |
| 为什么 Agent 需要自己的 Design System | [核心] | Agent 理解组件靠机器可读上下文，不是隐性经验 |
| PieChart 注释示例 | [支撑] | 说明注释即 Design System 的具体例子 |
| Atomic Design 分层：Atoms → recipe.md | [核心] | Canvas 的架构设计：4 层分层 |
| Canvas 成为下一次行动的入口 | [核心] | 关键转折：Canvas 不是输出终点，是行动起点 |
| AI Fix / Generate Test 交互示例 | [支撑] | 说明"携带上下文的按钮"的具体行为 |
| 展望：Agentic UI | [连接] | 收尾：Canvas 是 Agentic UI 的早期形态 |

---

## 📖 叙事结构

```
问题: Agent 输出复杂任务时，文本/HTML 让用户负担变重
↓
观察: HTML 证明输出可以是可交互产物，但 HTML 太自由（孤立、一次性）
↓
洞察: Agent 没有人类的隐性设计经验，需要机器可读的 Design System
↓
方案: Canvas = 基于代码库 + Design Tokens + recipe.md 的结构化生成系统
  ├→ 架构层: Atoms → Components → Templates → Recipes
  └→ 交互层: Canvas 节点 = 结果 + 上下文 + 下一步行动入口
↓
愿景: Canvas 是 Agentic UI 的早期形态
     UI 要回答：Agent 在做什么、为什么、下一步带哪些上下文、哪些需要人确认
```

---

## 🔑 核心论点与证据

| 论点 | 创新点 | 支撑证据 | 说服力 |
|------|--------|----------|--------|
| Agent 需要专属 Design System | 区别于传统给人设计的 DS，Agent 版需要机器可读上下文 | **例子**: `PieChart` 注释写明"适合占比，不适合时间序列，应改用 LineChart"——Agent 从中学到使用边界，而不只是"组件存在" | 强：逻辑清晰，例子具体 |
| Canvas 的 4 层架构 | Atoms / Components / Templates / Recipes 分层 | **例子**: Code Review recipe 规定先讲变更 → 按风险排序问题 → 关键 finding 展示 diff evidence → 可修复问题旁有 AI Fix | 中：架构合理，但实现细节未展开 |
| Canvas 节点 = 行动入口 | 按钮携带完整上下文（finding + 文件 + Diff + DS 约束 + 验证要求）进入下一步 | **例子**: 点击 AI Fix 不是发一句"帮我修"，而是把当前 finding、关联文件、Diff 证据、DS 约束打包带回 Chat | 强：与普通 HTML 的对比鲜明 |

---

## 💡 关键洞察

- **注释即 Design System**：对 Agent 来说，组件声明里的使用边界、反例、适用场景，就是它理解"应该怎么用"的唯一来源——传统 DS 靠人的隐性经验，Agent DS 靠机器可读文本。

- **recipe.md 是任务级的设计规则**：比组件更高一层，它规定某类任务（Code Review、QA Report）里信息如何组织、证据放哪里、哪些操作要暴露——这是让 Agent 生成有一致性输出的关键。

- **上下文携带是 Canvas 与 HTML 的本质区别**：普通 HTML 整理结果，Canvas 把结果 + 上下文 + 下一步行动放在同一结构里，按钮才能成为真正的协作入口而不只是触发器。

---

## 🤔 批判性思考

**1. recipe.md 的维护成本是否被低估了？**  
文章给了 Code Review 的 recipe 例子，听起来很自然。但现实中，每类任务都要有专属 recipe，且 recipe 要足够精确才能约束 Agent 行为——这意味着大量的人工定义和持续维护。如果 recipe 质量参差不齐，Canvas 输出反而可能比自由的 HTML 更差（因为有约束但约束错了）。

**2. "上下文携带"的边界在哪里？**  
"AI Fix 点击时把所有上下文带回 Chat"听起来理想，但实际上下文越多，LLM 的关注点可能越分散。文章没有讨论上下文选择的策略——什么该带、什么该过滤、带多少合适。这是实现层面的核心难题。

**3. 这套分层对小团队是否过重？**  
Atoms → Components → Templates → Recipes 四层 + 维护 recipe.md + 确保组件注释机器可读——对 Qoder 自己可行，但推广到外部团队时，改造成本可能成为阻碍。文章定位是 Qoder 的产品特性，这个问题不一定需要文章回答，但值得关注。
