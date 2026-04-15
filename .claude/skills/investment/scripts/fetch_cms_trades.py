#!/usr/bin/env python3
"""
从招商证券历史成交页面提取交易记录（通过 Chrome MCP）。

此脚本不能独立运行——它生成 JavaScript 代码片段，由 Claude 通过
Chrome DevTools MCP 在已登录的招商证券网页交易页面上执行。

前置条件:
  1. 在浏览器中登录招商证券网页交易: https://xtrade.newone.com.cn
  2. 导航到 历史成交 页面: https://xtrade.newone.com.cn/npctrade#/trade/ptjy/cx?page=lscj
  3. Chrome DevTools MCP 已连接到该页面

用法 (由 Claude 调用):
  # 生成提取数据的 JS 代码
  python fetch_cms_trades.py js --start 2025-10-01 --end 2026-03-22

  # 将 Chrome MCP 返回的 JSON 数据转为 CSV
  python fetch_cms_trades.py convert --json '<json_data>' -o trades.csv

  # 或从文件读取 JSON
  python fetch_cms_trades.py convert --json-file /tmp/cms_raw.json -o trades.csv

典型 Claude 工作流:
  1. Claude 执行 `python fetch_cms_trades.py js --start ... --end ...` 获取 JS
  2. Claude 通过 chrome-devtools evaluate_script 执行该 JS
  3. Claude 将返回的 JSON 传给 `python fetch_cms_trades.py convert ...`
  4. Claude 执行 `python write_trade_journal.py import-cms trades.csv` 导入
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

# 招商证券名称到交易日志品种名的映射
NAME_MAP = {
    "有色金属ETF": "有色金属ETF",
    "有色ETF大成": "有色ETF (大成)",
    "上证50ETF易方达": "上证50ETF",
    "工业有色ETF万家": "工业有色ETF (万家)",
}

# 需要跳过的操作类型（非买卖交易）
SKIP_OPS = {"股息入账", "红利入账", "配股入账", "送股入账", "转托管"}


def generate_js(start_date: str, end_date: str) -> str:
    """生成在招商证券页面执行的 JavaScript 代码。

    该 JS 代码会:
    1. 找到 lscj (历史成交) Vue 组件
    2. 设置日期范围
    3. 触发查询
    4. 等待数据加载
    5. 从 DOM 提取所有行数据并返回 JSON
    """
    return f"""async () => {{
  // 找到日期选择器 Vue 实例和父组件
  const picker = document.querySelector('.cmsui-date-picker.range-picker').__vue__;
  const lscj = picker.$parent;

  // 设置日期范围
  lscj.range = {{ start: '{start_date}', end: '{end_date}' }};
  lscj.dateChange(lscj.range);

  // 触发查询
  lscj.fetchDataLscj();

  // 等待数据加载
  await new Promise(resolve => setTimeout(resolve, 2000));

  // 从 DOM 提取表格数据
  const tbody = document.querySelector('.cmsui-table_body tbody');
  if (!tbody) return JSON.stringify({{ error: '未找到数据表格', trades: [] }});

  const rows = tbody.querySelectorAll('tr');
  const trades = Array.from(rows).map(row => {{
    const cells = row.querySelectorAll('td');
    const values = Array.from(cells).map(c => c.textContent.trim());
    return {{
      证券代码: values[0] || '',
      证券名称: values[1] || '',
      成交日期: values[2] || '',
      成交时间: values[3] || '',
      买卖标志: values[4] || '',
      成交价格: values[5] || '',
      成交数量: values[6] || '',
      成交金额: values[7] || '',
      成交编号: values[8] || '',
      委托编号: values[9] || '',
      股东代码: values[10] || ''
    }};
  }});

  return JSON.stringify({{
    count: trades.length,
    dateRange: {{ start: '{start_date}', end: '{end_date}' }},
    trades: trades
  }});
}}"""


def convert_to_csv(raw_data: list[dict], output_path: str | None = None) -> list[dict]:
    """将原始交易数据转为标准 CSV 格式。

    返回转换后的行列表。如果指定 output_path 则同时写入文件。
    """
    rows = []
    for trade in raw_data:
        op = trade.get("买卖标志", "")
        if op in SKIP_OPS:
            print(f"  跳过非交易记录: {trade.get('证券名称', '')} {op} {trade.get('成交日期', '')}", file=sys.stderr)
            continue

        name = trade.get("证券名称", "")
        mapped_name = NAME_MAP.get(name, name)

        qty_str = trade.get("成交数量", "0")
        qty = abs(float(qty_str))

        rows.append({
            "证券代码": trade.get("证券代码", ""),
            "证券名称": mapped_name,
            "成交日期": trade.get("成交日期", ""),
            "成交时间": trade.get("成交时间", ""),
            "买卖标志": op,
            "成交价格": trade.get("成交价格", ""),
            "成交数量": str(qty),
            "成交金额": trade.get("成交金额", ""),
            "成交编号": trade.get("成交编号", ""),
        })

    rows.sort(key=lambda r: r["成交日期"])

    if output_path:
        fieldnames = ["证券代码", "证券名称", "成交日期", "成交时间", "买卖标志",
                       "成交价格", "成交数量", "成交金额", "成交编号"]
        with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"已导出 {len(rows)} 条记录到 {output_path}", file=sys.stderr)

    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="招商证券历史成交数据提取工具（Chrome MCP）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # js 命令 - 生成 JavaScript
    js_parser = subparsers.add_parser("js", help="生成提取数据的 JavaScript 代码")
    js_parser.add_argument("--start", "-s", required=True, help="开始日期 (YYYY-MM-DD)")
    js_parser.add_argument("--end", "-e", required=True, help="结束日期 (YYYY-MM-DD)")

    # convert 命令 - JSON 转 CSV
    conv_parser = subparsers.add_parser("convert", help="将 JSON 数据转为 CSV")
    conv_group = conv_parser.add_mutually_exclusive_group(required=True)
    conv_group.add_argument("--json", help="JSON 字符串（Chrome MCP 返回的数据）")
    conv_group.add_argument("--json-file", help="JSON 文件路径")
    conv_parser.add_argument("--output", "-o", required=True, help="输出 CSV 路径")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == "js":
        print(generate_js(args.start, args.end))

    elif args.command == "convert":
        if args.json:
            data = json.loads(args.json)
        else:
            with open(args.json_file, encoding="utf-8") as f:
                data = json.load(f)

        trades = data.get("trades", data) if isinstance(data, dict) else data
        print(f"读取 {len(trades)} 条原始记录", file=sys.stderr)

        convert_to_csv(trades, args.output)

    else:
        print("请指定子命令: js, convert", file=sys.stderr)
        print("使用 --help 查看用法", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
