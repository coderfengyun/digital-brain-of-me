#!/usr/bin/env python3
"""
fetch_binance_trades.py 的测试用例

使用 mock 模拟币安 API 返回，基于典型现货交易数据验证。
"""

import argparse
import os
from unittest.mock import MagicMock, patch

import pytest

from fetch_binance_trades import (
    date_to_ms,
    discover_symbols,
    fetch_trades_for_symbol,
    format_output,
    format_timestamp,
)

# ---------------------------------------------------------------------------
# 模拟 API 返回数据（基于 Binance GET /api/v3/myTrades 格式）
# ---------------------------------------------------------------------------

MOCK_BTC_TRADES = [
    {
        "symbol": "BTCUSDT",
        "id": 100001,
        "orderId": 200001,
        "orderListId": -1,
        "price": "94980.00",
        "qty": "0.10000000",
        "quoteQty": "9498.00000000",
        "commission": "0.00010000",
        "commissionAsset": "BTC",
        "time": 1746518400000,  # 2025-05-06 08:00:00 UTC
        "isBuyer": False,
        "isMaker": False,
        "isBestMatch": True,
    },
    {
        "symbol": "BTCUSDT",
        "id": 100002,
        "orderId": 200002,
        "orderListId": -1,
        "price": "101687.00",
        "qty": "0.06000000",
        "quoteQty": "6101.22000000",
        "commission": "0.00006000",
        "commissionAsset": "BTC",
        "time": 1746691200000,  # 2025-05-08 08:00:00 UTC
        "isBuyer": False,
        "isMaker": True,
        "isBestMatch": True,
    },
]

MOCK_ETH_TRADES = [
    {
        "symbol": "ETHUSDT",
        "id": 300001,
        "orderId": 400001,
        "orderListId": -1,
        "price": "2680.00",
        "qty": "1.00000000",
        "quoteQty": "2680.00000000",
        "commission": "0.00100000",
        "commissionAsset": "ETH",
        "time": 1747555200000,  # 2025-05-18 08:00:00 UTC
        "isBuyer": False,
        "isMaker": False,
        "isBestMatch": True,
    },
]


# ---------------------------------------------------------------------------
# date_to_ms / format_timestamp tests
# ---------------------------------------------------------------------------

class TestDateConversion:
    def test_date_to_ms(self):
        ms = date_to_ms("2025-05-06")
        # 应该是 2025-05-06 00:00:00 本地时间的毫秒时间戳
        assert isinstance(ms, int)
        assert ms > 0

    def test_date_to_ms_invalid(self):
        with pytest.raises(ValueError):
            date_to_ms("not-a-date")

    def test_format_timestamp(self):
        result = format_timestamp(1746518400000)
        assert "2025" in result
        assert ":" in result

    def test_roundtrip(self):
        """date_to_ms 产生的时间戳格式化回来应包含原日期。"""
        ms = date_to_ms("2025-05-06")
        formatted = format_timestamp(ms)
        assert formatted.startswith("2025-05-06")


# ---------------------------------------------------------------------------
# fetch_trades_for_symbol tests
# ---------------------------------------------------------------------------

class TestFetchTradesForSymbol:
    def test_basic_fetch(self):
        """基本查询：API 返回不足 1000 条，无需分页。"""
        mock_client = MagicMock()
        mock_client.get_my_trades.return_value = MOCK_BTC_TRADES

        trades = fetch_trades_for_symbol(mock_client, "BTCUSDT")
        assert len(trades) == 2
        assert trades[0]["symbol"] == "BTCUSDT"
        mock_client.get_my_trades.assert_called_once()

    def test_with_date_range(self):
        """带日期范围的查询。"""
        mock_client = MagicMock()
        mock_client.get_my_trades.return_value = MOCK_BTC_TRADES

        start_ms = date_to_ms("2025-05-01")
        end_ms = date_to_ms("2025-05-31")
        trades = fetch_trades_for_symbol(
            mock_client, "BTCUSDT", start_ms=start_ms, end_ms=end_ms
        )
        assert len(trades) == 2

    def test_empty_result(self):
        """无记录时返回空列表。"""
        mock_client = MagicMock()
        mock_client.get_my_trades.return_value = []

        trades = fetch_trades_for_symbol(mock_client, "BTCUSDT")
        assert trades == []

    def test_pagination(self):
        """超过 1000 条时分页查询。"""
        mock_client = MagicMock()

        # 第一页：1000 条
        page1 = [
            {
                "symbol": "BTCUSDT",
                "id": i,
                "price": "100000.00",
                "qty": "0.001",
                "quoteQty": "100.00",
                "commission": "0.0001",
                "commissionAsset": "BTC",
                "time": 1746518400000 + i * 1000,
                "isBuyer": True,
            }
            for i in range(1000)
        ]
        # 第二页：50 条
        page2 = [
            {
                "symbol": "BTCUSDT",
                "id": 1000 + i,
                "price": "100000.00",
                "qty": "0.001",
                "quoteQty": "100.00",
                "commission": "0.0001",
                "commissionAsset": "BTC",
                "time": 1746518400000 + (1000 + i) * 1000,
                "isBuyer": True,
            }
            for i in range(50)
        ]

        mock_client.get_my_trades.side_effect = [page1, page2]

        trades = fetch_trades_for_symbol(mock_client, "BTCUSDT")
        assert len(trades) == 1050
        assert mock_client.get_my_trades.call_count == 2


