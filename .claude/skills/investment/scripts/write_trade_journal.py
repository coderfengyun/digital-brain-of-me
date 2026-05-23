#!/usr/bin/env python3
"""
交易日志汇总表 写入工具。

功能：
  - 向 交易日志汇总表.csv 中插入新交易记录
  - 自动按日期排序、自动编号
  - 校验数据符合 交易日志汇总表.schema.json 约束
  - 支持从币安 CSV 导入

用法：
  # 手动添加一条记录
  python write_trade_journal.py add \
    --品种 BTC --操作 买入 --价格 76653 --数量 0.00391 --金额 299.71 \
    --币种 USD --日期 2025-04-07 --备注 "币安API精确数据"

  # 从币安导出 CSV 导入
  python write_trade_journal.py import-binance trades.csv

  # 迁移旧格式 CSV 到新 schema 格式
  python write_trade_journal.py migrate

  # 校验现有 CSV 是否符合 schema
  python write_trade_journal.py validate
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

def _find_project_root() -> Path:
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / ".git").exists():
            return p
        p = p.parent
    return Path(__file__).resolve().parent

REPO_ROOT = _find_project_root()
PROJECT_DIR = REPO_ROOT / "investment" / "投资日志整理"
CSV_PATH = PROJECT_DIR / "交易日志汇总表.csv"
SCHEMA_PATH = PROJECT_DIR / "交易日志汇总表.schema.json"

SCHEMA_FIELDS = ["序号", "品种", "操作类型", "价格", "数量", "金额", "币种", "日期", "日期精确度", "交易平台", "备注"]
VALID_CURRENCIES = {"CNY", "USD", "HKD"}
VALID_OPS = {"买入", "卖出"}
VALID_PRECISION = {"精确", "周期范围"}
VALID_PLATFORMS = {"币安", "富途", "招行", "招商证券", "其他"}


def load_schema() -> dict:
    """加载 schema 定义。"""
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_csv() -> list[dict]:
    """读取现有 CSV，返回记录列表。"""
    if not CSV_PATH.exists():
        return []
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_csv(rows: list[dict]):
    """将记录写入 CSV，自动按日期排序并重新编号。"""
    # 按日期排序
    rows.sort(key=lambda r: r.get("日期", ""))
    # 重新编号
    for i, row in enumerate(rows, 1):
        row["序号"] = str(i)
    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"已写入 {len(rows)} 条记录到 {CSV_PATH}", file=sys.stderr)


def validate_row(row: dict) -> list[str]:
    """校验单条记录，返回错误列表（空列表表示通过）。"""
    errors = []

    # 必填字段
    for field in ["品种", "操作类型", "价格", "数量", "金额", "币种", "日期", "日期精确度", "交易平台"]:
        if not row.get(field):
            errors.append(f"缺少必填字段: {field}")

    # 操作类型
    if row.get("操作类型") and row["操作类型"] not in VALID_OPS:
        errors.append(f"操作类型必须为 买入/卖出，当前: {row['操作类型']}")

    # 币种
    if row.get("币种") and row["币种"] not in VALID_CURRENCIES:
        errors.append(f"币种必须为 CNY/USD/HKD，当前: {row['币种']}")

    # 日期精确度
    if row.get("日期精确度") and row["日期精确度"] not in VALID_PRECISION:
        errors.append(f"日期精确度必须为 精确/周期范围，当前: {row['日期精确度']}")

    # 交易平台
    if row.get("交易平台") and row["交易平台"] not in VALID_PLATFORMS:
        errors.append(f"交易平台必须为 {'/'.join(sorted(VALID_PLATFORMS))}，当前: {row['交易平台']}")

    # 数值字段不含货币符号或单位
    for field in ["价格", "数量", "金额"]:
        val = row.get(field, "")
        if val and re.search(r"[^\d.\-]", str(val)):
            errors.append(f"{field} 包含非数字字符: {val}")

    # 价格×数量 与 金额 偏差校验
    try:
        price = float(row.get("价格", 0))
        qty = float(row.get("数量", 0))
        amount = float(row.get("金额", 0))
        if price > 0 and qty > 0 and amount > 0:
            expected = price * qty
            deviation = abs(expected - amount) / amount
            if deviation > 0.01:
                errors.append(
                    f"金额偏差 {deviation:.2%} 超过 1%: "
                    f"价格({price}) × 数量({qty}) = {expected:.2f}, 金额 = {amount}"
                )
    except (ValueError, TypeError):
        pass  # 数值格式错误已在上面检出

    # 日期格式
    date_val = row.get("日期", "")
    if date_val:
        try:
            datetime.strptime(date_val, "%Y-%m-%d")
        except ValueError:
            errors.append(f"日期格式不正确（需 YYYY-MM-DD）: {date_val}")

    return errors


def validate_csv():
    """校验整个 CSV 文件。"""
    rows = load_csv()
    if not rows:
        print("CSV 文件为空或不存在", file=sys.stderr)
        return

    total_errors = 0
    for i, row in enumerate(rows, 1):
        errs = validate_row(row)
        if errs:
            total_errors += len(errs)
            print(f"第 {i} 行:", file=sys.stderr)
            for e in errs:
                print(f"  ✗ {e}", file=sys.stderr)

    if total_errors == 0:
        print(f"全部 {len(rows)} 条记录校验通过 ✓", file=sys.stderr)
    else:
        print(f"\n共 {total_errors} 个错误", file=sys.stderr)


def add_record(
    品种: str,
    操作类型: str,
    价格: float,
    数量: float,
    金额: float,
    币种: str,
    日期: str,
    日期精确度: str = "精确",
    交易平台: str = "其他",
    备注: str = "",
) -> dict:
    """构造并校验一条新记录，追加到 CSV。"""
    row = {
        "序号": "",  # 保存时自动编号
        "品种": 品种,
        "操作类型": 操作类型,
        "价格": str(价格),
        "数量": str(数量),
        "金额": str(金额),
        "币种": 币种,
        "日期": 日期,
        "日期精确度": 日期精确度,
        "交易平台": 交易平台,
        "备注": 备注,
    }
    errors = validate_row(row)
    if errors:
        print(f"记录校验失败:", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)

    rows = load_csv()
    rows.append(row)
    save_csv(rows)
    return row


def parse_old_price(val: str) -> tuple[float, str]:
    """解析旧格式价格字段如 '76653 $' -> (76653.0, 'USD')。"""
    val = val.strip()
    currency_map = {"$": "USD", "￥": "CNY", "HKD": "HKD"}
    for suffix, cur in currency_map.items():
        if val.endswith(suffix):
            num = val[: -len(suffix)].strip()
            return float(num), cur
    # 尝试提取 $/股、￥/g 等单位
    m = re.match(r"([\d.]+)\s*([$￥])", val)
    if m:
        return float(m.group(1)), currency_map.get(m.group(2), "CNY")
    return float(val), "CNY"


def parse_old_amount(val: str) -> tuple[float, str]:
    """解析旧格式金额字段如 '299.71 $' -> (299.71, 'USD')。"""
    return parse_old_price(val)


def parse_old_qty(val: str) -> float:
    """解析旧格式数量字段如 '0.00391 个'、'2g'、'6300 股'、'≈65 股'。"""
    val = val.strip()
    # 去掉 ≈ 前缀
    val = val.lstrip("≈").strip()
    # 去掉单位后缀
    val = re.sub(r"\s*(个|g|股|HKD)$", "", val).strip()
    return float(val)


def parse_old_date(val: str) -> tuple[str, str]:
    """解析旧格式日期，返回 (YYYY-MM-DD, 精确度)。

    支持格式:
      - '4/7/2025' -> ('2025-04-07', '精确')
      - '2025-05-18 ~ 05-25' -> ('2025-05-18', '周期范围')
      - '2025-06-22 ~ 06-29' -> ('2025-06-22', '周期范围')
      - '2025-12-29 ~ 2026-01-23' -> ('2025-12-29', '周期范围')
    """
    val = val.strip()
    # 范围日期
    if "~" in val:
        start = val.split("~")[0].strip()
        # 确保是 YYYY-MM-DD 格式
        if re.match(r"\d{4}-\d{2}-\d{2}", start):
            return start, "周期范围"
        # M/D/YYYY 格式
        m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", start)
        if m:
            return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}", "周期范围"
        return start, "周期范围"

    # M/D/YYYY 精确日期
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})$", val)
    if m:
        return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}", "精确"

    # YYYY-MM-DD
    if re.match(r"\d{4}-\d{2}-\d{2}$", val):
        return val, "精确"

    return val, "精确"


def migrate_csv():
    """将旧格式 CSV 迁移到 schema 格式。"""
    if not CSV_PATH.exists():
        print("CSV 文件不存在", file=sys.stderr)
        return

    with open(CSV_PATH, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        old_fields = reader.fieldnames
        old_rows = list(reader)

    print(f"读取 {len(old_rows)} 条旧格式记录", file=sys.stderr)
    print(f"旧字段: {old_fields}", file=sys.stderr)

    # 检测是否已经是新格式
    if old_fields and "币种" in old_fields and "日期精确度" in old_fields:
        print("CSV 已经是新格式，无需迁移", file=sys.stderr)
        return

    new_rows = []
    errors = []
    for i, old in enumerate(old_rows, 1):
        try:
            # 解析价格 -> 数值 + 币种
            price_val, currency = parse_old_price(old.get("价格", ""))
            # 解析金额 -> 数值 + 币种（校验一致性）
            amount_val, amt_currency = parse_old_amount(old.get("金额", ""))

            # 金额币种应与价格币种一致
            if currency != amt_currency:
                # 特殊处理：有些 HKD 价格用 HKD 后缀
                price_str = old.get("价格", "")
                if "HKD" in price_str:
                    currency = "HKD"

            qty_val = parse_old_qty(old.get("数量", ""))
            date_val, precision = parse_old_date(old.get("操作时间", ""))

            new_row = {
                "序号": "",
                "品种": old.get("品种", ""),
                "操作类型": old.get("买入/卖出", ""),
                "价格": str(round(price_val, 2)),
                "数量": str(round(qty_val, 8)),  # crypto 需要高精度
                "金额": str(round(amount_val, 2)),
                "币种": currency,
                "日期": date_val,
                "日期精确度": precision,
                "交易平台": old.get("交易平台", "其他"),
                "备注": old.get("备注", ""),
            }

            row_errors = validate_row(new_row)
            if row_errors:
                errors.append((i, new_row, row_errors))

            new_rows.append(new_row)
        except Exception as e:
            errors.append((i, old, [str(e)]))

    if errors:
        print(f"\n迁移中发现 {len(errors)} 条记录有问题:", file=sys.stderr)
        for idx, row, errs in errors:
            print(f"  第 {idx} 行 ({row.get('品种', '?')} {row.get('日期', '?')}):", file=sys.stderr)
            for e in errs:
                print(f"    ✗ {e}", file=sys.stderr)

    # 备份旧文件
    backup_path = CSV_PATH.with_suffix(".csv.bak")
    CSV_PATH.rename(backup_path)
    print(f"\n旧文件已备份到 {backup_path}", file=sys.stderr)

    save_csv(new_rows)
    print("迁移完成!", file=sys.stderr)


def import_binance(csv_path: str):
    """从币安导出 CSV 导入交易记录。

    币安 CSV 格式（由 fetch_binance_trades.py 生成）：
      成交时间,交易对,方向,数量,成交价,金额,手续费,手续费币种,成交编号

    同一时间戳+同一价格的订单会合并为一笔。
    """
    input_path = Path(csv_path)
    if not input_path.exists():
        print(f"文件不存在: {csv_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        raw_trades = list(reader)

    print(f"读取 {len(raw_trades)} 条币安原始记录", file=sys.stderr)

    # 聚合同一时间戳 + 同一交易对 + 同一方向 + 同一价格的订单
    aggregated: dict[str, dict] = {}
    for t in raw_trades:
        ts = t["成交时间"]
        symbol = t["交易对"]
        side = t["方向"]
        price = float(t["成交价"])
        key = f"{ts}|{symbol}|{side}|{price}"

        if key not in aggregated:
            aggregated[key] = {
                "成交时间": ts,
                "交易对": symbol,
                "方向": side,
                "成交价": price,
                "数量": 0.0,
                "金额": 0.0,
            }
        aggregated[key]["数量"] += float(t["数量"])
        aggregated[key]["金额"] += float(t["金额"])

    # 进一步聚合：同一秒内同一交易对同一方向（不同成交价的拆单也合并）
    time_aggregated: dict[str, dict] = {}
    for v in aggregated.values():
        ts = v["成交时间"]
        symbol = v["交易对"]
        side = v["方向"]
        key2 = f"{ts}|{symbol}|{side}"

        if key2 not in time_aggregated:
            time_aggregated[key2] = {
                "成交时间": ts,
                "交易对": symbol,
                "方向": side,
                "数量": 0.0,
                "金额": 0.0,
            }
        time_aggregated[key2]["数量"] += v["数量"]
        time_aggregated[key2]["金额"] += v["金额"]

    # 计算加权均价
    orders = []
    for v in time_aggregated.values():
        qty = v["数量"]
        amount = v["金额"]
        avg_price = amount / qty if qty > 0 else 0
        orders.append({**v, "均价": avg_price})

    orders.sort(key=lambda x: x["成交时间"])
    print(f"聚合为 {len(orders)} 笔订单", file=sys.stderr)

    # 币种映射
    symbol_to_asset = {
        "BTCUSDT": "BTC",
        "ETHUSDT": "ETH",
        "XRPUSDT": "XRP",
        "BNBUSDT": "BNB",
        "SOLUSDT": "SOL",
        "DOGEUSDT": "DOGE",
    }

    # 转为 schema 格式
    existing_rows = load_csv()
    new_count = 0

    for order in orders:
        symbol = order["交易对"]
        asset = symbol_to_asset.get(symbol, symbol.replace("USDT", ""))
        date_str = order["成交时间"][:10]  # YYYY-MM-DD

        # 检查是否已存在（同日期、同品种、同方向、金额接近）
        duplicate = False
        for existing in existing_rows:
            if (
                existing.get("品种") == asset
                and existing.get("操作类型") == order["方向"]
                and existing.get("日期") == date_str
            ):
                try:
                    existing_amount = float(existing.get("金额", 0))
                    if abs(existing_amount - order["金额"]) / max(order["金额"], 0.01) < 0.02:
                        duplicate = True
                        break
                except (ValueError, TypeError):
                    pass

        if duplicate:
            print(f"  跳过重复: {asset} {order['方向']} {date_str} ${order['金额']:.2f}", file=sys.stderr)
            continue

        row = {
            "序号": "",
            "品种": asset,
            "操作类型": order["方向"],
            "价格": str(round(order["均价"], 2)),
            "数量": str(round(order["数量"], 8)),
            "金额": str(round(order["金额"], 2)),
            "币种": "USD",
            "日期": date_str,
            "日期精确度": "精确",
            "交易平台": "币安",
            "备注": "币安API精确数据",
        }

        errors = validate_row(row)
        if errors:
            print(f"  校验失败 ({asset} {date_str}):", file=sys.stderr)
            for e in errors:
                print(f"    ✗ {e}", file=sys.stderr)
            continue

        existing_rows.append(row)
        new_count += 1
        print(f"  新增: {asset} {order['方向']} {date_str} ${order['金额']:.2f}", file=sys.stderr)

    if new_count > 0:
        save_csv(existing_rows)
        print(f"\n新增 {new_count} 条记录", file=sys.stderr)
    else:
        print("\n无新记录需要添加", file=sys.stderr)


def import_futu(csv_path: str):
    """从富途导出 CSV 导入交易记录。

    富途 CSV 格式（由 fetch_futu_trades.py 生成）：
      成交时间,方向,代码,名称,数量,成交价,成交编号,订单编号,状态

    代码前缀决定币种：US.→USD, HK.→HKD, SH./SZ.→CNY。
    同一秒内同一代码同一方向的记录会合并。
    """
    input_path = Path(csv_path)
    if not input_path.exists():
        print(f"文件不存在: {csv_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        raw_trades = list(reader)

    print(f"读取 {len(raw_trades)} 条富途原始记录", file=sys.stderr)

    # 按秒级时间戳 + 代码 + 方向聚合（拆单合并）
    aggregated: dict[str, dict] = {}
    for t in raw_trades:
        ts = t["成交时间"][:19]  # 截断毫秒
        code = t["代码"]
        side = t["方向"]
        key = f"{ts}|{code}|{side}"

        qty = float(t["数量"])
        price = float(t["成交价"])
        amount = qty * price

        if key not in aggregated:
            aggregated[key] = {
                "成交时间": ts,
                "代码": code,
                "名称": t["名称"],
                "方向": side,
                "数量": 0.0,
                "金额": 0.0,
            }
        aggregated[key]["数量"] += qty
        aggregated[key]["金额"] += amount

    orders = []
    for v in aggregated.values():
        qty = v["数量"]
        amount = v["金额"]
        avg_price = amount / qty if qty > 0 else 0
        orders.append({**v, "均价": avg_price})

    orders.sort(key=lambda x: x["成交时间"])
    print(f"聚合为 {len(orders)} 笔订单", file=sys.stderr)

    # 代码前缀 → 币种
    def get_currency(code: str) -> str:
        prefix = code.split(".")[0] if "." in code else ""
        if prefix == "US":
            return "USD"
        elif prefix == "HK":
            return "HKD"
        elif prefix in ("SH", "SZ"):
            return "CNY"
        return "USD"

    existing_rows = load_csv()
    new_count = 0

    for order in orders:
        code = order["代码"]
        asset = order["名称"]
        op = order["方向"]
        date_str = order["成交时间"][:10]
        price = order["均价"]
        qty = order["数量"]
        amount = order["金额"]
        currency = get_currency(code)

        # 去重：同日期、同品种、同方向、金额接近
        duplicate = False
        for existing in existing_rows:
            if (
                existing.get("品种") == asset
                and existing.get("操作类型") == op
                and existing.get("日期") == date_str
            ):
                try:
                    existing_amount = float(existing.get("金额", 0))
                    if abs(existing_amount - amount) / max(amount, 0.01) < 0.02:
                        duplicate = True
                        break
                except (ValueError, TypeError):
                    pass

        if duplicate:
            symbol = "$" if currency == "USD" else "HK$" if currency == "HKD" else "¥"
            print(f"  跳过重复: {asset} {op} {date_str} {symbol}{amount:.2f}", file=sys.stderr)
            continue

        row = {
            "序号": "",
            "品种": asset,
            "操作类型": op,
            "价格": str(round(price, 4)),
            "数量": str(round(qty, 4)),
            "金额": str(round(amount, 2)),
            "币种": currency,
            "日期": date_str,
            "日期精确度": "精确",
            "交易平台": "富途",
            "备注": f"{code} 富途API数据",
        }

        errors = validate_row(row)
        if errors:
            print(f"  校验失败 ({asset} {date_str}):", file=sys.stderr)
            for e in errors:
                print(f"    ✗ {e}", file=sys.stderr)
            continue

        existing_rows.append(row)
        new_count += 1
        symbol = "$" if currency == "USD" else "HK$" if currency == "HKD" else "¥"
        print(f"  新增: {asset} {op} {date_str} {symbol}{amount:.2f}", file=sys.stderr)

    if new_count > 0:
        save_csv(existing_rows)
        print(f"\n新增 {new_count} 条记录", file=sys.stderr)
    else:
        print("\n无新记录需要添加", file=sys.stderr)


def import_cms(csv_path: str):
    """从招商证券导出 CSV 导入交易记录。

    招商证券 CSV 格式（由 fetch_cms_trades.py convert 生成）：
      证券代码,证券名称,成交日期,成交时间,买卖标志,成交价格,成交数量,成交金额,成交编号
    """
    input_path = Path(csv_path)
    if not input_path.exists():
        print(f"文件不存在: {csv_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        raw_trades = list(reader)

    print(f"读取 {len(raw_trades)} 条招商证券记录", file=sys.stderr)

    existing_rows = load_csv()
    new_count = 0

    for trade in raw_trades:
        asset = trade["证券名称"]
        op = trade["买卖标志"]
        date_str = trade["成交日期"]
        price = float(trade["成交价格"])
        qty = abs(float(trade["成交数量"]))
        amount = float(trade["成交金额"])

        # 检查是否已存在（同日期、同品种、同方向、金额接近）
        duplicate = False
        for existing in existing_rows:
            if (
                existing.get("品种") == asset
                and existing.get("操作类型") == op
                and existing.get("日期") == date_str
            ):
                try:
                    existing_amount = float(existing.get("金额", 0))
                    if abs(existing_amount - amount) / max(amount, 0.01) < 0.02:
                        duplicate = True
                        break
                except (ValueError, TypeError):
                    pass

        if duplicate:
            print(f"  跳过重复: {asset} {op} {date_str} ¥{amount:.2f}", file=sys.stderr)
            continue

        row = {
            "序号": "",
            "品种": asset,
            "操作类型": op,
            "价格": str(round(price, 4)),
            "数量": str(round(qty, 4)),
            "金额": str(round(amount, 2)),
            "币种": "CNY",
            "日期": date_str,
            "日期精确度": "精确",
            "交易平台": "招商证券",
            "备注": "招商证券网页交易数据",
        }

        errors = validate_row(row)
        if errors:
            print(f"  校验失败 ({asset} {date_str}):", file=sys.stderr)
            for e in errors:
                print(f"    ✗ {e}", file=sys.stderr)
            continue

        existing_rows.append(row)
        new_count += 1
        print(f"  新增: {asset} {op} {date_str} ¥{amount:.2f}", file=sys.stderr)

    if new_count > 0:
        save_csv(existing_rows)
        print(f"\n新增 {new_count} 条记录", file=sys.stderr)
    else:
        print("\n无新记录需要添加", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="交易日志汇总表写入工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # add 命令
    add_parser = subparsers.add_parser("add", help="手动添加一条记录")
    add_parser.add_argument("--品种", required=True)
    add_parser.add_argument("--操作", required=True, choices=["买入", "卖出"])
    add_parser.add_argument("--价格", type=float, required=True)
    add_parser.add_argument("--数量", type=float, required=True)
    add_parser.add_argument("--金额", type=float, required=True)
    add_parser.add_argument("--币种", required=True, choices=["CNY", "USD", "HKD"])
    add_parser.add_argument("--日期", required=True, help="YYYY-MM-DD")
    add_parser.add_argument("--日期精确度", default="精确", choices=["精确", "周期范围"])
    add_parser.add_argument("--交易平台", default="其他", choices=["币安", "富途", "招行", "招商证券", "其他"])
    add_parser.add_argument("--备注", default="")

    # import-binance 命令
    import_parser = subparsers.add_parser("import-binance", help="从币安 CSV 导入")
    import_parser.add_argument("csv_file", help="币安 CSV 文件路径")

    # import-futu 命令
    futu_parser = subparsers.add_parser("import-futu", help="从富途 CSV 导入（由 fetch_futu_trades.py 生成）")
    futu_parser.add_argument("csv_file", help="富途 CSV 文件路径")

    # import-cms 命令
    cms_parser = subparsers.add_parser("import-cms", help="从招商证券 CSV 导入（由 fetch_cms_trades.py 生成）")
    cms_parser.add_argument("csv_file", help="招商证券 CSV 文件路径")

    # migrate 命令
    subparsers.add_parser("migrate", help="迁移旧格式 CSV 到 schema 格式")

    # validate 命令
    subparsers.add_parser("validate", help="校验 CSV 是否符合 schema")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == "add":
        add_record(
            品种=args.品种,
            操作类型=args.操作,
            价格=args.价格,
            数量=args.数量,
            金额=args.金额,
            币种=args.币种,
            日期=args.日期,
            日期精确度=args.日期精确度,
            交易平台=args.交易平台,
            备注=args.备注,
        )
    elif args.command == "import-binance":
        import_binance(args.csv_file)
    elif args.command == "import-futu":
        import_futu(args.csv_file)
    elif args.command == "import-cms":
        import_cms(args.csv_file)
    elif args.command == "migrate":
        migrate_csv()
    elif args.command == "validate":
        validate_csv()
    else:
        print("请指定子命令: add, import-binance, import-futu, import-cms, migrate, validate", file=sys.stderr)
        print("使用 --help 查看用法", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
