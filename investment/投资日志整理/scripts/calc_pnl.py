#!/usr/bin/env python3
"""
投资盈亏统计脚本

读取符合 schema 的交易日志 CSV，按品种 FIFO 计算已实现/浮动盈亏，
从互联网获取当前市场价格，输出分品种+汇总的盈亏报告。
"""

import sys
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

import pandas as pd

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent  # 投资日志整理/
CSV_PATH = PROJECT_DIR / "交易日志汇总表.csv"
REPORT_PATH = PROJECT_DIR / "盈亏统计报告.md"

EXPECTED_COLUMNS = ["序号", "品种", "操作类型", "价格", "数量", "金额", "币种", "日期", "日期精确度", "备注"]
VALID_OPS = {"买入", "卖出"}
VALID_CURRENCIES = {"CNY", "USD", "HKD"}
VALID_DATE_PRECISION = {"精确", "周期范围"}
AMOUNT_TOLERANCE = 0.01

EXCLUDED_ASSETS = {"BTC", "ETH"}

TICKER_MAP = {
    "白银ETF (SLV)": "SLV",
    "有色金属ETF": "512400.SS",
    "有色ETF (大成)": "159980.SZ",
    "恒生科技ETF": "3032.HK",
    "USO (石油ETF)": "USO",
}

FX_TICKERS = {
    "USD": "USDCNY=X",
    "HKD": "HKDCNY=X",
}

# ---------------------------------------------------------------------------
# Module 1: CSV reading & schema validation
# ---------------------------------------------------------------------------

class ValidationError(Exception):
    pass


