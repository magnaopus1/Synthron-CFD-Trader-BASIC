import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import logging

# Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class DataProcessing:
    """Class for data cleaning, normalization, preprocessing, and feature engineering."""

    @staticmethod
    def clean_data(data: pd.DataFrame, fill_method: str = 'ffill', handle_outliers: bool = False) -> pd.DataFrame:
        """
        Clean the input data by handling missing values, duplicates, and outliers.
        :param data: Input DataFrame.
        :param fill_method: Method for filling missing values ('ffill', 'bfill', or 'mean').
        :param handle_outliers: Whether to handle outliers (replace with NaN).
        :return: Cleaned DataFrame.
        """
        if not isinstance(data, pd.DataFrame):
            logger.error("Input data must be a pandas DataFrame.")
            raise ValueError("Input data must be a pandas DataFrame.")
        
        logger.info("Cleaning data: Handling missing values, duplicates, and outliers.")
        data = data.drop_duplicates()

        if handle_outliers:
            z_scores = np.abs((data - data.mean()) / data.std())
            data[z_scores > 3] = np.nan
            logger.info("Outliers replaced with NaN based on Z-score.")

        if fill_method == 'mean':
            data = data.fillna(data.mean())
        elif fill_method in ['ffill', 'bfill']:
            data = data.fillna(method=fill_method)
        else:
            logger.error("Invalid fill_method. Choose 'ffill', 'bfill', or 'mean'.")
            raise ValueError("Invalid fill_method. Choose 'ffill', 'bfill', or 'mean'.")
        
        return data

    @staticmethod
    def normalize_data(data: pd.DataFrame, method: str = 'minmax', feature_range=(0, 1)) -> pd.DataFrame:
        """
        Normalize the input data using the specified method.
        :param data: Input DataFrame.
        :param method: Normalization method ('minmax' or 'zscore').
        :param feature_range: Feature range for MinMaxScaler (used only with 'minmax').
        :return: Normalized DataFrame.
        """
        if not isinstance(data, pd.DataFrame):
            logger.error("Input data must be a pandas DataFrame.")
            raise ValueError("Input data must be a pandas DataFrame.")
        
        logger.info(f"Normalizing data using {method} method.")
        if method == 'minmax':
            scaler = MinMaxScaler(feature_range=feature_range)
            normalized_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns, index=data.index)
        elif method == 'zscore':
            scaler = StandardScaler()
            normalized_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns, index=data.index)
        else:
            logger.error("Invalid normalization method. Choose 'minmax' or 'zscore'.")
            raise ValueError("Invalid normalization method. Choose 'minmax' or 'zscore'.")
        
        return normalized_data

    @staticmethod
    def add_technical_indicators(data: pd.DataFrame, price_column: str, indicators: dict) -> pd.DataFrame:
        """
        Add technical indicators to the DataFrame.
        :param data: Input DataFrame.
        :param price_column: The column used for price-based indicators.
        :param indicators: Dictionary with indicator names and their respective functions.
        :return: DataFrame with added indicators.
        """
        if price_column not in data.columns:
            logger.error(f"Column {price_column} not found in data.")
            raise ValueError(f"Column {price_column} not found in data.")
        
        logger.info("Adding technical indicators to the dataset.")
        for name, func in indicators.items():
            try:
                data[name] = func(data[price_column])
                logger.info(f"Added indicator: {name}")
            except Exception as e:
                logger.error(f"Error adding indicator {name}: {e}")
        
        return data

    @staticmethod
    def add_custom_features(data: pd.DataFrame) -> pd.DataFrame:
        """
        Add custom features to the dataset.
        Example: Log returns, skewness, and kurtosis.
        :param data: Input DataFrame.
        :return: DataFrame with added custom features.
        """
        logger.info("Adding custom features to the dataset.")
        
        if 'Close' in data.columns:
            data['Log Return'] = np.log(data['Close'] / data['Close'].shift(1))
            data['Skewness'] = data['Close'].rolling(window=14).skew()
            data['Kurtosis'] = data['Close'].rolling(window=14).kurt()
            logger.info("Added 'Log Return', 'Skewness', and 'Kurtosis'.")

        if 'Volume' in data.columns:
            data['Volume Change'] = data['Volume'].pct_change()
            logger.info("Added 'Volume Change'.")

        return data

    @staticmethod
    def preprocess_data(data: pd.DataFrame, target_column: str, normalize: bool = True) -> tuple[pd.DataFrame, pd.Series]:
        """
        Preprocess the data for machine learning models.
        :param data: Input DataFrame.
        :param target_column: The target column for prediction.
        :param normalize: Whether to normalize the features.
        :return: Tuple of features (X) and target (y).
        """
        if target_column not in data.columns:
            logger.error(f"Target column {target_column} not found in data.")
            raise ValueError(f"Target column {target_column} not found in data.")
        
        logger.info("Preprocessing data for model training.")
        y = data[target_column]
        X = data.drop(columns=[target_column])

        if normalize:
            logger.info("Normalizing feature data.")
            X = DataProcessing.normalize_data(X)
        
        return X, y

    @staticmethod
    def generate_lag_features(data: pd.DataFrame, columns: list, lags: int) -> pd.DataFrame:
        """
        Generate lag features for time series data.
        :param data: Input DataFrame.
        :param columns: List of columns to generate lag features for.
        :param lags: Number of lags to generate.
        :return: DataFrame with lag features.
        """
        if not all(col in data.columns for col in columns):
            logger.error("One or more columns for lag features are missing in the data.")
            raise ValueError("Invalid columns for lag features.")
        
        logger.info(f"Generating lag features for columns: {columns}")
        for col in columns:
            for lag in range(1, lags + 1):
                data[f"{col}_lag{lag}"] = data[col].shift(lag)
                logger.info(f"Added lag feature: {col}_lag{lag}")
        
        return data
