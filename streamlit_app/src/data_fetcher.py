
"""
Data Fetcher Module
Handles fetching real-time stock data from Yahoo Finance with robust error handling
Author: Prof. V. Ravichandran
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import time
from typing import Tuple, Dict, Optional, List, Union


class DataFetcher:
    """
    Fetches real-time financial data for Gold (GLD) and S&P 500 (SPY) from Yahoo Finance
    with robust rate limit handling and error recovery
    """
    
    def __init__(self, tickers: Union[Dict, List], start_date: Optional[str] = None, end_date: Optional[str] = None):
        """
        Initialize DataFetcher
        
        Args:
            tickers: Can be dict {'gold': 'GLD', 'sp500': 'SPY'} or list ['GLD', 'SPY']
            start_date: Start date as string (YYYY-MM-DD), optional
            end_date: End date as string (YYYY-MM-DD), optional
        """
        # Handle both dict and list formats
        if isinstance(tickers, dict):
            self.tickers = list(tickers.values())  # Extract ticker symbols
            self.ticker_names = tickers  # Keep mapping for reference
        else:
            self.tickers = tickers if isinstance(tickers, list) else [tickers]
            self.ticker_names = {ticker.lower(): ticker for ticker in self.tickers}
        
        self.start_date = start_date
        self.end_date = end_date
        self.cache = {}
        self.data = None
        self.errors = []

    def fetch_all(self) -> Tuple[Optional[Dict], List]:
        """
        Fetches data with detailed error tracking, rate limit handling, and progress logging.
        Uses exponential backoff for rate limiting.
        
        Returns:
            Tuple of (raw_data dict, failed_tickers list)
        """
        raw_data = {}
        failed_tickers = []
        
        st.info(f"Starting data fetch for {len(self.tickers)} tickers: {', '.join(self.tickers)}...")
        print(f"Starting data fetch for {len(self.tickers)} tickers: {self.tickers}")
        
        # Process each ticker
        for idx, ticker in enumerate(self.tickers):
            try:
                print(f"Attempting to fetch: {ticker} ({idx+1}/{len(self.tickers)})")
                st.write(f"📥 Fetching {ticker}... ({idx+1}/{len(self.tickers)})")
                
                # Fetch data with retry logic
                df = self._fetch_with_retry(ticker)
                
                if df is not None and not df.empty:
                    raw_data[ticker] = df
                    print(f"Successfully fetched {ticker}: {len(df)} rows found.")
                    st.success(f"✅ {ticker}: {len(df)} rows fetched")
                else:
                    error_msg = f"{ticker} (No data found)"
                    print(f"Validation Check: {ticker} returned an empty DataFrame.")
                    failed_tickers.append(error_msg)
                    st.warning(f"⚠️ {error_msg}")
                
            except Exception as e:
                error_msg = f"Failed to fetch {ticker}: {str(e)}"
                print(f"ERROR: {error_msg}")
                st.error(f"❌ {error_msg}")
                failed_tickers.append(error_msg)
        
        # Check if any data was fetched
        if not raw_data:
            error_msg = "Critical Failure: No data was retrieved for any tickers."
            print(f"ERROR: {error_msg}")
            st.error(f"❌ {error_msg}")
            self.data = None
            self.errors = failed_tickers
            return None, failed_tickers
        
        # Log partial success if some tickers failed
        if failed_tickers:
            warning_msg = f"Partial success. Issues with: {', '.join(failed_tickers)}"
            print(f"WARNING: {warning_msg}")
            st.warning(warning_msg)
        else:
            success_msg = f"Success! Fetched data for all {len(raw_data)} tickers."
            print(f"INFO: {success_msg}")
            st.success(f"✅ {success_msg}")
        
        self.data = raw_data
        self.errors = failed_tickers
        return raw_data, failed_tickers

    def _fetch_with_retry(self, ticker: str, max_retries: int = 3) -> Optional[pd.DataFrame]:
        """
        Fetch data for a single ticker with exponential backoff retry logic
        
        Args:
            ticker: Ticker symbol (e.g., 'GLD', 'SPY')
            max_retries: Maximum number of retries
            
        Returns:
            DataFrame or None if fetch fails
        """
        base_wait = 5  # Start with 5 seconds
        
        for attempt in range(max_retries):
            try:
                print(f"  Attempt {attempt + 1}/{max_retries} for {ticker}")
                
                # Prepare download parameters
                kwargs = {
                    'progress': False,
                    'interval': '1d',
                    'timeout': 60
                }
                
                # Add date range if specified
                if self.start_date and self.end_date:
                    kwargs['start'] = self.start_date
                    kwargs['end'] = self.end_date
                    print(f"  Date range: {self.start_date} to {self.end_date}")
                else:
                    kwargs['period'] = '1y'
                    print(f"  Using period: 1 year")
                
                # Download data
                print(f"  Downloading {ticker} from Yahoo Finance...")
                data = yf.download(ticker, **kwargs)
                
                # Validate and process data
                if data is None or data.empty:
                    print(f"  WARNING: Empty data for {ticker}")
                    return None
                
                # Ensure DataFrame format with Close prices
                if isinstance(data, pd.Series):
                    data = data.to_frame()
                
                # Extract Close prices
                if 'Close' in data.columns:
                    close_data = data[['Close']].copy()
                elif len(data.columns) > 0:
                    close_data = data.iloc[:, [0]].copy()
                else:
                    print(f"  ERROR: No price data in {ticker}")
                    return None
                
                # Ensure DateTime index
                close_data.index = pd.to_datetime(close_data.index)
                
                # Remove NaN values
                close_data = close_data.dropna()
                
                if close_data.empty:
                    print(f"  WARNING: All data is NaN for {ticker}")
                    return None
                
                print(f"  SUCCESS: Fetched {len(close_data)} rows for {ticker}")
                return close_data
                
            except Exception as e:
                error_str = str(e).lower()
                
                # Check if it's a rate limit error
                is_rate_limit = any(keyword in error_str for keyword in 
                                   ['rate', 'too many', 'throttle', '429', '503', 'timeout', '403'])
                
                if is_rate_limit and attempt < max_retries - 1:
                    # Exponential backoff: 5s, 10s, 20s
                    wait_time = base_wait * (2 ** attempt)
                    print(f"  ⏳ Rate limited. Waiting {wait_time}s before retry...")
                    st.warning(f"⏳ Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{max_retries - 1}...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"  ERROR (attempt {attempt + 1}/{max_retries}): {str(e)}")
                    if attempt == max_retries - 1:
                        print(f"  All retries exhausted for {ticker}")
                        raise
        
        return None

    def get_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        Get data for specific ticker
        
        Args:
            ticker: Ticker symbol
            
        Returns:
            DataFrame or None
        """
        if self.data and ticker in self.data:
            return self.data[ticker]
        return None

    def get_summary(self) -> Dict:
        """
        Get summary of fetched data
        
        Returns:
            Dictionary with fetch summary
        """
        summary = {
            'total_tickers_requested': len(self.tickers),
            'tickers_fetched': len(self.data) if self.data else 0,
            'failed_tickers': len(self.errors),
            'tickers_list': list(self.data.keys()) if self.data else [],
            'errors': self.errors
        }
        return summary

    def validate_data(self, data: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate fetched data quality
        
        Args:
            data: Stock price data DataFrame
        
        Returns:
            Tuple of (is_valid, message)
        """
        if data is None or data.empty:
            return False, "Data is empty"
        
        # Check minimum data points (at least 50 trading days)
        if len(data) < 50:
            return False, f"Insufficient data: {len(data)} rows (need at least 50)"
        
        # Check for NaN values
        nan_count = data.isnull().sum().sum()
        if nan_count > 0:
            return False, f"Data contains {nan_count} NaN values"
        
        # Check data has positive prices
        if (data <= 0).any().any():
            return False, "Data contains non-positive prices"
        
        return True, "Data validation passed"
