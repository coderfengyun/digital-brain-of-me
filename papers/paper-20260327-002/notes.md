# How to 10x your Claude Skills (using Karpathy's autoresearch method)

**类型**: 方法

---

## 📖 核心叙事 (Narrative)

### 一句话概括
> 将 Karpathy 的 autoresearch 循环优化方法应用到 Claude Skills 上，通过「改一点→测一遍→保留/回滚」的自动循环，让 AI agent 自主将 skill 质量从 56% 提升到 92%。

### 叙事结构

```
问题: Claude Skills 的输出质量不稳定，约 30% 的时间会失败，用户往往不自知
↓
观察: Karpathy 发布了 autoresearch 方法——让 AI 在循环中自动做小改动、测量、保留/回滚
↓
假设: 这个方法不只适用于 ML 代码，任何「可度量+可改进」的东西都适用，包括 Claude Skills
↓
方法: 构建 autoresearch skill，核心三要素：
  1. Yes/No checklist 作为评分标准（3-6 个问题）
  2. 单次改一个变量的循环优化
  3. 自动保留/回滚机制 + live dashboard
↓
验证: Landing page copy skill 从 56% → 92%（4 轮，3 保留 1 回滚）
↓
结论: 只要能打分，就能 autoresearch——适用于 skills、网站性能、cold outreach、newsletter 等
```

---

## 📊 数据证据层 (Evidence)

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| Skills 输出不稳定 | - | 30% 失败率 | 作者经验估计 | ⭐ 弱（无系统测量） |
| Autoresearch 可自动优化 skill | 将 ML 领域的循环优化迁移到 prompt engineering | 56% → 92%，4 轮优化 | 作者实测 landing page skill | ⭐⭐ 中（单案例，无对照） |
| Yes/No checklist 比 1-10 评分更可靠 | 二值化评分消除主观波动 | **例子**: ① "Does the headline include a specific number or result?" ② "Is the copy free of buzzwords like 'revolutionary,' 'synergy,' 'cutting-edge'?" ③ "Does the first line call out a specific pain point?" | 文章论述 | ⭐⭐ 中（直觉合理但无定量对比） |
| 3-6 个 checklist 问题是最佳数量 | - | 过多会导致 skill "gaming the checklist" | 作者经验 | ⭐ 弱（无实验支撑） |
| 方法泛化到非 skill 场景 | - | 网站加速 1100ms → 67ms（67 轮） | 引用他人案例 | ⭐⭐ 中（二手数据，未验证） |

---

## 🤔 批判性思考 (Critical Thinking)

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | 假设: skill 质量可以分解为离散的 yes/no 检查项<br>失效场景: 1) 质量是整体性的（如创意写作的"味道"难以 checklist 化）；2) checklist 本身有缺陷——通过所有检查但整体仍差（Goodhart's Law） |
| 关键局限 | - 只展示了 1 个案例（landing page），泛化性未验证<br>- 没有说明每轮优化的 token 成本和时间开销<br>- 「谁来评分」的问题——用 LLM 评 LLM 的输出，评分本身可能不可靠<br>- 没有讨论 skill 之间的耦合——优化一个 skill 可能影响依赖它的其他 skill |
| 实验充分性 | 缺失验证: 1) 多个不同类型 skill 的对比实验；2) 与人工优化的效果对比；3) 优化后的长期稳定性测试；4) 不同 checklist 设计的影响 |

---

## 💡 可操作要点

### 方法的核心循环
1. 定义 3-6 个 yes/no 评分问题
2. 跑 baseline 得到初始分数
3. Agent 分析失败项 → 做一个小改动 → 重新测试
4. 分数提升则保留，下降则回滚
5. 重复直到 95%+ 连续 3 次，或手动停止

### Agent 实际做的优化类型（从案例中提取）
- 针对最常见失败项添加具体规则
- 添加黑名单（banned words list）
- 添加 worked example（让 skill "看到"好的输出长什么样）
- 尝试约束性改动但发现副作用后自动回滚

### 对我的启发
- 可以考虑将这个方法用于 digital-brain 的 skill 优化——特别是 content creation 类的 skill
- Checklist 设计是关键，本质上是把「品味」形式化为可度量的标准
- Changelog 的价值 > 最终优化结果——它是一份「什么对这个 skill 有效」的知识库
