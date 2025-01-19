# CFD Trading System - Strategies Documentation

## Overview

The strategies package in the CFD Trading System manages various aspects of trading strategies, including **Entry/Exit**, **Position Management**, **Risk Management**, and **Strategy Selection**. The package utilizes multiple types of strategies to identify trading opportunities based on market conditions, manage the risk associated with trades, and dynamically adjust position sizes.

### Key Components

- **EntryExitStrategy**: Defines rules for entering and exiting positions based on market indicators.
- **PositionManagement**: Handles position scaling, trailing stops, and conditional partial position closures.
- **RiskManagement**: Manages risk, stop-loss, take-profit, and position sizing based on account parameters.
- **StrategySelector**: Dynamically selects and executes multiple strategies based on market conditions and trading pairs.

---

## 1. EntryExitStrategy

### Purpose:
The **EntryExitStrategy** class manages the logic for entering and exiting trades. It uses a combination of technical indicators to determine when to buy or sell an asset.

### Functions:

#### `__init__(self, max_exposure_per_asset=0.01, sharpe_ratio_target=3)`
- **max_exposure_per_asset**: The maximum percentage of total portfolio risk allowed for each trade.
- **sharpe_ratio_target**: Target Sharpe ratio to evaluate the profitability of strategies.

#### `trend_following(self, data: pd.Series, period: int = 50, confirmation_period: int = 200)`
- **Purpose**: Identifies trends using Simple Moving Averages (SMA).
- **Logic**: If the current price is above the short-term SMA and the short-term SMA is above the long-term SMA, the strategy signals a **BUY**. Otherwise, it signals a **SELL**.

#### `mean_reversion(self, data: pd.Series, z_window: int = 20, confirmation_rsi: int = 14)`
- **Purpose**: Identifies mean reversion opportunities based on Z-score and Relative Strength Index (RSI).
- **Logic**: If the Z-score is above 2 and RSI is above 70, signal a **SELL**. If the Z-score is below -2 and RSI is below 30, signal a **BUY**.

#### `breakout_strategy(self, data: pd.Series, period: int = 14, confirmation_ema: int = 20)`
- **Purpose**: Identifies breakout opportunities using Bollinger Bands and Exponential Moving Average (EMA).
- **Logic**: If the price is above the upper Bollinger Band and the EMA, signal a **BUY**. If the price is below the lower Bollinger Band and the EMA, signal a **SELL**.

#### `momentum_strategy(self, data: pd.Series, period: int = 14, confirmation_z: int = 20)`
- **Purpose**: Momentum strategy using RSI with Z-score confirmation.
- **Logic**: If RSI is below 30 and Z-score is below -2, signal a **BUY**. If RSI is above 70 and Z-score is above 2, signal a **SELL**.

#### `scalping_strategy(self, data: pd.Series, period_fast: int = 5, period_slow: int = 20, confirmation_rsi: int = 14)`
- **Purpose**: A fast-paced strategy using fast and slow EMAs combined with RSI confirmation.
- **Logic**: Signal a **BUY** when the fast EMA is above the slow EMA and RSI is between 30 and 70. Signal a **SELL** when the fast EMA is below the slow EMA and RSI is between 30 and 70.

#### `cointegration_strategy(self, series1: pd.Series, series2: pd.Series, confirmation_z: int = 20)`
- **Purpose**: Pairs trading strategy using cointegration and Z-score.
- **Logic**: If the cointegration p-value is below 0.05, check the Z-score of the spread. If the Z-score is above 2, signal a **SELL**; if below -2, signal a **BUY**.

#### `combine_strategies(self, data: pd.DataFrame, pairwise_data: dict = None)`
- **Purpose**: Combines results from multiple strategies, including both single-asset and pairwise strategies.
- **Logic**: Executes single-asset strategies (trend-following, mean reversion, etc.) and pairwise strategies (cointegration).

#### `execute_trade(self, symbol: str, signal: str, current_exposure: float)`
- **Purpose**: Executes a trade based on the generated signal, ensuring no overexposure.
- **Logic**: Executes a **BUY** or **SELL** if the conditions are met, otherwise holds the position.

---

## 2. PositionManagement

### Purpose:
The **PositionManagement** class handles position scaling, trailing stops, and profit-locking mechanisms.

### Functions:

#### `__init__(self, trailing_stop_buffer=0.01, scale_in_threshold=0.005, scale_out_threshold=0.01)`
- **trailing_stop_buffer**: Buffer to adjust the trailing stop.
- **scale_in_threshold**: Threshold for scaling into a position.
- **scale_out_threshold**: Threshold for scaling out of a position.

#### `scale_in(self, current_price, entry_price, current_position, max_position, scale_step=0.1)`
- **Purpose**: Scales into a position if the price moves favorably by the scale-in threshold.
- **Logic**: Increases position size by a specified step if the price moves in the favorable direction.

