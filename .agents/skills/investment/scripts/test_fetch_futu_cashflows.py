"""fetch_futu_cashflows.py 的测试。"""

import argparse
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from fetch_futu_cashflows import fetch_cashflows, is_dividend_related, parse_date


DIVIDEND = {
    "cashflow_id": "306899",
    "clearing_date": "2026-10-16",
    "settlement_date": "2026-10-16",
    "currency": "HKD",
    "cashflow_type": "Cash Dividend",
    "cashflow_direction": "IN",
    "cashflow_amount": 2538.0,
    "cashflow_remark": "PAY IN HKD0.846/SH (NET) <SEHK 883 CNOOC> 3000 shares",
    "create_time": "N/A",
}

FEE = {
    **DIVIDEND,
    "cashflow_id": "306900",
    "cashflow_type": "Corporate Action Service Fee",
    "cashflow_direction": "OUT",
    "cashflow_amount": -30.0,
    "cashflow_remark": "Handling Charge 3000 shares <SEHK 883 CNOOC>",
}

UNRELATED = {
    **DIVIDEND,
    "cashflow_id": "519223",
    "cashflow_type": "Others",
    "cashflow_direction": "OUT",
    "cashflow_amount": -110.82,
    "cashflow_remark": "N/A",
}


def make_args(**overrides):
    defaults = dict(
        start="2026-10-15",
        end="2026-10-16",
        host="127.0.0.1",
        port=11111,
        acc_id=0,
        security_firm="FUTUSECURITIES",
        interval=0,
        all=False,
        output=None,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_parse_date_rejects_invalid_format():
    with pytest.raises(SystemExit):
        parse_date("2026/10/16")


def test_filter_recognizes_dividend_and_fee():
    assert is_dividend_related(pd.Series(DIVIDEND))
    assert is_dividend_related(pd.Series(FEE))
    assert not is_dividend_related(pd.Series(UNRELATED))


@patch("fetch_futu_cashflows.OpenSecTradeContext")
def test_queries_each_clearing_date_and_filters(mock_ctx_cls):
    ctx = MagicMock()
    ctx.get_acc_cash_flow.side_effect = [
        (0, pd.DataFrame([UNRELATED])),
        (0, pd.DataFrame([DIVIDEND, FEE])),
    ]
    mock_ctx_cls.return_value = ctx

    result = fetch_cashflows(make_args())

    assert result["流水编号"].astype(str).tolist() == ["306899", "306900"]
    assert ctx.get_acc_cash_flow.call_count == 2
    assert ctx.get_acc_cash_flow.call_args_list[0].kwargs["clearing_date"] == "2026-10-15"
    assert ctx.get_acc_cash_flow.call_args_list[1].kwargs["clearing_date"] == "2026-10-16"
    ctx.close.assert_called_once()


@patch("fetch_futu_cashflows.OpenSecTradeContext")
def test_all_keeps_unrelated_rows(mock_ctx_cls):
    ctx = MagicMock()
    ctx.get_acc_cash_flow.return_value = (0, pd.DataFrame([UNRELATED]))
    mock_ctx_cls.return_value = ctx

    result = fetch_cashflows(make_args(start="2026-10-16", all=True))

    assert len(result) == 1
    assert result.iloc[0]["流水编号"] == "519223"


@patch("fetch_futu_cashflows.OpenSecTradeContext")
def test_csv_output(mock_ctx_cls, tmp_path):
    ctx = MagicMock()
    ctx.get_acc_cash_flow.return_value = (0, pd.DataFrame([DIVIDEND, FEE]))
    mock_ctx_cls.return_value = ctx
    output = tmp_path / "cashflows.csv"

    fetch_cashflows(make_args(start="2026-10-16", output=str(output)))

    exported = pd.read_csv(output)
    assert exported["金额"].tolist() == [2538.0, -30.0]
    assert exported["类型"].tolist() == ["Cash Dividend", "Corporate Action Service Fee"]
