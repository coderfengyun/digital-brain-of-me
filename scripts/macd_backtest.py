#!/usr/bin/env python3
"""日线 MACD 金叉买入、死叉卖出回测。

默认使用 Yahoo Finance 行情：
  CL1!      -> CL=F
  HKEX:883  -> 0883.HK

信号在收盘后确认，并在下一交易日开盘执行，避免未来函数。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf


SYMBOL_ALIASES = {
    "CL1!": "CL=F",
    "HKEX:883": "0883.HK",
    "HKEX:0883": "0883.HK",
}


@dataclass(frozen=True)
class BacktestResult:
    symbol: str
    data_start: pd.Timestamp
    data_end: pd.Timestamp
    strategy_return: float
    buy_hold_return: float
    max_drawdown: float
    completed_trades: int
    win_rate: float | None
    position_open: bool
    trades: pd.DataFrame
    equity: pd.Series


def normalize_yfinance_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """将 yfinance 的单层或 MultiIndex 结果统一为 OHLC DataFrame。"""
    if frame.empty:
        return frame
    if isinstance(frame.columns, pd.MultiIndex):
        # 单 ticker 下载也可能返回 (Price, Ticker) 两层列。
        frame = frame.copy()
        frame.columns = frame.columns.get_level_values(0)
    required = ["Open", "High", "Low", "Close"]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"行情缺少列: {', '.join(missing)}")
    result = frame[required].copy()
    result.index = pd.to_datetime(result.index).tz_localize(None)
    return result.dropna(subset=["Open", "Close"]).sort_index()


def download_prices(
    symbol: str,
    start: date,
    end: date,
    *,
    warmup_days: int = 180,
    auto_adjust: bool = True,
) -> pd.DataFrame:
    yahoo_symbol = SYMBOL_ALIASES.get(symbol.upper(), symbol)
    download_start = start - timedelta(days=warmup_days)
    # yfinance 的 end 不包含当日。
    frame = yf.download(
        yahoo_symbol,
        start=download_start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        auto_adjust=auto_adjust,
        progress=False,
        actions=False,
    )
    frame = normalize_yfinance_frame(frame)
    if frame.empty:
        raise ValueError(f"{symbol} ({yahoo_symbol}) 未下载到行情")
    return frame


def add_macd(
    prices: pd.DataFrame,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    if not 0 < fast < slow or signal <= 0:
        raise ValueError("MACD 参数必须满足 0 < fast < slow 且 signal > 0")
    result = prices.copy()
    ema_fast = result["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = result["Close"].ewm(span=slow, adjust=False).mean()
    result["MACD"] = ema_fast - ema_slow
    result["Signal"] = result["MACD"].ewm(span=signal, adjust=False).mean()
    result["GoldenCross"] = (result["MACD"] > result["Signal"]) & (
        result["MACD"].shift(1) <= result["Signal"].shift(1)
    )
    result["DeathCross"] = (result["MACD"] < result["Signal"]) & (
        result["MACD"].shift(1) >= result["Signal"].shift(1)
    )
    return result


def run_backtest(
    prices: pd.DataFrame,
    symbol: str,
    start: date,
    end: date,
    *,
    cost_bps: float = 0.0,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> BacktestResult:
    """以 1 单位初始资金进行全仓、只做多回测，允许小数份额。"""
    if cost_bps < 0:
        raise ValueError("cost_bps 不能为负数")
    data = add_macd(prices, fast=fast, slow=slow, signal=signal)
    start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
    period = data.loc[(data.index >= start_ts) & (data.index <= end_ts)].copy()
    if period.empty:
        raise ValueError(f"{symbol} 在 {start} 至 {end} 没有行情")

    cost_rate = cost_bps / 10_000
    cash, units = 1.0, 0.0
    entry: dict[str, object] | None = None
    trades: list[dict[str, object]] = []
    equity_values: list[float] = []

    # 当天开盘执行前一交易日收盘确认的信号。
    for trading_day, row in period.iterrows():
        location = data.index.get_loc(trading_day)
        previous = data.iloc[location - 1] if location > 0 else None
        previous_day = data.index[location - 1] if location > 0 else None

        if previous is not None and previous_day >= start_ts:
            if bool(previous["GoldenCross"]) and units == 0:
                raw_price = float(row["Open"])
                execution_price = raw_price * (1 + cost_rate)
                units = cash / execution_price
                cash = 0.0
                entry = {
                    "买入信号日": previous_day.date().isoformat(),
                    "买入日": trading_day.date().isoformat(),
                    "买入价": raw_price,
                    "含成本买入价": execution_price,
                }
            elif bool(previous["DeathCross"]) and units > 0 and entry is not None:
                raw_price = float(row["Open"])
                execution_price = raw_price * (1 - cost_rate)
                cash = units * execution_price
                trade_return = execution_price / float(entry["含成本买入价"]) - 1
                trades.append(
                    {
                        **entry,
                        "卖出信号日": previous_day.date().isoformat(),
                        "卖出日": trading_day.date().isoformat(),
                        "卖出价": raw_price,
                        "含成本卖出价": execution_price,
                        "收益率": trade_return,
                        "状态": "已平仓",
                    }
                )
                units = 0.0
                entry = None

        equity_values.append(cash + units * float(row["Close"]))

    position_open = units > 0 and entry is not None
    if position_open:
        final_price = float(period.iloc[-1]["Close"])
        trades.append(
            {
                **entry,
                "卖出信号日": "",
                "卖出日": period.index[-1].date().isoformat(),
                "卖出价": final_price,
                "含成本卖出价": final_price,
                "收益率": final_price / float(entry["含成本买入价"]) - 1,
                "状态": "期末持有",
            }
        )

    equity = pd.Series(equity_values, index=period.index, name=symbol)
    drawdown = equity / equity.cummax() - 1
    completed = [trade for trade in trades if trade["状态"] == "已平仓"]
    win_rate = (
        sum(float(trade["收益率"]) > 0 for trade in completed) / len(completed)
        if completed
        else None
    )

    first_open = float(period.iloc[0]["Open"])
    last_close = float(period.iloc[-1]["Close"])
    buy_hold_return = last_close / (first_open * (1 + cost_rate)) - 1
    return BacktestResult(
        symbol=symbol,
        data_start=period.index[0],
        data_end=period.index[-1],
        strategy_return=float(equity.iloc[-1] - 1),
        buy_hold_return=buy_hold_return,
        max_drawdown=float(drawdown.min()),
        completed_trades=len(completed),
        win_rate=win_rate,
        position_open=position_open,
        trades=pd.DataFrame(trades),
        equity=equity,
    )


def percent(value: float | None) -> str:
    return "—" if value is None else f"{value:.2%}"


def print_result(result: BacktestResult) -> None:
    print(f"\n{result.symbol}  {result.data_start.date()} ~ {result.data_end.date()}")
    print(f"  MACD 策略收益: {percent(result.strategy_return)}")
    print(f"  买入持有收益: {percent(result.buy_hold_return)}")
    print(f"  最大回撤:     {percent(result.max_drawdown)}")
    print(f"  已平仓交易:   {result.completed_trades}")
    print(f"  已平仓胜率:   {percent(result.win_rate)}")
    print(f"  期末状态:     {'持仓' if result.position_open else '空仓'}")
    if result.trades.empty:
        print("  期间无交易")
    else:
        display = result.trades.copy()
        display["收益率"] = display["收益率"].map(lambda value: f"{value:.2%}")
        print(display.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbols", nargs="*", default=["CL1!", "HKEX:883"])
    parser.add_argument("--start", type=date.fromisoformat, default=date(2026, 1, 1))
    parser.add_argument("--end", type=date.fromisoformat, default=date.today())
    parser.add_argument("--fast", type=int, default=12)
    parser.add_argument("--slow", type=int, default=26)
    parser.add_argument("--signal", type=int, default=9)
    parser.add_argument(
        "--cost-bps",
        type=float,
        default=0.0,
        help="单边手续费与滑点合计（基点），默认 0",
    )
    parser.add_argument(
        "--raw-prices",
        action="store_true",
        help="使用未复权价格；默认使用自动复权价格",
    )
    parser.add_argument("--output-dir", type=Path, help="可选：保存逐笔交易和净值 CSV")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.end < args.start:
        raise SystemExit("--end 不能早于 --start")
    for symbol in args.symbols:
        prices = download_prices(
            symbol,
            args.start,
            args.end,
            auto_adjust=not args.raw_prices,
        )
        result = run_backtest(
            prices,
            symbol,
            args.start,
            args.end,
            cost_bps=args.cost_bps,
            fast=args.fast,
            slow=args.slow,
            signal=args.signal,
        )
        print_result(result)
        if args.output_dir:
            args.output_dir.mkdir(parents=True, exist_ok=True)
            safe_symbol = symbol.replace(":", "_").replace("!", "").replace("=", "_")
            result.trades.to_csv(
                args.output_dir / f"{safe_symbol}_trades.csv", index=False
            )
            result.equity.to_csv(args.output_dir / f"{safe_symbol}_equity.csv")


if __name__ == "__main__":
    main()
