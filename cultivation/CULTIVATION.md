# Cultivation — 个人修行

本模块用于沉淀个人修行中的原则、练习、体悟与阶段复盘。它关注“我如何实践并发生改变”，而不是单纯收藏经典、课程或他人观点。

## 目录结构

```text
cultivation/
├── CULTIVATION.md      # 模块入口、使用方法与边界
└── cultivation.jsonl  # 修行主题与练习索引
```

出现稳定内容后，可按需增加：

```text
cultivation/
├── practices/          # 已采用的具体练习及操作说明
├── reflections/        # 专题体悟与阶段性复盘
└── traditions/         # 儒、释、道等体系的个人理解与比较
```

不要为了预设分类而创建空目录；有第一份真实内容时再建立。

## 内容边界

### 放入 cultivation/

- 已准备实践或正在实践的修行方法
- 对自身习性、注意力、情绪、欲望和价值选择的观察
- 经过个人消化后的修行原则与框架
- 一段时间内的修习复盘、变化与问题
- 不同传统对同一实践问题的比较

### 不放入 cultivation/

- 书籍、讲座、论文原文及客观精读笔记：进入 `sources/` 后路由到相应领域
- 某位投研作者的原始内容：保留在 `investment/{作者}/`
- 日常生活流水账：放入 `weekly-review/`
- 长期身份、价值观和表达风格：放入 `identity/`
- 有明确截止时间的行动项：放入 `operations/tasks/`

## 数据格式

`cultivation.jsonl` 一行一条记录，只追加、不删除。ID 使用 `cult-XXX`。

```json
{
  "id": "cult-001",
  "title": "练习或修行主题",
  "type": "practice",
  "tradition": ["儒家"],
  "status": "candidate",
  "source_refs": ["relative/path/to/notes.md"],
  "tags": ["注意力", "反思"],
  "created_at": "YYYY-MM-DD",
  "last_practiced_at": "",
  "notes": "为什么要练、如何判断是否有效"
}
```

字段说明：

| 字段 | 含义 |
|---|---|
| `id` | 唯一编号，格式为 `cult-XXX` |
| `title` | 练习或主题名称 |
| `type` | `practice`、`principle`、`reflection`、`question` |
| `tradition` | 思想或修行传统，可多选；不确定时留空数组 |
| `status` | `candidate`、`active`、`paused`、`integrated` |
| `source_refs` | 原始材料或精读笔记的仓库相对路径 |
| `tags` | 跨模块统一标签 |
| `created_at` | 首次登记日期，`YYYY-MM-DD` |
| `last_practiced_at` | 最近实践日期，未开始时为空 |
| `notes` | 实践目的、方法、观察标准或简短结论 |

## 工作流

### 1. 来源进入系统

经典、文章、讲座或播客先通过 `sources/` 注册，并按来源作者或真实领域保存。来源中的观点不自动成为个人原则。

### 2. 转化为候选练习

只有当某个观点可以回答以下问题时，才登记到 `cultivation.jsonl`：

- 我准备具体做什么？
- 在什么情境、以什么频率做？
- 我如何观察它是否有帮助或副作用？

初始状态使用 `candidate`。

### 3. 实践与记录

开始实践后改为 `active`。日常简短记录可留在周记，并引用 `cult-XXX`；只有形成可复用的理解时，才在 `reflections/` 写专题复盘。

### 4. 阶段复盘

- 暂时停止：`paused`
- 已内化成稳定习惯或原则：`integrated`
- 原有判断变化：追加新记录或专题复盘，不删除历史记录

## 与其他模块的关系

- **sources → cultivation**：外部材料提供候选方法，但必须经过个人判断与实践。
- **investment → cultivation**：卢麒元等作者的原文与精读笔记保留在作者库，修行模块只建立引用和实践记录。
- **cultivation → weekly-review**：周记记录本周是否实践、出现了什么体验。
- **cultivation → identity**：经过长期验证并稳定内化的原则，才可能更新个人价值观。
- **cultivation → operations**：需要定时执行的练习，可拆成任务或目标；这里保留方法与反思，不承担提醒功能。

## 使用约定

- 区分“作者主张”“经典原文”“我的理解”“我的实际体验”。
- 宗教、哲学、心理学和科学性主张分别标注，不把隐喻当作实证事实。
- 不以单次强烈体验替代长期观察。
- 涉及心理或身体健康风险时，修行记录不能替代专业医疗建议。
- 以是否改善觉察、行动、关系和稳定性作为实践评价，而不是追求神秘体验。

## 当前入口

- `cult-001`：中庸修习“止定静安虑得”，来源于卢麒元《中庸》第26讲，当前为候选练习。
