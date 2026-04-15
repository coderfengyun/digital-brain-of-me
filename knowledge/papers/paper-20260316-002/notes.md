# Ralph Wiggum as a "Software Engineer"

**类型**: 方法

---

## 叙事线

```
问题: 如何让 AI 自主完成 greenfield 项目的软件开发？
↓
观察: 多 Agent 通信 = 非确定性的微服务 = 灾难；单 Agent 循环更可控
↓
假设: 一个 Bash 无限循环 + 单任务 + specs 锚定 + 背压验证 = 可用的自动化开发
↓
方法: Ralph 技术 — while :; do cat PROMPT.md | claude-code ; done
↓
验证: 用 Ralph 构建 CURSED（一门全新编程语言的编译器），$297 AI 成本交付 $50k 合同
↓
结论: greenfield 项目可达 ~90% 完成度，仍需资深工程师把关
```

## 证据表

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|-----------|
| 单 Agent 优于多 Agent | 类比微服务 vs 单体：非确定性系统不应再叠加分布式复杂度 | **例子**: 在 SFO 观察到大家尝试多 Agent 通信都搞成 red hot mess | 作者个人经历 | 中等——类比有说服力但缺少对照实验 |
| 一个循环只做一件事 | 保护 ~170k context window 不被消耗殆尽 | **例子**: 放宽到多任务后项目会 off the rails | 作者开发 CURSED 经验 | 中等——经验性结论，缺乏定量对比 |
| Specs 作为稳定上下文锚 | 区分 specs（稳定）和 prompt（可变），每次循环重新加载 specs | **例子**: lexer spec 中一个关键字定义了两次导致一个月浪费 | CURSED 开发过程 | 高——spec 错误导致的具体失败案例很有说服力 |
| Subagent 做搜索/写入，主 context 做调度 | 主 context window 当调度器，不做分配密集工作 | **例子**: 84 个并行 subagent 搜索文件系统；只允许 1 个 subagent 做 build/test 避免背压 | CURSED 构建视频 | 高——有具体的并行策略和背压控制 |
| 背压（类型系统+测试+静态分析）是质量关键 | 生成容易，验证难；轮子转得快才是关键 | **例子**: Rust 类型系统提供极端正确性但编译慢，需要权衡 | CURSED 用 Rust 的体验 | 高——揭示了生成速度 vs 验证正确性的 trade-off |
| ROI 极高 | $50k 合同用 $297 AI 成本交付 MVP | 单个案例数据 | 作者教会的一个工程师的合同 | 低——单案例，无法泛化 |

## 批判性思考

**1. 这个方法的适用边界在哪？**

作者自己明确说了："There's no way in heck would I use Ralph in an existing code base"。Ralph 本质上是一个 greenfield bootstrapping 技术，对存量代码库无效。但作者没有深入讨论为什么——可能是因为存量代码的隐式约束太多，specs 无法完整覆盖。

**2. "eventual consistency"的代价是什么？**

作者用了大量篇幅描述 Ralph 会犯错、会破坏代码库、需要 git reset --hard。这意味着 Ralph 的效率高度依赖操作者的判断力——什么时候该 reset、什么时候该调 prompt、什么时候该重新生成 TODO list。这些判断需要资深工程师，而文章把这部分轻描淡写了。

**3. Ralph 与你的课程生产 Agent 的异同？**

相同：都是单 Agent 循环、specs 驱动、背压验证。不同：Ralph 面向代码生成，你的 Agent 面向课程资料生成；Ralph 完全自动化运行（人只调 prompt），你的流程保留了人在 loop 中做验收。Ralph 的 fix_plan.md 对应你的阶段二专家反馈，但 Ralph 是 AI 自己维护 plan，你的是专家主动提供反馈。

---

## 🔑 关键洞察

- **Ralph 的核心**: `while :; do cat PROMPT.md | claude-code ; done` — 无限循环、单任务、specs 锚定、背压验证
- **单体优于多 Agent**: 非确定性系统不应再叠加分布式复杂度，一个进程、一个仓库、垂直扩展
- **Specs ≠ Prompt**: Specs 是稳定的上下文锚（每次循环重新加载），Prompt 是可变的执行指令
- **主 context = 调度器**: 不在主 context 做分配密集工作，subagent 做搜索/写入，主 context 做调度决策
- **背压是质量关键**: 类型系统、静态分析、测试作为 gate 拒绝无效生成；轮子转速 × 正确性 = 实际效率
- **fix_plan.md = 跨循环记忆**: 每个循环上下文独立，fix_plan.md 是循环间传递状态的唯一机制
- **"deterministically bad in an undeterministic world"**: Ralph 的可控性在于它的失败模式是可预测的，可以通过"竖标牌"（调 prompt）来修正
- **适用边界**: greenfield 项目 ~90% 完成度，不适用于存量代码库；仍需资深工程师判断和恢复
