#!/usr/bin/env python3
"""
write_trade_journal.py 的测试用例

覆盖：校验、日期解析、旧格式解析、CSV 读写排序、币安导入聚合与去重、迁移。
所有测试使用 tmp_path 隔离，不影响真实 CSV。
"""

import csv
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

import write_trade_journal as wj


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def tmp_csv(tmp_path):
    """将模块级 CSV_PATH 临时重定向到 tmp_path，测试结束后恢复。"""
    csv_path = tmp_path / "交易日志汇总表.csv"
    with patch.object(wj, "CSV_PATH", csv_path):
        yield csv_path


def _write_csv(path: Path, rows: list[dict], fieldnames=None):
    """辅助：向指定路径写入 CSV。"""
    if fieldnames is None:
        fieldnames = wj.SCHEMA_FIELDS
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _make_row(**overrides) -> dict:
    """构造一条符合 schema 的默认记录。"""
    defaults = {
        "序号": "1",
        "品种": "BTC",
        "操作类型": "买入",
        "价格": "100000.0",
        "数量": "0.01",
        "金额": "1000.0",
        "币种": "USD",
        "日期": "2025-06-01",
        "日期精确度": "精确",
        "备注": "",
    }
    defaults.update(overrides)
    return defaults


# ---------------------------------------------------------------------------
# validate_row tests
# ---------------------------------------------------------------------------

class TestValidateRow:
    def test_valid_row(self):
        row = _make_row()
        assert wj.validate_row(row) == []

    def test_missing_required_field(self):
        row = _make_row(品种="")
        errors = wj.validate_row(row)
        assert any("品种" in e for e in errors)

    def test_invalid_op_type(self):
        row = _make_row(操作类型="开仓")
        errors = wj.validate_row(row)
        assert any("操作类型" in e for e in errors)

    def test_invalid_currency(self):
        row = _make_row(币种="EUR")
        errors = wj.validate_row(row)
        assert any("币种" in e for e in errors)

    def test_invalid_precision(self):
        row = _make_row(日期精确度="大约")
        errors = wj.validate_row(row)
        assert any("日期精确度" in e for e in errors)

    def test_non_numeric_price(self):
        row = _make_row(价格="100 $")
        errors = wj.validate_row(row)
        assert any("价格" in e and "非数字" in e for e in errors)

    def test_non_numeric_qty(self):
        row = _make_row(数量="0.01 个")
        errors = wj.validate_row(row)
        assert any("数量" in e and "非数字" in e for e in errors)

    def test_amount_deviation_over_1_percent(self):
        # 价格 100 × 数量 10 = 1000, 金额 1020 → 偏差 2%
        row = _make_row(价格="100", 数量="10", 金额="1020")
        errors = wj.validate_row(row)
        assert any("偏差" in e for e in errors)

    def test_amount_deviation_within_1_percent(self):
        # 价格 100 × 数量 10 = 1000, 金额 1005 → 偏差 0.5%
        row = _make_row(价格="100", 数量="10", 金额="1005")
        assert wj.validate_row(row) == []

    def test_invalid_date_format(self):
        row = _make_row(日期="06/01/2025")
        errors = wj.validate_row(row)
        assert any("日期格式" in e for e in errors)

    def test_valid_date(self):
        row = _make_row(日期="2025-12-31")
        assert wj.validate_row(row) == []

    def test_empty_remark_is_ok(self):
        row = _make_row(备注="")
        assert wj.validate_row(row) == []


# ---------------------------------------------------------------------------
# parse_old_price / parse_old_amount tests
# ---------------------------------------------------------------------------

class TestParseOldPrice:
    def test_usd(self):
        assert wj.parse_old_price("76653 $") == (76653.0, "USD")

    def test_cny(self):
        assert wj.parse_old_price("801.60 ￥/g") == (801.60, "CNY")

    def test_cny_plain(self):
        assert wj.parse_old_price("791.48 ￥") == (791.48, "CNY")

    def test_hkd(self):
        assert wj.parse_old_price("5.545 HKD") == (5.545, "HKD")

    def test_usd_per_share(self):
        assert wj.parse_old_price("34.21 $/股") == (34.21, "USD")

    def test_plain_number_defaults_cny(self):
        assert wj.parse_old_price("762") == (762.0, "CNY")


# ---------------------------------------------------------------------------
# parse_old_qty tests
# ---------------------------------------------------------------------------

