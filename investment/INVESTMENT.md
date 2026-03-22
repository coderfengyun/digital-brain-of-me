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
├── satoshi-cafe-analysis/           # BTC 技术分析
├── 卢麒元.md                        # 投资笔记
└── *.md                             # 其他投资研究笔记
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

### 从招商证券导入（Chrome MCP）

```bash
# 前置：浏览器已登录招商证券网页交易，打开历史成交页面
# 1. Claude 通过 Chrome MCP evaluate_script 执行 JS 提取数据
# 2. 将 JSON 转为 CSV
python investment/投资日志整理/scripts/fetch_cms_trades.py convert \
  --json-file /tmp/cms_raw.json -o /tmp/cms_trades.csv

# 3. 导入到交易日志
python investment/投资日志整理/scripts/write_trade_journal.py import-cms /tmp/cms_trades.csv
```

### 批量更新交易记录

当用户说"更新我 YYYY-MM-DD 以后的交易记录"时，从三个平台拉取并导入：

**币安**（API，自动化）：
```bash
python3 fetch_binance_trades.py --start DATE --end TODAY --all -o /tmp/binance.csv
python3 write_trade_journal.py import-binance /tmp/binance.csv
```

**富途**（OpenD API，需本地运行 FutuOpenD 且已登录，端口 11111）：
```bash
python3 fetch_futu_trades.py --start DATE --end TODAY -o /tmp/futu.csv
# 导入需手动处理（尚无 import-futu 子命令）
```

**招商证券**（Chrome MCP，需浏览器已登录 xtrade.newone.com.cn 并打开历史成交页）：
```javascript
// 通过 chrome-devtools evaluate_script 执行：
// 1. 找到 Vue 组件，修改日期范围，触发查询
const picker = document.querySelector('.cmsui-date-picker.range-picker').__vue__;
const lscj = picker.$parent;
lscj.range = { start: 'YYYY-MM-DD', end: 'YYYY-MM-DD' };
lscj.dateChange(lscj.range);
lscj.fetchDataLscj();
// 2. 等待加载后从 .cmsui-table_body tbody 提取行数据
```
```bash
# 将提取的 JSON 转 CSV 后导入
python3 fetch_cms_trades.py convert --json-file /tmp/cms_raw.json -o /tmp/cms.csv
python3 write_trade_journal.py import-cms /tmp/cms.csv
```

**注意事项**：
- 各 import 子命令自带去重（同日期+同品种+同方向+金额接近 2%）
- 某个平台不可用时跳过并告知用户
- 最后运行 `validate` 校验

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
