import numpy as np
import pandas as pd
import pytest
from engine.metrics import (
    calculate_max_drawdown,
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_portfolio_returns,
    calculate_sharpe_ratio,
)


@pytest.fixture
def sample_returns_df():
    """Creates a 3 day sample DataFrame for 2 stocks."""
    data = {
        "APPL": [0.01, 0.02, -0.01],
        "MSFT": [0.02, -0.01, 0.03],
    }
    return pd.DataFrame(data)


def test_calculate_portfolio_returns(sample_returns_df):
    weights = [0.5, 0.5]
    result = calculate_portfolio_returns(sample_returns_df, weights)

    # Expected daily returns for 50/50 split:
    # Day 1: (0.01 * 0.5) + (0.02 * 0.5) = 0.015
    # Day 2: (0.02 * 0.5) + (-0.01 * 0.5) = 0.005
    # Day 3: (-0.01 * 0.5) + (0.03 * 0.5) = 0.010
    expected = pd.Series([0.015, 0.005, 0.010])

    pd.testing.assert_series_equal(result, expected)


def test_calculate_annualized_return():
    # 252 trading days: +10% on day 1, 0% after
    returns = pd.Series([0.10] + [0.0] * 251)

    result = calculate_annualized_return(returns, trading_days=252)

    # Total return over exactly 1.0 year is 10% (0.10)
    assert pytest.approx(result, rel=1e-5) == 0.10


def test_calculate_max_drawdown():
    # Sequence: Gain 100%, (doubles to 2.0) then lose 50% (drops back to 1.0)
    returns = pd.Series([1.0, -0.5])

    result = calculate_max_drawdown(returns)

    # Peak growth = 2.0, Drop = 1.0. Drawdown = (1.0 - 2.0) / 2.0 = -0.50 (-50%)
    assert pytest.approx(result, rel=1e-5) == -0.50


def test_sharpe_ratio_zero_volatility():
    # Portfolio with constant 0% return every day
    returns = pd.Series([0.0] * 252)

    result = calculate_sharpe_ratio(returns, risk_free_rate=0.04)

    # Should safely return 0.0 with no error
    assert result == 0.0
