# 多任务 Prompt 设计：Few-shot 的正交原则

## 核心观点

在多任务结构的 Prompt 设计中，一个重要的最佳实践是：

**将 few-shot 示例的应用范围缩小到单一任务，实现正交设计。**

简单来说：每个任务只看自己的例子，不看别人的例子。

## 什么是正交设计

正交（Orthogonal）在这里的含义是：任务之间相互独立，互不干扰。

在 few-shot 示例的上下文中，正交设计意味着：
- 任务 A 的示例只用于指导任务 A 的输出
- 任务 B 的示例只用于指导任务 B 的输出
- 两组示例之间没有交叉引用

## 为什么要这样做

### 问题：混合示例带来的干扰

假设我们有一个教学内容生成系统，需要同时输出：
1. 文本板书（写在屏幕上的内容）
2. 讲解发言（老师说的话）
3. 教具操作（互动组件的控制）

如果我们把所有示例混在一起，让发言、板书、教具指令都出现在同一段输出中：

```
示例 1:
发言开始:同学们，我们来看这个公式。<document-opt method="add" id="T1" type="text" belong="C1" content="勾股定理：a² + b² = c²" />这就是著名的勾股定理。<document-opt method="highlight" id="T1" />

示例 2:
发言开始:注意这里的推导步骤。<document-opt method="add" id="T2" type="text" belong="C1" belowOf="T1" content="证明过程：..." /><document-opt method="animate" id="T2" />
```

**问题出现了**：当模型学习这些示例时，三种任务的模式互相干扰：

- 发言风格可能混入板书内容的结构化特征
- 板书指令的 XML 标签格式可能干扰发言的自然语气
- 模型难以独立优化每种输出的质量

### 解决方案：正交的 few-shot 设计

将示例按任务类型拆分，每类任务有独立的示例集：

```
[板书任务示例]
示例: <document-opt method="add" id="T1" type="text" belong="C1" content="勾股定理：a² + b² = c²" />
示例: <document-opt method="add" id="T2" type="text" belong="C1" belowOf="T1" content="证明过程：..." />

[发言任务示例]
示例: 发言开始:同学们，我们来看这个公式。
示例: 发言开始:注意这里的推导步骤。

[教具操作示例]
示例: <document-opt method="highlight" id="T1" />
示例: <document-opt method="animate" id="T2" />
示例: <emotion type="super-affirm" />
```

每个任务独立参考自己的示例，输出更加纯粹和一致。

## 实践要点

### 1. 识别任务边界

首先明确系统中有哪些独立的输出任务。判断标准：
- 输出格式是否不同（文本 vs XML 标签 vs 结构化数据）
- 输出目的是否不同（展示 vs 控制 vs 交互）
- 输出风格是否不同（书面 vs 口语 vs 结构化）

### 2. 为每个任务准备专属示例

每组示例应该：
- 只包含该任务的输入输出
- 覆盖该任务的典型场景
- 体现该任务特有的风格和规范

### 3. 在 Prompt 结构中保持隔离

可以通过以下方式实现隔离：
- 分段落/分 section 组织
- 使用明确的任务标签
- 在指令中明确"只参考本节示例"

## 示例：教学内容生成系统

### 正交设计的 Prompt 结构

```markdown
## 任务 1: 生成文本板书

板书通过 document-opt 标签操作，支持添加、修改、高亮等动作。

示例输入: 展示勾股定理公式
示例输出:
<document-opt method="add" id="C1" type="container" theme="white" />
<document-opt method="add" id="T1" type="text" belong="C1" content="## 勾股定理" />
<document-opt method="add" id="T2" type="text" belong="C1" belowOf="T1" content="直角三角形中：a² + b² = c²" />

[当前任务]
输入: {user_input}
输出:

---

## 任务 2: 生成讲解发言

讲解发言以"发言开始:"为前缀，使用自然口语，引导性强。

示例输入: 引入勾股定理
示例输出: 发言开始:同学们，今天我们来认识一个非常重要的定理。你们看这个直角三角形...

示例输入: 肯定学生回答
示例输出: 发言开始:完全正确！<emotion type="super-affirm" />你的思路很清晰。

[当前任务]
输入: {user_input}
输出:

---

## 任务 3: 生成教具操作

教具操作使用 XML 标签，包括 document-opt（板书控制）和 emotion（情感表达）。

示例输入: 高亮公式
示例输出: <document-opt method="highlight" id="T2" />

示例输入: 表达赞赏
示例输出: <emotion type="super-affirm" />

示例输入: 等待学生回答
示例输出: <wait />

[当前任务]
输入: {user_input}
输出:
```

## 总结

正交的 few-shot 设计是多任务 Prompt 工程的重要原则：

| 做法 | 效果 |
|------|------|
| 混合所有任务的示例 | 风格混乱，输出不稳定 |
| 按任务隔离示例 | 风格一致，输出可控 |

**记住**：每个任务只看自己的例子，不看别人的例子。这就是 few-shot 的正交原则。
