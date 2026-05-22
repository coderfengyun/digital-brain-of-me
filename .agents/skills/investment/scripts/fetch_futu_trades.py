#!/usr/bin/env python3
"""
从富途 OpenD 获取历史成交记录。

前置条件:
  1. 安装 futu-api:  pip install futu-api
  2. 本地运行 FutuOpenD 并已登录（默认 127.0.0.1:11111）

用法:
  # 查询最近 90 天的成交
  python fetch_futu_trades.py

  # 指定日期范围
  python fetch_futu_trades.py --start 2026-02-28 --end 2026-03-09

  # 只查美股市场
  python fetch_futu_trades.py --start 2026-03-01 --end 2026-03-09 --market US

  # 导出到 CSV
  python fetch_futu_trades.py --start 2026-03-01 --end 2026-03-09 -o trades.csv
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

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
    "NONE": TrdMarket.NONE,
    "HK": TrdMarket.HK,
    "US": TrdMarket.US,
    "CN": TrdMarket.CN,
    "SG": TrdMarket.SG,
    "JP": TrdMarket.JP,
}

SIDE_LABEL = {"BUY": "买入", "SELL": "卖出"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从富途 OpenD 获取历史成交记录",
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
        "--market", "-m",
        choices=list(MARKET_MAP.keys()),
        default="NONE",
        help="筛选市场 (默认 NONE = 全部)",
    )
    parser.add_argument(
        "--code", "-c",
        default="",
        help="筛选证券代码，如 US.BNO",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="OpenD 地址 (默认 127.0.0.1)",
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=11111,
        help="OpenD 端口 (默认 11111)",
    )
    parser.add_argument(
        "--acc-id",
        type=int,
        default=0,
        help="交易账号 ID (默认 0 = 第一个账号)",
    )
    parser.add_argument(
        "--output", "-o",
        help="输出 CSV 文件路径（不指定则打印到终端）",
    )
    parser.add_argument(
        "--security-firm",
        choices=["FUTUSECURITIES", "FUTUINC"],
        default="FUTUSECURITIES",
        help="券商 (默认 FUTUSECURITIES，美国用户用 FUTUINC)",
    )
    return parser.parse_args()


def format_date(date_str: str | None, default_offset_days: int = 0) -> str:
    """Normalize a date string to 'YYYY-MM-DD 00:00:00', or return '' for API default."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"错误: 日期格式不正确 '{date_str}'，需要 YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def fetch_deals(args: argparse.Namespace):
    firm = getattr(SecurityFirm, args.security_firm)
    market = MARKET_MAP[args.market]

    print(f"连接 OpenD @ {args.host}:{args.port} ...", file=sys.stderr)
    trd_ctx = OpenSecTradeContext(
        filter_trdmarket=market,
        host=args.host,
        port=args.port,
        security_firm=firm,
    )

    try:
        start = format_date(args.start)
        end = format_date(args.end)

        date_desc = []
        if start:
            date_desc.append(f"从 {args.start}")
        if end:
            date_desc.append(f"到 {args.end}")
        if not date_desc:
            date_desc.append("最近 90 天")
        print(f"查询历史成交 ({' '.join(date_desc)}) ...", file=sys.stderr)

        ret, data = trd_ctx.history_deal_list_query(
            code=args.code,
            start=start,
            end=end,
            acc_id=args.acc_id,
        )

        if ret != RET_OK:
            print(f"错误: API 返回失败 — {data}", file=sys.stderr)
            sys.exit(1)

        if data.empty:
            print("该时间范围内无成交记录。", file=sys.stderr)
            return

        columns_to_show = [
            "create_time", "trd_side", "code", "stock_name",
            "qty", "price", "deal_id", "order_id", "status",
        ]
        available = [c for c in columns_to_show if c in data.columns]
        display_df = data[available].copy()

        display_df = display_df.sort_values("create_time").reset_index(drop=True)

        if "trd_side" in display_df.columns:
            display_df["trd_side"] = display_df["trd_side"].map(
                lambda x: SIDE_LABEL.get(x, x)
            )

        display_df.columns = [
            col.replace("create_time", "成交时间")
            .replace("trd_side", "方向")
            .replace("code", "代码")
            .replace("stock_name", "名称")
            .replace("qty", "数量")
            .replace("price", "成交价")
            .replace("deal_id", "成交编号")
            .replace("order_id", "订单编号")
            .replace("status", "状态")
            for col in display_df.columns
        ]

        print(f"\n共 {len(display_df)} 条成交记录:\n", file=sys.stderr)

        if args.output:
            out_path = Path(args.output)
            display_df.to_csv(out_path, index=False, encoding="utf-8-sig")
            print(f"已导出到 {out_path}", file=sys.stderr)
        else:
            print(display_df.to_string(index=False))

    finally:
        trd_ctx.close()


def main():
    args = parse_args()
    fetch_deals(args)


if __name__ == "__main__":
    main()
