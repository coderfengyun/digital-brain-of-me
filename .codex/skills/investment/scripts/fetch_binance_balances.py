#!/usr/bin/env python3
"""
从币安获取账户全部资产余额及 USD 估值。

前置条件:
  1. 安装依赖:  pip install python-binance python-dotenv
  2. 在项目根目录创建 .env 文件，填入:
     BINANCE_API_KEY=your_key
     BINANCE_API_SECRET=your_secret

用法:
  # 查看所有有余额的资产
  python fetch_binance_balances.py

  # 包含余额为 0 的资产（空投灰尘等）
  python fetch_binance_balances.py --all

  # 导出到 CSV
  python fetch_binance_balances.py -o balances.csv

  # 指定 .env 文件路径
  python fetch_binance_balances.py --env-file /path/to/.env
"""

from __future__ import annotations

import argparse
import sys
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

# 稳定币和法币（USD 等价物）
STABLECOINS = {"USDT", "USDC", "BUSD", "TUSD", "FDUSD", "USD"}

# LD 前缀是 Binance Earn 活期理财产品
EARN_PREFIX = "LD"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从币安获取账户资产余额及 USD 估值",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        dest="show_all",
        help="显示所有资产（包括余额为 0 的）",
    )
    parser.add_argument(
        "--output", "-o",
        help="导出到 CSV 文件",
    )
    parser.add_argument(
        "--env-file",
        default=None,
        help=".env 文件路径（默认项目根目录 .env）",
    )
    return parser.parse_args()


def find_env_file(specified_path: str | None) -> str | None:
    """查找 .env 文件。"""
    if specified_path:
        return specified_path
    current = Path(__file__).resolve().parent
    for _ in range(5):
        env_path = current / ".env"
        if env_path.exists():
            return str(env_path)
        current = current.parent
    return None


def get_real_ticker(asset: str) -> str:
    """去掉 LD 前缀获取真实 ticker。"""
    if asset.startswith(EARN_PREFIX) and asset != "LDO":  # LDO 是 Lido DAO，不是 Earn
        return asset[len(EARN_PREFIX):]
    return asset


def fetch_balances(client: Client, show_all: bool) -> list[dict]:
    """获取账户余额并计算 USD 价值。"""
    account = client.get_account()

    # 获取所有价格
    prices = {p["symbol"]: float(p["price"]) for p in client.get_all_tickers()}

    assets = []
    for b in account["balances"]:
        free = float(b["free"])
        locked = float(b["locked"])
        total = free + locked

        if not show_all and total == 0:
            continue

        asset = b["asset"]
        real_ticker = get_real_ticker(asset)
        is_earn = asset != real_ticker

        # 计算 USD 价值
        if real_ticker in STABLECOINS:
            usd_price = 1.0
            usd_value = total
        else:
            symbol = f"{real_ticker}USDT"
            if symbol in prices:
                usd_price = prices[symbol]
                usd_value = total * usd_price
            else:
                usd_price = 0
                usd_value = 0

        is_stable = real_ticker in STABLECOINS

        assets.append({
            "asset": asset,
            "real_ticker": real_ticker,
            "is_earn": is_earn,
            "free": free,
            "locked": locked,
            "total": total,
            "usd_price": usd_price,
            "usd_value": usd_value,
            "category": "稳定币" if is_stable else "加密货币",
        })

    # 按 USD 价值排序
    assets.sort(key=lambda x: -x["usd_value"])
    return assets


def print_balances(assets: list[dict]):
    """打印资产表格。"""
    print("=== 币安账户资产 ===\n")

    header = ["资产", "底层", "数量", "单价(USD)", "价值(USD)", "类型"]
    fmt = "{:<12s} {:<8s} {:>14s} {:>12s} {:>12s} {:<8s}"
    print(fmt.format(*header))
    print("-" * 72)

    total_usd = 0
    total_stable = 0
    total_crypto = 0

    for a in assets:
        if a["usd_value"] < 0.01 and a["total"] > 0:
            continue  # 跳过价值太小的灰尘

        label = a["asset"]
        if a["is_earn"]:
            label = f"{a['asset']}({a['real_ticker']})"

        print(fmt.format(
            label,
            "Earn" if a["is_earn"] else "",
            f"{a['total']:.4f}" if a["total"] < 1000 else f"{a['total']:,.2f}",
            f"${a['usd_price']:,.2f}",
            f"${a['usd_value']:,.2f}",
            a["category"],
        ))

        total_usd += a["usd_value"]
        if a["category"] == "稳定币":
            total_stable += a["usd_value"]
        else:
            total_crypto += a["usd_value"]

    print("-" * 72)
    print(f"{'合计':<12s} {'':>8s} {'':>14s} {'':>12s} ${total_usd:>11,.2f}")
    print()
    print(f"  稳定币:     ${total_stable:>11,.2f}")
    print(f"  加密货币:   ${total_crypto:>11,.2f}")
    print()


def export_csv(assets: list[dict], output_path: str):
    """导出到 CSV。"""
    import csv
    fields = ["asset", "real_ticker", "is_earn", "total", "usd_price", "usd_value", "category"]
    out = Path(output_path)
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for a in assets:
            writer.writerow({k: a[k] for k in fields})
    print(f"已导出到 {out}", file=sys.stderr)


def main():
    args = parse_args()

    env_path = find_env_file(args.env_file)
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

    client = Client(api_key, api_secret)
    assets = fetch_balances(client, args.show_all)

    if not assets:
        print("无资产余额。", file=sys.stderr)
        return

    print_balances(assets)

    if args.output:
        export_csv(assets, args.output)


if __name__ == "__main__":
    main()