class TestParseOldQty:
    def test_with_unit_ge(self):
        assert wj.parse_old_qty("0.00391 个") == 0.00391

    def test_with_unit_g(self):
        assert wj.parse_old_qty("2g") == 2.0

    def test_with_unit_shares(self):
        assert wj.parse_old_qty("6300 股") == 6300.0

    def test_approx_prefix(self):
        assert wj.parse_old_qty("≈65 股") == 65.0

    def test_plain_number(self):
        assert wj.parse_old_qty("14.6") == 14.6


# ---------------------------------------------------------------------------
# parse_old_date tests
# ---------------------------------------------------------------------------

class TestParseOldDate:
    def test_mdy_exact(self):
        assert wj.parse_old_date("4/7/2025") == ("2025-04-07", "精确")

    def test_iso_exact(self):
        assert wj.parse_old_date("2025-05-06") == ("2025-05-06", "精确")

    def test_range_iso(self):
        assert wj.parse_old_date("2025-05-18 ~ 05-25") == ("2025-05-18", "周期范围")

    def test_range_cross_year(self):
        assert wj.parse_old_date("2025-12-29 ~ 2026-01-23") == ("2025-12-29", "周期范围")

    def test_mdy_single_digit(self):
        assert wj.parse_old_date("5/6/2025") == ("2025-05-06", "精确")


# ---------------------------------------------------------------------------
# save_csv / load_csv tests（排序 + 编号）
# ---------------------------------------------------------------------------

class TestSaveCsvSorting:
    def test_sorts_by_date_and_renumbers(self, tmp_csv):
        rows = [
            _make_row(序号="", 品种="ETH", 日期="2025-06-15"),
            _make_row(序号="", 品种="BTC", 日期="2025-04-01"),
            _make_row(序号="", 品种="XRP", 日期="2025-05-10"),
        ]
        wj.save_csv(rows)

        loaded = wj.load_csv()
        assert len(loaded) == 3
        assert loaded[0]["品种"] == "BTC"
        assert loaded[1]["品种"] == "XRP"
        assert loaded[2]["品种"] == "ETH"
        assert [r["序号"] for r in loaded] == ["1", "2", "3"]

    def test_load_empty_csv(self, tmp_csv):
        assert wj.load_csv() == []

    def test_load_existing_csv(self, tmp_csv):
        _write_csv(tmp_csv, [_make_row()])
        rows = wj.load_csv()
        assert len(rows) == 1
        assert rows[0]["品种"] == "BTC"


# ---------------------------------------------------------------------------
# add_record tests
# ---------------------------------------------------------------------------

class TestAddRecord:
    def test_add_single_record(self, tmp_csv):
        wj.add_record(
            品种="BTC", 操作类型="买入",
            价格=76653, 数量=0.00391, 金额=299.71,
            币种="USD", 日期="2025-04-07", 备注="测试",
        )
        rows = wj.load_csv()
        assert len(rows) == 1
        assert rows[0]["品种"] == "BTC"
        assert rows[0]["序号"] == "1"

    def test_add_preserves_order(self, tmp_csv):
        wj.add_record(品种="ETH", 操作类型="卖出", 价格=2680, 数量=1, 金额=2680, 币种="USD", 日期="2025-05-18")
        wj.add_record(品种="BTC", 操作类型="买入", 价格=76653, 数量=0.00391, 金额=299.71, 币种="USD", 日期="2025-04-07")

        rows = wj.load_csv()
        assert len(rows) == 2
        assert rows[0]["品种"] == "BTC"  # 4月在前
        assert rows[1]["品种"] == "ETH"  # 5月在后
        assert rows[0]["序号"] == "1"
        assert rows[1]["序号"] == "2"

    def test_add_invalid_record_exits(self, tmp_csv):
        with pytest.raises(SystemExit):
            wj.add_record(
                品种="BTC", 操作类型="开仓",  # 无效操作类型
                价格=100, 数量=1, 金额=100,
                币种="USD", 日期="2025-01-01",
            )


# ---------------------------------------------------------------------------
# import_binance tests
# ---------------------------------------------------------------------------

