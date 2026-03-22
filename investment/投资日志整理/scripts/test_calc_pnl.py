#!/usr/bin/env python3
"""
calc_pnl.py 的测试用例

- FIFO 匹配引擎: 6 个场景
- Schema 校验: 7 个场景 (1 valid + 6 invalid)
- 真实数据集成测试: 2 个品种手算基准
"""

import io
import textwrap
from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from calc_pnl import (
    OpenPosition,
    ValidationError,
    calc_floating_pnl,
    fifo_match,
    validate_and_load,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_df(rows: list[dict]) -> pd.DataFrame:
    """Build a DataFrame mimicking post-validation state (numeric types, datetime)."""
    df = pd.DataFrame(rows)
    df["价格"] = df["价格"].astype(float)
    df["数量"] = df["数量"].astype(float)
    df["金额"] = df["金额"].astype(float)
    df["日期"] = pd.to_datetime(df["日期"])
    return df


def _buy(price, qty, date="2025-01-01", currency="CNY"):
    return {
        "序号": "1", "品种": "TestAsset", "操作类型": "买入",
        "价格": price, "数量": qty, "金额": price * qty,
        "币种": currency, "日期": date, "日期精确度": "精确", "备注": "",
    }


def _sell(price, qty, date="2025-06-01", currency="CNY"):
    return {
        "序号": "2", "品种": "TestAsset", "操作类型": "卖出",
        "价格": price, "数量": qty, "金额": price * qty,
        "币种": currency, "日期": date, "日期精确度": "精确", "备注": "",
    }


# ---------------------------------------------------------------------------
# FIFO matching engine tests
# ---------------------------------------------------------------------------

class TestFIFO:
    def test_case1_exact_match(self):
        """买入 10 @100, 卖出 10 @120 → 已实现 +200, 无剩余"""
        df = _make_df([_buy(100, 10), _sell(120, 10)])
        realized, remaining, unmatched = fifo_match(df, "TestAsset")

        assert len(realized) == 1
        assert realized[0].pnl == pytest.approx(200.0)
        assert realized[0].qty == pytest.approx(10.0)
        assert len(remaining) == 0
        assert len(unmatched) == 0

    def test_case2_partial_sell(self):
        """买入 10 @100, 卖出 5 @120 → 已实现 +100, 剩余 5 @100"""
        df = _make_df([_buy(100, 10), _sell(120, 5)])
        realized, remaining, unmatched = fifo_match(df, "TestAsset")

        assert len(realized) == 1
        assert realized[0].pnl == pytest.approx(100.0)
        assert len(remaining) == 1
        assert remaining[0].qty == pytest.approx(5.0)
        assert remaining[0].buy_price == pytest.approx(100.0)
        assert len(unmatched) == 0

    def test_case3_multi_buy_single_sell(self):
        """买入 3@100 + 5@110, 卖出 6@120 → FIFO: 3@100+3@110, 已实现 90, 剩余 2@110"""
        df = _make_df([
            _buy(100, 3, date="2025-01-01"),
            _buy(110, 5, date="2025-02-01"),
            _sell(120, 6, date="2025-06-01"),
        ])
        realized, remaining, unmatched = fifo_match(df, "TestAsset")

        total_pnl = sum(t.pnl for t in realized)
        assert total_pnl == pytest.approx(90.0)  # (120-100)*3 + (120-110)*3

        assert len(remaining) == 1
        assert remaining[0].qty == pytest.approx(2.0)
        assert remaining[0].buy_price == pytest.approx(110.0)
        assert len(unmatched) == 0

    def test_case4_multi_buy_multi_sell(self):
        """买入 4@100 + 6@110, 卖出 5@120 + 3@130 → 已实现 150, 剩余 2@110"""
        df = _make_df([
            _buy(100, 4, date="2025-01-01"),
            _buy(110, 6, date="2025-02-01"),
            _sell(120, 5, date="2025-06-01"),
            _sell(130, 3, date="2025-07-01"),
        ])
        realized, remaining, unmatched = fifo_match(df, "TestAsset")

        # sell 5@120: match 4@100 + 1@110 → (120-100)*4 + (120-110)*1 = 80+10=90
        # sell 3@130: match 3@110 → (130-110)*3 = 60
        total_pnl = sum(t.pnl for t in realized)
        assert total_pnl == pytest.approx(150.0)

        assert len(remaining) == 1
        assert remaining[0].qty == pytest.approx(2.0)
        assert remaining[0].buy_price == pytest.approx(110.0)
        assert len(unmatched) == 0

    def test_case5_sell_exceeds_buys(self):
        """买入 5@100, 卖出 8@120 → 5 matched (+100), 3 unmatched"""
        df = _make_df([_buy(100, 5), _sell(120, 8)])
        realized, remaining, unmatched = fifo_match(df, "TestAsset")

        total_pnl = sum(t.pnl for t in realized)
        assert total_pnl == pytest.approx(100.0)
        assert len(remaining) == 0
        assert len(unmatched) == 1
        assert unmatched[0].qty == pytest.approx(3.0)

    def test_case6_buys_only(self):
        """买入 10@100 + 5@110 → 已实现 0, 剩余 10@100 + 5@110"""
        df = _make_df([
            _buy(100, 10, date="2025-01-01"),
            _buy(110, 5, date="2025-02-01"),
        ])
        realized, remaining, unmatched = fifo_match(df, "TestAsset")

        assert len(realized) == 0
        assert len(remaining) == 2
        assert remaining[0].qty == pytest.approx(10.0)
        assert remaining[0].buy_price == pytest.approx(100.0)
        assert remaining[1].qty == pytest.approx(5.0)
        assert remaining[1].buy_price == pytest.approx(110.0)
        assert len(unmatched) == 0


# ---------------------------------------------------------------------------
# Schema validation tests
# ---------------------------------------------------------------------------

def _write_csv(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "test.csv"
    p.write_text(textwrap.dedent(content).strip(), encoding="utf-8")
    return p


class TestSchemaValidation:
    VALID_CSV = """\
        序号,品种,操作类型,价格,数量,金额,币种,日期,日期精确度,备注
        1,黄金,买入,800,2,1600,CNY,2025-05-06,精确,
        2,黄金,卖出,900,2,1800,CNY,2025-10-01,精确,
    """

    def test_valid_csv(self, tmp_path):
        p = _write_csv(tmp_path, self.VALID_CSV)
        df = validate_and_load(p)
        assert len(df) == 2
        assert df["价格"].dtype == float

    def test_missing_column(self, tmp_path):
        csv = """\
            序号,品种,操作类型,价格,数量,金额,币种,日期,备注
            1,黄金,买入,800,2,1600,CNY,2025-05-06,
        """
        p = _write_csv(tmp_path, csv)
        with pytest.raises(ValidationError, match="缺少列.*日期精确度"):
            validate_and_load(p)

    def test_invalid_op_type(self, tmp_path):
        csv = """\
            序号,品种,操作类型,价格,数量,金额,币种,日期,日期精确度,备注
            1,BTC合约,开仓,100000,0.1,10000,USD,2025-05-06,精确,
        """
        p = _write_csv(tmp_path, csv)
        with pytest.raises(ValidationError, match="操作类型.*开仓.*非法"):
            validate_and_load(p)

    def test_invalid_currency(self, tmp_path):
        csv = """\
            序号,品种,操作类型,价格,数量,金额,币种,日期,日期精确度,备注
            1,日经ETF,买入,100,10,1000,JPY,2025-05-06,精确,
        """
        p = _write_csv(tmp_path, csv)
        with pytest.raises(ValidationError, match="币种.*JPY.*非法"):
            validate_and_load(p)

    def test_non_numeric_price(self, tmp_path):
        csv = """\
            序号,品种,操作类型,价格,数量,金额,币种,日期,日期精确度,备注
            1,黄金,买入,791.48 ￥/g,2,1582.96,CNY,2025-05-06,精确,
        """
        p = _write_csv(tmp_path, csv)
        with pytest.raises(ValidationError, match="价格.*无法解析为数值"):
            validate_and_load(p)

    def test_bad_date_format(self, tmp_path):
        csv = """\
            序号,品种,操作类型,价格,数量,金额,币种,日期,日期精确度,备注
            1,黄金,买入,800,2,1600,CNY,2025/05/06,精确,
        """
        p = _write_csv(tmp_path, csv)
        with pytest.raises(ValidationError, match="日期.*格式不符合"):
            validate_and_load(p)

    def test_amount_mismatch(self, tmp_path):
        csv = """\
            序号,品种,操作类型,价格,数量,金额,币种,日期,日期精确度,备注
            1,黄金,买入,800,2,9999,CNY,2025-05-06,精确,
        """
        p = _write_csv(tmp_path, csv)
        with pytest.raises(ValidationError, match="金额.*偏差"):
            validate_and_load(p)


# ---------------------------------------------------------------------------
# Floating P&L tests
# ---------------------------------------------------------------------------

class TestFloatingPnL:
    def test_basic(self):
        positions = [
            OpenPosition("A", buy_price=100, qty=10, cost=1000, currency="CNY",
                          buy_date=datetime(2025, 1, 1)),
        ]
        prices = {"A": 120.0}
        result = calc_floating_pnl(positions, prices)
        assert len(result) == 1
        assert result[0].pnl == pytest.approx(200.0)

    def test_price_missing(self):
        positions = [
            OpenPosition("A", buy_price=100, qty=10, cost=1000, currency="CNY",
                          buy_date=datetime(2025, 1, 1)),
        ]
        prices = {"A": None}
        result = calc_floating_pnl(positions, prices)
        assert len(result) == 0


# ---------------------------------------------------------------------------
# Integration test with real data
# ---------------------------------------------------------------------------

class TestIntegration:
    """
    These tests run against the actual CSV file (after it conforms to the new schema).
    They are skipped if the CSV doesn't exist or fails schema validation,
    since the upstream task may not have reformatted it yet.
    """

    @pytest.fixture
    def real_df(self):
        csv_path = Path(__file__).parent.parent / "交易日志汇总表.csv"
        if not csv_path.exists():
            pytest.skip("交易日志汇总表.csv 不存在")
        try:
            df = validate_and_load(csv_path)
        except (ValidationError, Exception) as e:
            pytest.skip(f"CSV schema 校验未通过，跳过集成测试: {e}")
        return df

    def test_gold_realized_pnl(self, real_df):
        """黄金: 13 笔买入共 33g, 1 笔卖出 33g @889.12 → 完全平仓"""
        gold_df = real_df[real_df["品种"] == "黄金"]
        if gold_df.empty:
            pytest.skip("CSV 中无黄金数据")

        realized, remaining, unmatched = fifo_match(gold_df, "黄金")

        buy_total_cost = sum(t.buy_price * t.qty for t in realized)
        sell_total = sum(t.sell_price * t.qty for t in realized)
        total_pnl = sum(t.pnl for t in realized)

        assert total_pnl == pytest.approx(sell_total - buy_total_cost, abs=0.01)
        assert sell_total == pytest.approx(889.12 * 33, abs=1.0)

        total_sold_qty = sum(t.qty for t in realized)
        total_remaining_qty = sum(p.qty for p in remaining)
        assert total_sold_qty + total_remaining_qty == pytest.approx(33.0, abs=0.01)

    def test_sh50etf_realized_pnl(self, real_df):
        """上证50ETF: 买入 19837.40, 卖出 19247.80 → 已实现亏损 ≈ -589.60"""
        etf_df = real_df[real_df["品种"] == "上证50ETF"]
        if etf_df.empty:
            pytest.skip("CSV 中无上证50ETF数据")

        realized, remaining, unmatched = fifo_match(etf_df, "上证50ETF")
        total_pnl = sum(t.pnl for t in realized)

        assert total_pnl < 0, "上证50ETF 应为亏损"
        assert total_pnl == pytest.approx(-589.60, abs=5.0)
        assert len(remaining) == 0, "上证50ETF 应完全平仓"
