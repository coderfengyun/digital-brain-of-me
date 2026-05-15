# 用评估（Evals）系统化地测试智能体技能

> 来源: https://developers.openai.com/blog/eval-skills
> 作者: Dominik Kundel, Gabriel Chua
> 日期: 2026年1月22日
> 主题: Codex

一份实用指南：如何将智能体技能变成可测试、可评分、可持续改进的东西。

当你在为 Codex 这样的智能体迭代一个技能时，很难判断你是真的在改进它，还是只是改变了它的行为。一个版本感觉更快了，另一个似乎更可靠了，然后回归悄然出现：技能没有触发、跳过了必要步骤，或者留下了多余的文件。

技能的本质是一组[有组织的提示词和指令](https://developers.openai.com/codex/skills)。随着时间推移，改进技能最可靠的方式就是像[评估任何其他 LLM 应用的提示词](https://platform.openai.com/docs/guides/evaluation-best-practices)一样去评估它。

**Evals**（即**评估**）用于检查模型的输出及其产出过程是否符合你的预期。与其问"这感觉好些了吗？"（或者靠直觉），evals 让你能问出具体的问题：

- 智能体调用了这个技能吗？
- 它执行了预期的命令吗？
- 它产出的结果遵循了你关心的约定吗？

具体来说，一个 eval 就是：一个提示词 → 一次捕获的运行（trace + 产物） → 一小组检查 → 一个可以跨时间比较的分数。

在实践中，智能体技能的 evals 很像轻量级的端到端测试：运行智能体，记录发生了什么，然后根据一小组规则对结果评分。

本文介绍了一套清晰的模式：从定义成功标准开始，然后添加确定性检查和基于评分标准的打分，使改进（和回归）一目了然。

## 1. 在编写技能之前先定义成功标准

在编写技能本身之前，先用你能实际衡量的术语写下"成功"意味着什么。一种有用的思考方式是将检查分为几个类别：

- **结果目标：** 任务完成了吗？应用能运行吗？
- **过程目标：** Codex 调用了技能并遵循了你预期的工具和步骤吗？
- **风格目标：** 输出遵循了你要求的约定吗？
- **效率目标：** 它是否没有反复折腾（例如不必要的命令或过度的 token 消耗）就完成了？

保持这个清单简短，聚焦于必须通过的检查。目标不是预先编码每一个偏好，而是捕捉你最关心的行为。

以本文为例，指南评估的是一个搭建演示应用的技能。一些检查是具体的：它执行了 `npm install` 吗？它创建了 `package.json` 吗？指南将这些与结构化的风格评分标准配对，以评估约定和布局。

这种混合是有意为之的。你需要的是快速、有针对性的信号来尽早暴露特定的回归，而不是最后只有一个通过/失败的判决。

## 2. 创建技能

Codex 技能是一个包含 `SKILL.md` 文件的目录，该文件包括 YAML 前置元数据（`name`、`description`），后面是定义技能行为的 Markdown 指令，以及可选的资源和脚本。名称和描述比看起来更重要。它们是 Codex 用来决定**是否**调用该技能以及**何时**将 `SKILL.md` 的其余部分注入智能体上下文的主要信号。如果这些内容模糊或过载，技能将无法可靠地触发。

最快的入门方式是使用 Codex 内置的技能创建器（[它本身也是一个技能](https://github.com/openai/skills/tree/main/skills/.system/skill-creator)）。它会引导你完成：

```
$skill-creator
```

创建器会问你技能做什么、何时触发、是纯指令型还是脚本支持型（默认推荐纯指令型）。要了解更多关于创建技能的信息，[请查看文档](https://developers.openai.com/codex/skills#create-a-skill)。

### 示例技能

本文使用了一个刻意简化的示例：一个以可预测、可重复的方式搭建小型 React 演示应用的技能。

这个技能将：
- 使用 Vite 的 React + TypeScript 模板搭建项目
- 使用官方 Vite 插件方式配置 Tailwind CSS
- 强制执行一个最小的、一致的文件结构
- 定义明确的"完成定义"，使成功易于评估

以下是一个简洁的草稿，你可以粘贴到：
- `.codex/skills/setup-demo-app/SKILL.md`（仓库级），或
- `~/.codex/skills/setup-demo-app/SKILL.md`（用户级）。

```markdown
---
name: setup-demo-app
description: 搭建一个 Vite + React + Tailwind 演示应用，具有小型且一致的项目结构。
---

## 何时使用

当你需要一个全新的演示应用来进行快速 UI 实验或问题复现时使用。

## 构建内容

创建一个 Vite React TypeScript 应用并配置 Tailwind。保持最小化。

搭建后的项目结构：

- src/
  - main.tsx（入口）
  - App.tsx（根 UI）
  - components/
    - Header.tsx
    - Card.tsx
  - index.css（Tailwind 导入）
- index.html
- package.json

风格要求：

- TypeScript 组件
- 仅使用函数式组件
- 使用 Tailwind 类进行样式设置（不用 CSS modules）
- 不使用额外的 UI 库

## 步骤

1. 使用 Vite 的 React TS 模板搭建：
   npm create vite@latest demo-app -- --template react-ts

2. 安装依赖：
   cd demo-app
   npm install

3. 使用 Vite 插件安装和配置 Tailwind。
   - npm install tailwindcss @tailwindcss/vite
   - 将 tailwind 插件添加到 vite.config.ts
   - 在 src/index.css 中，将内容替换为：
     @import "tailwindcss";

4. 实现最小化 UI：
   - Header：应用标题和简短副标题
   - Card：可复用的卡片容器
   - App：渲染 Header + 2 个带占位文本的 Card

## 完成定义

- npm run dev 成功启动
- package.json 存在
- src/components/Header.tsx 和 src/components/Card.tsx 存在
```

这个示例技能故意采用了明确的立场。没有清晰的约束，就没有具体的东西可以评估。

## 3. 手动触发技能以暴露隐含假设

由于技能的调用在很大程度上取决于 `SKILL.md` 中的 `name` 和 `description`，首先要检查的是 `setup-demo-app` 技能是否在你预期的时候触发。

早期阶段，在一个真实的仓库或临时目录中显式激活技能——通过 `/skills` 斜杠命令或用 `$` 前缀引用它——然后观察它在哪里出问题。这就是你暴露遗漏的地方：技能完全没有触发的情况、触发过于积极的情况，或者运行了但偏离预期步骤的情况。

在这个阶段，你不是在优化速度或完善度。你是在寻找技能正在做出的隐含假设，例如：

- **触发假设**：像"搭建一个快速 React 演示"这样的提示词*应该*调用 `setup-demo-app` 但实际没有，或者更通用的提示词（"添加 Tailwind 样式"）无意中触发了它。
- **环境假设**：技能假设它在一个空目录中运行，或者假设 `npm` 可用且被偏好使用。
- **执行假设**：智能体跳过了 `npm install` 因为它假设依赖已安装，或者在 Vite 项目创建之前就配置了 Tailwind。

当你准备好让这些运行可重复时，切换到 `codex exec`。它是为自动化和 CI 设计的：将进度流式输出到 `stderr`，仅将最终结果写入 `stdout`，这使得运行更易于脚本化、捕获和检查。

默认情况下，`codex exec` 在受限沙箱中运行。如果你的任务需要写入文件，使用 `--full-auto` 运行。一般原则是，尤其在自动化时，使用完成任务所需的最小权限。

一个基本的手动运行可能如下：

```bash
codex exec --full-auto \
  '使用 $setup-demo-app 技能在此目录中创建项目。'
```

这第一次动手尝试与其说是验证正确性，不如说是发现边界情况。你在这里做的每一个手动修复——添加缺失的 `npm install`、修正 Tailwind 配置、收紧触发描述——都是未来 eval 的候选项，这样你就能在大规模评估之前锁定预期行为。

## 4. 使用小型、有针对性的 prompt 集来尽早捕获回归

你不需要一个大型基准测试集就能从 evals 中获得价值。对于单个技能，10-20 个 prompt 的小集合就足以尽早暴露回归并确认改进。

从一个小 CSV 开始，随着你在开发或使用过程中遇到真实的失败逐渐扩展。每一行应代表你关心 `setup-demo-app` 技能**是否**激活的情境，以及当它激活时成功是什么样子。

例如，一个初始的 `evals/setup-demo-app.prompts.csv` 可能如下：

```csv
id,should_trigger,prompt
test-01,true,"使用 $setup-demo-app 技能创建一个名为 `devday-demo` 的演示应用"
test-02,true,"搭建一个带 Tailwind 的最小化 React 演示应用，用于快速 UI 实验"
test-03,true,"创建一个小型演示应用来展示 Responses API"
test-04,false,"给我现有的 React 应用添加 Tailwind 样式"
```

每个测试用例测试的内容略有不同：

**显式调用（test-01）**：这个 prompt 直接点名了技能。它确保 Codex 在被要求时能调用 `setup-demo-app`，并且技能名称、描述或指令的更改不会破坏直接使用。

**隐式调用（test-02）**：这个 prompt *精确*描述了技能所针对的场景——搭建一个最小化的 React + Tailwind 演示——但没有提到技能的名字。它测试 `SKILL.md` 中的名称和描述是否足够强，使 Codex 能自行选择该技能。

**上下文调用（test-03）**：这个 prompt 添加了领域上下文（Responses API），但仍然需要相同的底层搭建。它检查技能在真实的、略带噪声的 prompt 中是否能触发，以及生成的应用是否仍然符合预期的结构和约定。

**负控制（test-04）**：这个 prompt *不应该*调用 `setup-demo-app`。它是一个常见的相邻请求（"给现有应用添加 Tailwind"），可能会无意中匹配技能的描述（"React + Tailwind 演示"）。包含至少一个 `should_trigger=false` 的用例有助于捕获**假阳性**——Codex 过于积极地选择技能，在用户想要对现有项目做增量修改时搭建了一个新项目。

这种混合是有意为之的。一些 evals 应该确认技能在显式调用时行为正确；另一些应该检查它在用户根本没提到技能名字的真实世界 prompt 中是否能激活。

当你发现遗漏——未能触发技能的 prompt，或输出偏离你预期的情况——将它们作为新行添加。随着时间推移，这个小 CSV 会成为 `setup-demo-app` 技能必须持续正确处理的场景的活文档。

## 5. 从轻量级确定性评分器开始

这是评估步骤的核心：使用 `codex exec --json`，让你的 eval 框架能对**实际发生的事情**评分，而不仅仅是最终输出看起来是否正确。

当你启用 `--json` 时，`stdout` 变成一个 JSONL 结构化事件流。这使得编写与你关心的行为直接相关的确定性检查变得很简单，例如：

- 它执行了 `npm install` 吗？
- 它创建了 `package.json` 吗？
- 它按预期顺序调用了预期的命令吗？

这些检查是故意轻量的。它们在你添加任何基于模型的评分之前，就给你快速、可解释的信号。

### 最小化的 Node.js 运行器

一个"足够好"的方案如下：

1. 对每个 prompt，运行 `codex exec --json --full-auto "<prompt>"`
2. 将 JSONL trace 保存到磁盘
3. 解析 trace 并对事件运行确定性检查

```javascript
// evals/run-setup-demo-app-evals.mjs
import { spawnSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import path from "node:path";

function runCodex(prompt, outJsonlPath) {
  const res = spawnSync(
    "codex",
    [
      "exec",
      "--json", // 必需：输出结构化事件
      "--full-auto", // 允许文件系统更改
      prompt,
    ],
    { encoding: "utf8" }
  );

  mkdirSync(path.dirname(outJsonlPath), { recursive: true });

  // 启用 --json 时 stdout 是 JSONL
  writeFileSync(outJsonlPath, res.stdout, "utf8");

  return { exitCode: res.status ?? 1, stderr: res.stderr };
}

function parseJsonl(jsonlText) {
  return jsonlText
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

// 确定性检查：智能体是否运行了 `npm install`？
function checkRanNpmInstall(events) {
  return events.some(
    (e) =>
      (e.type === "item.started" || e.type === "item.completed") &&
      e.item?.type === "command_execution" &&
      typeof e.item?.command === "string" &&
      e.item.command.includes("npm install")
  );
}

// 确定性检查：`package.json` 是否被创建？
function checkPackageJsonExists(projectDir) {
  return existsSync(path.join(projectDir, "package.json"));
}

// 示例单案例运行
const projectDir = process.cwd();
const tracePath = path.join(projectDir, "evals", "artifacts", "test-01.jsonl");

const prompt =
  "使用 $setup-demo-app 技能创建一个名为 demo-app 的演示应用";

runCodex(prompt, tracePath);

const events = parseJsonl(readFileSync(tracePath, "utf8"));

console.log({
  ranNpmInstall: checkRanNpmInstall(events),
  hasPackageJson: checkPackageJsonExists(path.join(projectDir, "demo-app")),
});
```

这里的价值在于一切都是**确定性的且可调试的**。

如果一个检查失败，你可以打开 JSONL 文件查看确切发生了什么。每个命令执行都按顺序作为 `item.*` 事件出现。这使得回归可以直接解释和修复——这正是你在这个阶段想要的。

## 6. 使用 Codex 和基于评分标准的打分进行定性检查

确定性检查回答了**"它做了基本的事情吗？"**，但没有回答**"它是按你想要的方式做的吗？"**

对于像 `setup-demo-app` 这样的技能，许多需求是定性的：组件结构、样式约定，或者 Tailwind 是否遵循了预期的配置方式。这些很难仅通过基本的文件存在性检查或命令计数来捕获。

一个务实的解决方案是在你的 eval 流水线中添加第二个模型辅助的步骤：

1. 运行搭建技能（这会将代码写入磁盘）
2. 对生成的仓库运行一个**只读的风格检查**
3. 要求一个**结构化响应**，使你的框架能一致地评分

Codex 通过 `--output-schema` 直接支持这一点，它将最终响应约束为你定义的 JSON Schema。

### 小型评分标准 Schema

首先定义一个小 schema 来捕获你关心的检查。例如，创建 `evals/style-rubric.schema.json`：

```json
{
  "type": "object",
  "properties": {
    "overall_pass": { "type": "boolean" },
    "score": { "type": "integer", "minimum": 0, "maximum": 100 },
    "checks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "pass": { "type": "boolean" },
          "notes": { "type": "string" }
        },
        "required": ["id", "pass", "notes"],
        "additionalProperties": false
      }
    }
  },
  "required": ["overall_pass", "score", "checks"],
  "additionalProperties": false
}
```

这个 schema 给你提供了稳定的字段（`overall_pass`、`score`、每项检查结果），你可以在多次运行中组合、对比和追踪。

### 风格检查 prompt

接下来，运行第二次 `codex exec`，**仅检查仓库**并输出符合评分标准的 JSON 响应：

```bash
codex exec \
  "根据以下要求评估 demo-app 仓库：
   - 存在 Vite + React + TypeScript 项目
   - Tailwind 通过 @tailwindcss/vite 配置，CSS 导入了 tailwindcss
   - src/components 包含 Header.tsx 和 Card.tsx
   - 组件是函数式的，使用 Tailwind 工具类样式（无 CSS modules）
   以 JSON 返回评分标准结果，检查项 id 为：vite, tailwind, structure, style。" \
  --output-schema ./evals/style-rubric.schema.json \
  -o ./evals/artifacts/test-01.style.json
```

这就是 `--output-schema` 派上用场的地方。你得到的不是难以解析或比较的自由格式文本，而是一个可预测的 JSON 对象，你的 eval 框架可以跨多次运行进行评分。

如果你后续将这套 eval 迁移到 CI 中，Codex GitHub Action 明确支持通过 `codex-args` 传递 `--output-schema`，这样你就能在自动化工作流中强制执行相同的结构化输出。

## 7. 随着技能成熟扩展你的 evals

一旦核心循环到位，你就可以沿着对你的技能最重要的方向扩展 evals。从小处着手，只在能真正增加信心的地方加入更深层的检查。

一些示例包括：

- **命令计数和反复折腾：** 计算 JSONL trace 中的 `command_execution` 项目数，以捕获智能体开始循环或重复运行命令的回归。Token 使用量也可在 `turn.completed` 事件中获得。
- **Token 预算：** 追踪 `usage.input_tokens` 和 `usage.output_tokens`，以发现意外的 prompt 膨胀并比较不同版本间的效率。
- **构建检查：** 在技能完成后运行 `npm run build`。这是一个更强的端到端信号，可以捕获损坏的导入或配置不正确的工具。
- **运行时烟雾测试：** 启动 `npm run dev` 并用 `curl` 访问开发服务器，或者如果你已经有轻量级 Playwright 检查就运行它。选择性使用——它增加信心但消耗时间。
- **仓库清洁度：** 确保运行没有生成不需要的文件，且 `git status --porcelain` 为空（或匹配一个明确的允许列表）。
- **沙箱和权限回归：** 验证技能在不超出你预期权限的情况下仍然可用。最小权限默认值在自动化时尤为重要。

模式是一致的：从解释行为的快速检查开始，只在能降低风险的地方添加更慢、更重的检查。

## 8. 核心要点

这个小小的 `setup-demo-app` 示例展示了从"感觉更好了"到"有证据"的转变：运行智能体，记录发生了什么，用一小组检查来评分。一旦这个循环建立起来，每次调整都更容易确认，每次回归都一目了然。以下是核心要点：

- **衡量重要的事情。** 好的 evals 让回归清晰可见，让失败可以解释。
- **从可检查的完成定义开始。** 使用 `$skill-creator` 引导创建，然后收紧指令直到成功标准毫无歧义。
- **将 evals 锚定在行为上。** 用 `codex exec --json` 捕获 JSONL，针对 `command_execution` 事件编写确定性检查。
- **在规则不足时使用 Codex。** 添加一个结构化的、基于评分标准的评估环节，用 `--output-schema` 可靠地评分风格和约定。
- **让真实的失败驱动覆盖率。** 每次手动修复都是一个信号。把它变成一个测试，让技能持续做对。
