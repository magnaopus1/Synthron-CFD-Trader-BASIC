# Data Package Documentation

The `data` package provides robust tools for data fetching, cleaning, preprocessing, and technical indicator calculations, essential for building scalable and effective trading systems. It includes modules for interacting with the MetaTrader 5 API, transforming raw market data, and generating features for analysis and machine learning models.

---

## Table of Contents

1. [Data Loader (`data_loader.py`)](#data-loader)
2. [Data Processing (`data_processing.py`)](#data-processing)
3. [Indicators (`indicators.py`)](#indicators)

---

## Data Loader

### File: `data_loader.py`

The `data_loader` module is designed to fetch market data using the MetaTrader 5 (MT5) API. It supports concurrent data fetching, validation, and retrieval of critical account and symbol information.

### Classes and Methods

#### 1. `DataLoader`

Fetches and manages data from the MetaTrader 5 API.

- **Attributes**:
  - `max_workers`: Maximum number of threads for concurrent data fetching.

- **Methods**:
  - `fetch_symbol_info(symbol)`: Retrieves detailed information about a specific symbol.
  - `fetch_symbol_tick(symbol)`: Fetches the latest tick data for a given symbol.
  - `fetch_historical_data(symbol, timeframe, start, end)`: Retrieves historical OHLC data for a symbol.
  - `fetch_open_positions()`: Retrieves all currently open positions.
  - `fetch_margin_requirements(symbol, lot_size, trade_type)`: Calculates the margin required for a trade.
  - `fetch_all_symbols()`: Returns a list of all symbols available on the MT5 platform.
  - `fetch_leverage(symbol)`: Retrieves the leverage for a specified symbol.
  - `fetch_account_info()`: Fetches information about the connected trading account.
  - `fetch_live_data(symbols)`: Concurrently fetches live tick data for multiple symbols.
  - `validate_symbols(symbols)`: Validates a list of symbols to ensure they are tradable.
  - `shutdown()`: Closes the connection to the MT5 API.

---

## Data Processing

### File: `data_processing.py`

The `data_processing` module provides utilities for cleaning, normalizing, and transforming raw market data. It includes methods for handling outliers, generating lag features, and creating features for machine learning.

### Classes and Methods

#### 1. `DataProcessing`

Processes raw market data for analysis and modeling.

- **Methods**:
  - `clean_data(data, fill_method, handle_outliers)`: Cleans the input data by handling missing values, duplicates, and outliers.
  - `normalize_data(data, method, feature_range)`: Normalizes data using Min-Max scaling or Z-score standardization.
  - `add_technical_indicators(data, price_column, indicators)`: Adds user-defined technical indicators to the dataset.
  - `add_custom_features(data)`: Generates custom features like log returns, skewness, and kurtosis.
  - `preprocess_data(data, target_column, normalize)`: Prepares data for machine learning by splitting into features (`X`) and target (`y`).
  - `generate_lag_features(data, columns, lags)`: Creates lagged features for time-series modeling.

---

## Indicators

### File: `indicators.py`

The `indicators` module provides a comprehensive suite of technical indicators for analyzing market trends, volatility, and momentum. These indicators can be directly applied to price and volume data for trading strategy development.

### Classes and Methods

#### 1. `Indicators`

Calculates technical indicators for financial data.

- **Methods**:
  - `moving_average(data, period)`: Computes the Simple Moving Average (SMA).
  - `exponential_moving_average(data, period)`: Computes the Exponential Moving Average (EMA).
  - `bollinger_bands(data, period, std_dev)`: Calculates Bollinger Bands with configurable standard deviations.
  - `relative_strength_index(data, period)`: Computes the Relative Strength Index (RSI).
  - `macd(data, fast_period, slow_period, signal_period)`: Calculates the Moving Average Convergence Divergence (MACD) and signal line.
  - `stochastic(data, high, low, period)`: Computes the Stochastic Oscillator (%K and %D lines).
  - `z_score(data, window)`: Calculates the Z-score for a rolling window.
  - `correlation_matrix(data)`: Computes the correlation matrix for a dataset.
  - `cointegration(series1, series2)`: Determines the cointegration between two time-series.
  - `on_balance_volume(close, volume)`: Computes the On-Balance Volume (OBV) for trend confirmation.

