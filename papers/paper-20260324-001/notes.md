# Improving AI Skills with autoresearch & evals-skills

**类型**: 叙事

---

## 核心叙事

### 一句话概括
> 你无法通过自动化跳过理解——在用工具优化 AI skill 之前，你必须亲自阅读输出、建立失败直觉、手动校准评估标准。

### 叙事结构

```
问题: 如何系统性地改进 AI skills 的质量？
↓
尝试1: 把 skill 直接扔给 Auto Research，让它自动生成测试输入、评判标准、跑优化循环
↓
失败: 分数上升了，但 skill 并没有真正变好——机器在优化错误的标准
↓
尝试2: 引入 Hamel 的 evals-skills 生成更好的测试输入（定义输入空间维度，结构化生成）
↓
部分改善: 输入更多样了，但评判标准仍然是机器生成的，没有基于真实失败观察
↓
顿悟: 阅读 Hamel 的 Evals 课程，理解了 "Three Gulfs" 框架
↓
尝试3: 先手动阅读输出 → 编码失败模式 → 构建失败分类 → 写评判标准 → 手动验证 → 再跑优化
↓
结论: 理解鸿沟（Gulf of Comprehension）只能靠人来关闭，自动化无法替代
```

---

## 背景

作者使用 Karpathy 的 [Auto Research](https://github.com/karpathy/autoresearch) 库来优化自己为 AI PM 技能库构建的 skills。Auto Research 的核心思路是：定义测试输入 + 评判标准 → 跑自动优化循环 → 输出更好的 prompt/skill。

Ole 在 X 上分享了将 auto-research 改造为 skill-tuning-skill 的 fork，作者尝试使用这个工具。

## 核心故事：三次迭代

### 第一次：完全自动化
把 skill 直接交给 Auto Research，让它自动完成一切（生成测试输入、写评判标准、跑循环）。分数快速上升，但实际 skill 质量没提升。

**根因**：评判标准是机器凭空生成的，没有任何真实失败行为的依据。机器在高效地优化一个错误的目标函数。

### 第二次：更好的输入，仍然自动化评判
引入 Hamel Husain 的 [evals-skills](https://github.com/hamelsmu/evals-skills)，通过定义输入空间维度（用户角色、场景、功能需求）生成更结构化的测试用例。

**改善**：输入更多样、边缘覆盖更好。
**仍然失败**：评判标准没变，作者仍然没有亲自阅读任何输出。"评判标准是理解力的载体"——没有人工理解，评判标准就是空中楼阁。

### 第三次：先理解，再自动化
重新学习 Hamel 的 Evals 课程，理解了 **Three Gulfs** 框架和 **Analyze-Measure-Improve** 生命周期：

**Three Gulfs（三个鸿沟）**：

| 鸿沟 | 含义 | 关闭方式 |
|------|------|----------|
| Gulf of Comprehension（理解鸿沟） | 你以为系统做了什么 vs 实际做了什么 | 只能靠人工阅读输出 |
| Gulf of Specification（规格鸿沟） | 你想让系统做什么 vs 评判标准实际衡量什么 | 基于真实失败观察写评判标准 |
| Gulf of Generalization（泛化鸿沟） | 测试集表现 vs 未见输入表现 | Auto Research 等自动化工具可以解决——但前提是前两个已关闭 |

**Error Analysis 四步法**（关闭理解鸿沟的方法）：

1. **Open coding**：跑多样输入，阅读每个输出，写自由笔记（不分类）
2. **Axial coding**：将笔记归纳为失败分类体系（二元类别："过于抽象"、"忽略约束"等）
3. **Write judges**：基于分类体系写评判标准
4. **Validate judges**：手动评分 15-20 个输出，校准评判标准与人工判断的一致性

### 关键转折

课程的一句话点醒了作者：**"If you are not willing to look at some data manually on a regular cadence you are wasting your time with evals."**

三次实验的共同模式：总想跳过理解步骤直接进入自动化，感觉更快，但实际是让机器高效地衡量错误的东西。

## 产品管理的类比

作者将这一发现延伸到产品管理：

- PM 跳过手动理解阶段 → 直接跳到解决方案/成功指标 → 根据不反映实际问题的标准衡量
- **产品版的理解鸿沟** = 你以为用户在挣扎什么 vs 用户实际在挣扎什么
- 关闭方式：亲自阅读足够多的客户对话、支持工单、访谈，建立对失败的直觉

---

## 关键洞察

- **自动化无法替代理解**：Three Gulfs 必须按顺序关闭。理解鸿沟是第一个，也是唯一不能被自动化的。你必须亲自阅读输出才能建立失败直觉。
- **评判标准是理解力的载体**（"judges are where comprehension lives"）：如果你没见过真实失败，写出的评判标准就是在衡量一个想象中的目标，优化它等于优化幻想。
- **Goodhart's Law 在 AI evals 中的体现**：当评判标准与真实质量脱节时，优化分数 ≠ 优化质量。机器会非常擅长满足错误的标准。
- **Open coding → Axial coding** 是从混沌观察中提取结构的通用方法，来自质性研究方法论（grounded theory），可以广泛应用于任何需要从观察中建立评估框架的场景。
- **产品决策同理**：在设置仪表盘和指标之前，先亲自接触足够多的用户真实反馈，否则你衡量的可能是错误的东西。
