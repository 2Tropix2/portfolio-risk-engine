from unittest.mock import patch
import pandas as pd
import pytest
from engine.fetcher import DataFetcher


@pytest.fixture
def mock_yf_data():
    """Creates a fake pandas DataFrame mimicking yfinance download structure."""
    dates = pd.date_range(start="2023-01-01", periods=3, freq="D")

    # Create MultiIndex columns like yfinance returns for multiple tickers
    cols = pd.MultiIndex.from_tuples([
        ("Adj Close", "AAPL"),
        ("Adj Close", "MSFT"),
        ("Close", "AAPL"),
        ("Close", "MSFT"),
    ])

    data = pd.DataFrame(
        [
            [100.0, 200.0, 100.0, 200.0],
            [105.0, 202.0, 105.0, 202.0],
            [102.0, 204.0, 102.0, 204.0],
        ],
        index=dates,
        columns=cols,
    )
    return data


def test_fetch_prices_multi_ticker(mock_yf_data):
    # Test fetching prices for multiple tickers using mocked data.
    with patch("yfinance.download", return_value=mock_yf_data):
        fetcher = DataFetcher()  # No cache
        prices = fetcher.fetch_prices(
            tickers=["AAPL", "MSFT"], start="2023-01-01", end="2023-01-03")

        assert isinstance(prices, pd.DataFrame)
        assert list(prices.columns) == ["AAPL", "MSFT"]
        assert len(prices) == 3
        assert prices.loc["2023-01-01", "AAPL"] == 100.0


def test_fetch_returns(mock_yf_data):
    # Test daily return calculations from fetched prices.
    with patch("yfinance.download", return_value=mock_yf_data):
        fetcher = DataFetcher()
        returns = fetcher.fetch_returns(
            tickers=["AAPL", "MSFT"], start="2023-01-01", end="2023-01-03")

        assert len(returns) == 2  # First tow dropped for pct change
        assert pytest.approx(returns.loc["2023-01-02", "AAPL"], 0.0001) == 0.05


def test_empty_data_raises_error():
    # Test that empty yfinance response raises a ValueError.
    with patch("yfinance.download", return_value=pd.DataFrame()):
        fetcher = DataFetcher()
        with pytest.raises(ValueError, match="No data returned"):
            fetcher.fetch_prices(
                tickers="INVALID", start="2023-01-01", end="2023-01-03")


def test_catching(tmp_path, mock_yf_data):
    # Test that second call loads from cache directory without calling yfinance
    cache_dir = tmp_path / "test_cache"
    fetcher = DataFetcher(cache_dir=cache_dir)

    with patch("yfinance.download", return_value=mock_yf_data) as mock_download:
        # First call fetches and saves to cache
        prices1 = fetcher.fetch_prices(
            tickers=["AAPL", "MSFT"], start="2023-01-01", end="2023-01-03")
        assert mock_download.call_count == 1

        # Second call loads directly from cache disk without calling yfinace download
        prices2 = fetcher.fetch_prices(
            tickers=["AAPL", "MSFT"], start="2023-01-01", end="2023-01-03")
        assert mock_download.call_count == 1  # Download count stays 1!
        pd.testing.assert_frame_equal(prices1, prices2, check_freq=False)
