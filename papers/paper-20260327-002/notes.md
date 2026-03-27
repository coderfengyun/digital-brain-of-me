# How to 10x your Claude Skills (using Karpathy's autoresearch method)

**类型**: 方法

---

## 📖 核心叙事 (Narrative)

### 一句话概括
> 将 Karpathy 的 autoresearch 循环优化方法应用于 Claude Skills：用 yes/no checklist 定义质量标准，让 agent 自动测试、微调、保留/回滚，实现 skill prompt 的无人值守持续改进。

### 叙事结构

```
问题: Claude Skills 的输出质量不稳定，可能 30% 的时候失败而用户不自知
↓
观察: Karpathy 提出了 autoresearch 方法——让 AI agent 在循环中自动改进 ML 代码，每次做一个小改动并用指标判断保留或回滚
↓
假设: 这个方法不仅适用于 ML 代码，任何「可以被评分」的东西都能用——包括 skill prompt
↓
方法: 构建 autoresearch skill：(1) 用 yes/no checklist 定义质量标准 (2) agent 自动运行 skill 并评分 (3) 每轮改一个变量 (4) 保留提升、回滚退步 (5) 循环直到 95%+ 或手动停止
↓
验证: 作者的 landing page copy skill 从 56% → 92%，4 轮改动中 3 轮保留、1 轮回滚；另一案例网页加载从 1100ms → 67ms（67 轮）
↓
结论: 只要能定义 checklist，就能用 autoresearch 自动优化任何重复使用的 prompt/skill
```

---

## 📊 数据证据层 (Evidence)

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| Skill 可以被自动优化 | 将 autoresearch 从 ML 代码迁移到 prompt/skill 优化 | Landing page skill: 56% → 92%，4 轮改动 | 作者亲测案例 | ⭐⭐ 中（单一案例，无对照组） |
| Yes/No checklist 是稳定的评分机制 | 用二元 checklist 替代主观评分（如 1-10 分），保证评分一致性 | **例子**: ① "Does the headline include a specific number or result?" ② "Is the copy free of buzzwords like 'revolutionary,' 'synergy,' 'cutting-edge,' 'next-level'?" ③ "Does the CTA use a specific verb phrase?" ④ "Does the first line call out a specific pain point?" ⑤ "Is the total copy under 150 words?" | Checklist 设计示例 | ⭐⭐⭐ 强（checklist 设计思路清晰具体，可直接复用） |
| 3-6 个 checklist 问题是最佳数量 | 太多会导致 skill "gaming the checklist" | **例子**: 类比为「学生背答案而不理解内容」 | 作者经验 | ⭐⭐ 中（无定量实验支撑最优区间） |
| 每轮只改一个变量是关键 | 类比做菜：每次换一种调料，测 10 次，保留或回滚 | **例子**: agent 实际做的改动——① 加入 headline 必须含具体数字的规则 ② 加入 banned buzzwords 列表 ③ 加入 worked example 展示好的 landing page ④ 尝试更严格字数限制但因 CTA 受损而回滚 | 作者 landing page skill 的 changelog | ⭐⭐⭐ 强（changelog 详细记录了每一步决策逻辑） |
| 方法具有通用性 | 可应用于非 prompt 场景 | 网页加载优化: 1100ms → 67ms（67 轮）；cold outreach、newsletter intros 等 | 文中提及案例 | ⭐⭐ 中（网页速度案例说服力强但细节不足，其他为设想） |

---

## 🤔 批判性思考 (Critical Thinking)

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | 假设: skill 的质量可以被 yes/no checklist 完整捕获<br>失效场景: 当质量维度难以二元化时（如「文风自然度」「创意性」），checklist 可能无法覆盖真正重要的质量维度，导致优化方向偏离 |
| 关键局限 | - 仅一个完整案例（landing page skill），样本量不足以证明方法的通用性<br>- 未讨论 LLM-as-judge 的评分稳定性问题（用 LLM 判断 yes/no 本身可能有 variance）<br>- 未涉及 checklist 之间可能存在的冲突（如「简洁」vs「具体」） |
| 实验充分性 | 缺失验证: 不同类型 skill 的效果对比；checklist 数量对最终质量的影响曲线；与人工优化的效果/效率对比 |
