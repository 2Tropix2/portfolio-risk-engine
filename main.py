# main.py


from engine.fetcher import DataFetcher
from engine.metrics import (
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)


def main():
    print("=== Quantitative Engine Demo ===")

    # Initialize fetcher with local caching enabled
    fetcher = DataFetcher(cache_dir=".data_cache")

    tickers = ["AAPL", "MSFT", "SPY"]
    start_date = "2023-01-01"
    end_date = "2024-01-01"

    print(
        f"Fetching return data for {tickers} from {start_date} to {end_date}...")
    returns_df = fetcher.fetch_returns(
        tickers=tickers, start=start_date, end=end_date)

    print("\n--- Asset Performance Metrics ---")
    for ticker in returns_df.columns:
        series = returns_df[ticker]

        ann_ret = calculate_annualized_return(series)
        ann_vol = calculate_annualized_volatility(series)
        sharpe = calculate_sharpe_ratio(series)
        max_dd = calculate_max_drawdown(series)

        print(f"\n{ticker}:")
        print(f"  Annualized Return:     {ann_ret * 100:.2f}%")
        print(f"  Annualized Volatility: {ann_vol * 100:.2f}%")
        print(f"  Sharpe Ratio:          {sharpe:.2f}")
        print(f"  Max Drawdown:          {max_dd * 100:.2f}%")


if __name__ == "__main__":
    main()
