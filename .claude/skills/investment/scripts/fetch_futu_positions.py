#!/usr/bin/env python3
"""
从富途 OpenD 获取账户持仓和资金概览。

前置条件:
  1. 安装 futu-api:  pip install futu-api
  2. 本地运行 FutuOpenD 并已登录（默认 127.0.0.1:11111）

用法:
  # 查询所有持仓（默认合并美股和港股）
  python fetch_futu_positions.py

  # 只查美股
  python fetch_futu_positions.py --market US

  # 同时显示账户资金明细
  python fetch_futu_positions.py --funds

  # 导出到 CSV
  python fetch_futu_positions.py -o positions.csv
"""

from __future__ import annotations

import argparse
import sys

try:
    from futu import (
        OpenSecTradeContext,
        RET_OK,
        SecurityFirm,
        TrdEnv,
        TrdMarket,
    )
except ImportError:
    print("错误: 请先安装 futu-api:  pip install futu-api", file=sys.stderr)
    sys.exit(1)


MARKET_MAP = {
    "ALL": TrdMarket.NONE,
    "HK": TrdMarket.HK,
    "US": TrdMarket.US,
    "CN": TrdMarket.CN,
}

# 近似汇率，用于统一折算 USD
APPROX_TO_USD = {
    "USD": 1.0,
    "HKD": 0.129,
    "CNH": 0.137,
    "CNY": 0.137,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从富途 OpenD 获取账户持仓和资金概览",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--market", "-m",
        default="ALL",
        choices=list(MARKET_MAP.keys()),
        help="市场（默认 ALL = 所有市场）",
    )
    parser.add_argument(
        "--funds", "-f",
        action="store_true",
        help="显示账户资金明细",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="OpenD 地址（默认 127.0.0.1）",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=11111,
        help="OpenD 端口（默认 11111）",
    )
    parser.add_argument(
        "--output", "-o",
        help="导出持仓到 CSV 文件",
    )
    return parser.parse_args()


def query_positions(ctx, trd_market):
    """查询持仓。"""
    ret, data = ctx.position_list_query(trd_env=TrdEnv.REAL)
    if ret != RET_OK:
        print(f"查询持仓失败: {data}", file=sys.stderr)
        return None
    if data.empty:
        print("无持仓", file=sys.stderr)
        return None
    return data


def query_funds(ctx):
    """查询账户资金。"""
    ret, data = ctx.accinfo_query(trd_env=TrdEnv.REAL)
    if ret != RET_OK:
        print(f"查询资金失败: {data}", file=sys.stderr)
        return None
    return data


def print_positions(data):
    """打印持仓表格。"""
    cols = ["code", "stock_name", "qty", "cost_price", "market_val", "pl_val", "pl_ratio", "currency"]
    available = [c for c in cols if c in data.columns]

    # 计算 USD 等值
    usd_vals = []
    for _, row in data.iterrows():
        rate = APPROX_TO_USD.get(row["currency"], 1.0)
        usd_vals.append(row["market_val"] * rate)
    data = data.copy()
    data["usd_equiv"] = usd_vals

    # 按 USD 等值排序
    data = data.sort_values("usd_equiv", ascending=False)

    print("=== 持仓 ===\n")
    header = ["代码", "名称", "数量", "成本价", "市值", "盈亏", "盈亏%", "币种", "≈USD"]
    fmt = "{:<12s} {:<30s} {:>10s} {:>10s} {:>12s} {:>12s} {:>8s} {:>5s} {:>12s}"
    print(fmt.format(*header))
    print("-" * 120)

    total_usd = 0
    total_pl_usd = 0
    for _, row in data.iterrows():
        rate = APPROX_TO_USD.get(row["currency"], 1.0)
        usd_eq = row["market_val"] * rate
        pl_usd = row["pl_val"] * rate
        total_usd += usd_eq
        total_pl_usd += pl_usd
        print(fmt.format(
            row["code"],
            row["stock_name"][:28],
            f"{row['qty']:.2f}",
            f"{row['cost_price']:.2f}",
            f"{row['market_val']:,.2f}",
            f"{row['pl_val']:+,.2f}",
            f"{row['pl_ratio']:+.1f}%",
            row["currency"],
            f"${usd_eq:,.0f}",
        ))

    print("-" * 120)
    print(f"{'持仓合计':>54s} {'':>12s} {f'${total_pl_usd:+,.0f}':>8s} {'':>5s} ${total_usd:>11,.0f}")
    print()


def print_funds(data):
    """打印账户资金明细。"""
    row = data.iloc[0]
    print("=== 账户资金 ===\n")

    print(f"  总资产:         {row['total_assets']:>15,.2f} {row['currency']}")
    print(f"  证券市值:       {row['market_val']:>15,.2f} {row['currency']}")
    print(f"  现金:           {row['cash']:>15,.2f} {row['currency']}")
    print(f"  购买力:         {row['power']:>15,.2f} {row['currency']}")
    print(f"  可提金额:       {row['avl_withdrawal_cash']:>15,.2f} {row['currency']}")
    print(f"  风险状态:       {row['risk_status']}")
    print(f"  维持保证金:     {row['maintenance_margin']:>15,.2f} {row['currency']}")
    print()

    # 分币种明细
    currencies = [
        ("USD", "us_cash", "usd_assets"),
        ("HKD", "hk_cash", "hkd_assets"),
        ("CNH", "cn_cash", "cnh_assets"),
    ]
    print("  分币种明细:")
    print(f"    {'币种':<6s} {'现金':>15s} {'资产':>15s}")
    print(f"    {'-'*6} {'-'*15} {'-'*15}")
    for label, cash_col, asset_col in currencies:
        cash = row.get(cash_col, 0)
        assets = row.get(asset_col, 0)
        if cash != 0 or assets != 0:
            print(f"    {label:<6s} {cash:>15,.2f} {assets:>15,.2f}")
    print()


def export_csv(data, output_path):
    """导出持仓到 CSV。"""
    from pathlib import Path
    import csv

    cols = ["code", "stock_name", "qty", "cost_price", "market_val", "pl_val", "pl_ratio", "currency"]
    available = [c for c in cols if c in data.columns]

    out = Path(output_path)
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=available)
        writer.writeheader()
        for _, row in data.iterrows():
            writer.writerow({c: row[c] for c in available})
    print(f"已导出到 {out}", file=sys.stderr)


def main():
    args = parse_args()
    trd_market = MARKET_MAP[args.market]

    ctx = OpenSecTradeContext(
        host=args.host,
        port=args.port,
        security_firm=SecurityFirm.FUTUSECURITIES,
        filter_trdmarket=trd_market,
    )

    try:
        positions = query_positions(ctx, trd_market)
        if positions is not None:
            print_positions(positions)
            if args.output:
                export_csv(positions, args.output)

        if args.funds:
            funds = query_funds(ctx)
            if funds is not None:
                print_funds(funds)
    finally:
        ctx.close()


if __name__ == "__main__":
    main()