#### `scale_out(self, current_price, entry_price, current_position, min_position, scale_step=0.1)`
- **Purpose**: Scales out of a position if the price moves unfavorably.
- **Logic**: Reduces position size by a specified step if the price moves in the unfavorable direction.

#### `apply_trailing_stop(self, current_price, trailing_stop_price, direction="long")`
- **Purpose**: Adjusts the trailing stop based on market movement.
- **Logic**: Moves the trailing stop based on favorable price movements.

#### `lock_profit(self, current_price, entry_price, position_size, lock_threshold=0.02)`
- **Purpose**: Locks in profits by partially closing the position when the profit threshold is met.
- **Logic**: Closes part of the position (typically 25%) if the price has moved in the favorable direction by the specified profit threshold.

#### `partial_closing(self, current_price, entry_price, position_size, levels=None)`
- **Purpose**: Conditionally closes partial positions at multiple profit levels.
- **Logic**: Closes portions of the position at predetermined profit levels (e.g., 2%, 5%, 10%).

---

## 3. RiskManagement

### Purpose:
The **RiskManagement** class manages risk via stop-loss, take-profit, and position sizing based on account parameters.

### Functions:

#### `__init__(self, account_balance, leverage, max_drawdown, risk_per_trade, default_lot_size)`
- **account_balance**: The current account balance.
- **leverage**: The leverage applied to the account.
- **max_drawdown**: Maximum allowable drawdown percentage.
- **risk_per_trade**: Percentage of the account balance risked per trade.
- **default_lot_size**: Default lot size for the trades.

#### `calculate_position_size(self, stop_loss_pips, pip_value)`
- **Purpose**: Calculates the position size based on risk per trade and stop-loss distance.
- **Logic**: Determines the number of lots to trade based on the user's risk parameters.

#### `calculate_stop_loss(self, entry_price, direction, stop_loss_buffer)`
- **Purpose**: Calculates the stop-loss price based on entry price and a buffer.
- **Logic**: Computes the stop-loss price based on the direction of the trade (long or short).

#### `calculate_take_profit(self, entry_price, direction, take_profit_buffer)`
- **Purpose**: Calculates the take-profit price based on entry price and buffer.
- **Logic**: Computes the take-profit price based on the direction of the trade (long or short).

#### `check_drawdown_limit(self, current_drawdown)`
- **Purpose**: Checks if the current drawdown exceeds the maximum allowable limit.
- **Logic**: If the drawdown exceeds the limit, trading is halted.

#### `validate_trade_conditions(self, spread, min_spread_threshold, max_spread_threshold, current_open_trades, max_open_trades)`
- **Purpose**: Validates trade execution conditions, such as spread and open trades.
- **Logic**: Ensures that the spread is within acceptable limits and that the number of open trades does not exceed the maximum.

#### `apply_stop_loss_take_profit(self, entry_price, direction, stop_loss_buffer, take_profit_buffer)`
- **Purpose**: Applies stop-loss and take-profit levels for a trade.
- **Logic**: Calculates both stop-loss and take-profit levels based on entry price, direction, and buffers.

---

## 4. StrategySelector

### Purpose:
The **StrategySelector** class selects and executes strategies based on market conditions.

### Functions:

#### `__init__(self, strategies, max_concurrent_strategies=5)`
- **strategies**: A dictionary of available strategy functions.
- **max_concurrent_strategies**: Maximum number of strategies that can run concurrently.

#### `select_strategy(self, market_condition, pairwise=False)`
- **Purpose**: Selects appropriate strategies based on market conditions.
- **Logic**: Chooses strategies based on market state (e.g., trend, range, volatility).

#### `execute_strategy(self, strategy_name, asset_identifier, asset_data)`
- **Purpose**: Executes a specific strategy for a given asset or pair.
- **Logic**: Runs the strategy and logs the result.

#### `run_concurrent_strategies(self, asset_identifier, asset_data, selected_strategies)`
- **Purpose**: Runs multiple strategies concurrently on the same asset.
- **Logic**: Uses concurrent execution to run multiple strategies in parallel.

#### `run_multiple_assets(self, assets_data, market_conditions, pairwise_data=None)`
- **Purpose**: Executes strategies across multiple assets and asset pairs.
- **Logic**: Runs both single-asset and pairwise strategies concurrently.

---

## Conclusion

This comprehensive documentation outlines the full set of functionalities available in the strategies package of the CFD Trading System. The system is designed to be flexible, scalable, and capable of handling complex trading operations with dynamic risk management, strategy selection, and position management. The integration of multiple strategies ensures that the system can adapt to varying market conditions and execute trades efficiently.
