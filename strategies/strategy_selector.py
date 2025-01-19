import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class StrategySelector:
    """Manages strategy selection and execution for different assets."""

    def __init__(self, strategies, max_concurrent_strategies=5):
        """
        Initialize the strategy selector.
        
        :param strategies: Dictionary of strategy objects.
        :param max_concurrent_strategies: Maximum number of concurrent strategies.
        """
        self.strategies = strategies  # {'strategy_name': strategy_object}
        self.max_concurrent_strategies = max_concurrent_strategies

    def select_strategy(self, market_condition, time_frame, pairwise=False):
        """
        Select an appropriate strategy based on market conditions and time frame.
        
        :param market_condition: Current market condition ('trend', 'range', 'volatility', etc.).
        :param time_frame: Time frame for the strategy (e.g., "1m", "1h", "1D").
        :param pairwise: Boolean indicating if the strategy applies to pairwise data.
        :return: Selected strategy names.
        """
        strategy_map = {
            "trend": {"allowed_timeframes": ["1m", "5m", "1h", "4h", "1D"], "strategies": ["trend_following", "scalping"]},
            "range": {"allowed_timeframes": ["5m", "15m", "30m"], "strategies": ["mean_reversion", "scalping"]},
            "volatility": {"allowed_timeframes": ["15m", "1h", "4h", "1D"], "strategies": ["breakout_strategy", "momentum_strategy"]},
        }

        if market_condition not in strategy_map:
            logger.warning(f"Unrecognized market condition: {market_condition}. Defaulting to trend-following.")
            market_condition = "trend"

        # Check if the time frame is valid for the selected market condition
        if time_frame not in strategy_map[market_condition]["allowed_timeframes"]:
            logger.warning(f"Time frame {time_frame} not supported for {market_condition} strategy. Using default.")
            time_frame = strategy_map[market_condition]["allowed_timeframes"][0]  # Default to the first allowed time frame

        strategies = strategy_map[market_condition]["strategies"]
        return strategies

    def execute_strategy(self, strategy_name, asset_identifier, asset_data, time_frame):
        """
        Execute a specific strategy for a given asset or pair, considering the time frame.
        
        :param strategy_name: Name of the strategy to execute.
        :param asset_identifier: Identifier for the asset (symbol or pair name).
        :param asset_data: Market data for the asset (or tuple for pairs).
        :param time_frame: Time frame for strategy execution (e.g., "1m", "1h").
        :return: Strategy result.
        """
        if strategy_name not in self.strategies:
            logger.error(f"Strategy {strategy_name} not found.")
            return None

        strategy = self.strategies[strategy_name]
        try:
            result = strategy(asset_data, time_frame)  # Pass time frame along with asset data to strategy
            logger.info(f"Executed {strategy_name} for {asset_identifier} with time frame {time_frame}. Result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error executing {strategy_name} for {asset_identifier}: {e}")
            return None

    def run_concurrent_strategies(self, asset_identifier, asset_data, selected_strategies, time_frame):
        """
        Run multiple strategies concurrently on the same asset, considering the time frame.
        
        :param asset_identifier: Identifier for the asset being traded.
        :param asset_data: Market data for the asset.
        :param selected_strategies: List of strategy names to execute.
        :param time_frame: Time frame for strategy execution (e.g., "1m", "1h").
        :return: Dictionary of strategy results.
        """
        results = {}
        with ThreadPoolExecutor(max_workers=self.max_concurrent_strategies) as executor:
            futures = {
                executor.submit(self.execute_strategy, strategy_name, asset_identifier, asset_data, time_frame): strategy_name
                for strategy_name in selected_strategies
            }
            for future in as_completed(futures):
                strategy_name = futures[future]
                try:
                    results[strategy_name] = future.result()
                except Exception as e:
                    logger.error(f"Error in concurrent execution of {strategy_name}: {e}")
                    results[strategy_name] = None
        return results

    def run_multiple_assets(self, assets_data, market_conditions, time_frames, pairwise_data=None):
        """
        Run strategies concurrently across multiple assets and asset pairs, considering time frames.
        
        :param assets_data: Dictionary of market data for each asset.
        :param market_conditions: Dictionary of market conditions for each asset.
        :param time_frames: Dictionary of time frames for each asset.
        :param pairwise_data: Dictionary of paired data for pairwise strategies.
                              Example: {"pair_name": (series1, series2)}.
        :return: Nested dictionary of results by asset/pair and strategy.
        """
        overall_results = {}

        # Single-asset strategies
        with ThreadPoolExecutor(max_workers=self.max_concurrent_strategies) as executor:
            single_asset_futures = {
                executor.submit(
                    self.run_concurrent_strategies,
                    asset_symbol,
                    asset_data,
                    self.select_strategy(market_conditions.get(asset_symbol, "trend"), time_frames.get(asset_symbol, "1h")),
                    time_frames.get(asset_symbol, "1h")
                ): asset_symbol
                for asset_symbol, asset_data in assets_data.items()
            }
            for future in as_completed(single_asset_futures):
                asset_symbol = single_asset_futures[future]
                try:
                    overall_results[asset_symbol] = future.result()
                except Exception as e:
                    logger.error(f"Error in concurrent execution for {asset_symbol}: {e}")
                    overall_results[asset_symbol] = None

        # Pairwise strategies
        if pairwise_data:
            with ThreadPoolExecutor(max_workers=self.max_concurrent_strategies) as executor:
                pairwise_futures = {
                    executor.submit(
                        self.run_concurrent_strategies,
                        pair_name,
                        (series1, series2),
                        self.select_strategy("volatility", time_frames.get(pair_name, "1h"), pairwise=True),
                        "1h"
                    ): pair_name
                    for pair_name, (series1, series2) in pairwise_data.items()
                }
                for future in as_completed(pairwise_futures):
                    pair_name = pairwise_futures[future]
                    try:
                        overall_results[pair_name] = future.result()
                    except Exception as e:
                        logger.error(f"Error in pairwise execution for {pair_name}: {e}")
                        overall_results[pair_name] = None

        return overall_results
