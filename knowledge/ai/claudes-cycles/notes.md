# Claude's Cycles

**类型**: 叙事

---

## 📖 完整叙事

### 背景

Donald Knuth 在为《计算机程序设计艺术》撰写有向哈密顿回路章节时，遇到了一个开放问题：

> 考虑一个有 m³ 个顶点的有向图，每个顶点 ijk（0 ≤ i, j, k < m）有三条出边。能否将所有边分解为三个有向哈密顿回路？（m > 2）

Knuth 解决了 m = 3 的情况，他的朋友 Filip Stappers 经验性地发现了 4 ≤ m ≤ 16 的解，但通用构造仍是未解之谜。

### 核心故事

Filip 决定把这个问题交给 Claude Opus 4.6。他给了 Claude 一个关键指令：每次运行探索程序后必须立即记录进度。

Claude 的探索历程堪称精彩：

**探索 1-5**：尝试简单方案
- 重新表述问题为排列分配
- 尝试线性/二次函数 → 失败
- DFS 暴力搜索 → 太慢
- 发现 2D 蛇形模式和 Cayley 图结构
- 构造 3D 蛇形模式（实际上是 Gray 码）→ 残余图结构僵硬

**探索 6-14**：多条死路
- 各种方法都没有突破

**探索 15**：关键转折！
- Claude 引入"纤维分解"（fiber decomposition）
- 发现商映射 φ(i,j,k) = i+j+k mod m 将图分层
- 问题从 3D 降维为分层的 2D 问题

**探索 16-25**：深入纤维框架
- 实现纤维框架代码
- m = 3 的穷举搜索在 0.1 秒内成功
- 模拟退火找到 m = 4 的解
- 但模拟退火"无法给出通用构造，需要纯数学"

**探索 26-30**：接近突破
- Claude 自言自语："也许正确的思路是：不要用纤维思考，直接思考什么构成哈密顿回路"
- 探索 27 差点成功：用坐标旋转生成三个回路，但有 3(m-1) 个顶点冲突
- 探索 30 回头看模拟退火的解，发现关键规律：每层的选择只依赖单个坐标

**探索 31**：胜利！
- 构造出 Python 程序
- 对 m = 3, 5, 7, 9, 11 全部成功
- "所有三个回路都是哈密顿的，所有边都被使用，完美分解！"

整个过程约 1 小时。

### 关键转折

**转折一**：纤维分解的发现（探索 15）
- 将看似复杂的 3D 问题转化为可处理的分层结构

**转折二**：从数值解回到结构洞察（探索 30）
- Claude 没有执着于模拟退火找更多解，而是分析已有解的结构
- 发现"每层只依赖单坐标"这个关键规律

**转折三**：人机协作的微妙之处
- Filip 需要反复提醒 Claude 记录进度
- Claude 有时会卡住或出错，需要重启
- 但整体方向是正确的

### 结果与意义

**直接成果**：
- 奇数 m 的完全解决方案（约 1 小时）
- Knuth 给出严格证明
- 存在 760 种 "Claude-like" 有效分解

**后续发展**（Postscript）：
- 偶数情况后来由 GPT-5.3-codex 解决（m ≥ 8）
- GPT-5.4 Pro 生成了 14 页完整证明
- Kim Morrison 用 Lean 形式化验证了 Claude 的构造
- 多智能体协作（Claude + GPT）产出了更简洁的解法

**Knuth 的感慨**：
> "Shock! Shock! ... What a joy it is to learn not only that my conjecture has a nice solution but also to celebrate this dramatic advance in automatic deduction and creative problem solving."

> "I think Claude Shannon's spirit is probably proud to know that his name is now being associated with such advances. Hats off to Claude!"

---

## 🔑 关键洞察

- **AI 可以解决开放数学问题**：不是暴力搜索，而是通过重新表述问题、发现结构、逐步逼近
- **探索过程的价值**：31 轮探索中大部分是"失败"，但每次失败都缩小了搜索空间或提供了新视角
- **人机协作的必要性**：Filip 的提示策略（强制记录进度）对成功至关重要；Claude 有时会迷失方向
- **多模型协作的潜力**：最终最简解法来自 GPT 和 Claude 的"对话"——不同模型有互补的优势
- **从数值到结构**：关键突破不是找到更多数值解，而是从已有解中发现结构规律
