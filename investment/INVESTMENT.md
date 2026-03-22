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
│   │   ├── calc_pnl.py             # 盈亏计算（FIFO 匹配）
│   │   └── test_*.py               # 测试用例
│   ├── TASK_盈亏情况统计.md          # 盈亏统计任务定义
│   ├── DESIGN_盈亏统计系统设计.md    # 系统设计文档
│   ├── 招商证券交易日志/             # 原始交易截图（招商证券）
│   └── 招行黄金交易日志/             # 原始交易截图（招行黄金）
├── 洪灏/                            # 投资分析文章
├── satoshi-cafe-analysis/           # BTC 技术分析
├── 卢麒元.md                        # 投资笔记
└── *.md                             # 其他投资研究笔记
```

## Data Schema

<a id="data-schema"></a>

交易日志使用 CSV 格式，Schema 定义见 [`交易日志汇总表.schema.json`](投资日志整理/交易日志汇总表.schema.json)。

```csv
序号,品种,操作类型,价格,数量,金额,币种,日期,日期精确度,备注
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
| 备注 | string | 可选 |

## Usage

<a id="usage"></a>

### 添加交易记录

```bash
python investment/投资日志整理/scripts/write_trade_journal.py add \
  --品种 BTC --操作 买入 --价格 76653 --数量 0.00391 --金额 299.71 \
  --币种 USD --日期 2025-04-07 --备注 "币安API精确数据"
```

### 从币安导入

```bash
# 1. 获取币安交易记录
python investment/投资日志整理/scripts/fetch_binance_trades.py \
  --start 2025-04-01 --end 2025-10-31 -o /tmp/binance_trades.csv

# 2. 导入到交易日志
python investment/投资日志整理/scripts/write_trade_journal.py import-binance /tmp/binance_trades.csv
```

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
