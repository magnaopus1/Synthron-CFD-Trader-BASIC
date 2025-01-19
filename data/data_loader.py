import MetaTrader5 as mt5
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, max_workers: int = 5):
        """
        Initialize DataLoader and connect to MT5.
        :param max_workers: Maximum number of threads for concurrent data fetching.
        """
        self.max_workers = max_workers
        if not mt5.initialize():
            logger.error(f"Failed to initialize MT5: {mt5.last_error()}")
            raise RuntimeError("MT5 Initialization failed")
        logger.info("MT5 initialized successfully.")

    def fetch_symbol_info(self, symbol: str) -> Optional[Dict]:
        """Fetch symbol information."""
        if not symbol:
            logger.error("Symbol cannot be empty.")
            return None
        info = mt5.symbol_info(symbol)
        if info is None:
            logger.warning(f"Symbol {symbol} information not found: {mt5.last_error()}")
            return None
        return info._asdict()

    def fetch_symbol_tick(self, symbol: str) -> Optional[Dict]:
        """Fetch the latest tick data for a symbol."""
        if not symbol:
            logger.error("Symbol cannot be empty.")
            return None
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            logger.warning(f"Tick data for symbol {symbol} not found: {mt5.last_error()}")
            return None
        return tick._asdict()

    def fetch_historical_data(
        self, symbol: str, timeframe: int, start: datetime, end: datetime
    ) -> Optional[pd.DataFrame]:
        """Fetch historical bars for a symbol."""
        if not symbol or not start or not end:
            logger.error("Symbol, start date, and end date must be provided.")
            return None
        if start >= end:
            logger.error("Start date must be earlier than the end date.")
            return None
        rates = mt5.copy_rates_range(symbol, timeframe, start, end)
        if rates is None:
            logger.error(f"Failed to fetch historical data for {symbol}: {mt5.last_error()}")
            return None
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def fetch_open_positions(self) -> List[Dict]:
        """Fetch all open positions."""
        positions = mt5.positions_get()
        if positions is None:
            logger.error(f"Failed to fetch open positions: {mt5.last_error()}")
            return []
        return [pos._asdict() for pos in positions]

    def fetch_margin_requirements(self, symbol: str, lot_size: float, trade_type: int) -> Optional[float]:
        """Calculate margin requirements for a trade."""
        if lot_size <= 0:
            logger.error("Lot size must be greater than zero.")
            return None
        margin = mt5.order_calc_margin(trade_type, symbol, lot_size, 0)
        if margin is None:
            logger.error(f"Failed to calculate margin for {symbol}: {mt5.last_error()}")
            return None
        return margin

    def fetch_all_symbols(self) -> List[str]:
        """Fetch all symbols available in the terminal."""
        symbols = mt5.symbols_get()
        if symbols is None:
            logger.error(f"Failed to fetch symbols: {mt5.last_error()}")
            return []
        return [symbol.name for symbol in symbols]

    def fetch_leverage(self, symbol: str) -> Optional[float]:
        """Fetch leverage information for a symbol."""
        info = self.fetch_symbol_info(symbol)
        if info:
            return info.get("margin_rate")
        return None

    def fetch_account_info(self) -> Optional[Dict]:
        """Fetch account information."""
        info = mt5.account_info()
        if info is None:
            logger.error(f"Failed to fetch account info: {mt5.last_error()}")
            return None
        return info._asdict()

    def fetch_live_data(self, symbols: List[str]) -> List[Dict]:
        """Fetch live data for multiple symbols concurrently."""
        if not symbols:
            logger.error("Symbol list cannot be empty.")
            return []
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.fetch_symbol_tick, symbol): symbol for symbol in symbols}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    logger.error(f"Error fetching live data: {e}")
        return results

    def validate_symbols(self, symbols: List[str]) -> List[str]:
        """Validate if symbols are available in the market."""
        available_symbols = self.fetch_all_symbols()
        valid_symbols = [symbol for symbol in symbols if symbol in available_symbols]
        if len(valid_symbols) != len(symbols):
            logger.warning("Some symbols are invalid or unavailable.")
        return valid_symbols

    def shutdown(self):
        """Shutdown MT5 connection."""
        if mt5.shutdown():
            logger.info("MT5 shutdown completed.")
        else:
            logger.error(f"Failed to shutdown MT5: {mt5.last_error()}")
