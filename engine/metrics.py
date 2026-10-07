import numpy as np
import pandas as pd


def calculate_portfolio_returns(returns_df: pd.DataFrame, weights: list[float]) -> pd.Series:
    """
    Calculates weighted portfolio returns daily
    """

    weights = np.array(weights)
    portfolio_daily_returns = returns_df.dot(weights)
    return portfolio_daily_returns


def calculate_annualized_return(portfolio_returns: pd.Series, trading_days: int = 252) -> float:
    """
    Calculates compound annualized return
    """
    total_cum_return = (1 + portfolio_returns).prod() - 1
    num_years = len(portfolio_returns) / trading_days
    if num_years == 0:
        return 0.0
    annualized_return = (1 + total_cum_return) ** (1 / num_years) - 1
    return float(annualized_return)


def calculate_annualized_volatility(portfolio_returns: pd.Series, trading_days: int = 252) -> float:
    """
    Calculates annual volatility (standard deviation).
    """
    daily_vol = portfolio_returns.std()
    annualized_vol = daily_vol * np.sqrt(trading_days)
    return float(annualized_vol)


def calculate_sharpe_ratio(portfolio_returns: pd.Series, risk_free_rate: float = 0.04, trading_days: int = 252) -> float:
    """
    Calculates the sharpe ratio
    """
    annual_return = calculate_annualized_return(
        portfolio_returns, trading_days)
    annual_vol = calculate_annualized_volatility(
        portfolio_returns, trading_days)

    if annual_vol == 0:
        return 0.0
    sharpe = (annual_return - risk_free_rate) / annual_vol
    return float(sharpe)


def calculate_max_drawdown(portfolio_returns: pd.Series) -> float:
    """
    Calculates maximum drawdown
    """
    cum_growth = (1 + portfolio_returns).cumprod()
    rolling_peak = cum_growth.cummax()
    drawdowns = (cum_growth - rolling_peak) / rolling_peak
    max_drawdown = drawdowns.min()
    return float(max_drawdown)
