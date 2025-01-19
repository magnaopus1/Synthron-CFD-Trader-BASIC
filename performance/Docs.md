# Performance Package Documentation

The `performance` package is designed to analyze, evaluate, and report the results of trading strategies within the CFD Trading System. It includes modules for backtesting, calculating performance metrics, and generating reports. These tools enable users to understand the effectiveness and risks of their trading strategies in a robust and scalable manner.

---

## Table of Contents

1. [Backtesting (`backtesting.py`)](#backtesting)
2. [Performance Metrics (`metrics.py`)](#performance-metrics)
3. [Reporting (`reporting.py`)](#reporting)

---

## Backtesting

### File: `backtesting.py`

The `backtesting` module allows users to simulate trading strategies using historical data. It provides a framework to evaluate the profitability, risk, and execution of strategies.

### Classes and Methods

#### 1. `BacktestingEngine`

Simulates trading strategies with features like commission, slippage, and spread.

- **Attributes**:
  - `data`: Historical OHLCV data (DataFrame).
  - `strategy`: User-defined strategy function generating buy/sell signals.
  - `initial_balance`: Starting balance for the simulation.
  - `commission`, `spread`, `slippage`: Costs applied to trades.
  - `trades`: List of executed trades.
  - `balance_history`: Tracks balance and position changes over time.

- **Methods**:
  - `_validate_data(data)`: Ensures the data has required columns (`Open`, `High`, `Low`, `Close`, `Volume`).
  - `_execute_trade(signal, price, timestamp)`: Executes trades based on signals and updates balances and positions.
  - `run_backtest()`: Simulates the strategy on the provided historical data.
  - `load_historical_data_from_csv(file_path)`: Loads historical data from a CSV file.
  - `load_historical_data_from_mt5(symbol, timeframe, start, end)`: Fetches historical data from the MetaTrader 5 API.

---

## Performance Metrics

### File: `metrics.py`

The `metrics` module calculates quantitative performance metrics to assess trading strategies. It provides insights into profitability, risk, and strategy efficiency.

### Classes and Methods

#### 1. `PerformanceMetrics`

Analyzes trading and balance data to compute key metrics.

- **Attributes**:
  - `trades`: Trade details (timestamp, signal, price, balance, position).
  - `balance_history`: Balance and position data over time.
  - `risk_free_rate`: Risk-free rate for calculating Sharpe Ratio.

- **Methods**:
  - `calculate_sharpe_ratio()`: Computes the Sharpe Ratio.
  - `calculate_win_ratio()`: Calculates the percentage of profitable trades.
  - `calculate_risk_of_ruin()`: Estimates the likelihood of losing all capital.
  - `calculate_max_drawdown()`: Calculates the maximum drawdown as a percentage.
  - `calculate_avg_daily_gain()`: Computes average daily returns.
  - `calculate_avg_weekly_gain()`: Computes average weekly returns.
  - `calculate_metrics_summary()`: Summarizes all metrics in a dictionary.
  - `display_metrics_table(display_prompt)`: Displays metrics as a table.
  - `plot_performance(display_prompt)`: Plots balance, drawdown, and return distributions.

---

## Reporting

### File: `reporting.py`

The `reporting` module generates summaries and visualizations of trading performance. It also provides functionality to export results to various formats for further analysis.

### Classes and Methods

#### 1. `Reporting`

Generates and exports reports based on trading results.

- **Attributes**:
  - `trades`: DataFrame containing executed trade details.
  - `balance_history`: DataFrame with balance and performance history.
  - `log_file`: Path to the log file for tracking reporting actions.

- **Methods**:
  - `log_event(message, level)`: Logs significant events or errors.
  - `generate_trade_summary()`: Summarizes trading activity (e.g., win ratio, net profit).
  - `generate_performance_table()`: Creates daily, weekly, and monthly performance tables.
  - `export_report(file_path)`: Exports the report to an Excel file.
  - `display_trade_summary()`: Displays the trade summary in the console.
  - `display_historical_performance()`: Prints historical performance tables (daily, weekly, monthly).

### Features

- **Trade Summary**:
  - Provides an overview of total trades, win ratio, average trade profit, and net profit.

- **Historical Performance**:
  - Generates tables for daily, weekly, and monthly performance.
  - Includes percentage changes for easy comparison.

- **Export Functionality**:
  - Allows exporting reports to Excel files for offline analysis.

---

