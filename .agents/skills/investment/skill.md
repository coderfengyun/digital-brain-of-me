---
name: investment
description: "投资交易日志、盈亏计算、券商导入、投研作者管理。触发场景：交易记录（'交易记录', '更新交易', '导入交易'）；盈亏与持仓（'盈亏', '算算收益', '持仓', '仓位', 'P&L'）；券商（'币安', '富途', '招商证券', 'Binance', 'Futu'）；投研作者——提到 '洪灏'/'洪浩'/'卢麒元' 任何上下文都触发（读文章、讨论观点、更新索引、增加/追加发言或内容——即使操作看似简单也必须触发，因为有索引更新步骤）；研报（'研报', '微博研报', '下载微博', '最新文章'）；微博VIP群发言记录。Note: image OCR is handled by the standalone 'ocr' skill."
---

# Investment

交易日志管理 + 投研内容管理。

## Data Location

- 交易日志：`investment/投资日志整理/交易日志汇总表.csv`
- CSV Schema：`investment/投资日志整理/交易日志汇总表.schema.json`
- 投研作者索引：`investment/{作者名}/{作者名}.md`
- 设计文档：`investment/投资日志整理/DESIGN_盈亏统计系统设计.md`

## 交易日志操作

### 添加单条记录

```bash
python .codex/skills/investment/scripts/write_trade_journal.py add \
  --品种 BTC --代码 BTCUSDT --操作 买入 --价格 76653 --数量 0.00391 --金额 299.71 \
  --币种 USD --日期 2025-04-07 --交易平台 币安
```

必填：`--品种`、`--操作`、`--价格`、`--数量`、`--金额`、`--币种`、`--日期`。可选：`--代码`（资产唯一标识，如 US.SLV, HK.00883, 512400, BTCUSDT）、`--交易平台`（注意不是 `--平台`）、`--日期精确度`、`--备注`。完整参数见 `add --help`。

### 批量更新交易记录

当用户说"更新交易记录"时，按顺序拉取三个平台（币安 → 富途 → 招商证券）。详细步骤见 [`references/trade-import.md`](references/trade-import.md)。

### 工具命令

| 操作 | 命令 |
|------|------|
| 校验数据 | `python3 .codex/skills/investment/scripts/write_trade_journal.py validate` |
| 盈亏计算 | `python3 .codex/skills/investment/scripts/calc_pnl.py` |
| 运行测试 | `cd .codex/skills/investment/scripts && python3 -m pytest -v` |

---

## 投研内容管理

每位长期跟踪的作者在 `investment/` 下有独立目录，以 `{作者名}.md` 为索引。索引文件汇聚该作者在整个 repo 中的全部内容（研究文章、OCR 转换、podcast 转录、原始发言等），是查找某位作者观点的唯一入口。

**现有作者索引**：
- [`洪灏/洪灏.md`](../../../investment/洪灏/洪灏.md) — 宏观分析、地缘-能源-通胀传导、黄金/美元结构性分析
- [`卢麒元/卢麒元.md`](../../../investment/卢麒元/卢麒元.md) — 马克思资本论框架、货币体系、资产配置三三四原则
- [`Medi_and_莎姐/Medi_and_莎姐.md`](../../../investment/Medi_and_莎姐/Medi_and_莎姐.md) — 加密资产市场结构、流动性计算、多时间框架与仓位管理

**新建作者索引时**：
1. 在 `investment/{作者名}/` 下创建 `{作者名}.md`
2. 开头用 blockquote 简述身份、分析风格、核心关注领域
3. 按内容类型分节（Podcast 转录 / 研究文章 / 投资研究 / 一手发言等），用相对路径链接到实际文件
4. 附"关键观点速查"表格（主题 / 观点 / 出处）
5. 更新本 skill 的"现有作者索引"列表

**内容文件夹命名规则**：`YYYYMMDD-标题`（发布日期前缀），例如 `20260606-港股指数开始AI化`。同一天多篇追加字母：`20260519a-全球债券收益率飙升`、`20260519b-香港劲揪`。这样文件系统按字母排序即为时间线，且插入历史内容不影响已有文件夹名。

**向已有作者添加新内容时**：
1. 按命名规则创建文件夹，获取/保存原文为 `article.md`
2. **触发 paper-reading 全流程**：
   - 非中文文章 → 生成中文翻译 `article-zh.md`
   - 按 paper-reading skill Phase 1-3 生成精读笔记 `notes.md`
   - 注册到 `sources/sources.jsonl`（分配 ID、填写 output 路径）
3. 更新该作者的索引文件，添加链接（含翻译和笔记链接）
4. 判断是否更新"关键观点速查"表：只有**新的分析框架、新指标、或与已有观点矛盾/显著升级的判断**才追加；已有观点的重复验证或应用实例不追加

### 获取洪灏的微博研报（端到端 pipeline）

当用户要求获取洪灏最新或指定的微博研报时，必须先完整阅读并执行 [`references/weibo-report.md`](references/weibo-report.md)。该流程涵盖选帖、正文与原图保存、OCR 校对、结构化笔记、来源注册和作者索引更新；用户明确只下载时按 Reference 中的范围规则停止。

### 获取洪灏的微博视频投研内容

当用户分享洪灏的微博视频链接，或 `take_snapshot` 发现洪灏的微博帖子是视频（有"播放视频"按钮）而非图文时：

1. 点击"播放视频" → `list_network_requests(resourceTypes=["media"])` 获取 `.mp4` URL → `curl -L -H "Referer: https://weibo.com/"` 下载到 `investment/洪灏/{主题}/video.mp4`
2. 触发 `transcribe` skill 对 `video.mp4` 进行转录（输出到同一目录）
3. 基于转录内容直接生成精读笔记 `notes-YYYYMMDD.md`（不询问用户）
4. 更新作者索引，按规则判断是否更新"关键观点速查"表
5. 清理 `video.mp4`

### 更新洪灏的知识星球帖子

当用户要求更新、续读或获取洪灏在知识星球「洪灏的宏观策略」发表的帖子时，必须先完整阅读并执行 [`references/zsxq-posts.md`](references/zsxq-posts.md)。该流程从本地索引中最近一次已读帖子处续读，直到页面最新一条。

### 获取卢麒元的微博 VIP 群发言

当用户要求更新卢麒元在微博 VIP 群中的发言，或从上次记录继续收集群主文字消息时，必须先完整阅读并执行 [`references/weibo-vip-chat.md`](references/weibo-vip-chat.md)。该流程包含固定群聊与发言人、断点回溯、文字消息筛选、原文写入和作者索引更新规则。

### 获取 Medi 或莎姐的微信群发言

当用户要求从微信群「Satoshi Coffeehouse」提取、搜索或续更 Medi（群昵称 `Mercator Moderatus`）或莎姐（群昵称 `中本莎`）的历史发言时，必须先完整阅读并执行 [`references/wechat-group-search.md`](references/wechat-group-search.md)。该流程包含按群成员筛选、日期换算、断点续更、投资内容筛选、原文与翻译保存、笔记生成、来源注册和作者索引更新规则。
