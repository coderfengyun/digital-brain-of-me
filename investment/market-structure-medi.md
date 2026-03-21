# Market Structure 分析要点（Medi 体系）

## 核心原则

**结构由 Swing 定义，不由时间或形态定义。**

问题不是"这段时间内的高低点在哪"，而是：**这根 Swing 做了什么？它创造了新高还是新低？**

---

## 结构边界

- Range High / Range Low 由 **有意义的 Swing** 决定，不是时间段内的最高最低点
- 只有产生新高或新低的 Swing 才定义边界，其他 bar 是噪音

---

## 新结构的判定

**两个条件缺一不可：**

1. Candle **close** 突破当前 range（不是 wick，是 close）
2. 产生这个突破的 **Swing 起点** = 新结构的起点

> 突破是信号，Swing 起点是结构的锚。

### Sweep 的处理
- 单根 K 线刺穿 range 但未 close 突破 → 视为 **sweep**，仍属于原结构内部
- Sweep 不触发新结构

---

## 结构嵌套

| 层级 | 用途 |
|------|------|
| Bigger Structure | 判断整体方向和预期 |
| Smaller Structure | 大结构内部的子结构，有独立的 range 和预期 |

- Smaller structure 内的 **failure/expectation not met** 必须标记进去，不能忽略
- 它是大结构叙事的一部分

---

## 预期（Expectation）推导

递推逻辑：每个 B 的结果决定下一个 B 的预期方向。

- B1 完成 → 期待 B2 创新高（或新低）
- B2 **未达成预期** → B3 预期：突破（get below）B1 的 range low

---

## 待确认问题

- [ ] **Swing 的起点如何精确定义？**（是方向性移动开始的 K 线，还是有其他规则？）
- [ ] **Flat structure 具体指什么形态？** failure to achieve 发生后价格横盘，此时小结构起点的选取规则是什么？
