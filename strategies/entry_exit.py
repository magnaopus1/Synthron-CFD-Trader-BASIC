import pandas as pd
from data.indicators import Indicators
from utils.logger import logger


class EntryExitStrategy:
    """Defines entry and exit strategies based on indicators and market conditions."""

    def __init__(self, max_exposure_per_asset=0.01, sharpe_ratio_target=3):
        """
        Initialize the entry and exit strategy.
        
        :param max_exposure_per_asset: Maximum allowable exposure per asset.
        :param sharpe_ratio_target: Target Sharpe ratio for strategy selection.
        """
        self.max_exposure_per_asset = max_exposure_per_asset
        self.sharpe_ratio_target = sharpe_ratio_target

    def trend_following(self, data: pd.Series, period: int = 50, confirmation_period: int = 200, time_frame="1H"):
        """Trend-following strategy using multiple moving averages with confirmation."""
        valid_timeframes = {
            "1m": [5, 15],
            "5m": [15, 30],
            "15m": [30, 60],
            "1h": [50, 200],
            "4h": [50, 200],
            "1D": [200, 500],
            "1W": [500, 1000]
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for Trend Following strategy. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        sma_short = Indicators.moving_average(data, valid_timeframes[time_frame][0])
        sma_long = Indicators.moving_average(data, valid_timeframes[time_frame][1])
        current_price = data.iloc[-1]
        
        if current_price > sma_short.iloc[-1] and sma_short.iloc[-1] > sma_long.iloc[-1]:
            logger.info(f"Trend-following: Buy signal confirmed on {time_frame} time frame.")
            return "BUY"
        elif current_price < sma_short.iloc[-1] and sma_short.iloc[-1] < sma_long.iloc[-1]:
            logger.info(f"Trend-following: Sell signal confirmed on {time_frame} time frame.")
            return "SELL"
        return "HOLD"

    def mean_reversion(self, data: pd.Series, z_window: int = 20, confirmation_rsi: int = 14, time_frame="1H"):
        """Mean reversion strategy using Z-score and RSI for confirmation."""
        valid_timeframes = {
            "5m": [5, 15],
            "15m": [15, 30],
            "30m": [30, 60],
            "1h": [50, 200],
            "4h": [50, 200],
            "1D": [200, 500],
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for Mean Reversion strategy. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        z_score = Indicators.z_score(data, valid_timeframes[time_frame][0])
        rsi = Indicators.relative_strength_index(data, confirmation_rsi)
        
        if z_score.iloc[-1] > 2 and rsi.iloc[-1] > 70:
            logger.info(f"Mean Reversion: Sell signal confirmed on {time_frame} time frame.")
            return "SELL"
        elif z_score.iloc[-1] < -2 and rsi.iloc[-1] < 30:
            logger.info(f"Mean Reversion: Buy signal confirmed on {time_frame} time frame.")
            return "BUY"
        return "HOLD"

    def breakout_strategy(self, data: pd.Series, period: int = 14, confirmation_ema: int = 20, time_frame="1H"):
        """Breakout strategy using Bollinger Bands and EMA for confirmation."""
        valid_timeframes = {
            "15m": [5, 15],
            "1h": [14, 30],
            "4h": [14, 50],
            "1D": [50, 100],
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for Breakout strategy. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        bands = Indicators.bollinger_bands(data, valid_timeframes[time_frame][0])
        ema = Indicators.exponential_moving_average(data, valid_timeframes[time_frame][1])
        current_price = data.iloc[-1]
        
        if current_price > bands['Upper Band'].iloc[-1] and current_price > ema.iloc[-1]:
            logger.info(f"Breakout: Buy signal confirmed on {time_frame} time frame.")
            return "BUY"
        elif current_price < bands['Lower Band'].iloc[-1] and current_price < ema.iloc[-1]:
            logger.info(f"Breakout: Sell signal confirmed on {time_frame} time frame.")
            return "SELL"
        return "HOLD"

    def momentum_strategy(self, data: pd.Series, period: int = 14, confirmation_z: int = 20, time_frame="1H"):
        """Momentum strategy using RSI with Z-score confirmation."""
        valid_timeframes = {
            "1m": [5, 10],
            "5m": [5, 15],
            "15m": [10, 30],
            "1h": [30, 50],
            "4h": [50, 100],
            "1D": [100, 200],
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for Momentum strategy. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        rsi = Indicators.relative_strength_index(data, valid_timeframes[time_frame][0])
        z_score = Indicators.z_score(data, confirmation_z)
        
        if rsi.iloc[-1] < 30 and z_score.iloc[-1] < -2:
            logger.info(f"Momentum: Buy signal confirmed on {time_frame} time frame.")
            return "BUY"
        elif rsi.iloc[-1] > 70 and z_score.iloc[-1] > 2:
            logger.info(f"Momentum: Sell signal confirmed on {time_frame} time frame.")
            return "SELL"
        return "HOLD"

    def scalping_strategy(self, data: pd.Series, period_fast: int = 5, period_slow: int = 20, confirmation_rsi: int = 14, time_frame="1m"):
        """Scalping strategy using fast and slow EMAs with RSI confirmation."""
        valid_timeframes = {
            "1m": [5, 10],
            "5m": [5, 10],
            "15m": [10, 15],
            "30m": [15, 20],
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for Scalping strategy. Defaulting to 1m.")
            time_frame = "1m"  # Default fallback

        ema_fast = Indicators.exponential_moving_average(data, valid_timeframes[time_frame][0])
        ema_slow = Indicators.exponential_moving_average(data, valid_timeframes[time_frame][1])
        rsi = Indicators.relative_strength_index(data, confirmation_rsi)
        
        if ema_fast.iloc[-1] > ema_slow.iloc[-1] and 30 < rsi.iloc[-1] < 70:
            logger.info(f"Scalping: Buy signal confirmed on {time_frame} time frame.")
            return "BUY"
        elif ema_fast.iloc[-1] < ema_slow.iloc[-1] and 30 < rsi.iloc[-1] < 70:
            logger.info(f"Scalping: Sell signal confirmed on {time_frame} time frame.")
            return "SELL"
        return "HOLD"

    def cointegration_strategy(self, series1: pd.Series, series2: pd.Series, confirmation_z: int = 20, time_frame="1h"):
        """Pairs trading strategy using cointegration with Z-score confirmation."""
        valid_timeframes = {
            "1h": [20],
            "4h": [50],
            "1D": [100],
        }

        if time_frame not in valid_timeframes:
            logger.warning(f"Time frame {time_frame} not supported for Cointegration strategy. Defaulting to 1H.")
            time_frame = "1H"  # Default fallback

        p_value = Indicators.cointegration(series1, series2)
        if p_value < 0.05:
            logger.info(f"Cointegration: Pair is cointegrated on {time_frame} time frame.")
            spread = series1 - series2
            z_score = Indicators.z_score(spread, confirmation_z)
            if z_score.iloc[-1] > 2:
                logger.info(f"Cointegration: Sell signal on spread confirmed on {time_frame} time frame.")
                return "SELL"
            elif z_score.iloc[-1] < -2:
                logger.info(f"Cointegration: Buy signal on spread confirmed on {time_frame} time frame.")
                return "BUY"
        logger.info(f"Cointegration: No trade signal on {time_frame} time frame.")
        return "HOLD"
    
    # Method for combining strategies with time frame condition applied
    def combine_strategies(self, data: pd.DataFrame, pairwise_data: dict = None, time_frame="1H"):
        """
        Combine multiple strategies to generate trade signals.
        
        :param data: A DataFrame containing price and volume data for single-asset strategies.
        :param pairwise_data: A dictionary containing paired data for cointegration strategies.
                            Example: {"pair_name": (series1, series2)}.
        :param time_frame: Time frame for strategy execution.
        :return: A dictionary of trade signals for each strategy.
        """
        signals = {}

        # Single-asset strategies
        for symbol, series in data.iteritems():
            trend_signal = self.trend_following(series, time_frame=time_frame)
            mean_reversion_signal = self.mean_reversion(series, time_frame=time_frame)
            breakout_signal = self.breakout_strategy(series, time_frame=time_frame)
            momentum_signal = self.momentum_strategy(series, time_frame=time_frame)
            scalping_signal = self.scalping_strategy(series, time_frame=time_frame)

            signals[symbol] = {
                "TrendFollowing": trend_signal,
                "MeanReversion": mean_reversion_signal,
                "Breakout": breakout_signal,
                "Momentum": momentum_signal,
                "Scalping": scalping_signal,
            }

        # Pairwise strategies
        if pairwise_data:
            for pair_name, (series1, series2) in pairwise_data.items():
                cointegration_signal = self.cointegration_strategy(series1, series2, time_frame=time_frame)
                signals[pair_name] = {"Cointegration": cointegration_signal}

        return signals
