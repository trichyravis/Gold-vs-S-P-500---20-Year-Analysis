"""
Data Fetcher Module - Yahoo Finance API Wrapper
Fetches historical price data for Gold (GLD) and S&P 500 (SPY)
Author: Prof. V. Ravichandran
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, Tuple, Optional
import warnings

# Suppress yfinance warnings
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.WARNING)

class DataFetcher:
    """Fetch historical financial data from Yahoo Finance"""
    
    def __init__(self, tickers: Dict[str, str], start_date: str, end_date: str = None):
        """
        Initialize DataFetcher
        
        Args:
            tickers: Dict of {name: ticker_symbol}
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD), defaults to today
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date or datetime.today().strftime('%Y-%m-%d')
        self.data = {}
        self.errors = []
        
    def fetch_single_ticker(self, ticker_symbol: str, ticker_name: str) -> Optional[pd.DataFrame]:
        """
        Fetch data for a single ticker
        
        Args:
            ticker_symbol: Ticker symbol (e.g., 'GLD')
            ticker_name: Friendly name (e.g., 'Gold')
            
        Returns:
            DataFrame or None if error
        """
        try:
            print(f"📥 Fetching {ticker_name} ({ticker_symbol})...")
            
            # Download data from Yahoo Finance
            data = yf.download(
                ticker_symbol,
                start=self.start_date,
                end=self.end_date,
                progress=False,
                interval='1d'
            )
            
            if data.empty:
                self.errors.append(f"No data found for {ticker_name} ({ticker_symbol})")
                return None
            
            # Reset index to make Date a column
            data.reset_index(inplace=True)
            
            # Rename columns for consistency
            data.columns = [col.lower() for col in data.columns]
            
            # Keep only relevant columns
            data = data[['date', 'close']].copy()
            data.columns = ['date', ticker_name.lower()]
            
            # Ensure date is datetime
            data['date'] = pd.to_datetime(data['date'])
            
            # Sort by date
            data = data.sort_values('date').reset_index(drop=True)
            
            print(f"✅ Successfully fetched {len(data)} rows for {ticker_name}")
            return data
            
        except Exception as e:
            error_msg = f"Error fetching {ticker_name}: {str(e)}"
            self.errors.append(error_msg)
            print(f"❌ {error_msg}")
            return None
    
    def fetch_all(self) -> Tuple[Optional[pd.DataFrame], list]:
        """
        Fetch data for all tickers and merge them
        
        Returns:
            Tuple of (merged_dataframe, list_of_errors)
        """
        dfs = {}
        
        # Fetch each ticker
        for name, symbol in self.tickers.items():
            df = self.fetch_single_ticker(symbol, name.capitalize())
            if df is not None:
                dfs[name] = df
        
        # Check if we got all data
        if len(dfs) == 0:
            return None, self.errors
        
        # Merge on common dates
        merged = None
        for name, df in dfs.items():
            if merged is None:
                merged = df.copy()
            else:
                merged = pd.merge(merged, df, on='date', how='inner')
        
        if merged is None or merged.empty:
            self.errors.append("Failed to merge data from all tickers")
            return None, self.errors
        
        # Rename columns to proper format
        merged.columns = ['date', 'gold', 'sp500']
        
        return merged, self.errors
    
    def validate_dates(self, df: pd.DataFrame) -> Tuple[bool, list]:
        """
        Validate date range and consistency
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        if df.empty:
            issues.append("DataFrame is empty")
            return False, issues
        
        # Check date range
        min_date = df['date'].min()
        max_date = df['date'].max()
        
        print(f"📅 Date range: {min_date.date()} to {max_date.date()}")
        
        # Check for future dates
        if max_date > datetime.today():
            issues.append(f"Future dates detected: {max_date}")
        
        # Check for duplicates
        if df['date'].duplicated().any():
            issues.append(f"Duplicate dates found: {df['date'][df['date'].duplicated()].unique()}")
        
        # Check date continuity (allowing for weekends/holidays)
        date_diffs = df['date'].diff().dt.days
        suspicious_gaps = date_diffs[date_diffs > 2]
        if len(suspicious_gaps) > 0:
            issues.append(f"Suspicious date gaps (> 2 days): {len(suspicious_gaps)} occurrences")
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    def get_basic_stats(self, df: pd.DataFrame) -> Dict:
        """
        Calculate basic statistics
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary of statistics
        """
        stats = {
            'total_rows': len(df),
            'start_date': df['date'].min(),
            'end_date': df['date'].max(),
            'total_days': (df['date'].max() - df['date'].min()).days,
            'gold_price_min': df['gold'].min(),
            'gold_price_max': df['gold'].max(),
            'gold_price_avg': df['gold'].mean(),
            'sp500_price_min': df['sp500'].min(),
            'sp500_price_max': df['sp500'].max(),
            'sp500_price_avg': df['sp500'].mean(),
        }
        return stats