def _write_binance_csv(path: Path, rows: list[dict]):
    """辅助：写入币安格式 CSV。"""
    fields = ["成交时间", "交易对", "方向", "数量", "成交价", "金额", "手续费", "手续费币种", "成交编号"]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class TestImportBinance:
    def test_import_single_trade(self, tmp_csv, tmp_path):
        binance_csv = tmp_path / "binance.csv"
        _write_binance_csv(binance_csv, [{
            "成交时间": "2025-04-07 14:17:13",
            "交易对": "BTCUSDT",
            "方向": "买入",
            "数量": "0.00391",
            "成交价": "76653.0",
            "金额": "299.71323",
            "手续费": "0.0004",
            "手续费币种": "BNB",
            "成交编号": "100001",
        }])

        wj.import_binance(str(binance_csv))

        rows = wj.load_csv()
        assert len(rows) == 1
        assert rows[0]["品种"] == "BTC"
        assert rows[0]["操作类型"] == "买入"
        assert rows[0]["币种"] == "USD"
        assert rows[0]["日期"] == "2025-04-07"

    def test_aggregates_split_orders(self, tmp_csv, tmp_path):
        """同一时间戳的拆单应合并为一笔。"""
        binance_csv = tmp_path / "binance.csv"
        _write_binance_csv(binance_csv, [
            {
                "成交时间": "2025-07-15 05:49:18",
                "交易对": "BTCUSDT",
                "方向": "卖出",
                "数量": "0.02",
                "成交价": "120056.72",
                "金额": "2401.1344",
                "手续费": "0.001",
                "手续费币种": "BNB",
                "成交编号": "200001",
            },
            {
                "成交时间": "2025-07-15 05:49:18",
                "交易对": "BTCUSDT",
                "方向": "卖出",
                "数量": "0.03",
                "成交价": "120056.72",
                "金额": "3601.7016",
                "手续费": "0.002",
                "手续费币种": "BNB",
                "成交编号": "200002",
            },
        ])

        wj.import_binance(str(binance_csv))

        rows = wj.load_csv()
        assert len(rows) == 1  # 合并为 1 笔
        assert float(rows[0]["数量"]) == pytest.approx(0.05, abs=1e-8)
        assert float(rows[0]["金额"]) == pytest.approx(6002.836, abs=0.01)

    def test_skips_duplicates(self, tmp_csv, tmp_path):
        """已存在的记录应被跳过。"""
        # 先写入一条已有记录
        _write_csv(tmp_csv, [_make_row(
            品种="BTC", 操作类型="买入", 价格="76653.0",
            数量="0.00391", 金额="299.71", 币种="USD",
            日期="2025-04-07", 日期精确度="精确", 备注="已有",
        )])

        binance_csv = tmp_path / "binance.csv"
        _write_binance_csv(binance_csv, [{
            "成交时间": "2025-04-07 14:17:13",
            "交易对": "BTCUSDT",
            "方向": "买入",
            "数量": "0.00391",
            "成交价": "76653.0",
            "金额": "299.71323",
            "手续费": "0.0004",
            "手续费币种": "BNB",
            "成交编号": "100001",
        }])

        wj.import_binance(str(binance_csv))

        rows = wj.load_csv()
        assert len(rows) == 1  # 没有新增
        assert rows[0]["备注"] == "已有"  # 保持原记录不变

    def test_import_xrp(self, tmp_csv, tmp_path):
        """非 BTC/ETH 品种（XRP）也能正确导入。"""
        binance_csv = tmp_path / "binance.csv"
        _write_binance_csv(binance_csv, [{
            "成交时间": "2026-03-14 00:28:02",
            "交易对": "XRPUSDT",
            "方向": "买入",
            "数量": "142.3",
            "成交价": "1.4044",
            "金额": "199.84612",
            "手续费": "0.1423",
            "手续费币种": "XRP",
            "成交编号": "300001",
        }])

        wj.import_binance(str(binance_csv))

        rows = wj.load_csv()
        assert len(rows) == 1
        assert rows[0]["品种"] == "XRP"

    def test_import_unknown_symbol(self, tmp_csv, tmp_path):
        """未在映射表中的交易对，去掉 USDT 后缀作为品种名。"""
        binance_csv = tmp_path / "binance.csv"
        _write_binance_csv(binance_csv, [{
            "成交时间": "2025-08-01 10:00:00",
            "交易对": "AVAXUSDT",
            "方向": "买入",
            "数量": "10",
            "成交价": "25.0",
            "金额": "250.0",
            "手续费": "0.01",
            "手续费币种": "AVAX",
            "成交编号": "400001",
        }])

        wj.import_binance(str(binance_csv))

        rows = wj.load_csv()
        assert rows[0]["品种"] == "AVAX"

    def test_import_nonexistent_file(self, tmp_csv):
        with pytest.raises(SystemExit):
            wj.import_binance("/tmp/nonexistent_binance_file.csv")


# ---------------------------------------------------------------------------
# migrate_csv tests
# ---------------------------------------------------------------------------

