import logging

logger = logging.getLogger(__name__)

class RiskManagement:
    """Manages risk via stop-loss, take-profit, and position sizing."""

    def __init__(self, account_balance, leverage, max_drawdown, risk_per_trade, default_lot_size):
        """
        Initialize the risk management module.
        
        :param account_balance: Current account balance.
        :param leverage: Account leverage.
        :param max_drawdown: Maximum allowable drawdown as a percentage.
        :param risk_per_trade: Risk per trade as a percentage of account balance.
        :param default_lot_size: Default lot size for trading.
        """
        self.account_balance = account_balance
        self.leverage = leverage
        self.max_drawdown = max_drawdown
        self.risk_per_trade = risk_per_trade
        self.default_lot_size = default_lot_size

    def calculate_position_size(self, stop_loss_pips, pip_value):
        """
        Calculate the appropriate position size based on risk per trade.
        
        :param stop_loss_pips: Stop-loss in pips.
        :param pip_value: Value of one pip for the trading pair.
        :return: Position size in lots.
        """
        risk_amount = self.account_balance * self.risk_per_trade
        position_size = risk_amount / (stop_loss_pips * pip_value)
        logger.info(f"Calculated position size: {position_size} lots for risk amount: {risk_amount}.")
        return round(position_size, 2)

    def calculate_stop_loss(self, entry_price, direction, stop_loss_buffer, time_frame="1H"):
        """
        Calculate stop-loss price based on entry price and buffer, adjusted for time frame.
        
        :param entry_price: The entry price of the trade.
        :param direction: 'long' or 'short'.
        :param stop_loss_buffer: Buffer for stop-loss in percentage.
        :param time_frame: Time frame for strategy (e.g., "1m", "5m", "1h").
        :return: Stop-loss price.
        """
        valid_timeframes = {
            "1m": 0.001,  # 0.1% movement for 1m time frame
            "5m": 0.002,  # 0.2% movement for 5m time frame
            "1h": 0.005,  # 0.5% movement for 1h time frame
            "4h": 0.01,   # 1% movement for 4h time frame
            "1D": 0.02,   # 2% movement for 1D time frame
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for stop-loss. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        buffer = valid_timeframes[time_frame]
        if direction == "long":
            stop_loss = entry_price * (1 - buffer)
        elif direction == "short":
            stop_loss = entry_price * (1 + buffer)
        else:
            raise ValueError("Direction must be 'long' or 'short'.")
        
        logger.info(f"Stop-loss calculated at: {stop_loss} for direction: {direction} with time frame {time_frame}.")
        return stop_loss

    def calculate_take_profit(self, entry_price, direction, take_profit_buffer, time_frame="1H"):
        """
        Calculate take-profit price based on entry price and buffer, adjusted for time frame.
        
        :param entry_price: The entry price of the trade.
        :param direction: 'long' or 'short'.
        :param take_profit_buffer: Buffer for take-profit in percentage.
        :param time_frame: Time frame for strategy (e.g., "1m", "5m", "1h").
        :return: Take-profit price.
        """
        valid_timeframes = {
            "1m": 0.002,   # 0.2% for 1m
            "5m": 0.005,   # 0.5% for 5m
            "1h": 0.01,    # 1% for 1h
            "4h": 0.02,    # 2% for 4h
            "1D": 0.05,    # 5% for 1D
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for take-profit. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        buffer = valid_timeframes[time_frame]
        if direction == "long":
            take_profit = entry_price * (1 + take_profit_buffer * buffer)
        elif direction == "short":
            take_profit = entry_price * (1 - take_profit_buffer * buffer)
        else:
            raise ValueError("Direction must be 'long' or 'short'.")
        
        logger.info(f"Take-profit calculated at: {take_profit} for direction: {direction} with time frame {time_frame}.")
        return take_profit

    def check_drawdown_limit(self, current_drawdown):
        """
        Check if the current drawdown exceeds the maximum allowed drawdown.
        
        :param current_drawdown: Current drawdown as a percentage of the account balance.
        :return: Boolean indicating whether trading should halt.
        """
        if current_drawdown > self.max_drawdown:
            logger.warning("Maximum drawdown exceeded. Halting trading.")
            return False
        logger.info("Drawdown within acceptable limits.")
        return True

    def validate_trade_conditions(self, spread, min_spread_threshold, max_spread_threshold, current_open_trades, max_open_trades):
        """
        Validate if a trade can be executed based on conditions.
        
        :param spread: Current spread of the trading pair.
        :param min_spread_threshold: Minimum acceptable spread.
        :param max_spread_threshold: Maximum acceptable spread.
        :param current_open_trades: Number of currently open trades.
        :param max_open_trades: Maximum allowable open trades.
        :return: Boolean indicating whether trade conditions are met.
        """
        if not (min_spread_threshold <= spread <= max_spread_threshold):
            logger.warning(f"Spread {spread} out of acceptable range [{min_spread_threshold}, {max_spread_threshold}].")
            return False
        if current_open_trades >= max_open_trades:
            logger.warning(f"Max open trades limit reached: {current_open_trades}/{max_open_trades}.")
            return False
        logger.info("Trade conditions validated successfully.")
        return True

    def apply_stop_loss_take_profit(self, entry_price, direction, stop_loss_buffer, take_profit_buffer, time_frame="1H"):
        """
        Apply stop-loss and take-profit levels for a trade, adjusted by time frame.
        
        :param entry_price: Entry price of the trade.
        :param direction: 'long' or 'short'.
        :param stop_loss_buffer: Buffer for stop-loss in percentage.
        :param take_profit_buffer: Buffer for take-profit in percentage.
        :param time_frame: Time frame for strategy (e.g., "1m", "5m", "1h").
        :return: Dictionary containing stop-loss and take-profit levels.
        """
        stop_loss = self.calculate_stop_loss(entry_price, direction, stop_loss_buffer, time_frame)
        take_profit = self.calculate_take_profit(entry_price, direction, take_profit_buffer, time_frame)
        logger.info(f"Stop-loss: {stop_loss}, Take-profit: {take_profit} with time frame {time_frame}")
        return {"stop_loss": stop_loss, "take_profit": take_profit}
