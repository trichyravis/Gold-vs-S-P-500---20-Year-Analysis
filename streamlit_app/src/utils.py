
"""
Data fetcher module for Yahoo Finance data
Author: Prof. V. Ravichandran
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetch financial data from Yahoo Finance"""

    def __init__(self, tickers: list, start_date: str, end_date: Optional[str] = None):
        """
        Initialize DataFetcher
        
        Args:
            tickers: List of ticker symbols (e.g., ['GLD', 'SPY'])
            start_date: Start date as string (YYYY-MM-DD)
            end_date: End date as string (YYYY-MM-DD), defaults to today
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date if end_date else datetime.now().strftime('%Y-%m-%d')
        self.data = {}
        self.errors = {}

    def fetch_all(self) -> Tuple[Optional[Dict], Dict]:
        """
        Fetch data for all tickers
        
        Returns:
            Tuple of (data_dict, errors_dict)
        """
        logger.info(f"Starting fetch for tickers: {self.tickers}")
        logger.info(f"Date range: {self.start_date} to {self.end_date}")
        
        for ticker in self.tickers:
            try:
                logger.info(f"Fetching {ticker}...")
                self.data[ticker], error = self.fetch_ticker(ticker)
                if error:
                    self.errors[ticker] = error
                    logger.error(f"Error fetching {ticker}: {error}")
            except Exception as e:
                error_msg = f"Exception fetching {ticker}: {str(e)}"
                self.errors[ticker] = error_msg
                logger.error(error_msg)

        if not self.data or all(v is None for v in self.data.values()):
            logger.error("No data fetched for any ticker")
            return None, self.errors

        logger.info(f"Successfully fetched data for: {list(self.data.keys())}")
        return self.data, self.errors

    def fetch_ticker(self, ticker: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Fetch data for single ticker
        
        Args:
            ticker: Ticker symbol (e.g., 'GLD')
            
        Returns:
            Tuple of (dataframe, error_message)
        """
        try:
            logger.info(f"Downloading {ticker} from {self.start_date} to {self.end_date}")
            
            # Download data
            data = yf.download(
                ticker,
                start=self.start_date,
                end=self.end_date,
                progress=False
            )
            
            if data is None or data.empty:
                error_msg = f"No data returned for {ticker}"
                logger.warning(error_msg)
                return None, error_msg
            
            # Ensure DataFrame format
            if isinstance(data, pd.Series):
                data = data.to_frame()
            
            logger.info(f"Successfully downloaded {len(data)} rows for {ticker}")
            return data, None
            
        except Exception as e:
            error_msg = f"Error downloading {ticker}: {str(e)}"
            logger.error(error_msg)
            return None, error_msg

    def validate_data(self) -> Tuple[bool, str]:
        """
        Validate fetched data
        
        Returns:
            Tuple of (is_valid, message)
        """
        if not self.data:
            return False, "No data available"

        for ticker, df in self.data.items():
            if df is None or df.empty:
                return False, f"Empty data for {ticker}"

        return True, "Data validation passed"

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of fetched data"""
        summary = {}
        for ticker, df in self.data.items():
            if df is not None and not df.empty:
                summary[ticker] = {
                    'rows': len(df),
                    'columns': list(df.columns),
                    'date_range': f"{df.index[0]} to {df.index[-1]}",
                    'missing_values': df.isna().sum().to_dict()
                }
        return summary
