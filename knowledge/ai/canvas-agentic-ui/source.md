# /canvas：不止是更漂亮的输出，而是下一代人机协作

**作者**: Phodal  
**来源**: https://mp.weixin.qq.com/s/gYBMDqJm1g6iArB8POjAog  
**发布时间**: 2026年5月21日

---

加入 Qoder 团队之后的第一个 feature，欢迎体验，有问题欢迎入群反馈。下载地址：https://qoder.com/desktop

在过去很长一段时间里，我们默认 Agent 的主要输出形态是聊天窗口里的文本：Markdown、代码块、命令结果、Diff 摘要、长长的分析。一旦任务开始变复杂时，文本会很快变成负担。你需要在一大段回复里找风险点、找文件、找下一步操作，还要把上下文重新复制回 Chat 里继续追问。

所以，最近一个很自然的趋势是：Agent 开始把复杂结果生成 HTML。它不再只是给你一段回答，而是把数据看板、PR Review、架构图、测试报告、调研结果组织成一个可以阅读、筛选、点击的页面。

HTML 证明了一件事：Agent 的输出不一定只能是文本，它也可以是一种可交互的产物。但 HTML 也太自由了，Agent 可以随手写颜色、布局和组件，每次生成都可能变成一个漂亮但孤立的一次性页面。

对 Qoder 来说，我们真正想做的让它基于代码库、组件体系、Design Tokens 和任务上下文生成 Canvas。Canvas 不只是输出格式，而是一套给 Coding Agent 使用的 Design System。

## 为什么 Agent 需要自己的 Design System？

传统 Design System 是给人设计的。

设计师看 Figma，前端看组件文档，团队通过 Storybook、组件 API、设计规范和 Review 流程保持一致性。人在使用组件时，会自然带入很多隐性判断：什么场景该用什么组件，哪些属性是主路径，哪些组合方式更常见，哪些视觉模式已经被团队接受。

但 Agent 没有这些默认经验。

它理解组件，主要依赖代码库里能读到的东西：类型声明、导出关系、注释、示例、调用频率、文件结构和最近修改痕迹。也就是说，影响 Agent 输出质量的，不只是组件库本身，而是组件库在当前代码库里的表达方式。

比如，一个组件如果只是暴露成类型声明，Agent 只能知道它"可以用"；但如果声明里写清楚使用场景、边界、反例和示例，Agent 才可能理解它"应该怎么用"。

```tsx
/**
 * Pie or donut chart for part-of-whole breakdowns.
 *
 * Use for small slice counts, such as request share by region or incident
 * impact by customer tier. Do not use for time series or precise ranking; use
 * `LineChart` or `BarChart` instead.
 *
 * @example
 * ```tsx
 * <PieChart
 *   donut
 *   data={[
 *     { label: "Free", value: 320 },
 *     { label: "Enterprise", value: 48, tone: "warning" },
 *   ]}
 * />
 * ```
 */
export declare function PieChart(props: PieChartProps): JSX.Element;
```

这段注释对 Agent 来说，就是设计系统的一部分。它不只说明 `PieChart` 存在，还说明它适合表达占比，不适合表达趋势或排序；遇到后两种场景时，应该转向 `LineChart` 或 `BarChart`。

所以，面向 Agent 的 Design System，不能只是把组件库暴露出去，而是要把团队的设计经验变成机器可读的上下文：组件适用边界、推荐组合、设计 token、布局模式，以及那些代码里真实发生过的产品判断。

这也是 Qoder Canvas 的起点。我们不只是给 Agent 一个可以渲染 React 的画布，而是希望它在生成界面时，能从 Qoder 当前代码库、SDK 类型、Design Tokens 和 recipe 中理解：在这个产品里，界面应该怎样被设计。

## 从原子设计到 recipe.md：让 Agent 知道怎么组合

如果把 Qoder Canvas 当成一套给 Agent 使用的 Design System，它也需要类似 Atomic Design 的分层。