def validate_and_load(csv_path: Path) -> pd.DataFrame:
    """Read CSV and validate against schema. Returns cleaned DataFrame."""
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)

    errors: list[str] = []

    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    extra = set(df.columns) - set(EXPECTED_COLUMNS)
    if missing:
        errors.append(f"缺少列: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"多余列: {', '.join(sorted(extra))}")
    if errors:
        raise ValidationError("\n".join(errors))

    df = df[EXPECTED_COLUMNS]

    for idx, row in df.iterrows():
        row_num = idx + 2  # CSV header is line 1

        if row["操作类型"] not in VALID_OPS:
            errors.append(f"第{row_num}行: 操作类型 '{row['操作类型']}' 非法，仅允许 {VALID_OPS}")

        if row["币种"] not in VALID_CURRENCIES:
            errors.append(f"第{row_num}行: 币种 '{row['币种']}' 非法，仅允许 {VALID_CURRENCIES}")

        if row["日期精确度"] not in VALID_DATE_PRECISION:
            errors.append(f"第{row_num}行: 日期精确度 '{row['日期精确度']}' 非法，仅允许 {VALID_DATE_PRECISION}")

        for field in ("价格", "数量", "金额"):
            try:
                float(row[field])
            except ValueError:
                errors.append(f"第{row_num}行: {field} '{row[field]}' 无法解析为数值")

        try:
            datetime.strptime(row["日期"], "%Y-%m-%d")
        except ValueError:
            errors.append(f"第{row_num}行: 日期 '{row['日期']}' 格式不符合 YYYY-MM-DD")

        try:
            price = float(row["价格"])
            qty = float(row["数量"])
            amount = float(row["金额"])
            expected = price * qty
            if expected != 0 and abs(amount - expected) / expected > AMOUNT_TOLERANCE:
                errors.append(
                    f"第{row_num}行: 金额 {amount} 与 价格×数量 {expected:.2f} 偏差超过 {AMOUNT_TOLERANCE:.0%}"
                )
        except ValueError:
            pass  # already caught above

    if errors:
        raise ValidationError("\n".join(errors))

    df["价格"] = df["价格"].astype(float)
    df["数量"] = df["数量"].astype(float)
    df["金额"] = df["金额"].astype(float)
    df["日期"] = pd.to_datetime(df["日期"])

    return df


# ---------------------------------------------------------------------------
# Module 2: FIFO matching engine
# ---------------------------------------------------------------------------

class RealizedTrade(NamedTuple):
    asset: str
    buy_price: float
    sell_price: float
    qty: float
    pnl: float
    currency: str
    buy_date: datetime
    sell_date: datetime


class OpenPosition(NamedTuple):
    asset: str
    buy_price: float
    qty: float
    cost: float
    currency: str
    buy_date: datetime


class UnmatchedSell(NamedTuple):
    """Sell with no corresponding buy (unknown cost basis)."""
    asset: str
    sell_price: float
    qty: float
    proceeds: float
    currency: str
    sell_date: datetime


def fifo_match(df: pd.DataFrame, asset: str) -> tuple[list[RealizedTrade], list[OpenPosition], list[UnmatchedSell]]:
    """Run FIFO matching for a single asset. df must be filtered to one asset."""
    records = df.sort_values("日期").to_dict("records")
    buy_queue: deque[dict] = deque()
    realized: list[RealizedTrade] = []
    unmatched_sells: list[UnmatchedSell] = []

    for rec in records:
        currency = rec["币种"]
        if rec["操作类型"] == "买入":
            buy_queue.append({"price": rec["价格"], "qty": rec["数量"], "date": rec["日期"]})
        else:
            sell_remaining = rec["数量"]
            sell_price = rec["价格"]
            sell_date = rec["日期"]

            while sell_remaining > 1e-9 and buy_queue:
                buy = buy_queue[0]
                matched = min(sell_remaining, buy["qty"])

                realized.append(RealizedTrade(
                    asset=asset,
                    buy_price=buy["price"],
                    sell_price=sell_price,
                    qty=matched,
                    pnl=(sell_price - buy["price"]) * matched,
                    currency=currency,
                    buy_date=buy["date"],
                    sell_date=sell_date,
                ))

                buy["qty"] -= matched
                sell_remaining -= matched

                if buy["qty"] < 1e-9:
                    buy_queue.popleft()

            if sell_remaining > 1e-9:
                unmatched_sells.append(UnmatchedSell(
                    asset=asset,
                    sell_price=sell_price,
                    qty=sell_remaining,
                    proceeds=sell_price * sell_remaining,
                    currency=currency,
                    sell_date=sell_date,
                ))

    open_positions = [
        OpenPosition(
            asset=asset,
            buy_price=b["price"],
            qty=b["qty"],
            cost=b["price"] * b["qty"],
            currency=records[0]["币种"] if records else "CNY",
            buy_date=b["date"],
        )
        for b in buy_queue
        if b["qty"] > 1e-9
    ]

    return realized, open_positions, unmatched_sells


def run_fifo_all(df: pd.DataFrame) -> tuple[list[RealizedTrade], list[OpenPosition], list[UnmatchedSell]]:
    """Run FIFO matching for all assets."""
    all_realized: list[RealizedTrade] = []
    all_open: list[OpenPosition] = []
    all_unmatched: list[UnmatchedSell] = []

    for asset in df["品种"].unique():
        asset_df = df[df["品种"] == asset]
        r, o, u = fifo_match(asset_df, asset)
        all_realized.extend(r)
        all_open.extend(o)
        all_unmatched.extend(u)

    return all_realized, all_open, all_unmatched


# ---------------------------------------------------------------------------
# Module 3: Fetch current market prices
# ---------------------------------------------------------------------------

def fetch_current_prices(open_positions: list[OpenPosition]) -> tuple[dict[str, float | None], dict[str, float]]:
    """
    Fetch current prices for assets with open positions, plus FX rates.
    Returns (asset_prices, fx_rates_to_cny).
    fx_rates_to_cny maps currency code -> CNY multiplier (CNY->CNY is 1.0).
    """
    try:
        import yfinance as yf
    except ImportError:
        print("WARNING: yfinance 未安装，无法获取当前价格。请运行: pip install yfinance", file=sys.stderr)
        return {}, {"CNY": 1.0}

    needed_assets = {pos.asset for pos in open_positions}
    needed_tickers: dict[str, str] = {}
    for asset in needed_assets:
        if asset in TICKER_MAP:
            needed_tickers[asset] = TICKER_MAP[asset]

    needed_currencies = {pos.currency for pos in open_positions} - {"CNY"}
    fx_ticker_map: dict[str, str] = {}
    for cur in needed_currencies:
        if cur in FX_TICKERS:
            fx_ticker_map[cur] = FX_TICKERS[cur]

    all_tickers = list(needed_tickers.values()) + list(fx_ticker_map.values())
    if not all_tickers:
        return {}, {"CNY": 1.0}

    print(f"正在获取市场价格: {', '.join(all_tickers)} ...")
    raw: dict[str, float | None] = {}
    for ticker_symbol in all_tickers:
        try:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period="5d")
            if hist.empty:
                raw[ticker_symbol] = None
            else:
                raw[ticker_symbol] = float(hist["Close"].iloc[-1])
        except Exception as e:
            print(f"WARNING: 获取 {ticker_symbol} 失败: {e}", file=sys.stderr)
            raw[ticker_symbol] = None

    asset_prices: dict[str, float | None] = {}
    for asset, ticker_symbol in needed_tickers.items():
        asset_prices[asset] = raw.get(ticker_symbol)

    fx_rates: dict[str, float] = {"CNY": 1.0}
    for cur, ticker_symbol in fx_ticker_map.items():
        rate = raw.get(ticker_symbol)
        if rate is not None:
            fx_rates[cur] = rate
        else:
            print(f"WARNING: 无法获取 {cur}/CNY 汇率，该币种盈亏将无法折算 CNY", file=sys.stderr)

    failed = [a for a, p in asset_prices.items() if p is None]
    if failed:
        print(f"\nWARNING: 以下品种当前价格获取失败: {', '.join(failed)}", file=sys.stderr)
        print("这些品种的浮动盈亏将无法计算。", file=sys.stderr)

    return asset_prices, fx_rates


