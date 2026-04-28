# 用 WebMCP 为板书/教具前端构建策略迭代 Harness

## 需求

AI 教具的策略迭代缺乏一个结构化的反馈机制。

目前策略的验证方式是：改 Prompt → 用肉眼看课程回放 → 凭直觉判断好不好 → 再改。这个闭环既慢又不可靠。核心问题在于——策略的执行效果散落在前端页面的各种视觉状态里，但没有一个结构化的通道把这些状态暴露给 Agent，让 Agent 能自动判断"这次策略执行得怎么样"。

Chrome 146 引入的 WebMCP 提供了一个思路：让网页主动声明自己的能力和状态，AI Agent 不需要"猜" UI，而是通过结构化的 tool 直接与页面交互。

本文讨论如何借鉴这个思路，为板书和教具的前端构建一个类似的 MCP 层——不是给 Chrome 用的通用标准，而是给我们自己的策略迭代 Agent 用的专用 Harness。

---

## 一、WebMCP 是什么

### 问题：AI Agent 与网页的交互靠"猜"

传统的 AI Agent 操作网页的方式是：截图 → 识别 UI 元素 → 点击/输入。这本质上是在用视觉模型"猜"网页的结构和功能。问题很多：

- **脆弱**：CSS 改了个样式，Agent 就认不出按钮了
- **低效**：每次操作都需要截图+推理，延迟高
- **不完整**：很多页面状态（如 loading 状态、隐藏的数据字段）在视觉上不可见

### WebMCP 的解法：网页主动声明能力

Google 在 Chrome 146 中推出 WebMCP（W3C 草案标准，Google + Microsoft 联合推动），核心思想是翻转交互方向——不是 Agent 去猜网页能做什么，而是网页主动告诉 Agent：

> "我有这些 tool 可以用，每个 tool 的输入输出是什么。"

两种接入方式：

**1. HTML 属性声明**（适合简单场景）
```html
<button mcp-tool="submit_order"
        mcp-description="提交当前购物车订单"
        mcp-params='{"confirm": "boolean"}'>
  下单
</button>
```

**2. JS Tool 注册**（适合复杂交互）
```javascript
navigator.ai.tools.register({
  name: "get_cart_items",
  description: "获取购物车中的所有商品",
  parameters: { /* JSON Schema */ },
  handler: async (params) => {
    return await cartService.getItems();
  }
});
```

核心点在于：网页从"被动的 UI 界面"变成了"主动暴露能力的 tool 提供者"。Agent 不再需要理解 DOM 结构，只需要调用声明好的 tool。

### 对我们的启发

WebMCP 解决的是通用场景——任意网页与任意 AI Agent 的交互。我们的场景更窄也更深：**板书/教具前端**与**策略迭代 Agent** 的交互。但核心思路完全适用：让前端主动暴露结构化的状态和操作接口，而不是让 Agent 去猜。

---

## 二、当前痛点：策略迭代缺乏结构化反馈

### 策略迭代的闭环长什么样

在 AI 教具的语境下，"策略"指的是 Prompt 中定义的教学行为规则——什么时候出题、什么时候给提示、教具动作怎么编排。策略迭代的理想闭环：

```
策略定义（Prompt）
    ↓
策略执行（AI Teacher 在课堂中按策略行动）
    ↓
效果观测（执行后学生和教具处于什么状态）
    ↓
信号判定（这次执行是好是坏）
    ↓
策略修改（基于信号调整 Prompt）
    ↓ 循环
```

### 断在哪里

问题出在**效果观测**和**信号判定**两个环节。

**效果观测的困境：状态散落在前端，Agent 看不到。**

AI Teacher 在一轮对话中发出多个教具动作，比如：`showGrid()` → `highlightColumn(3)` → `placeMarker(3, 2)`。这些动作的执行效果全部体现在前端页面的视觉变化上——网格出现了、第三列亮了、标记放到了 (3,2) 位置。

但策略迭代 Agent 能看到什么？它能看到 Prompt，能看到 AI Teacher 的输出文本和 function call 记录，但**看不到前端实际渲染出了什么**。Agent 不知道：

- 网格是否正确渲染了
- highlight 是否真的生效了
- 学生是否看到了预期的视觉引导