class TestMigrateCsv:
    def test_migrate_old_format(self, tmp_csv):
        """旧格式 CSV 应迁移为新 schema 格式。"""
        old_fields = ["序号", "品种", "买入/卖出", "价格", "数量", "金额", "操作时间", "备注"]
        old_rows = [
            {"序号": "1", "品种": "BTC", "买入/卖出": "买入", "价格": "76653 $",
             "数量": "0.00391 个", "金额": "299.71 $", "操作时间": "4/7/2025", "备注": "测试"},
            {"序号": "2", "品种": "黄金", "买入/卖出": "买入", "价格": "801.60 ￥/g",
             "数量": "2g", "金额": "1603.20 ￥", "操作时间": "4/21/2025", "备注": ""},
        ]
        _write_csv(tmp_csv, old_rows, fieldnames=old_fields)

        wj.migrate_csv()

        rows = wj.load_csv()
        assert len(rows) == 2

        btc = rows[0]
        assert btc["品种"] == "BTC"
        assert btc["操作类型"] == "买入"
        assert float(btc["价格"]) == 76653.0
        assert float(btc["数量"]) == 0.00391
        assert btc["币种"] == "USD"
        assert btc["日期"] == "2025-04-07"
        assert btc["日期精确度"] == "精确"

        gold = rows[1]
        assert gold["币种"] == "CNY"
        assert float(gold["价格"]) == 801.6

    def test_migrate_range_date(self, tmp_csv):
        """周期范围日期应标记为 '周期范围'。"""
        old_fields = ["序号", "品种", "买入/卖出", "价格", "数量", "金额", "操作时间", "备注"]
        _write_csv(tmp_csv, [{
            "序号": "1", "品种": "ETH", "买入/卖出": "卖出", "价格": "2680 $",
            "数量": "1 个", "金额": "2680 $", "操作时间": "2025-05-18 ~ 05-25", "备注": "",
        }], fieldnames=old_fields)

        wj.migrate_csv()

        rows = wj.load_csv()
        assert rows[0]["日期精确度"] == "周期范围"
        assert rows[0]["日期"] == "2025-05-18"

    def test_migrate_already_new_format(self, tmp_csv):
        """已经是新格式的 CSV 不应重复迁移。"""
        _write_csv(tmp_csv, [_make_row()])

        wj.migrate_csv()

        rows = wj.load_csv()
        assert len(rows) == 1  # 不变

    def test_migrate_creates_backup(self, tmp_csv):
        """迁移应创建 .bak 备份。"""
        old_fields = ["序号", "品种", "买入/卖出", "价格", "数量", "金额", "操作时间", "备注"]
        _write_csv(tmp_csv, [{
            "序号": "1", "品种": "BTC", "买入/卖出": "买入", "价格": "100 $",
            "数量": "0.01 个", "金额": "1 $", "操作时间": "1/1/2025", "备注": "",
        }], fieldnames=old_fields)

        wj.migrate_csv()

        backup = tmp_csv.with_suffix(".csv.bak")
        assert backup.exists()

    def test_migrate_hkd_currency(self, tmp_csv):
        """HKD 币种应正确识别。"""
        old_fields = ["序号", "品种", "买入/卖出", "价格", "数量", "金额", "操作时间", "备注"]
        _write_csv(tmp_csv, [{
            "序号": "1", "品种": "恒生科技ETF", "买入/卖出": "买入",
            "价格": "5.545 HKD", "数量": "2000 股", "金额": "11090 HKD",
            "操作时间": "2025-11-26 ~ 12-29", "备注": "",
        }], fieldnames=old_fields)

        wj.migrate_csv()

        rows = wj.load_csv()
        assert rows[0]["币种"] == "HKD"
        assert float(rows[0]["价格"]) == pytest.approx(5.545, abs=0.01)


# ---------------------------------------------------------------------------
# validate_csv integration test
# ---------------------------------------------------------------------------

class TestValidateCsv:
    def test_validate_passes_for_valid_data(self, tmp_csv, capsys):
        _write_csv(tmp_csv, [_make_row(), _make_row(序号="2", 品种="ETH", 日期="2025-07-01")])
        wj.validate_csv()
        captured = capsys.readouterr()
        assert "校验通过" in captured.err

    def test_validate_detects_errors(self, tmp_csv, capsys):
        _write_csv(tmp_csv, [_make_row(操作类型="开仓")])
        wj.validate_csv()
        captured = capsys.readouterr()
        assert "错误" in captured.err


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
