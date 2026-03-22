#!/usr/bin/env python3
"""
从币安获取现货历史成交记录。

前置条件:
  1. 安装依赖:  pip install python-binance python-dotenv
  2. 在项目根目录创建 .env 文件，填入:
     BINANCE_API_KEY=your_key
     BINANCE_API_SECRET=your_secret

用法:
  # 自动发现所有交易过的币种并获取成交记录
  python fetch_binance_trades.py

  # 指定日期范围
  python fetch_binance_trades.py --start 2025-05-01 --end 2025-05-31

  # 只查某个交易对
  python fetch_binance_trades.py --symbol BTCUSDT

  # 导出到 CSV
  python fetch_binance_trades.py --start 2025-05-01 --end 2025-10-31 -o trades.csv
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    from binance.client import Client
except ImportError:
    print("错误: 请先安装 python-binance:  pip install python-binance", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("错误: 请先安装 python-dotenv:  pip install python-dotenv", file=sys.stderr)
    sys.exit(1)

import os

SIDE_LABEL = {"BUY": "买入", "SELL": "卖出", True: "买入", False: "卖出"}

# 自动发现时忽略的稳定币和法币（它们本身不需要作为 base asset 查询）
SKIP_ASSETS = {"USDT", "USDC", "BUSD", "TUSD", "FDUSD", "USD", "EUR", "GBP"}

# 默认 quote 币种（用于拼交易对）
QUOTE_CURRENCIES = ["USDT", "BUSD", "USDC", "FDUSD"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从币安获取现货历史成交记录",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--start", "-s",
        help="起始日期 (YYYY-MM-DD)，默认 90 天前",
    )
    parser.add_argument(
        "--end", "-e",
        help="结束日期 (YYYY-MM-DD)，默认今天",
    )
    parser.add_argument(
        "--symbol",
        nargs="+",
        default=None,
        help="交易对，如 BTCUSDT ETHUSDT（不指定则自动发现有余额的币种）",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        dest="all_assets",
        help="查询所有资产（包括余额为 0 的），默认只查有余额的",
    )
    parser.add_argument(
        "--output", "-o",
        help="输出 CSV 文件路径（不指定则打印到终端）",
    )
    parser.add_argument(
        "--env-file",
        default=None,
        help=".env 文件路径（默认项目根目录 .env）",
    )
    return parser.parse_args()


def date_to_ms(date_str: str) -> int:
    """将 YYYY-MM-DD 转为毫秒时间戳。"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(dt.timestamp() * 1000)


def format_timestamp(ts_ms: int) -> str:
    """将毫秒时间戳转为可读时间。"""
    return datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")


def fetch_trades_for_symbol(
    client: Client,
    symbol: str,
    start_ms: int | None = None,
    end_ms: int | None = None,
) -> list[dict]:
    """获取某个交易对的全部成交记录（自动分页）。

    策略：只传 startTime（不传 endTime 以避免 24h 限制），
    用 fromId 翻页，最后按 end_ms 过滤。
    """
    all_trades = []
    from_id = None

    while True:
        kwargs: dict = {"symbol": symbol, "limit": 1000}
        if from_id is not None:
            kwargs["fromId"] = from_id
        elif start_ms is not None:
            # 只传 startTime，不传 endTime，避免 24h 限制
            kwargs["startTime"] = start_ms

        trades = client.get_my_trades(**kwargs)

        if not trades:
            break

        if from_id is not None:
            # fromId 查询包含该 id 本身，跳过避免重复
            trades = [t for t in trades if t["id"] != from_id]
            if not trades:
                break

        # 按 end_ms 过滤并判断是否超出范围
        if end_ms is not None:
            trades = [t for t in trades if t["time"] <= end_ms]
            if not trades:
                break

        all_trades.extend(trades)

        if len(trades) < 1000:
            break

        from_id = trades[-1]["id"]
        time.sleep(0.2)  # 翻页时稍作暂停

    return all_trades


def format_output(trades: list[dict]) -> list[dict]:
    """将原始 API 数据转为中文列名的输出格式。"""
    rows = []
    for t in trades:
        rows.append({
            "成交时间": format_timestamp(t["time"]),
            "交易对": t["symbol"],
            "方向": SIDE_LABEL.get(t.get("isBuyer"), t.get("isBuyer", "")),
            "数量": float(t["qty"]),
            "成交价": float(t["price"]),
            "金额": float(t["quoteQty"]),
            "手续费": float(t["commission"]),
            "手续费币种": t["commissionAsset"],
            "成交编号": t["id"],
        })
    rows.sort(key=lambda x: x["成交时间"])
    return rows