这正是前面讨论过的教具设计中的核心矛盾——AI Teacher 基于**预测状态**做决策，但预测状态和真实状态之间可能存在偏差。而策略迭代 Agent 连预测状态都看不到，它只能看到 function call 的参数。

**信号判定的困境：没有明确的"好/坏"定义。**

即便策略迭代 Agent 能看到前端状态，它也不知道怎么判断"这次策略执行得好不好"。目前的判断靠人——课程设计师回放课程录像，凭经验判断。这个判断是主观的、不可复现的、不可规模化的。

缺乏的是一个**结构化的评测标准**：给定当前教学目标和学生状态，教具应该处于什么状态，AI Teacher 应该做出什么反应。

### 一句话概括痛点

策略迭代 Agent 既看不到策略的执行效果（前端状态不可观测），也没有判断效果好坏的依据（缺乏结构化评测标准）。

---

## 三、方案：为前端设计一个 Teaching Tool MCP

### 核心思路

借鉴 WebMCP 的思路，让教具前端主动暴露两类信息：

1. **状态查询 tool**：Agent 可以随时查询教具当前的完整状态
2. **断言/检查 tool**：Agent 可以对教具状态做结构化的检查，得到明确的 pass/fail

这不是一个通用的 Web 标准，而是我们自己的教具前端与策略迭代 Agent 之间的**专用协议**。

### 具体设计

#### 3.1 状态查询类 Tool

每个教具暴露一个 `getState()` tool，返回结构化的完整状态。

以坐标网格教具为例：

```json
{
  "tool": "coordinate_grid.getState",
  "response": {
    "grid": {
      "rows": 5,
      "columns": 5,
      "visible": true
    },
    "markers": [
      {"position": [3, 2], "type": "student_placed", "style": "default"}
    ],
    "highlights": [
      {"target": "column", "index": 3, "color": "yellow"}
    ],
    "labels": {
      "x_axis": "列",
      "y_axis": "行"
    },
    "interaction": {
      "mode": "student_can_place_marker",
      "enabled_cells": "all"
    }
  }
}
```

关键：这个状态不是 DOM dump，而是**教具自己的领域模型状态**——与 `ai-teaching-tool-design-principles.md` 中讨论的"状态 = 数学模型 + 视觉呈现"一致。前端有责任把 DOM 状态翻译成领域语言。

#### 3.2 动作执行类 Tool

教具暴露的动作接口，与 AI Teacher 用的 function call 一致，但增加了**执行结果的结构化返回**：

```json
{
  "tool": "coordinate_grid.placeMarker",
  "params": {"x": 3, "y": 2, "type": "teacher"},
  "response": {
    "success": true,
    "state_change": {
      "before": {"markers_count": 1},
      "after": {"markers_count": 2}
    },
    "side_effects": ["triggered_student_feedback_animation"]
  }
}
```

对比当前的 function call 方式：AI Teacher 调用 `placeMarker(3, 2)` 后，什么返回值都没有，只能靠预测推演后续状态。有了 MCP 层，每个动作都有明确的执行结果和状态变更记录。

#### 3.3 断言/检查类 Tool

这是 Harness 能力的核心——让 Agent 可以对教具状态做**结构化断言**：

```json
{
  "tool": "coordinate_grid.checkState",
  "params": {
    "assertions": [
      {"type": "marker_at", "position": [3, 2], "expected": true},
      {"type": "column_highlighted", "index": 3, "expected": true},
      {"type": "student_interaction_enabled", "expected": true}
    ]
  },
  "response": {
    "all_passed": true,
    "results": [
      {"assertion": "marker_at([3,2])", "passed": true},
      {"assertion": "column_highlighted(3)", "passed": true},
      {"assertion": "student_interaction_enabled", "passed": true}
    ]
  }
}
```

断言是**前端定义的**，不是 Agent 定义的。前端最清楚自己的状态空间，也最清楚什么样的检查是有意义的。Agent 只需要组合这些原子断言。

---

## 四、从 MCP 到 Harness：提供明确的成功/失败信号

### MCP ≠ Harness

上面设计的 MCP 层解决的是"可观测性"问题——Agent 能看到前端状态了。但 Harness 要解决的是更上一层的问题：**给定一个策略和一个教学场景，自动判断策略执行的效果。**

Harness 建立在 MCP 之上，增加了两个维度：

