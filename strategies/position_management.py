import logging

logger = logging.getLogger(__name__)

class PositionManagement:
    """Handles position scaling, trailing stops, and conditional partial position closures."""

    def __init__(self, trailing_stop_buffer=0.01, scale_in_threshold=0.005, scale_out_threshold=0.01):
        """
        Initialize position management logic.
        
        :param trailing_stop_buffer: Percentage buffer for trailing stop adjustments.
        :param scale_in_threshold: Threshold for scaling into a position.
        :param scale_out_threshold: Threshold for scaling out of a position.
        """
        self.trailing_stop_buffer = trailing_stop_buffer
        self.scale_in_threshold = scale_in_threshold
        self.scale_out_threshold = scale_out_threshold

    def scale_in(self, current_price, entry_price, current_position, max_position, scale_step=0.1, time_frame="1H"):
        """
        Scale into a position if the price moves favorably by the scale-in threshold based on the time frame.
        
        :param current_price: Current market price.
        :param entry_price: Entry price of the position.
        :param current_position: Current size of the position.
        :param max_position: Maximum allowable position size.
        :param scale_step: Incremental scale-in percentage of max_position.
        :param time_frame: Time frame for strategy (e.g., "1m", "5m", "1h").
        :return: Adjusted position size.
        """
        valid_timeframes = {
            "1m": 0.5,  # 0.5% movement for 1m time frame
            "5m": 1,    # 1% movement for 5m time frame
            "15m": 1.5, # 1.5% movement for 15m time frame
            "30m": 2,   # 2% movement for 30m time frame
            "1h": 3,    # 3% movement for 1h time frame
            "4h": 5,    # 5% movement for 4h time frame
            "1D": 10,   # 10% movement for 1D time frame
        }
        
        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for scale-in. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        scale_threshold = valid_timeframes[time_frame]
        if current_price > entry_price * (1 + scale_threshold / 100) and current_position < max_position:
            scale_amount = min(scale_step * max_position, max_position - current_position)
            new_position = current_position + scale_amount
            logger.info(f"Scaling in: Added {scale_amount} to position. New position size: {new_position}")
            return new_position
        logger.info(f"Scale-in conditions not met for time frame {time_frame}.")
        return current_position

    def scale_out(self, current_price, entry_price, current_position, min_position, scale_step=0.1, time_frame="1H"):
        """
        Scale out of a position if the price moves against the scale-out threshold based on the time frame.
        
        :param current_price: Current market price.
        :param entry_price: Entry price of the position.
        :param current_position: Current size of the position.
        :param min_position: Minimum allowable position size.
        :param scale_step: Incremental scale-out percentage of current position.
        :param time_frame: Time frame for strategy (e.g., "1m", "5m", "1h").
        :return: Adjusted position size.
        """
        valid_timeframes = {
            "1m": 0.5,  # 0.5% movement for 1m time frame
            "5m": 1,    # 1% movement for 5m time frame
            "15m": 1.5, # 1.5% movement for 15m time frame
            "30m": 2,   # 2% movement for 30m time frame
            "1h": 3,    # 3% movement for 1h time frame
            "4h": 5,    # 5% movement for 4h time frame
            "1D": 10,   # 10% movement for 1D time frame
        }
        
        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for scale-out. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        scale_threshold = valid_timeframes[time_frame]
        if current_price < entry_price * (1 - scale_threshold / 100) and current_position > min_position:
            scale_amount = min(scale_step * current_position, current_position - min_position)
            new_position = current_position - scale_amount
            logger.info(f"Scaling out: Reduced position by {scale_amount}. New position size: {new_position}")
            return new_position
        logger.info(f"Scale-out conditions not met for time frame {time_frame}.")
        return current_position

    def apply_trailing_stop(self, current_price, trailing_stop_price, direction="long", time_frame="1H"):
        """
        Adjust trailing stop based on market movement and time frame.
        
        :param current_price: Current market price.
        :param trailing_stop_price: Current trailing stop price.
        :param direction: Direction of the position ('long' or 'short').
        :param time_frame: Time frame for strategy (e.g., "1m", "5m", "1h").
        :return: Updated trailing stop price.
        """
        valid_timeframes = {
            "1m": 0.001,  # 0.1% movement for 1m time frame
            "5m": 0.002,  # 0.2% movement for 5m time frame
            "1h": 0.005,  # 0.5% movement for 1h time frame
            "1D": 0.01,   # 1% movement for 1D time frame
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for trailing stop. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        buffer = valid_timeframes[time_frame]
        if direction == "long" and current_price > trailing_stop_price * (1 + buffer):
            new_stop = current_price * (1 - self.trailing_stop_buffer)
            logger.info(f"Trailing stop adjusted for long position: New stop price: {new_stop}")
            return new_stop
        elif direction == "short" and current_price < trailing_stop_price * (1 - buffer):
            new_stop = current_price * (1 + self.trailing_stop_buffer)
            logger.info(f"Trailing stop adjusted for short position: New stop price: {new_stop}")
            return new_stop
        logger.info("No trailing stop adjustment needed.")
        return trailing_stop_price

    def lock_profit(self, current_price, entry_price, position_size, lock_threshold=0.02, time_frame="1H"):
        """
        Lock in profit by partially closing the position when profit threshold is met, based on time frame.
        
        :param current_price: Current market price.
        :param entry_price: Entry price of the position.
        :param position_size: Current size of the position.
        :param lock_threshold: Profit percentage threshold for locking in profits.
        :param time_frame: Time frame for strategy (e.g., "1m", "5m", "1h").
        :return: Adjusted position size and profit locked.
        """
        valid_timeframes = {
            "1m": 0.5,  # 0.5% profit lock for 1m time frame
            "5m": 1,    # 1% profit lock for 5m time frame
            "1h": 2,    # 2% profit lock for 1h time frame
            "1D": 5,    # 5% profit lock for 1D time frame
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for profit locking. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        profit_threshold = valid_timeframes[time_frame]
        profit_percent = (current_price - entry_price) / entry_price if current_price > entry_price else 0
        if profit_percent >= profit_threshold / 100:
            lock_size = position_size * 0.25  # Lock 25% of the position
            new_position_size = position_size - lock_size
            logger.info(f"Profit locked: Closed {lock_size} of position. Remaining size: {new_position_size}")
            return new_position_size, lock_size
        logger.info("Profit-locking conditions not met.")
        return position_size, 0

    def partial_closing(self, current_price, entry_price, position_size, levels=None, time_frame="1H"):
        """
        Conditionally close partial positions at multiple profit levels, adjusted for time frame.
        
        :param current_price: Current market price.
        :param entry_price: Entry price of the position.
        :param position_size: Current size of the position.
        :param levels: List of profit percentage levels for partial closures.
        :param time_frame: Time frame for strategy (e.g., "1m", "5m", "1h").
        :return: Adjusted position size.
        """
        valid_timeframes = {
            "1m": [0.02],   # 2% profit levels for 1m
            "5m": [0.02, 0.05],  # 2%, 5% for 5m
            "1h": [0.05, 0.1],  # 5%, 10% for 1h
            "1D": [0.1, 0.2],  # 10%, 20% for 1D
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for partial closing. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        levels = valid_timeframes[time_frame]
        for level in levels:
            if current_price >= entry_price * (1 + level):
                partial_close = position_size * 0.1  # Close 10% of the position at each level
                position_size -= partial_close
                logger.info(f"Partial close: Closed {partial_close} of position at profit level {level * 100}%.")
        
        return position_size
