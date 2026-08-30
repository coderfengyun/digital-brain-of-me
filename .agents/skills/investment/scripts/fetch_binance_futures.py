#!/usr/bin/env python3
"""
从币安获取 USDT-M 合约历史成交记录。

前置条件:
  1. 安装依赖:  pip install python-binance python-dotenv
  2. 在项目根目录创建 .env 文件，填入:
     BINANCE_API_KEY=your_key
     BINANCE_API_SECRET=your_secret

用法:
  # 查询指定日期范围的合约交易
  python fetch_binance_futures.py --start 2026-05-29 --end 2026-06-28

  # 只查某个交易对
  python fetch_binance_futures.py --start 2026-06-01 --end 2026-06-28 --symbol BTCUSDT

  # 导出到 CSV
  python fetch_binance_futures.py --start 2026-06-01 --end 2026-06-28 -o futures.csv
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv


DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT"]
MAX_INTERVAL_DAYS = 7


def parse_args():
    parser = argparse.ArgumentParser(description="从币安获取合约历史成交记录")
    parser.add_argument("--start", "-s", required=True, help="起始日期 (YYYY-MM-DD)")
    parser.add_argument("--end", "-e", required=True, help="结束日期 (YYYY-MM-DD)")
    parser.add_argument(
        "--symbol",
        nargs="+",
        default=DEFAULT_SYMBOLS,
        help=f"交易对，默认 {' '.join(DEFAULT_SYMBOLS)}",
    )
    parser.add_argument("--output", "-o", help="输出 CSV 文件路径（不指定则打印到终端）")
    parser.add_argument(
        "--env-file", default=None, help=".env 文件路径（默认项目根目录 .env）"
    )
    return parser.parse_args()


def create_client(env_file: str | None = None):
    from binance.client import Client

    if env_file:
        env_path = Path(env_file)
    else:
        env_path = Path(__file__).resolve().parents[4] / ".env"

    if env_path.exists():
        load_dotenv(env_path)
        print(f"已加载 .env: {env_path}", file=sys.stderr)

    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print(
            "错误: 未找到 BINANCE_API_KEY / BINANCE_API_SECRET\n"
            "请在 .env 文件中配置，或设置环境变量",
            file=sys.stderr,
        )
        sys.exit(1)

    return Client(api_key, api_secret)


def fetch_futures_trades(client, symbol: str, start_date: datetime, end_date: datetime) -> list[dict]:
    """分段查询合约交易（API 限制最多7天一段）。"""
    all_trades = []
    chunk_start = start_date

    while chunk_start < end_date:
        chunk_end = min(chunk_start + timedelta(days=MAX_INTERVAL_DAYS) - timedelta(seconds=1), end_date)
        s_ms = int(chunk_start.timestamp() * 1000)
        e_ms = int(chunk_end.timestamp() * 1000)

        trades = client.futures_account_trades(symbol=symbol, startTime=s_ms, endTime=e_ms)
        all_trades.extend(trades)

        chunk_start = chunk_end + timedelta(seconds=1)

    return all_trades


def format_trade(t: dict) -> dict:
    """将 API 返回的交易记录格式化为可读字典。"""
    return {
        "日期": datetime.fromtimestamp(t["time"] / 1000).strftime("%Y-%m-%d"),
        "时间": datetime.fromtimestamp(t["time"] / 1000).strftime("%H:%M:%S"),
        "交易对": t["symbol"],
        "方向": t["side"],
        "价格": t["price"],
        "数量": t["qty"],
        "金额": t["quoteQty"],
        "已实现盈亏": t["realizedPnl"],
        "手续费": t["commission"],
        "手续费币种": t["commissionAsset"],
        "持仓方向": t.get("positionSide", ""),
        "订单ID": str(t["orderId"]),
    }


def main():
    args = parse_args()
    client = create_client(args.env_file)

    start_date = datetime.strptime(args.start, "%Y-%m-%d")
    end_date = datetime.strptime(args.end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

    print(
        f"查询合约交易: {', '.join(args.symbol)} (从 {args.start} 到 {args.end})",
        file=sys.stderr,
    )

    all_trades = []
    for i, symbol in enumerate(args.symbol):
        print(f"  获取 {symbol} ({i+1}/{len(args.symbol)}) ...", file=sys.stderr)
        trades = fetch_futures_trades(client, symbol, start_date, end_date)
        if trades:
            print(f"    {len(trades)} 条记录", file=sys.stderr)
        all_trades.extend(trades)

    if not all_trades:
        print("该时间范围内无合约成交记录。", file=sys.stderr)
        return

    all_trades.sort(key=lambda x: x["time"])
    rows = [format_trade(t) for t in all_trades]
    print(f"\n共 {len(rows)} 条合约成交记录:\n", file=sys.stderr)

    if args.output:
        out_path = Path(args.output)
        fieldnames = list(rows[0].keys())
        with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"已导出到 {out_path}", file=sys.stderr)
    else:
        header = list(rows[0].keys())
        widths = [max(len(str(r[h])) for r in rows + [{h: h for h in header}]) for h in header]
        fmt = "  ".join(f"{{:<{w}}}" for w in widths)
        print(fmt.format(*header))
        print(fmt.format(*["-" * w for w in widths]))
        for r in rows:
            print(fmt.format(*[str(r[h]) for h in header]))


if __name__ == "__main__":
    main()
