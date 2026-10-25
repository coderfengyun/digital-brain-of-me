#!/usr/bin/env python3
"""从富途 OpenD 按清算日读取账户现金流水。

富途部分账户不支持用起止日期一次查询资金流水，只支持
``clearing_date`` 单日查询。本脚本逐日调用该接口，并默认只保留股息和
相关公司行动服务费。
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

try:
    from futu import OpenSecTradeContext, RET_OK, SecurityFirm, TrdEnv, TrdMarket
except ImportError:
    print("错误: 请先安装 futu-api", file=sys.stderr)
    sys.exit(1)


DIVIDEND_MARKERS = ("dividend", "股息", "红利")
RELATED_FEE_MARKERS = ("corporate action service fee", "公司行动服务费")

OUTPUT_COLUMNS = {
    "cashflow_id": "流水编号",
    "clearing_date": "清算日期",
    "settlement_date": "交收日期",
    "currency": "币种",
    "cashflow_type": "类型",
    "cashflow_direction": "方向",
    "cashflow_amount": "金额",
    "cashflow_remark": "备注",
    "create_time": "创建时间",
}


def parse_args() -> argparse.Namespace:
    today = date.today()
    parser = argparse.ArgumentParser(
        description="从富途 OpenD 读取现金流水（默认只显示股息及相关费用）"
    )
    parser.add_argument("--start", default=(today - timedelta(days=30)).isoformat())
    parser.add_argument("--end", default=today.isoformat())
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=11111)
    parser.add_argument("--acc-id", type=int, default=0)
    parser.add_argument(
        "--security-firm",
        choices=["FUTUSECURITIES", "FUTUINC"],
        default="FUTUSECURITIES",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.6,
        help="逐日请求间隔秒数；默认 1.6，以满足每 30 秒最多 20 次的限制",
    )
    parser.add_argument("--all", action="store_true", help="显示所有现金流水")
    parser.add_argument("--output", "-o", help="导出 CSV；不指定则打印到终端")
    return parser.parse_args()


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        print(f"错误: 日期格式不正确 '{value}'，需要 YYYY-MM-DD", file=sys.stderr)
        raise SystemExit(2)


def iter_dates(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def is_dividend_related(row: pd.Series) -> bool:
    flow_type = str(row.get("cashflow_type", "")).lower()
    remark = str(row.get("cashflow_remark", "")).lower()
    text = f"{flow_type} {remark}"
    return any(marker in text for marker in DIVIDEND_MARKERS + RELATED_FEE_MARKERS)


def fetch_cashflows(args: argparse.Namespace) -> pd.DataFrame:
    start = parse_date(args.start)
    end = parse_date(args.end)
    if start > end:
        print("错误: 起始日期不能晚于结束日期", file=sys.stderr)
        raise SystemExit(2)
    if args.interval < 0:
        print("错误: --interval 不能为负数", file=sys.stderr)
        raise SystemExit(2)

    firm = getattr(SecurityFirm, args.security_firm)
    ctx = OpenSecTradeContext(
        filter_trdmarket=TrdMarket.NONE,
        host=args.host,
        port=args.port,
        security_firm=firm,
    )

    frames: list[pd.DataFrame] = []
    errors: list[tuple[str, str]] = []
    days = list(iter_dates(start, end))
    print(f"逐日查询富途现金流水：{start}～{end}（{len(days)} 天）", file=sys.stderr)

    try:
        for index, clearing_day in enumerate(days):
            ret, data = ctx.get_acc_cash_flow(
                clearing_date=clearing_day.isoformat(),
                trd_env=TrdEnv.REAL,
                acc_id=args.acc_id,
            )
            if ret == RET_OK:
                if not data.empty:
                    frames.append(data.copy())
            else:
                errors.append((clearing_day.isoformat(), str(data)))

            if index < len(days) - 1 and args.interval:
                time.sleep(args.interval)
    finally:
        ctx.close()

    if errors:
        for clearing_day, message in errors:
            print(f"警告: {clearing_day} 查询失败 — {message}", file=sys.stderr)

    if not frames:
        result = pd.DataFrame(columns=list(OUTPUT_COLUMNS))
    else:
        result = pd.concat(frames, ignore_index=True)
        if "cashflow_id" in result.columns:
            result = result.drop_duplicates(subset=["cashflow_id"], keep="last")
        result = result.sort_values(
            [column for column in ("clearing_date", "cashflow_id") if column in result.columns]
        ).reset_index(drop=True)

    if not args.all and not result.empty:
        result = result[result.apply(is_dividend_related, axis=1)].reset_index(drop=True)

    available = [column for column in OUTPUT_COLUMNS if column in result.columns]
    display = result[available].rename(columns=OUTPUT_COLUMNS)

    if display.empty:
        print("该时间范围内无相关现金流水。", file=sys.stderr)
    elif args.output:
        output_path = Path(args.output)
        display.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"已导出 {len(display)} 条记录到 {output_path}", file=sys.stderr)
    else:
        print(display.to_string(index=False))

    return display


def main():
    fetch_cashflows(parse_args())


if __name__ == "__main__":
    main()
