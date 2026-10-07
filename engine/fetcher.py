# engine/fetcher.py

from pathlib import Path
import pandas as pd
import yfinance as yf


class DataFetcher:
    # Fetches, cleans and optionally caches historical market data using yfinance

    def __init__(self, cache_dir: str | Path | None = None):
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch_prices(
            self,
            tickers: str | list[str],
            start: str,
            end: str,
            column: str = "Adj Close",
    ) -> pd.DataFrame:
        if isinstance(tickers, str):
            tickers = [tickers]

        tickers = [t.upper() for t in tickers]

        cache_key = f"{'_'.join(sorted(tickers))}_{start}_{end}_{column.lower().replace(' ', '_')}.parquet"
        if self.cache_dir:
            cache_path = self.cache_dir / cache_key
            if cache_path.exists():
                return pd.read_parquet(cache_path)

        data = yf.download(
            tickers=tickers,
            start=start,
            end=end,
            progress=False,
            auto_adjust=False,
        )

        if data.empty:
            raise ValueError(
                f"No data returned for tickers {tickers} between {start} and {end}.")

        if len(tickers) == 1:
            if isinstance(data.columns, pd.MultiIndex):
                prices = data[column]
            else:
                prices = data[[column]]
            prices.columns = tickers
        else:
            prices = data[column]

        prices = prices.dropna(how="all")
        prices.index = pd.to_datetime(prices.index)
        prices.index.name = "Date"

        if self.cache_dir:
            prices.to_parquet(cache_path)

        return prices

    def fetch_returns(
            self,
            tickers: str | list[str],
            start: str,
            end: str,
            column: str = "Adj Close",
    ) -> pd.DataFrame:
        prices = self.fetch_prices(
            tickers=tickers, start=start, end=end, column=column)
        returns = prices.pct_change().dropna(how="all")
        return returns
