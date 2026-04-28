# 用 WebMCP 为板书/教具前端构建策略迭代 Harness

## 需求

AI 教具的策略迭代闭环是：改 Prompt → 看回放 → 凭直觉判断 → 再改。既慢又不可靠。

核心问题：策略执行效果散落在前端视觉状态里，没有结构化通道暴露给 Agent。Chrome 146 的 WebMCP 提供了一个思路——让网页主动声明能力和状态，Agent 通过结构化 tool 直接交互，不用"猜" UI。

本文借鉴这个思路，为教具前端设计一个专用 MCP 层，作为策略迭代的 Harness。

---

## 一、WebMCP 是什么

传统 AI Agent 操作网页靠截图+识别，脆弱（CSS 一改就崩）、低效（每次都要推理）、不完整（隐藏状态看不到）。

Google 在 Chrome 146 推出 WebMCP（W3C 草案，Google + Microsoft 联合推动），**翻转交互方向**——网页主动告诉 Agent "我有哪些 tool、输入输出是什么"：

```javascript
// JS Tool 注册
navigator.ai.tools.register({
  name: "get_cart_items",
  description: "获取购物车中的所有商品",
  parameters: { /* JSON Schema */ },
  handler: async (params) => {
    return await cartService.getItems();
  }
});
```

核心点：网页从"被动 UI"变成"主动的 tool 提供者"。

我们的场景更窄也更深：**教具前端**与**策略迭代 Agent** 的交互。但思路完全适用。

---

## 二、当前痛点

"策略"指 Prompt 中的教学行为规则。理想迭代闭环：策略定义 → 执行 → 效果观测 → 信号判定 → 修改。**断在"效果观测"和"信号判定"两个环节。**

**观测断裂：** AI Teacher 调用 `showGrid()` → `highlightColumn(3)` → `placeMarker(3, 2)`，效果全在前端页面上。但策略迭代 Agent 只能看到 function call 参数，**看不到前端实际渲染了什么**——网格是否出现、highlight 是否生效、学生看到了什么。

这与教具设计中的核心矛盾一致：AI Teacher 基于**预测状态**决策，但预测和真实状态可能有偏差，而策略迭代 Agent 连预测状态都看不到。

**判定缺失：** 即便能看到状态，也没有结构化的"好/坏"标准。目前靠人看回放凭经验判断——主观、不可复现、不可规模化。

一句话：Agent 既看不到执行效果，也没有判断好坏的依据。

---

## 三、方案：Teaching Tool MCP

让教具前端主动暴露三类 tool：**状态查询**、**动作执行（带返回值）**、**断言检查**。

#### 3.1 状态查询

每个教具暴露 `getState()`，返回**领域模型状态**（不是 DOM dump）。以坐标网格为例：

```json
{
  "tool": "coordinate_grid.getState",
  "response": {
    "grid": { "rows": 5, "columns": 5, "visible": true },
    "markers": [{"position": [3, 2], "type": "student_placed"}],
    "highlights": [{"target": "column", "index": 3, "color": "yellow"}],
    "interaction": { "mode": "student_can_place_marker", "enabled_cells": "all" }
  }
}
```

这与教具设计原则中"状态 = 数学模型 + 视觉呈现"一致。前端负责把 DOM 翻译成领域语言。

#### 3.2 动作执行回溯

AI Teacher 的教具动作不是 function call，而是发言文本中嵌入的 XML 标签——发出后没有返回值，前端静默执行。策略迭代 Agent 需要的能力是：**指定一个已执行的动作，回查它对页面的实际影响和是否报错。**

```json
{
  "tool": "coordinate_grid.inspectAction",
  "params": { "action_index": 2, "turn_id": "ai-turn-003" },
  "response": {
    "action": "<place-marker x=\"3\" y=\"2\" type=\"teacher\" />",
    "executed": true,
    "error": null,
    "state_diff": {
      "markers": { "added": [{"position": [3, 2], "type": "teacher"}] }
    }
  }
}
```

这补上了当前缺失的一环：动作发出后，前端到底发生了什么——执行成功还是静默失败、状态变更是否符合预期。

#### 3.3 断言检查

Harness 能力的核心——对教具状态做**结构化断言**：

```json
{
  "tool": "coordinate_grid.checkState",
  "params": {
    "assertions": [
      {"type": "marker_at", "position": [3, 2], "expected": true},
      {"type": "column_highlighted", "index": 3, "expected": true}
    ]
  },
  "response": {
    "all_passed": true,
    "results": [
      {"assertion": "marker_at([3,2])", "passed": true},
      {"assertion": "column_highlighted(3)", "passed": true}
    ]
  }
}
```

断言由**前端定义**——前端最清楚自己的状态空间和什么检查有意义。Agent 只管组合。

---

## 四、从 MCP 到 Harness

MCP 解决"可观测性"。Harness 在此基础上增加**场景定义**和**验收标准**，自动判断策略执行效果：

```
Harness = 场景定义 + MCP（状态查询 + 断言）+ 验收标准
```

### 示例：教"数对"概念

```yaml
harness: teach_number_pairs_grid_intro

setup:
  teaching_goal: "学生理解列和行的概念"
  initial_state:
    grid: { rows: 5, columns: 5, visible: false }

student_actions:
  - wait: "AI Teacher 完成网格介绍"
  - respond: "老师，列是竖的吗？"
  - action: { type: "place_marker", position: [3, 2] }

checkpoints:
  after_ai_first_turn:
    - coordinate_grid.checkState:
        assertions:
          - { type: "grid_visible", expected: true }
          - { type: "labels_shown", expected: true }
    - ai_output.checkContains: { keywords: ["列", "竖"] }

  after_student_question:
    - ai_output.checkBehavior:
        expected: "回答关于列方向的问题，而非忽略"

  after_student_marker:
    - coordinate_grid.checkState:
        assertions: [{ type: "marker_at", position: [3, 2], expected: true }]
    - ai_output.checkBehavior:
        expected: "对标记给出反馈，确认或纠正"

pass_criteria: "所有 checkpoint 全部通过"
```

### 策略迭代闭环

```
策略定义 → Harness 执行（场景 + 模拟学生）→ MCP 观测 → 断言判定（pass/fail）→ 策略修改 → 循环
```

| 维度 | 之前 | 有 Harness 后 |
|------|------|---------------|
| 效果观测 | 人看回放 | MCP 自动采集 |
| 信号判定 | 主观直觉 | 结构化 pass/fail |
| 迭代速度 | 一天几轮 | 分钟级 |
| 可复现性 | 不可复现 | 同一定义反复执行 |

本质上就是 Inner Loop 验证：Agent 产出 → 模拟执行 → 评测 → 迭代。MCP 提供基础设施，Harness 编排成闭环。

---

## 还不成熟的部分

- **学生行为模拟**：Harness 中 `student_actions` 是预定义的，真实课堂千变万化。可能的演进：真实课堂数据 → 抽取典型路径 → 自动生成 Harness。
- **断言粒度**：太细（"必须黄色高亮"）丧失灵活性，太粗（"有高亮"）失去检验力。需要实践中摸索。
- **实现成本**：每个教具需实现 `getState` 和 `checkState`。状态管理规范的教具成本低（暴露已有状态即可），状态散落在 DOM 里的改造成本大——这也倒逼教具从设计之初就遵循"状态 + 动作"原则。
- **与 WebMCP 标准的关系**：我们是专用协议，不需要遵循 WebMCP 格式。未来 WebMCP 成熟后可考虑对接，但不是现在的事。
