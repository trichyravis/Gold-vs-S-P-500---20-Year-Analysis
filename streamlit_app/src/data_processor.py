"""
Data Processor Module - Validation, cleaning, and quality assessment
Author: Prof. V. Ravichandran
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Tuple, List
import json
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Process and validate financial data"""
    
    def __init__(self, validation_rules: Dict):
        """
        Initialize DataProcessor
        
        Args:
            validation_rules: Dictionary of validation parameters
        """
        self.validation_rules = validation_rules
        self.quality_checks = []
        self.data = None
        
    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main processing pipeline
        
        Args:
            df: Raw DataFrame from fetcher
            
        Returns:
            Processed DataFrame
        """
        # Make a copy to avoid modifying original
        processed = df.copy()
        
        # Ensure date column is datetime
        processed['date'] = pd.to_datetime(processed['date'])
        
        # Sort by date
        processed = processed.sort_values('date').reset_index(drop=True)
        
        # Handle missing values (forward fill)
        processed = self._handle_missing_values(processed)
        
        # Ensure numeric types
        processed['gold'] = pd.to_numeric(processed['gold'], errors='coerce')
        processed['sp500'] = pd.to_numeric(processed['sp500'], errors='coerce')
        
        # Calculate daily returns
        processed['gold_return'] = processed['gold'].pct_change() * 100
        processed['sp500_return'] = processed['sp500'].pct_change() * 100
        
        # Calculate cumulative returns
        processed['gold_cumulative'] = (1 + processed['gold_return'] / 100).cumprod() - 1
        processed['sp500_cumulative'] = (1 + processed['sp500_return'] / 100).cumprod() - 1
        
        self.data = processed
        return processed
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values with forward fill"""
        # Forward fill for price columns
        df['gold'] = df['gold'].fillna(method='ffill').fillna(method='bfill')
        df['sp500'] = df['sp500'].fillna(method='ffill').fillna(method='bfill')
        
        return df
    
    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, Dict, float]:
        """
        Perform comprehensive data validation
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, results_dict, quality_score)
        """
        results = {
            'passed': [],
            'failed': [],
            'warnings': [],
            'details': {}
        }
        
        # Check 1: No negative prices
        check_name = "No negative prices"
        if (df['gold'] < 0).any() or (df['sp500'] < 0).any():
            results['failed'].append(check_name)
        else:
            results['passed'].append(check_name)
        
        # Check 2: No future dates
        check_name = "No future dates"
        future_dates = df['date'] > datetime.today()
        if future_dates.any():
            results['failed'].append(check_name)
            results['details'][check_name] = f"Found {future_dates.sum()} future dates"
        else:
            results['passed'].append(check_name)
        
        # Check 3: Reasonable daily changes
        check_name = "Reasonable daily price changes (max 10%)"
        gold_changes = df['gold'].pct_change().abs() * 100
        sp500_changes = df['sp500'].pct_change().abs() * 100
        
        max_change = self.validation_rules.get('max_daily_change_pct', 10.0)
        gold_outliers = (gold_changes > max_change).sum()
        sp500_outliers = (sp500_changes > max_change).sum()
        
        if gold_outliers > 0 or sp500_outliers > 0:
            results['warnings'].append(check_name)
            results['details'][check_name] = f"Gold: {gold_outliers}, S&P500: {sp500_outliers} changes > {max_change}%"
        else:
            results['passed'].append(check_name)
        
        # Check 4: Date continuity
        check_name = "Complete date range (no gaps > 2 business days)"
        date_diffs = df['date'].diff().dt.days
        max_gap = self.validation_rules.get('max_gap_business_days', 2)
        gaps = (date_diffs > max_gap).sum()
        
        if gaps > 0:
            results['warnings'].append(check_name)
            results['details'][check_name] = f"Found {gaps} gaps > {max_gap} days (expected on weekends/holidays)"
        else:
            results['passed'].append(check_name)
        
        # Check 5: Same number of records
        check_name = "Same number of records for both assets"
        gold_count = df['gold'].notna().sum()
        sp500_count = df['sp500'].notna().sum()
        
        if gold_count != sp500_count:
            results['failed'].append(check_name)
            results['details'][check_name] = f"Gold: {gold_count}, S&P500: {sp500_count}"
        else:
            results['passed'].append(check_name)
        
        # Check 6: No duplicate dates
        check_name = "No duplicate dates"
        duplicates = df['date'].duplicated().sum()
        
        if duplicates > 0:
            results['failed'].append(check_name)
            results['details'][check_name] = f"Found {duplicates} duplicate dates"
        else:
            results['passed'].append(check_name)
        
        # Check 7: Numeric prices
        check_name = "Prices are numeric"
        gold_numeric = pd.to_numeric(df['gold'], errors='coerce').notna().sum() == len(df)
        sp500_numeric = pd.to_numeric(df['sp500'], errors='coerce').notna().sum() == len(df)
        
        if not (gold_numeric and sp500_numeric):
            results['failed'].append(check_name)
        else:
            results['passed'].append(check_name)
        
        # Check 8: Consistent date format
        check_name = "Date format is consistent"
        try:
            all_dates = pd.to_datetime(df['date'])
            results['passed'].append(check_name)
        except:
            results['failed'].append(check_name)
        
        # Check 9: No NULL values
        check_name = "No NULL values (or properly handled)"
        gold_nulls = df['gold'].isna().sum()
        sp500_nulls = df['sp500'].isna().sum()
        
        if gold_nulls > 0 or sp500_nulls > 0:
            results['warnings'].append(check_name)
            results['details'][check_name] = f"Gold NULLs: {gold_nulls}, S&P500 NULLs: {sp500_nulls} (forward-filled)"
        else:
            results['passed'].append(check_name)
        
        # Check 10: Expected trading days
        check_name = "Data matches expected trading days"
        expected_trading_days = len(df)
        actual_trading_days = (df['date'].max() - df['date'].min()).days
        
        # Trading days should be roughly 252 per year
        expected_per_year = 252
        years = (df['date'].max() - df['date'].min()).days / 365.25
        expected_total = int(expected_per_year * years)
        
        trading_ratio = expected_trading_days / expected_total if expected_total > 0 else 0
        
        if trading_ratio < 0.95:  # Allow 5% variance
            results['warnings'].append(check_name)
            results['details'][check_name] = f"Expected ~{expected_total}, got {expected_trading_days} (ratio: {trading_ratio:.1%})"
        else:
            results['passed'].append(check_name)
        
        # Calculate quality score
        total_checks = len(results['passed']) + len(results['failed'])
        passed_checks = len(results['passed'])
        
        # Failures count more than warnings
        failure_penalty = len(results['failed']) * 10
        warning_penalty = len(results['warnings']) * 2
        
        quality_score = max(0, 100 - failure_penalty - warning_penalty)
        quality_score = min(100, quality_score)
        
        # Determine if data is valid (at least 8/10 checks passed)
        is_valid = len(results['failed']) == 0
        
        results['summary'] = {
            'total_checks': total_checks,
            'passed': len(results['passed']),
            'failed': len(results['failed']),
            'warnings': len(results['warnings']),
            'quality_score': round(quality_score, 1)
        }
        
        return is_valid, results, quality_score
    
    def calculate_quality_metrics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate detailed quality metrics
        
        Args:
            df: Processed DataFrame
            
        Returns:
            Dictionary of quality metrics
        """
        metrics = {
            'data_completeness': {
                'gold': {
                    'total_rows': len(df),
                    'non_null': df['gold'].notna().sum(),
                    'null_count': df['gold'].isna().sum(),
                    'completeness_pct': (df['gold'].notna().sum() / len(df) * 100) if len(df) > 0 else 0
                },
                'sp500': {
                    'total_rows': len(df),
                    'non_null': df['sp500'].notna().sum(),
                    'null_count': df['sp500'].isna().sum(),
                    'completeness_pct': (df['sp500'].notna().sum() / len(df) * 100) if len(df) > 0 else 0
                }
            },
            'duplicate_check': {
                'duplicate_dates': df['date'].duplicated().sum(),
                'unique_dates': df['date'].nunique(),
                'is_duplicate_free': df['date'].duplicated().sum() == 0
            },
            'outlier_check': {
                'gold_max_daily_change': df['gold'].pct_change().abs().max() * 100,
                'sp500_max_daily_change': df['sp500'].pct_change().abs().max() * 100,
            },
            'date_range': {
                'start_date': df['date'].min().strftime('%Y-%m-%d') if len(df) > 0 else None,
                'end_date': df['date'].max().strftime('%Y-%m-%d') if len(df) > 0 else None,
                'total_days': (df['date'].max() - df['date'].min()).days if len(df) > 0 else 0,
                'trading_days': len(df)
            }
        }
        
        return metrics
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict:
        """
        Get summary statistics for display
        
        Args:
            df: Processed DataFrame
            
        Returns:
            Dictionary of summary statistics
        """
        stats = {
            'gold': {
                'mean': df['gold'].mean(),
                'median': df['gold'].median(),
                'std': df['gold'].std(),
                'min': df['gold'].min(),
                'max': df['gold'].max(),
                'latest': df['gold'].iloc[-1] if len(df) > 0 else None,
                'change_pct': ((df['gold'].iloc[-1] - df['gold'].iloc[0]) / df['gold'].iloc[0] * 100) if len(df) > 0 else 0
            },
            'sp500': {
                'mean': df['sp500'].mean(),
                'median': df['sp500'].median(),
                'std': df['sp500'].std(),
                'min': df['sp500'].min(),
                'max': df['sp500'].max(),
                'latest': df['sp500'].iloc[-1] if len(df) > 0 else None,
                'change_pct': ((df['sp500'].iloc[-1] - df['sp500'].iloc[0]) / df['sp500'].iloc[0] * 100) if len(df) > 0 else 0
            }
        }
        
        return stats
