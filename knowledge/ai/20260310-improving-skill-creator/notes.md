# Improving Skill-Creator: Test, Measure, and Refine Agent Skills

**类型**: 叙事

---

## 📖 完整叙事

### 背景

Anthropic 观察到一个关键问题：大多数 skill 作者是**领域专家而非工程师**。他们了解自己的工作流程，但缺乏工具来判断：
- skill 在新模型上是否仍然有效
- skill 是否在正确的时机被触发
- 修改后 skill 是否真的变好了

### 核心故事

为解决这一问题，Anthropic 为 skill-creator 推出了一套完整的测试、度量和优化工具链：

**1. Evaluation Framework（评估框架）**
作者可以编写 evals——检查 Claude 对给定 prompt 是否产生预期输出的测试。例如 PDF skill 通过 evals 发现了处理非填充表单的失败，进而改用改进的文本坐标锚定方法修复。

**2. Benchmark Mode（基准模式）**
标准化评估工具，追踪：
- eval 通过率
- 执行时间
- token 使用量

帮助作者识别：模型改进何时让某个 skill 变得不再必要，或何时发生质量回退。

**3. Multi-Agent Support（多 Agent 支持）**
独立 agent 并行运行 evals，使用干净上下文，消除测试间的交叉污染，提供更快结果和独立的 token/时间指标。

**4. A/B Comparison（A/B 对比）**
比较器 agent 在两个 skill 版本之间（或 skill vs baseline）进行盲评，判断改动是否真正带来提升。

**5. Skill Description Optimization（描述优化）**
skill-creator 分析当前描述与示例 prompt，建议改进以减少误触发（false positive）和漏触发（false negative）。测试显示 6 个文档创建 skill 中有 5 个的触发精度得到改善。

### 关键转折

文章最后指出一个深刻洞察：随着模型能力提升，**"skill" 和 "specification" 的边界将模糊化**。
- 当前：SKILL.md 文件作为"实现计划"，提供详细指令
- 未来：自然语言描述期望结果即可，模型自主决定如何执行

### 结果与意义

这套工具链让非工程师也能：
1. 验证 skill 是否正常工作
2. 捕获性能回退
3. 持续改进 skill 描述

本质上是将软件工程的 CI/CD 理念引入 AI skill 开发。

---

## 🔑 关键洞察

- **Skill 作者画像**：领域专家而非工程师 → 需要无代码的测试工具
- **两类 Skill**：Capability uplift（能力提升）vs Encoded preference（偏好编码）
- **测试四件套**：Evals + Benchmark + Multi-Agent + A/B Comparison
- **未来趋势**：Skill（How）→ Specification（What），模型自主决定实现方式
- **触发优化有效**：6 个 skill 中 5 个改善（83% 成功率）