最底层是 Atoms：Design Tokens、颜色、字体、间距、圆角、阴影、状态语义。它们不负责表达业务，只负责提供稳定的视觉原子。Agent 生成界面时，不能每次重新发明颜色和布局，而应该从 `useHostTheme().tokens` 这样的语义 token 里取值。

再往上是基础组件：Button、Tag、Card、Table、Input、PieChart、LineChart、FileReview、DiffGroup。这些组件就像 Molecules，它们已经带有更明确的表达能力：标签表达状态，图表表达数据关系，Diff 表达代码变化，FileReview 表达审查上下文。

但 Agent 真正面对的任务，通常不是"画一个组件"，而是"生成一次 Code Review"、"整理一份 QA Report"、"解释一次失败测试"、"生成一个架构说明"。这时就需要更高一层的 Template / Recipe。

recipe.md 就是这一层。它不只是告诉 Agent 有哪些组件，而是告诉它：在某类任务里，信息应该怎样组织，证据应该放在哪里，哪些操作应该暴露出来，哪些视觉形式应该避免。比如 Code Review recipe 应该要求 Agent 先讲变更，再按风险排序问题，关键 finding 要展示 diff evidence，可修复的问题旁边要有 AI Fix。

所以 Qoder Canvas 的结构大概是：

- Atoms 是 Design Tokens。
- Components 是 SDK primitives。
- Templates 是任务结构。
- Recipes 是可复用的生成规则。

最终生成出来的 Canvas，才是面向用户的协作界面。

## 让 Canvas 成为下一次行动的入口

如果 Canvas 只是把结果组织得更清楚，那它仍然停留在"输出"的位置。用户看完之后，下一步还是要回到 Chat：重新描述问题，重新贴文件名，重新说明这段 Diff 为什么重要，重新告诉 Agent 想修复还是想解释。

真正的交互变化，应该发生在这里。

Canvas 里的每一个结构化节点，都不应该只是展示结果。它应该能够成为下一次行动的入口。比如在 Code Review 里，一个问题不再只是一段风险描述。它应该同时带着优先级、关联文件、Diff 证据、影响范围、推荐修复方式，以及它来自哪个 recipe。用户看到这个问题时，不需要再把上下文复制回 Chat，只要在这个节点上继续：

点击 AI Fix，不是发送一句"帮我修一下"，而是把当前 finding、关联文件、Diff 证据、Design System 约束和验证要求一起带回 Chat。点击 Generate Test，也不是泛泛地说"补测试"，而是带着缺失覆盖的逻辑、风险路径和边界条件进入测试生成。

这就是 Canvas 和普通 HTML 的差别。

普通 HTML 更多是在整理结果。Canvas 则应该把结果、上下文和下一步行动放在同一个结构里。没有这些上下文，按钮只是按钮；有了 Design System 和 recipe.md，按钮才变成可执行的协作入口。

所以，Canvas 不是 Chat 的替代品。它的位置，是把 Chat、代码、Diff、测试和工作流组织成一个可以继续行动的工作台。前面的 Atoms（最小元素）、Components、Templates 和 Recipes，让 Agent 知道如何生成界面；这一层交互，则让用户能够沿着界面继续推进任务。

## 展望与总结：从 Canvas 到 Agentic UI

Canvas 只是 Agentic UI 的早期形态。

过去的界面默认由人操作系统；到了 Agent 时代，界面里多了一个会读上下文、提建议、调用工具、修改文件的新行动者。

所以 UI 要回答的问题也变了：Agent 正在做什么，为什么这样做，下一步会带入哪些上下文，哪些动作需要人确认，出错后能不能暂停、修改和回退。

所以，Qoder Canvas 想做的不是"让 AI 多生成几个页面"。更像是让页面本身能接住 Agent。Chat 还在，代码、Diff、测试也都还在。Canvas 只是把它们放到一个可以继续行动的界面里。

再往后看，这大概就是 Agentic UI 会慢慢长出来的地方。