1. **场景定义**：一组初始条件 + 模拟学生行为
2. **验收标准**：一组必须通过的断言

```
Harness = 场景定义 + MCP（状态查询 + 断言检查）+ 验收标准
```

### 一个完整的 Harness 示例

场景：教"数对"概念时，AI Teacher 应该先展示网格、再引导学生标记位置。

```yaml
harness: teach_number_pairs_grid_intro
description: 验证策略是否正确引导学生认识坐标网格

# 场景设定
setup:
  teaching_goal: "学生理解列和行的概念"
  initial_state:
    grid: { rows: 5, columns: 5, visible: false }
    markers: []

# 模拟学生行为（按顺序触发）
student_actions:
  - wait: "AI Teacher 完成网格介绍"
  - respond: "老师，列是竖的吗？"
  - action: { type: "place_marker", position: [3, 2] }

# 验收标准（使用 MCP 断言 tool）
checkpoints:
  after_ai_first_turn:
    - coordinate_grid.checkState:
        assertions:
          - { type: "grid_visible", expected: true }
          - { type: "labels_shown", expected: true }
    - ai_output.checkContains:
        keywords: ["列", "竖"]

  after_student_question:
    - ai_output.checkBehavior:
        expected: "回答学生关于列方向的问题，而非忽略或跳过"

  after_student_marker:
    - coordinate_grid.checkState:
        assertions:
          - { type: "marker_at", position: [3, 2], expected: true }
    - ai_output.checkBehavior:
        expected: "对学生的标记给出反馈，确认或纠正位置"

# 判定
pass_criteria: "所有 checkpoint 的 assertions 全部通过"
```

### Harness 如何改变策略迭代

有了 Harness，策略迭代的闭环变成：

```
策略定义（Prompt）
    ↓
Harness 执行（自动运行场景 + 模拟学生）
    ↓
MCP 观测（通过 getState/checkState 采集前端状态）
    ↓
断言判定（pass/fail，有明确的失败原因）
    ↓
策略修改（Agent 基于结构化反馈自动调整，或人工介入）
    ↓ 循环
```

对比之前：

| 维度 | 之前 | 有 Harness 后 |
|------|------|---------------|
| 效果观测 | 人看回放 | MCP 自动采集前端状态 |
| 信号判定 | 主观直觉 | 结构化断言，pass/fail |
| 迭代速度 | 一天改几轮 | 自动化运行，分钟级 |
| 可复现性 | 不可复现 | 同一 Harness 定义可反复执行 |
| Agent 参与 | Agent 只写 Prompt | Agent 可读断言结果，自动迭代 |

### 与 Inner Loop 的关系

这个 Harness 本质上就是 principles.md 中提到的 **Inner Loop 验证**：

> Agent 产出 → 模拟执行 → 评测 → 迭代，形成自动化改进闭环

MCP 提供了"模拟执行"和"评测"所需要的基础设施，Harness 把它们编排成可重复运行的闭环。

---

## 还不成熟的部分，边想边写

**学生行为模拟的真实性问题。** Harness 中的 `student_actions` 是预定义的，但真实课堂中学生的反应千变万化。一个 Harness 只能覆盖一条路径。解决思路可能是：积累真实课堂数据 → 抽取典型路径 → 自动生成 Harness。但这个还在设想阶段。

**断言的粒度问题。** 太细的断言（"第三列必须是黄色高亮"）让策略失去灵活性——也许用橙色高亮也可以。太粗的断言（"页面上有高亮"）又失去了检验能力。需要在实践中找到合适的粒度。

**MCP 层的实现成本。** 每个教具都需要额外实现 `getState` 和 `checkState`。如果教具本身的状态管理就比较规范（遵循原则一和原则二），这个成本不高——把已有的内部状态通过 MCP 接口暴露出来即可。但如果教具的状态散落在各种 DOM 节点里，改造成本就大了。这也倒逼教具在设计之初就遵循"状态 + 动作"的原则。

**与 WebMCP 标准的关系。** 我们的 Teaching Tool MCP 是专用协议，不需要也不应该遵循 WebMCP 的标准格式。但如果未来 WebMCP 成熟了，可以考虑把我们的教具注册为标准 WebMCP tool，让外部 Agent 也能与教具交互。这是一个可选的演进路径，不是现在需要做的事。