def find_env_file(specified_path: str | None) -> str | None:
    """查找 .env 文件：优先使用指定路径，否则向上查找项目根目录。"""
    if specified_path:
        return specified_path

    # 从当前脚本位置向上查找
    current = Path(__file__).resolve().parent
    for _ in range(5):
        env_path = current / ".env"
        if env_path.exists():
            return str(env_path)
        current = current.parent
    return None


def create_client(env_file: str | None = None) -> Client:
    """创建币安客户端，从 .env 读取 API Key。"""
    env_path = find_env_file(env_file)
    if env_path:
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


def discover_symbols(client: Client, include_zero_balance: bool = False) -> list[str]:
    """从账户信息自动发现交易对。

    Args:
        include_zero_balance: 为 True 时包含余额为 0 的资产（空投灰尘等），
                              为 False 时只返回有实际余额的资产。
    """
    print("自动发现交易过的币种...", file=sys.stderr)

    # 获取所有交易所支持的交易对
    exchange_info = client.get_exchange_info()
    valid_symbols = {s["symbol"] for s in exchange_info["symbols"] if s["status"] == "TRADING"}

    # 获取账户资产
    account = client.get_account()
    if include_zero_balance:
        assets = [
            b["asset"]
            for b in account["balances"]
            if b["asset"] not in SKIP_ASSETS
        ]
    else:
        assets = [
            b["asset"]
            for b in account["balances"]
            if b["asset"] not in SKIP_ASSETS
            and (float(b["free"]) > 0 or float(b["locked"]) > 0)
        ]

    # 对每个资产尝试拼出交易对
    symbols = []
    for asset in assets:
        for quote in QUOTE_CURRENCIES:
            pair = f"{asset}{quote}"
            if pair in valid_symbols:
                symbols.append(pair)
                break  # 每个 base asset 只取第一个匹配的 quote

    if symbols:
        print(f"  发现 {len(symbols)} 个交易对: {', '.join(symbols)}", file=sys.stderr)
    else:
        print("  未发现任何交易对", file=sys.stderr)

    return symbols


def fetch_and_display(args: argparse.Namespace):
    client = create_client(args.env_file)

    if args.symbol:
        symbols = args.symbol
    else:
        symbols = discover_symbols(client, include_zero_balance=args.all_assets)
        if not symbols:
            print("未发现任何交易过的币种。", file=sys.stderr)
            return

    start_ms = None
    end_ms = None
    if args.start:
        start_ms = date_to_ms(args.start)
    else:
        # 默认 90 天前
        start_ms = int((datetime.now() - timedelta(days=90)).timestamp() * 1000)

    if args.end:
        # 结束日期取当天 23:59:59
        end_ms = date_to_ms(args.end) + 86400000 - 1

    date_desc = []
    if args.start:
        date_desc.append(f"从 {args.start}")
    else:
        date_desc.append("最近 90 天")
    if args.end:
        date_desc.append(f"到 {args.end}")
    print(f"查询交易对: {', '.join(symbols)} ({' '.join(date_desc)})", file=sys.stderr)

    all_trades = []
    for i, symbol in enumerate(symbols):
        print(f"  获取 {symbol} ({i+1}/{len(symbols)}) ...", file=sys.stderr)
        trades = fetch_trades_for_symbol(client, symbol, start_ms, end_ms)
        all_trades.extend(trades)
        if trades:
            print(f"    {len(trades)} 条记录", file=sys.stderr)
        # 每 10 个请求暂停 1 秒，避免触发频率限制
        if (i + 1) % 10 == 0 and i + 1 < len(symbols):
            time.sleep(1)

    if not all_trades:
        print("该时间范围内无成交记录。", file=sys.stderr)
        return

    rows = format_output(all_trades)
    print(f"\n共 {len(rows)} 条成交记录:\n", file=sys.stderr)

    if args.output:
        import csv
        out_path = Path(args.output)
        fieldnames = list(rows[0].keys())
        with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"已导出到 {out_path}", file=sys.stderr)
    else:
        # 打印表格
        header = list(rows[0].keys())
        widths = [max(len(str(r[h])) for r in rows + [{h: h for h in header}]) for h in header]
        fmt = "  ".join(f"{{:<{w}}}" for w in widths)
        print(fmt.format(*header))
        print(fmt.format(*["-" * w for w in widths]))
        for r in rows:
            print(fmt.format(*[str(r[h]) for h in header]))


def main():
    args = parse_args()
    fetch_and_display(args)


if __name__ == "__main__":
    main()
