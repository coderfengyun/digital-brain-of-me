# Investment - 投资交易记录与盈亏分析

个人投资交易的结构化管理：从各券商/交易所获取交易记录，汇总到统一的交易日志，计算盈亏统计。

## Structure

```
investment/
├── INVESTMENT.md                    # 本文件
├── 投资日志整理/
│   ├── 交易日志汇总表.csv           # 核心数据：全部现货交易记录
│   ├── 交易日志汇总表.schema.json   # CSV Schema (Frictionless Table Schema)
│   ├── scripts/                     # 自动化脚本
│   │   ├── write_trade_journal.py   # 交易日志写入工具（添加/导入/迁移/校验）
│   │   ├── fetch_binance_trades.py  # 币安交易记录获取
│   │   ├── fetch_futu_trades.py     # 富途交易记录获取
│   │   ├── fetch_cms_trades.py      # 招商证券交易记录获取（Chrome MCP）
│   │   ├── calc_pnl.py             # 盈亏计算（FIFO 匹配）
│   │   └── test_*.py               # 测试用例
│   ├── TASK_盈亏情况统计.md          # 盈亏统计任务定义
│   ├── DESIGN_盈亏统计系统设计.md    # 系统设计文档
│   ├── 招商证券交易日志/             # 原始交易截图（招商证券）
│   └── 招行黄金交易日志/             # 原始交易截图（招行黄金）
├── 洪灏/                            # 投资分析文章
├── M_Medi/                          # M_Medi 市场结构分析
├── satoshi-cafe-analysis/           # BTC 技术分析
└── 卢麒元/                          # 卢麒元投资笔记与资料
```

## Data Schema

<a id="data-schema"></a>

交易日志使用 CSV 格式，Schema 定义见 [`交易日志汇总表.schema.json`](投资日志整理/交易日志汇总表.schema.json)。

```csv
序号,品种,操作类型,价格,数量,金额,币种,日期,日期精确度,交易平台,备注
```

| 字段 | 类型 | 说明 |
|------|------|------|
| 序号 | string | 唯一递增标识 |
| 品种 | string | 资产名称（全局统一命名） |
| 操作类型 | enum | `买入` / `卖出` |
| 价格 | number | 纯数值，无货币符号 |
| 数量 | number | 纯数值，无单位后缀 |
| 金额 | number | = 价格 × 数量（误差 ≤1%） |
| 币种 | enum | `CNY` / `USD` / `HKD` |
| 日期 | date | `YYYY-MM-DD` |
| 日期精确度 | enum | `精确` / `周期范围` |
| 交易平台 | enum | `币安` / `富途` / `招行` / `招商证券` / `其他` |
| 备注 | string | 可选 |

## Usage

<a id="usage"></a>

### 添加交易记录

```bash
python investment/投资日志整理/scripts/write_trade_journal.py add \
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
python investment/投资日志整理/scripts/fetch_binance_trades.py \
  --start 2025-04-01 --end 2025-10-31 -o /tmp/binance_trades.csv

# 2. 导入到交易日志
python investment/投资日志整理/scripts/write_trade_journal.py import-binance /tmp/binance_trades.csv
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
python investment/投资日志整理/scripts/fetch_cms_trades.py js \
  --start 2026-03-03 --end 2026-03-28

# Step 3: 通过 chrome-devtools evaluate_script 执行该 JS，获取 JSON 结果

# Step 4: 将 JSON 保存到文件并转为 CSV
python investment/投资日志整理/scripts/fetch_cms_trades.py convert \
  --json-file /tmp/cms_raw.json -o /tmp/cms_trades.csv

# Step 5: 导入到交易日志
python investment/投资日志整理/scripts/write_trade_journal.py import-cms /tmp/cms_trades.csv
```

> **注意**：如果数据量只有几条且已存在于日志中，可以跳过 Step 4-5，直接确认无新记录即可。

### 批量更新交易记录

当用户说"更新交易记录"时：

**Step 0**：用 `tail -1 交易日志汇总表.csv` 确定最后记录日期，次日作为起始日期。

**Step 1：币安**（API）
```bash
# ⚠️ 不要用 --all（400+ 交易对会触发限速），指定近期活跃品种
python3 fetch_binance_trades.py --start DATE --end TODAY \
  --symbol BTCUSDT XRPUSDT ETHUSDT SOLUSDT ZBTUSDT -o /tmp/binance.csv
python3 write_trade_journal.py import-binance /tmp/binance.csv
```
> 如果 import 因金额偏差 >1% 跳过记录（手续费导致），用 `add` 手动添加。

**Step 2：富途**（需 FutuOpenD 运行，端口 11111；连接被拒绝则跳过）
```bash
python3 fetch_futu_trades.py --start DATE --end TODAY -o /tmp/futu.csv
# 无 import-futu 子命令，有新记录时用 add 逐条添加
```

**Step 3：招商证券**（Chrome MCP，需浏览器已登录）
```bash
# 1. navigate_page → https://xtrade.newone.com.cn/npctrade#/trade/ptjy/cx?page=lscj (timeout: 60000)
# 2. 生成+执行 JS
python3 fetch_cms_trades.py js --start DATE --end TODAY
# 3. evaluate_script 执行 JS，获取 JSON
# 4. 有新记录则 convert + import-cms
python3 fetch_cms_trades.py convert --json-file /tmp/cms_raw.json -o /tmp/cms.csv
python3 write_trade_journal.py import-cms /tmp/cms.csv
```
> 页面"服务异常"或有错误弹窗 = 会话过期，提示用户重新登录。用 `take_snapshot` 确认。

**Step 4**：`python3 write_trade_journal.py validate`

**注意**：import 自带去重；平台不可用时跳过并告知用户。

### 校验数据

```bash
python investment/投资日志整理/scripts/write_trade_journal.py validate
```

### 盈亏计算

```bash
python investment/投资日志整理/scripts/calc_pnl.py
```

### 运行测试

```bash
cd investment/投资日志整理/scripts && python3 -m pytest -v
```

## Integration with Other Modules

- **Operations**: 投资决策可关联到 `operations/goals/` 中的财务目标
- **Knowledge**: 投资研究文章（`investment/*.md`）可作为 knowledge 模块的补充
- **Content**: 投资分析可转化为 content 创作素材
