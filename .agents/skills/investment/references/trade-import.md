# 交易记录导入详细指南

各平台的详细导入步骤。从 SKILL.md 的"批量更新"流程引用此文件。

---

## 批量更新流程

当用户说"更新交易记录"时，按顺序执行以下步骤。

### Step 0：确定各平台起始日期

每个平台的 `START_DATE` 独立计算：取该平台在 CSV 中最后一笔记录日期的次日。`END_DATE` 统一为今天。

```bash
# 各平台最后记录日期（grep 平台名，取最后一行的日期列）
grep '币安' investment/投资日志整理/交易日志汇总表.csv | tail -1
grep '富途' investment/投资日志整理/交易日志汇总表.csv | tail -1
grep '招商证券' investment/投资日志整理/交易日志汇总表.csv | tail -1
```

### Step 1：币安（API）

**现货：**

```bash
# 不要用 --all（400+ 交易对会触发限速），指定近期活跃品种
python3 .codex/skills/investment/scripts/fetch_binance_trades.py \
  --start START_DATE --end END_DATE \
  --symbol BTCUSDT XRPUSDT ETHUSDT SOLUSDT ZBTUSDT \
  -o /tmp/binance.csv

python3 .codex/skills/investment/scripts/write_trade_journal.py import-binance /tmp/binance.csv
```

> 如果 import 因金额偏差 >1% 跳过记录（手续费导致），用 `add` 手动添加。

**合约（USDT-M）：**

```bash
python3 .codex/skills/investment/scripts/fetch_binance_futures.py \
  --start START_DATE --end END_DATE \
  -o /tmp/binance_futures.csv
```

> 合约 API 限制单次最多7天，脚本自动分段查询。
> 合约交易需用 `write_trade_journal.py add` 手动录入（品种填"BTC合约"，备注标注开仓/平仓及PnL）。

### Step 2：富途（需 FutuOpenD 运行，端口 11111）

```bash
python3 .codex/skills/investment/scripts/fetch_futu_trades.py \
  --start START_DATE --end END_DATE -o /tmp/futu.csv

python3 .codex/skills/investment/scripts/write_trade_journal.py import-futu /tmp/futu.csv
```

- 连接被拒绝 = FutuOpenD 未运行，跳过并告知用户
- `import-futu` 自带去重、品种名映射（`FUTU_NAME_MAP`）和代码字段填充
- 新品种首次导入时，如映射表中没有对应中文名，会使用富途原始英文名；后续可在映射表中补充

### Step 3：招商证券（掌上证券 MAC 金融终端）

**前置条件**：
- macOS 上已启动并登录“掌上证券 MAC 金融终端”
- 已进入“普通交易”模块

**步骤**：

1. 在左侧菜单选择 **普通交易 → 查询 → 历史委托**。
2. 将起始日期设为 `START_DATE`，终止日期设为 `END_DATE`，执行查询。
3. 读取查询结果中的成交日期、证券代码、证券名称、买卖方向、成交价格、成交数量、成交金额、成交编号等字段。
4. 若终端支持导出，将结果导出为 CSV；按 `write_trade_journal.py import-cms` 所需的招商证券字段格式整理后导入：

```bash
uv run .codex/skills/investment/scripts/write_trade_journal.py import-cms /tmp/cms.csv
```

5. 若终端不支持导出，逐笔使用 `add` 命令写入交易日志；备注中保留成交编号、委托编号及终端显示的结算金额，便于去重和复核。

> - “历史委托”是本流程的查询入口；只将已成交的委托写入交易日志，未成交或已撤单的委托不记录为交易。
> - 如果查询结果为空，确认日期范围、账户和交易市场后即可记为本期无新成交。
> - `fetch_cms_trades.py` 原有的网页提取脚本不再作为招商证券的默认数据来源。

### Step 4：校验

```bash
python3 .codex/skills/investment/scripts/write_trade_journal.py validate
```

### 通用注意事项

- import 自带去重，重复记录会被跳过
- 平台不可用时跳过并告知用户，不要因为一个平台失败就中断整个流程

---

## 单平台导入

如果用户只需要从特定平台导入，参照上方对应 Step 即可。
- 币安：Step 1
- 富途：Step 2
- 招商证券：Step 3
