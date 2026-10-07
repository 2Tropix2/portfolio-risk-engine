# Portfolio Risk Engine

A lightweight Python quantitative analysis engine for fetching historical data via Yahoo Finance. Can compute risk, price data and performance metrics. Caches datasets locally for quick backtesting.

## Features 

- **Data Retrieval & Normalization:** Standizes market price downloads from Yahoo Finance (`yfinance`) for single and multi-asset portfolios across customizable data ranges.
- **Local Parquet Caching:** Caches downloaded data locally using `pyarrow` and `parquet` format to eliminate request limits.
- **Performance & Risk Metrics:** Implements core metrics including:
  - Annualized Return & Annualized Volatility
  - Sharpe Ratio 
  - Maximum Drawdown 
- **Modular Unit Tests:** Comprehensive unit tests with offline mocking using `pytest` and `unittest.mock`.

---

## Project Structure

```text
quant-engine/
│
├── engine/
│   ├── __init__.py
│   ├── fetcher.py        # DataFetcher class with yfinance & Parquet caching
│   └── metrics.py        # Portfolio return, Sharpe ratio, & volatility formulas
│
├── tests/
│   ├── test_fetcher.py   # Unit tests for data retrieval, caching, & edge cases
│   └── test_metrics.py   # Unit tests for quantitative financial formulas
│
├── .gitignore            # Ignores local caches, venv, and IDE files
├── main.py               # End-to-end demo execution pipeline
├── README.md             # Project documentation
└── requirements.txt      # Project dependencies