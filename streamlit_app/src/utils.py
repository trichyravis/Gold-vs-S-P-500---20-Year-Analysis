
"""
Data fetcher module for Yahoo Finance data with Streamlit integration
Author: Prof. V. Ravichandran
"""

import yfinance as yf
import pandas as pd
import logging
import streamlit as st
from datetime import datetime, timedelta
from typing import Tuple, Dict, Optional, List

# Configure logging to show in Streamlit Cloud "Manage App" console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetch financial data from Yahoo Finance with error handling and progress tracking"""

    def __init__(self, tickers: List[str], start_date: Optional[str] = None, end_date: Optional[str] = None):
        """
        Initialize DataFetcher
        
        Args:
            tickers: List of ticker symbols (e.g., ['GLD', 'SPY'])
            start_date: Start date as string (YYYY-MM-DD), optional
            end_date: End date as string (YYYY-MM-DD), optional
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.errors = []

    def fetch_all(self) -> Tuple[Optional[Dict], List]:
        """
        Fetches data with detailed error tracking and progress logging.
        
        Returns:
            Tuple of (raw_data dict, failed_tickers list)
        """
        raw_data = {}
        failed_tickers = []
        
        st.info(f"Starting data fetch for {len(self.tickers)} tickers...")
        logger.info(f"Starting data fetch for {len(self.tickers)} tickers: {self.tickers}")
        
        for ticker in self.tickers:
            try:
                logger.info(f"Attempting to fetch: {ticker}")
                st.write(f"📥 Fetching {ticker}...")
                
                # Create ticker object
                ticker_obj = yf.Ticker(ticker)
                
                # Fetch historical data
                if self.start_date and self.end_date:
                    logger.info(f"Fetching {ticker} from {self.start_date} to {self.end_date}")
                    df = ticker_obj.history(start=self.start_date, end=self.end_date)
                else:
                    logger.info(f"Fetching {ticker} for last 1 year")
                    df = ticker_obj.history(period="1y")
                
                # Validate data
                if df is None or df.empty:
                    logger.warning(f"Validation Check: {ticker} returned an empty DataFrame.")
                    failed_tickers.append(f"{ticker} (No data found)")
                    continue
                
                # Store data
                raw_data[ticker] = df
                logger.info(f"Successfully fetched {ticker}: {len(df)} rows found.")
                st.success(f"✅ {ticker}: {len(df)} rows fetched")
                
            except Exception as e:
                error_msg = f"Failed to fetch {ticker}: {str(e)}"
                logger.error(error_msg)
                st.error(f"❌ {error_msg}")
                failed_tickers.append(error_msg)
        
        # Check if any data was fetched
        if not raw_data:
            logger.error("Critical Failure: No data was retrieved for any tickers.")
            st.error("❌ Critical Failure: No data was retrieved for any tickers.")
            return None, failed_tickers
        
        # Log partial success if some tickers failed
        if failed_tickers:
            warning_msg = f"Partial success. Issues with: {', '.join(failed_tickers)}"
            logger.warning(warning_msg)
            st.warning(warning_msg)
        else:
            logger.info(f"Success! Fetched data for all {len(raw_data)} tickers.")
            st.success(f"✅ Success! Fetched data for all {len(raw_data)} tickers.")
        
        self.data = raw_data
        self.errors = failed_tickers
        return raw_data, failed_tickers

    def get_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """Get data for specific ticker"""
        if self.data and ticker in self.data:
            return self.data[ticker]
        return None

    def get_summary(self) -> Dict:
        """Get summary of fetched data"""
        summary = {
            'total_tickers_requested': len(self.tickers),
            'tickers_fetched': len(self.data) if self.data else 0,
            'failed_tickers': len(self.errors),
            'tickers_list': list(self.data.keys()) if self.data else [],
            'errors': self.errors
        }
        return summary