# ---------------------------------------------------------------------------
# Module 4: Floating P&L calculation
# ---------------------------------------------------------------------------

class FloatingPnL(NamedTuple):
    asset: str
    qty: float
    cost: float
    current_value: float
    pnl: float
    currency: str


def calc_floating_pnl(
    open_positions: list[OpenPosition],
    current_prices: dict[str, float | None],
) -> list[FloatingPnL]:
    """Calculate floating P&L for each open position."""
    results: list[FloatingPnL] = []
    for pos in open_positions:
        price = current_prices.get(pos.asset)
        if price is None:
            continue
        current_value = price * pos.qty
        pnl = current_value - pos.cost
        results.append(FloatingPnL(
            asset=pos.asset,
            qty=pos.qty,
            cost=pos.cost,
            current_value=current_value,
            pnl=pnl,
            currency=pos.currency,
        ))
    return results


# ---------------------------------------------------------------------------
# Module 5: Report generation
# ---------------------------------------------------------------------------

def _pnl_label(value: float, realized: bool) -> str:
    if realized:
        return "实现盈利" if value >= 0 else "实现亏损"
    return "浮盈" if value >= 0 else "浮亏"


def _fmt(value: float, currency: str) -> str:
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:,.2f} {currency}"


def generate_report(
    realized: list[RealizedTrade],
    open_positions: list[OpenPosition],
    unmatched_sells: list[UnmatchedSell],
    floating_pnls: list[FloatingPnL],
    current_prices: dict[str, float | None],
    fx_rates: dict[str, float],
    data_date_range: tuple[str, str],
) -> str:
    """Generate markdown report string."""

    all_assets = sorted(set(
        [t.asset for t in realized]
        + [p.asset for p in open_positions]
        + [u.asset for u in unmatched_sells]
    ))

    lines: list[str] = []
    lines.append("# 投资盈亏统计报告\n")
    lines.append(f"数据范围: {data_date_range[0]} ~ {data_date_range[1]}")
    lines.append(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # --- Level 1: per-asset ---
    lines.append("## 分品种盈亏（第一层）\n")

    total_realized_cny = 0.0
    total_floating_cny = 0.0
    currency_conversion_available = True

    for asset in all_assets:
        lines.append(f"### {asset}\n")

        asset_realized = [t for t in realized if t.asset == asset]
        asset_open = [p for p in open_positions if p.asset == asset]
        asset_floating = [f for f in floating_pnls if f.asset == asset]
        asset_unmatched = [u for u in unmatched_sells if u.asset == asset]

        if asset_realized:
            currency = asset_realized[0].currency
            total_r = sum(t.pnl for t in asset_realized)
            total_proceeds = sum(t.sell_price * t.qty for t in asset_realized)
            total_cost = sum(t.buy_price * t.qty for t in asset_realized)
            total_qty = sum(t.qty for t in asset_realized)
            label = _pnl_label(total_r, realized=True)

            lines.append(f"**已实现盈亏: {_fmt(total_r, currency)}** 【{label}】\n")
            lines.append(f"- 卖出总额: {total_proceeds:,.2f} {currency}")
            lines.append(f"- 对应成本: {total_cost:,.2f} {currency}")
            lines.append(f"- 已平仓数量: {total_qty:,.4g}")
            lines.append("")

            fx = fx_rates.get(currency)
            if fx is not None:
                total_realized_cny += total_r * fx
            else:
                currency_conversion_available = False

        if asset_unmatched:
            currency = asset_unmatched[0].currency
            total_proceeds = sum(u.proceeds for u in asset_unmatched)
            total_qty = sum(u.qty for u in asset_unmatched)
            lines.append(f"**成本未知的卖出: {total_proceeds:,.2f} {currency}（{total_qty:,.4g} 单位，无对应买入记录）**\n")

        if asset_floating:
            currency = asset_floating[0].currency
            total_f = sum(f.pnl for f in asset_floating)
            total_cost = sum(f.cost for f in asset_floating)
            total_value = sum(f.current_value for f in asset_floating)
            total_qty = sum(f.qty for f in asset_floating)
            label = _pnl_label(total_f, realized=False)
            current_price = current_prices.get(asset)

            lines.append(f"**浮动盈亏: {_fmt(total_f, currency)}** 【{label}】\n")
            lines.append(f"- 持仓数量: {total_qty:,.4g}")
            lines.append(f"- 持仓成本: {total_cost:,.2f} {currency}")
            lines.append(f"- 当前市值: {total_value:,.2f} {currency}")
            if current_price is not None:
                lines.append(f"- 当前价格: {current_price:,.4f} {currency}/单位")
            lines.append("")

            fx = fx_rates.get(currency)
            if fx is not None:
                total_floating_cny += total_f * fx
            else:
                currency_conversion_available = False
        elif asset_open and not asset_floating:
            currency = asset_open[0].currency
            total_qty = sum(p.qty for p in asset_open)
            total_cost = sum(p.cost for p in asset_open)
            lines.append(f"**持仓（当前价格获取失败，无法计算浮动盈亏）**\n")
            lines.append(f"- 持仓数量: {total_qty:,.4g}")
            lines.append(f"- 持仓成本: {total_cost:,.2f} {currency}")
            lines.append("")

        if not asset_realized and not asset_floating and not asset_open and not asset_unmatched:
            lines.append("无交易记录\n")

        lines.append("---\n")

    # --- Level 2: overall ---
    lines.append("## 整体盈亏汇总（第二层）\n")

    if not currency_conversion_available:
        lines.append("> 注意: 部分币种汇率获取失败，以下 CNY 汇总可能不完整。\n")

    lines.append(f"- **总已实现盈亏: {_fmt(total_realized_cny, 'CNY')}**")
    lines.append(f"- **总浮动盈亏: {_fmt(total_floating_cny, 'CNY')}**")
    total = total_realized_cny + total_floating_cny
    lines.append(f"- **综合盈亏: {_fmt(total, 'CNY')}**\n")

    lines.append("### 使用的汇率\n")
    for cur, rate in sorted(fx_rates.items()):
        if cur != "CNY":
            lines.append(f"- 1 {cur} = {rate:.4f} CNY")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"读取交易日志: {CSV_PATH}")
    try:
        df = validate_and_load(CSV_PATH)
    except FileNotFoundError:
        print(f"ERROR: 文件不存在: {CSV_PATH}", file=sys.stderr)
        sys.exit(1)
    except ValidationError as e:
        print(f"ERROR: CSV schema 校验失败:\n{e}", file=sys.stderr)
        sys.exit(1)

    print(f"共 {len(df)} 条交易记录")

    excluded = df[df["品种"].isin(EXCLUDED_ASSETS)]
    if not excluded.empty:
        print(f"排除品种 ({', '.join(EXCLUDED_ASSETS)}): {len(excluded)} 条")
    df = df[~df["品种"].isin(EXCLUDED_ASSETS)]
    print(f"参与计算: {len(df)} 条，品种: {', '.join(df['品种'].unique())}")

    date_min = df["日期"].min().strftime("%Y-%m-%d")
    date_max = df["日期"].max().strftime("%Y-%m-%d")

    print("\n--- FIFO 匹配 ---")
    realized, open_positions, unmatched = run_fifo_all(df)
    print(f"已实现交易: {len(realized)} 笔")
    print(f"未平仓持仓: {len(open_positions)} 笔")
    if unmatched:
        print(f"WARNING: 成本未知的卖出: {len(unmatched)} 笔")

    print("\n--- 获取当前市场价格 ---")
    current_prices, fx_rates = fetch_current_prices(open_positions)
    for asset, price in current_prices.items():
        if price is not None:
            print(f"  {asset}: {price:.4f}")
        else:
            print(f"  {asset}: 获取失败")

    print("\n--- 计算浮动盈亏 ---")
    floating = calc_floating_pnl(open_positions, current_prices)
    for f in floating:
        label = _pnl_label(f.pnl, realized=False)
        print(f"  {f.asset}: {_fmt(f.pnl, f.currency)} 【{label}】")

    print("\n--- 生成报告 ---")
    report = generate_report(
        realized, open_positions, unmatched, floating,
        current_prices, fx_rates, (date_min, date_max),
    )

    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"报告已输出: {REPORT_PATH}")


if __name__ == "__main__":
    main()
