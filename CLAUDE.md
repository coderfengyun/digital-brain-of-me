# Digital Brain — 请求处理协议

本文件是 Claude 处理用户请求的协议。结构按消费频率排列：路由（每次请求查）→ 约束（始终生效）→ 环境（偶尔参考）→ 参考文档索引。

---

## 路由

用户请求涉及数据操作时，直接读取对应模块入口文件了解格式和操作方式：

| 请求类型 | 入口文件 |
|---------|---------|
| 内容创作（写文章、post） | 先读 `identity/voice/style.md`，再看 `content/CONTENT.md` |
| 内容创意 | 运行 `scripts/content_ideas.py` 或读 `content/ideas/ideas.jsonl` |
| 书签/链接保存 | `knowledge/KNOWLEDGE.md` |
| 任务管理 | `operations/OPERATIONS.md` |
| 目标跟踪 | `operations/goals/goals.yaml` |
| 周记/周报 | `weekly-review/WEEKLY-REVIEW.md` |
| 添加外部来源（论文/文章/研报/播客） | `sources/SOURCES.md`（注册后路由到对应 skill，输出到领域目录） |
| 探索性项目/技术实验 | `labs/`（每个子目录一个独立探索，含 README） |

**关键规则**：内容创作类任务必须先读 `identity/voice/style.md` 再动笔。

---

## 约束

以下规则无论路由到哪个模块都始终生效。

### 语言

- 用户用中文交流，用中文回复

### 权限

- Allow all file read/write/edit operations within this project
- 当用户提供 web URL 或需要将网页内容转成 Markdown，统一使用 Chrome MCP（navigate_page + take_snapshot），不使用 WebFetch 或 agent-browser

### 格式约定

- 流程图只保存 Mermaid 源代码（.mmd 文件），不保存生成的图片
- JSONL 文件：一行一个 JSON 对象，只追加不删除
- 唯一 ID 格式：`type-XXX`（如 `idea-001`, `paper-YYYYMMDD-XXX`）；weekly-review 文件用 `YYYY-MM-DD~MM-DD.md` 命名
- 跨模块保持一致的 tagging 以便发现关联

### 操作纪律

**DON'T:**
- 删除 JSONL 文件中的条目
- 不读就写（覆盖已有数据前必须先读）
- 不读 voice.md 就生成内容
- 修改 template 条目
- 移动/重命名文件前不搜索引用

**DO:**
- 修改数据时更新 timestamp
- 移动/重命名文件前 `grep -r "filename"` 搜索并更新所有引用
- 数字脑操作失败时，优先修复相关模块的设计/指令

---

## 环境

### 依赖管理

项目所有依赖通过 `bash setup.sh` 一键安装（幂等、可重跑）。

| 层级 | 管理方式 | 配置文件 |
|------|---------|---------|
| Python 包 | uv | `pyproject.toml` + `uv.lock` |
| Node.js 包 | npm | `package.json` |
| 系统工具 | brew / apt | `setup.sh` 中声明 |
| 模型文件 | curl 下载 | `setup.sh` 中声明 |

### 日常操作

- 执行 Python 脚本：`uv run <script.py>`（不使用系统 `python3`）
- 新增 Python 依赖：`uv add <package>`
- 新增系统工具依赖：在 `setup.sh` 的"系统工具"段落添加检测+安装逻辑

---

## 参考文档

以下文档记录系统的设计理念和方法论，不是每次请求都需要读，但在做架构决策或理解系统设计意图时应参考：

| 文档 | 内容 |
|------|------|
| [the-file-system-is-the-new-database.md](the-file-system-is-the-new-database.md) | 系统设计哲学：context engineering、progressive disclosure、data/skill separation 等核心原则 |
| [multi-component-design.md](multi-component-design.md) | 多组件协作设计方法论：协作方式 → 反推组件要求 → 验证可行性 → 识别缺口。涉及多组件集成的任务时读此文档 |
