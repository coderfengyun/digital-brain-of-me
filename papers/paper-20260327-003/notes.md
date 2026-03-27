# AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness

**类型**: 方法
**作者**: Xinghua Lou, Miguel Lázaro-Gredilla, Antoine Dedieu, Carter Wendelken, Wolfgang Lehrach, Kevin P. Murphy (Google DeepMind)
**来源**: arXiv:2603.03329

---

## 📖 核心叙事 (Narrative)

### 一句话概括
> LLM 做 agent 时频繁产生非法动作（如国际象棋中 78% 的失败来自非法走步），本文让 LLM 自己通过代码搜索生成 harness（动作验证器/策略），用小模型 + 自动 harness 打败大模型。

### 叙事结构

```
问题: LLM 作为 agent 时，经常执行环境不允许的非法动作（如 Kaggle GameArena 中 Gemini-2.5-Flash 78% 的国际象棋败局源于非法走步）
↓
观察: 传统方案要么微调（昂贵且损害其他能力），要么手写 harness（脆弱、费力、每个游戏都要重写）
↓
假设: LLM 自身的代码生成能力可以用来自动合成 harness——让 LLM 编写验证/过滤非法动作的代码，通过环境反馈迭代优化
↓
方法: "Code as Harness" 框架——维护代码假设的树结构，用 Thompson Sampling 选择下一个节点进行优化，LLM 作为 mutation operator 根据环境反馈（非法动作错误信息）迭代修改代码。三种变体:
  1. Harness-as-Action-Filter: 代码生成合法动作集，LLM 排序选择
  2. Harness-as-Action-Verifier: LLM 生成动作 → 代码验证 → 非法则重试（主要聚焦）
  3. Harness-as-Policy: 整个策略都是代码，推理时不需要 LLM
↓
验证: 在 TextArena 的 145 个游戏上训练 harness，全部达到 100% 合法动作率；
  - 2P 游戏: Flash+Harness 56.3% 胜率 vs Pro 38.2%
  - 1P 游戏: Flash+Harness 平均 reward 0.745 vs Pro 0.707
  - Harness-as-Policy: 纯代码策略 reward 0.870，超过 GPT-5.2-High (0.844)，推理成本近乎为零
↓
结论: 小模型 + 自动合成 harness 可以超越大模型，且更经济；极端情况下可完全消除推理时的 LLM 调用
```

---

## 📊 数据证据层 (Evidence)

| 论点 | 创新点 | 支撑数据 | 数据来源 | 说服力评估 |
|------|--------|----------|----------|------------|
| LLM agent 的主要失败模式是非法动作 | 问题定义明确 | Kaggle GameArena 国际象棋中 Gemini-2.5-Flash 78% 败局来自非法走步 | §1, Kaggle 2025 比赛数据 | ⭐⭐⭐ 强——来自真实竞赛的定量数据 |
| 自动生成的 harness 能完全消除非法动作 | 树搜索 + Thompson Sampling 的代码优化框架 | 145 个 TextArena 游戏全部达到 100% 合法动作率；平均仅需 14.5 轮迭代 | §4.1, Table 1 | ⭐⭐⭐ 强——覆盖面广（145 个游戏），100% 成功率 |
| 小模型 + Harness 超越大模型（2P） | Harness-as-Action-Verifier | Flash+Harness 赢 9/16 游戏（56.3% 胜率）vs Pro（38.2%）；对 vanilla Flash 赢 12/16（64.8%） | §4.2, Fig.3 | ⭐⭐ 中——16 个游戏的样本量有限，但趋势清晰 |
| 小模型 + Harness 超越大模型（1P） | 同上 | Flash+Harness 平均 reward 0.745 vs Pro 0.707 vs Flash 0.673；8/16 游戏胜出，5/16 平局 | §4.2, Fig.4 | ⭐⭐ 中——优势相对温和（0.745 vs 0.707） |
| 纯代码策略可超越所有 LLM agent | Harness-as-Policy: 完全消除推理时 LLM | 平均 reward 0.870，超过 GPT-5.2-High (0.844)、Pro (0.707)；推理成本近乎零 vs GPT-5.2 实验花费 $640 | §4.3, Fig.5 | ⭐⭐⭐ 强——性能最优且成本降维打击 |
| 方法在复杂游戏上也能收敛 | 去掉 "Available Moves" 提示增加难度 | 即使移除合法动作列表提示（如 Chess-v0 示例），harness 仍能通过代码逻辑推导合法动作 | §4, Appendix A.4 | ⭐⭐ 中——展示了鲁棒性，但只给了定性示例 |
| 训练效率高 | Thompson Sampling 引导的搜索 | **例子**: 简单游戏如 Bandit-v0 仅需 2 轮迭代；复杂游戏如 Chess-v0 需 64 轮、Othello-v0 需 62 轮，但仍能收敛到 100% | §4.1, Fig.2, Table 1 | ⭐⭐ 中——收敛性好，但缺少与 baseline 搜索策略的对比 |

---

## 🤔 批判性思考 (Critical Thinking)

| 问题 | 分析 |
|------|------|
| 核心假设及失效场景 | 假设: 游戏环境能提供明确的"非法动作"反馈信号，且动作空间可通过规则性代码描述<br>失效场景: 1) 开放式文本对话游戏（论文已排除 9 个此类游戏，如 Mafia、Codenames）；2) 动作合法性依赖于对手心理/隐藏信息而非固定规则；3) 连续动作空间（如机器人控制中的精确力矩值） |
| 关键局限 | - 每个游戏需要独立训练 harness，145 个游戏 = 145 次独立搜索，无跨游戏迁移<br>- 仅在 TextArena 文本游戏上验证，未证明在多模态、物理交互等环境的适用性<br>- Harness-as-Policy 仅评估 1P 游戏，作者承认 2P 策略需要 MCTS 类搜索更难学习<br>- 评估的 32 个游戏是从 145 个中选出的，选择标准未详细说明 |
| 实验充分性 | 缺失验证: 1) 未与手写 harness baseline 对比性能和开发成本；2) 未消融 Thompson Sampling 的贡献（vs 简单迭代优化）；3) 未测试在非游戏 agent 场景（如 web browsing、tool use）的效果；4) Harness-as-Policy 的 256 轮训练成本未报告 |
