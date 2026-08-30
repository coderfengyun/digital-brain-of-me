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

## Scripts

All scripts live in `.Codex/skills/investment/scripts/`:

- `write_trade_journal.py` — 交易日志写入工具（添加/导入/迁移/校验）
- `fetch_binance_trades.py` — 币安交易记录获取
- `fetch_binance_balances.py` — 币安账户全部资产余额及 USD 估值
- `fetch_futu_trades.py` — 富途交易记录获取
- `fetch_futu_positions.py` — 富途账户持仓及资金概览
- `fetch_cms_trades.py` — 招商证券交易记录获取（Chrome MCP）
- `calc_pnl.py` — 盈亏计算（FIFO 匹配）

---

## 交易日志操作

### 添加单条记录

```bash
python .Codex/skills/investment/scripts/write_trade_journal.py add \
  --品种 BTC --操作 买入 --价格 76653 --数量 0.00391 --金额 299.71 \
  --币种 USD --日期 2025-04-07 --交易平台 币安 --备注 "币安API精确数据"
```

必填：`--品种`、`--操作`、`--价格`、`--数量`、`--金额`、`--币种`、`--日期`。可选：`--交易平台`（注意不是 `--平台`）、`--日期精确度`、`--备注`。完整参数见 `add --help`。

### 批量更新交易记录

当用户说"更新交易记录"时，按顺序拉取三个平台（币安 → 富途 → 招商证券）。详细步骤见 [`references/trade-import.md`](references/trade-import.md)。

### 工具命令

| 操作 | 命令 |
|------|------|
| 校验数据 | `python3 .Codex/skills/investment/scripts/write_trade_journal.py validate` |
| 盈亏计算 | `python3 .Codex/skills/investment/scripts/calc_pnl.py` |
| 运行测试 | `cd .Codex/skills/investment/scripts && python3 -m pytest -v` |

---

## 投研内容管理

每位长期跟踪的作者在 `investment/` 下有独立目录，以 `{作者名}.md` 为索引。索引文件汇聚该作者在整个 repo 中的全部内容（研究文章、OCR 转换、podcast 转录、原始发言等），是查找某位作者观点的唯一入口。

**现有作者索引**：
- [`洪灏/洪灏.md`](../../../investment/洪灏/洪灏.md) — 宏观分析、地缘-能源-通胀传导、黄金/美元结构性分析
- [`卢麒元/卢麒元.md`](../../../investment/卢麒元/卢麒元.md) — 马克思资本论框架、货币体系、资产配置三三四原则

**新建作者索引时**：
1. 在 `investment/{作者名}/` 下创建 `{作者名}.md`
2. 开头用 blockquote 简述身份、分析风格、核心关注领域
3. 按内容类型分节（Podcast 转录 / 研究文章 / 投资研究 / 一手发言等），用相对路径链接到实际文件
4. 附"关键观点速查"表格（主题 / 观点 / 出处）
5. 更新本 skill 的"现有作者索引"列表

**向已有作者添加新内容时**：
1. 内容文件放到该作者目录下
2. 更新该作者的索引文件，添加链接
3. 判断是否更新"关键观点速查"表：只有**新的分析框架、新指标、或与已有观点矛盾/显著升级的判断**才追加；已有观点的重复验证或应用实例不追加

### 获取微博研报（端到端 pipeline）

当用户要求获取洪灏最新或指定的微博研报时，必须先完整阅读并执行 [`references/weibo-report.md`](references/weibo-report.md)。该流程涵盖选帖、正文与原图保存、OCR 校对、结构化笔记、来源注册和作者索引更新；用户明确只下载时按 Reference 中的范围规则停止。
