#!/usr/bin/env python3
"""
fetch_futu_trades.py 的测试用例

使用 mock 模拟 OpenD 连接，基于 2026-03-01 ~ 2026-03-09 的真实返回数据验证。
"""

import argparse
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from fetch_futu_trades import fetch_deals, format_date

# ---------------------------------------------------------------------------
# 真实返回数据 (2026-03-01 ~ 2026-03-09 查询结果)
# ---------------------------------------------------------------------------

MOCK_DEAL_DATA = pd.DataFrame([
    {
        "trd_side": "BUY",
        "deal_id": "3973453259418397735",
        "order_id": "FH1C27EA8EF7E48000",
        "code": "US.BNO",
        "stock_name": "United Sts Brent Oil Fd Lp Unit",
        "qty": 50.0,
        "price": 39.68,
        "create_time": "2026-03-03 10:00:46.405",
        "status": "OK",
    },
    {
        "trd_side": "BUY",
        "deal_id": "8147077543248932797",
        "order_id": "FH1C2A8BEC82DFA000",
        "code": "US.BNO",
        "stock_name": "United Sts Brent Oil Fd Lp Unit",
        "qty": 24.0,
        "price": 40.03,
        "create_time": "2026-03-05 11:02:46.228",
        "status": "OK",
    },
])


# ---------------------------------------------------------------------------
# format_date tests
# ---------------------------------------------------------------------------

class TestFormatDate:
    def test_valid_date(self):
        assert format_date("2026-03-01") == "2026-03-01 00:00:00"

    def test_none_returns_empty(self):
        assert format_date(None) == ""

    def test_empty_string_returns_empty(self):
        assert format_date("") == ""

    def test_invalid_format_exits(self):
        with pytest.raises(SystemExit):
            format_date("03/01/2026")


# ---------------------------------------------------------------------------
# fetch_deals integration test (mocked OpenD)
# ---------------------------------------------------------------------------

class TestFetchDeals:
    """基于 2026-03-01~03-09 真实查询结果的回归测试"""

    def _make_args(self, **overrides):
        defaults = dict(
            start="2026-03-01", end="2026-03-09", market="NONE",
            code="", host="127.0.0.1", port=11111, acc_id=0,
            output=None, security_firm="FUTUSECURITIES",
        )
        defaults.update(overrides)
        return argparse.Namespace(**defaults)

    @patch("fetch_futu_trades.OpenSecTradeContext")
    def test_returns_2_bno_deals(self, mock_ctx_cls, capsys):
        mock_ctx = MagicMock()
        mock_ctx.history_deal_list_query.return_value = (0, MOCK_DEAL_DATA.copy())
        mock_ctx_cls.return_value = mock_ctx

        fetch_deals(self._make_args())

        stdout = capsys.readouterr().out
        assert "US.BNO" in stdout
        assert "39.68" in stdout
        assert "40.03" in stdout
        assert "50.0" in stdout
        assert "24.0" in stdout

    @patch("fetch_futu_trades.OpenSecTradeContext")
    def test_side_label_chinese(self, mock_ctx_cls, capsys):
        mock_ctx = MagicMock()
        mock_ctx.history_deal_list_query.return_value = (0, MOCK_DEAL_DATA.copy())
        mock_ctx_cls.return_value = mock_ctx

        fetch_deals(self._make_args())

        stdout = capsys.readouterr().out
        assert "买入" in stdout
        assert "BUY" not in stdout

    @patch("fetch_futu_trades.OpenSecTradeContext")
    def test_sorted_by_time(self, mock_ctx_cls, capsys):
        reversed_data = MOCK_DEAL_DATA.iloc[::-1].reset_index(drop=True)
        mock_ctx = MagicMock()
        mock_ctx.history_deal_list_query.return_value = (0, reversed_data)
        mock_ctx_cls.return_value = mock_ctx

        fetch_deals(self._make_args())

        stdout = capsys.readouterr().out
        pos_first = stdout.index("39.68")
        pos_second = stdout.index("40.03")
        assert pos_first < pos_second, "03-03 成交应排在 03-05 之前"

    @patch("fetch_futu_trades.OpenSecTradeContext")
    def test_csv_output(self, mock_ctx_cls, tmp_path):
        mock_ctx = MagicMock()
        mock_ctx.history_deal_list_query.return_value = (0, MOCK_DEAL_DATA.copy())
        mock_ctx_cls.return_value = mock_ctx

        out_csv = tmp_path / "deals.csv"
        fetch_deals(self._make_args(output=str(out_csv)))

        df = pd.read_csv(out_csv)
        assert len(df) == 2
        assert "成交时间" in df.columns
        assert "方向" in df.columns
        assert df["成交价"].tolist() == [39.68, 40.03]

    @patch("fetch_futu_trades.OpenSecTradeContext")
    def test_empty_result(self, mock_ctx_cls, capsys):
        mock_ctx = MagicMock()
        mock_ctx.history_deal_list_query.return_value = (0, pd.DataFrame())
        mock_ctx_cls.return_value = mock_ctx

        fetch_deals(self._make_args())

        stderr = capsys.readouterr().err
        assert "无成交记录" in stderr

    @patch("fetch_futu_trades.OpenSecTradeContext")
    def test_api_error(self, mock_ctx_cls):
        mock_ctx = MagicMock()
        mock_ctx.history_deal_list_query.return_value = (-1, "网络超时")
        mock_ctx_cls.return_value = mock_ctx

        with pytest.raises(SystemExit):
            fetch_deals(self._make_args())
