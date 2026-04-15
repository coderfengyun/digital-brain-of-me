# 投资盈亏统计系统设计

## 1. 系统概述

本系统从交易日志中统计金融投资的盈亏情况，分为两个层次：
1. **分品种盈亏**：每个投资品种的已实现盈亏和浮动盈亏
2. **整体盈亏**：所有品种按汇率折算 CNY 后的汇总

## 2. 系统架构

```
券商/交易所 API
       │
       ▼
┌──────────────────────────┐
│ 上游：交易记录获取 & 写入   │  .claude/skills/investment/scripts/
│ (程序化执行)               │    write_trade_journal.py
│                            │
└─────────┬────────────────┘
          │ 输出：交易日志汇总表.csv（严格遵循 Schema）
          ▼
┌──────────────────────────┐
│ 下游：盈亏计算脚本          │  .claude/skills/investment/scripts/calc_pnl.py
│ (纯程序执行)               │
└─────────┬────────────────┘
          │ 输出：盈亏统计报告.md
          ▼
     最终报告
```

**核心设计原则：上下游解耦**
- 上游（API 脚本 + write_trade_journal.py）负责从各数据源获取交易记录并写入 CSV
- 下游（calc_pnl.py）负责数值计算，保证准确性
- 两者通过 CSV Schema 契约连接

## 3. CSV Schema 契约

Schema 采用 [Frictionless Table Schema](https://specs.frictionlessdata.io/table-schema/) 规范，机器可读定义见 [交易日志汇总表.schema.json](交易日志汇总表.schema.json)。人类可读版本见 [INVESTMENT.md](../INVESTMENT.md#data-schema)。

```csv
序号,品种,操作类型,价格,数量,金额,币种,日期,日期精确度,备注
```

共 10 个字段，其中 3 个 enum 字段、3 个纯数值字段、1 个日期字段。
Schema 格式选用 Frictionless Table Schema 而非 JSON Schema 或 W3C CSVW，因为它专为表格数据设计，语义简洁且足够表达字段类型、枚举约束和主键。

## 4. calc_pnl.py 模块设计

### 4.1 模块划分

```
calc_pnl.py
├── 模块 1: validate_and_load()     # CSV 读取 & Schema 校验
├── 模块 2: fifo_match()            # FIFO 匹配引擎（单品种）
│           run_fifo_all()           # 全品种批量运行
├── 模块 3: fetch_current_prices()  # 获取当前市场价格 & 汇率
├── 模块 4: calc_floating_pnl()     # 浮动盈亏计算
├── 模块 5: generate_report()       # Markdown 报告生成
└── main()                          # 主流程编排
```

### 4.2 数据结构

使用 NamedTuple 定义四种核心数据结构：

- **RealizedTrade** -- 一笔已实现交易（买卖匹配后的结果）
  - `asset`, `buy_price`, `sell_price`, `qty`, `pnl`, `currency`, `buy_date`, `sell_date`

- **OpenPosition** -- 一笔未平仓持仓
  - `asset`, `buy_price`, `qty`, `cost`, `currency`, `buy_date`

- **UnmatchedSell** -- 一笔成本未知的卖出（无对应买入记录）
  - `asset`, `sell_price`, `qty`, `proceeds`, `currency`, `sell_date`

- **FloatingPnL** -- 一笔浮动盈亏
  - `asset`, `qty`, `cost`, `current_value`, `pnl`, `currency`

### 4.3 FIFO 匹配引擎

按品种独立运行。将同一品种的交易按日期升序排列，维护一个买入队列。遇到买入则入队，遇到卖出则从队首逐笔消耗买入量（先进先出），每匹配一对记录一笔已实现盈亏。若卖出耗尽买入队列仍有余量，记录为成本未知的卖出。遍历结束后队列中剩余的买入即为未平仓持仓。浮点精度上使用 1e-9 作为零值阈值。

### 4.4 当前价格获取

使用 `yfinance` 获取仍持有品种的当前价格和汇率。品种名到 yfinance ticker 的映射表硬编码在脚本配置区（`TICKER_MAP`），新增品种时需手动添加。

容错策略：单个 ticker 获取失败不中断全局，标记该品种为"价格获取失败"，在报告中仅展示持仓成本。

### 4.5 报告生成

输出文件：`盈亏统计报告.md`

**第一层（分品种）**：每个品种一个段落，包含：
- 已实现盈亏金额 + 标记（实现盈利/实现亏损）
- 浮动盈亏金额 + 标记（浮盈/浮亏）
- 持仓明细（数量、成本、当前市值、当前价格）
- 成本未知的卖出（如有）

**第二层（整体汇总）**：
- 总已实现盈亏（折算 CNY）
- 总浮动盈亏（折算 CNY）
- 综合盈亏 = 总已实现 + 总浮动
- 附注：使用的汇率

### 4.6 主流程

```
main():
    1. validate_and_load(csv_path)    → DataFrame
    2. 过滤排除品种 (ETH — BTC 已有买入记录，可纳入计算)
    3. run_fifo_all(df)               → realized, open_positions, unmatched
    4. fetch_current_prices(open_pos)  → prices, fx_rates
    5. calc_floating_pnl(open_pos, prices) → floating
    6. generate_report(...)            → markdown string
    7. write to 盈亏统计报告.md
```

## 5. 排除项说明

| 排除项 | 原因 |
|--------|------|
| BTC | ~~已补充买入记录（币安 API），可纳入计算~~ → 从排除列表移除 |
| ETH | CSV 中仅有卖出记录（非币安交易），无买入成本，暂排除 |
| BTC 合约 (C1-C4) | 合约交易语义不同且数据不完整（如"微盈利"），已在 schema 层面排除 |

## 6. 文件清单

```
investment/投资日志整理/
├── TASK_盈亏情况统计.md            # 本任务需求定义
├── DESIGN_盈亏统计系统设计.md      # 本文件
├── 交易日志汇总表.schema.json      # CSV Schema 机器可读定义 (Frictionless Table Schema)
├── 交易日志汇总表.csv              # 数据文件
└── 盈亏统计报告.md                 # 输出报告（由脚本生成）

.claude/skills/investment/scripts/
├── write_trade_journal.py          # 交易日志写入工具
├── calc_pnl.py                     # 盈亏计算脚本
└── test_calc_pnl.py                # 测试用例
```

## 7. 扩展点

- **新增品种**：在 `TICKER_MAP` 中添加品种名到 yfinance ticker 的映射
- **新增币种**：在 `VALID_CURRENCIES` 和 `FX_TICKERS` 中添加
- **合约交易支持**：需设计独立的 schema 和匹配逻辑（开仓/平仓语义不同于买入/卖出）
- **BTC 已纳入**：买入记录已通过币安 API 补充
- **ETH 纳入**：待确认买入交易所并补充买入记录后，从 `EXCLUDED_ASSETS` 中移除