# ---------------------------------------------------------------------------
# format_output tests
# ---------------------------------------------------------------------------

class TestFormatOutput:
    def test_format_basic(self):
        """基本格式化输出。"""
        rows = format_output(MOCK_BTC_TRADES)
        assert len(rows) == 2

        first = rows[0]
        assert first["交易对"] == "BTCUSDT"
        assert first["方向"] == "卖出"
        assert first["数量"] == 0.1
        assert first["成交价"] == 94980.0
        assert first["金额"] == 9498.0
        assert first["手续费"] == 0.0001
        assert first["手续费币种"] == "BTC"

    def test_format_sorted_by_time(self):
        """输出应按时间排序。"""
        combined = MOCK_ETH_TRADES + MOCK_BTC_TRADES
        rows = format_output(combined)
        times = [r["成交时间"] for r in rows]
        assert times == sorted(times)

    def test_buy_side(self):
        """买入方向标签。"""
        buy_trade = [{
            "symbol": "ETHUSDT",
            "id": 1,
            "price": "3000.00",
            "qty": "1.0",
            "quoteQty": "3000.00",
            "commission": "0.001",
            "commissionAsset": "ETH",
            "time": 1746518400000,
            "isBuyer": True,
        }]
        rows = format_output(buy_trade)
        assert rows[0]["方向"] == "买入"


# ---------------------------------------------------------------------------
# discover_symbols tests
# ---------------------------------------------------------------------------

class TestDiscoverSymbols:
    def test_discovers_btc_and_eth(self):
        """能从账户余额中发现 BTC 和 ETH 的 USDT 交易对。"""
        mock_client = MagicMock()
        mock_client.get_account.return_value = {
            "balances": [
                {"asset": "BTC", "free": "0.05", "locked": "0.0"},
                {"asset": "ETH", "free": "1.0", "locked": "0.0"},
                {"asset": "USDT", "free": "500.0", "locked": "0.0"},
            ]
        }
        mock_client.get_exchange_info.return_value = {
            "symbols": [
                {"symbol": "BTCUSDT", "status": "TRADING"},
                {"symbol": "ETHUSDT", "status": "TRADING"},
                {"symbol": "BNBUSDT", "status": "TRADING"},
            ]
        }

        symbols = discover_symbols(mock_client)
        assert "BTCUSDT" in symbols
        assert "ETHUSDT" in symbols
        assert len(symbols) == 2  # USDT 本身被排除

    def test_skips_stablecoins(self):
        """稳定币不作为 base asset 查询。"""
        mock_client = MagicMock()
        mock_client.get_account.return_value = {
            "balances": [
                {"asset": "USDT", "free": "1000.0", "locked": "0.0"},
                {"asset": "USDC", "free": "500.0", "locked": "0.0"},
                {"asset": "BUSD", "free": "200.0", "locked": "0.0"},
                {"asset": "BTC", "free": "0.01", "locked": "0.0"},
            ]
        }
        mock_client.get_exchange_info.return_value = {
            "symbols": [
                {"symbol": "BTCUSDT", "status": "TRADING"},
            ]
        }

        symbols = discover_symbols(mock_client)
        assert symbols == ["BTCUSDT"]

    def test_fallback_to_busd(self):
        """如果 USDT 对不存在，回退到 BUSD。"""
        mock_client = MagicMock()
        mock_client.get_account.return_value = {
            "balances": [
                {"asset": "SOL", "free": "10.0", "locked": "0.0"},
            ]
        }
        mock_client.get_exchange_info.return_value = {
            "symbols": [
                {"symbol": "SOLBUSD", "status": "TRADING"},
            ]
        }

        symbols = discover_symbols(mock_client)
        assert symbols == ["SOLBUSD"]

    def test_empty_account(self):
        """空账户返回空列表。"""
        mock_client = MagicMock()
        mock_client.get_account.return_value = {
            "balances": [
                {"asset": "USDT", "free": "0.0", "locked": "0.0"},
            ]
        }
        mock_client.get_exchange_info.return_value = {
            "symbols": []
        }

        symbols = discover_symbols(mock_client)
        assert symbols == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
