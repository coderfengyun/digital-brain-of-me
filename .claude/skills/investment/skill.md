---
name: investment
description: "Investment trade journal, P&L calculation, broker imports, and research content management. Use when: user wants to add/import/update trade records, calculate profit/loss, fetch trades from brokers (Binance, Futu, CMS/招商证券), or manage investment research authors. Trigger on phrases like '交易记录', 'investment', '盈亏', 'add trade', 'import trades', '更新交易记录', 'P&L', '导入交易', '币安', '富途', '招商证券'. Use this skill even for partial matches like asking about specific assets (BTC, gold, oil) in a trading context. Note: image OCR is handled by the standalone 'ocr' skill."
---

# Investment

交易日志管理 + 投研内容管理。

## Data Location

- 交易日志：`investment/投资日志整理/交易日志汇总表.csv`
- CSV Schema：`investment/投资日志整理/交易日志汇总表.schema.json`
- 投研作者索引：`investment/{作者名}/{作者名}.md`
- 设计文档：`investment/投资日志整理/DESIGN_盈亏统计系统设计.md`

## Scripts

All scripts live in `.claude/skills/investment/scripts/`:

- `write_trade_journal.py` — 交易日志写入工具（添加/导入/迁移/校验）
- `fetch_binance_trades.py` — 币安交易记录获取
- `fetch_binance_balances.py` — 币安账户全部资产余额及 USD 估值
- `fetch_futu_trades.py` — 富途交易记录获取
- `fetch_futu_positions.py` — 富途账户持仓及资金概览
- `fetch_cms_trades.py` — 招商证券交易记录获取（Chrome MCP）
- `calc_pnl.py` — 盈亏计算（FIFO 匹配）

---

## 交易日志操作

### 添加交易记录

```bash
python .claude/skills/investment/scripts/write_trade_journal.py add \
  --品种 BTC --操作 买入 --价格 76653 --数量 0.00391 --金额 299.71 \
  --币种 USD --日期 2025-04-07 --交易平台 币安 --备注 "币安API精确数据"
```

完整参数列表（`add --help`）：
- `--品种`、`--操作`、`--价格`、`--数量`、`--金额`、`--币种`、`--日期` — 必填
- `--交易平台` — 可选，注意**不是** `--平台`
- `--日期精确度` — 可选，默认 `精确`
- `--备注` — 可选

### 从币安导入

```bash
# 1. 获取币安交易记录
python .claude/skills/investment/scripts/fetch_binance_trades.py \
  --start 2025-04-01 --end 2025-10-31 -o /tmp/binance_trades.csv

# 2. 导入到交易日志
python .claude/skills/investment/scripts/write_trade_journal.py import-binance /tmp/binance_trades.csv
```

### 从招商证券导入（Chrome MCP）

需要 Chrome MCP 连接到已登录的招商证券网页交易页面。完整步骤：

**前置条件**：
- Chrome 以 `--remote-debugging-port=9222` 启动
- Chrome MCP 已连接（`claude mcp list` 显示 ✓）
- 浏览器已登录招商证券

**历史成交页面 URL**（必须含 `/npctrade` 路径前缀）：
```
https://xtrade.newone.com.cn/npctrade#/trade/ptjy/cx?page=lscj
```

**步骤**：

```bash
# Step 1: 使用 chrome-devtools navigate_page 导航到上述 URL（timeout: 60000）

# Step 2: 用 fetch_cms_trades.py 生成提取数据的 JS
python .claude/skills/investment/scripts/fetch_cms_trades.py js \
  --start 2026-03-03 --end 2026-03-28

# Step 3: 通过 chrome-devtools evaluate_script 执行该 JS，获取 JSON 结果

# Step 4: 将 JSON 保存到文件并转为 CSV
python .claude/skills/investment/scripts/fetch_cms_trades.py convert \
  --json-file /tmp/cms_raw.json -o /tmp/cms_trades.csv

# Step 5: 导入到交易日志
python .claude/skills/investment/scripts/write_trade_journal.py import-cms /tmp/cms_trades.csv
```

> **注意**：如果数据量只有几条且已存在于日志中，可以跳过 Step 4-5，直接确认无新记录即可。

### 批量更新交易记录

当用户说"更新交易记录"时：

**Step 0**：用 `tail -1 investment/投资日志整理/交易日志汇总表.csv` 确定最后记录日期，次日作为起始日期。

**Step 1：币安**（API）
```bash
# 不要用 --all（400+ 交易对会触发限速），指定近期活跃品种
python3 .claude/skills/investment/scripts/fetch_binance_trades.py --start DATE --end TODAY \
  --symbol BTCUSDT XRPUSDT ETHUSDT SOLUSDT ZBTUSDT -o /tmp/binance.csv
python3 .claude/skills/investment/scripts/write_trade_journal.py import-binance /tmp/binance.csv
```
> 如果 import 因金额偏差 >1% 跳过记录（手续费导致），用 `add` 手动添加。

**Step 2：富途**（需 FutuOpenD 运行，端口 11111；连接被拒绝则跳过）
```bash
python3 .claude/skills/investment/scripts/fetch_futu_trades.py --start DATE --end TODAY -o /tmp/futu.csv
# 无 import-futu 子命令，有新记录时用 add 逐条添加
```

**Step 3：招商证券**（Chrome MCP，需浏览器已登录）
```bash
# 1. navigate_page → https://xtrade.newone.com.cn/npctrade#/trade/ptjy/cx?page=lscj (timeout: 60000)
# 2. 生成+执行 JS
python3 .claude/skills/investment/scripts/fetch_cms_trades.py js --start DATE --end TODAY
# 3. evaluate_script 执行 JS，获取 JSON
# 4. 有新记录则 convert + import-cms
python3 .claude/skills/investment/scripts/fetch_cms_trades.py convert --json-file /tmp/cms_raw.json -o /tmp/cms.csv
python3 .claude/skills/investment/scripts/write_trade_journal.py import-cms /tmp/cms.csv
```
> 页面"服务异常"或有错误弹窗 = 会话过期，提示用户重新登录。用 `take_snapshot` 确认。

**Step 4**：`python3 .claude/skills/investment/scripts/write_trade_journal.py validate`

**注意**：import 自带去重；平台不可用时跳过并告知用户。

### 校验数据

```bash
python .claude/skills/investment/scripts/write_trade_journal.py validate
```

### 盈亏计算

```bash
python .claude/skills/investment/scripts/calc_pnl.py
```

### 运行测试

```bash
cd .claude/skills/investment/scripts && python3 -m pytest -v
```

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
