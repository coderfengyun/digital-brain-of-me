# 交易记录导入详细指南

各平台的详细导入步骤。从 skill.md 的"批量更新"流程引用此文件。

---

## 批量更新流程

当用户说"更新交易记录"时，按顺序执行以下步骤。

### Step 0：确定起始日期

```bash
tail -1 investment/投资日志整理/交易日志汇总表.csv
```

取最后记录日期的次日作为 `START_DATE`，`END_DATE` 为今天。

### Step 1：币安（API）

```bash
# 不要用 --all（400+ 交易对会触发限速），指定近期活跃品种
python3 .claude/skills/investment/scripts/fetch_binance_trades.py \
  --start START_DATE --end END_DATE \
  --symbol BTCUSDT XRPUSDT ETHUSDT SOLUSDT ZBTUSDT \
  -o /tmp/binance.csv

python3 .claude/skills/investment/scripts/write_trade_journal.py import-binance /tmp/binance.csv
```

> 如果 import 因金额偏差 >1% 跳过记录（手续费导致），用 `add` 手动添加。

### Step 2：富途（需 FutuOpenD 运行，端口 11111）

```bash
python3 .claude/skills/investment/scripts/fetch_futu_trades.py \
  --start START_DATE --end END_DATE -o /tmp/futu.csv
```

- 连接被拒绝 = FutuOpenD 未运行，跳过并告知用户
- 无 `import-futu` 子命令，有新记录时用 `add` 逐条添加

### Step 3：招商证券（Chrome MCP）

**前置条件**：
- Chrome 以 `--remote-debugging-port=9222` 启动，Chrome MCP 已连接
- 浏览器已登录招商证券

**历史成交页面 URL**（必须含 `/npctrade` 路径前缀）：
```
https://xtrade.newone.com.cn/npctrade#/trade/ptjy/cx?page=lscj
```

**步骤**：

```bash
# 1. chrome-devtools navigate_page 导航到上述 URL（timeout: 60000）

# 2. 生成提取数据的 JS
python3 .claude/skills/investment/scripts/fetch_cms_trades.py js \
  --start START_DATE --end END_DATE

# 3. chrome-devtools evaluate_script 执行该 JS，获取 JSON 结果

# 4. JSON → CSV → 导入
python3 .claude/skills/investment/scripts/fetch_cms_trades.py convert \
  --json-file /tmp/cms_raw.json -o /tmp/cms.csv
python3 .claude/skills/investment/scripts/write_trade_journal.py import-cms /tmp/cms.csv
```

> - 如果数据量只有几条且已存在于日志中，可跳过 convert + import，确认无新记录即可
> - 页面"服务异常"或有错误弹窗 = 会话过期，提示用户重新登录（用 `take_snapshot` 确认）

### Step 4：校验

```bash
python3 .claude/skills/investment/scripts/write_trade_journal.py validate
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
