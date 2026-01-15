
"""
Data processor module for processing financial data
Author: Prof. V. Ravichandran
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and validate financial data"""

    def __init__(self, validation_rules: Optional[Dict] = None):
        """
        Initialize DataProcessor
        
        Args:
            validation_rules: Dictionary of validation rules
        """
        self.validation_rules = validation_rules or {}

    def process_data(self, raw_data: Dict) -> pd.DataFrame:
        """
        Process raw data from Yahoo Finance
        
        Args:
            raw_data: Dictionary with ticker as key, DataFrame as value
                     Each DataFrame has DatetimeIndex and Close column
            
        Returns:
            Processed DataFrame with combined data
        """
        try:
            if not raw_data:
                return pd.DataFrame()
            
            # Start with an empty DataFrame
            processed = None
            
            # Process each ticker
            for ticker, df in raw_data.items():
                if df is None or df.empty:
                    logger.warning(f"Skipping empty data for {ticker}")
                    continue
                
                # Get the Close column
                if 'Close' in df.columns:
                    # Extract Close prices and rename to ticker
                    ticker_data = df[['Close']].copy()
                    ticker_data.columns = [ticker]
                else:
                    # If no Close column, use first column
                    ticker_data = df.iloc[:, [0]].copy()
                    ticker_data.columns = [ticker]
                
                # Join with existing data
                if processed is None:
                    processed = ticker_data
                else:
                    processed = processed.join(ticker_data, how='outer')
            
            # If no data was processed, return empty DataFrame
            if processed is None or processed.empty:
                logger.error("No valid data after processing")
                return pd.DataFrame()
            
            # Reset index to make date a column
            processed = processed.reset_index()
            processed.columns = ['Date'] + list(processed.columns[1:])
            
            # Ensure Date column is datetime
            processed['Date'] = pd.to_datetime(processed['Date'])
            
            # Forward fill any missing values
            processed = processed.fillna(method='ffill')
            
            # Drop remaining NaN rows
            processed = processed.dropna()
            
            logger.info(f"Successfully processed data: {len(processed)} rows, {processed.shape[1]} columns")
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            return pd.DataFrame()

    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, Dict, float]:
        """
        Validate processed data
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, validation_results, quality_score)
        """
        try:
            passed = []
            failed = []
            warnings = []
            
            if df.empty:
                return False, {
                    'passed': [], 
                    'failed': ['Data is empty'], 
                    'warnings': [], 
                    'summary': {'quality_score': 0, 'completeness': 0}
                }, 0.0
            
            # Check data has required columns
            required_cols = ['Date']
            for col in required_cols:
                if col in df.columns:
                    passed.append(f"Column '{col}' present")
                else:
                    failed.append(f"Column '{col}' missing")
            
            # Check for ticker data columns
            ticker_cols = [col for col in df.columns if col != 'Date']
            if len(ticker_cols) >= 2:
                passed.append(f"Both asset columns present ({', '.join(ticker_cols)})")
            else:
                failed.append(f"Missing asset data columns (found {len(ticker_cols)})")
            
            # Check data completeness
            completeness = 1 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]))
            if completeness >= 0.95:
                passed.append("Data completeness >= 95%")
            elif completeness >= 0.80:
                warnings.append(f"Data completeness is {completeness*100:.1f}% (target: 95%)")
            else:
                failed.append(f"Data completeness < 80% ({completeness*100:.1f}%)")
            
            # Check for minimum rows
            if len(df) >= 250:
                passed.append(f"Sufficient data rows ({len(df)})")
            else:
                failed.append(f"Insufficient data rows ({len(df)}, need at least 250)")
            
            # Check date range
            if 'Date' in df.columns and len(df) > 0:
                date_range_days = (df['Date'].max() - df['Date'].min()).days
                if date_range_days >= 365 * 15:  # At least 15 years
                    passed.append(f"Date range sufficient ({date_range_days} days)")
                else:
                    warnings.append(f"Date range is {date_range_days} days (target: 20 years)")
            
            # Check for duplicate dates
            if 'Date' in df.columns:
                duplicates = df['Date'].duplicated().sum()
                if duplicates == 0:
                    passed.append("No duplicate dates")
                else:
                    failed.append(f"Found {duplicates} duplicate dates")
            
            # Check for positive prices in ticker columns
            ticker_cols = [col for col in df.columns if col != 'Date']
            for col in ticker_cols:
                if col in df.columns:
                    positive_check = (df[col] > 0).all()
                    if positive_check:
                        passed.append(f"{col} prices are all positive")
                    else:
                        failed.append(f"{col} contains non-positive prices")
            
            # Calculate quality score
            total_checks = len(passed) + len(failed)
            quality_score = (len(passed) / total_checks * 100) if total_checks > 0 else 50
            
            results = {
                'passed': passed,
                'failed': failed,
                'warnings': warnings,
                'summary': {
                    'quality_score': round(quality_score, 2),
                    'completeness': round(completeness * 100, 2),
                    'total_rows': len(df),
                    'total_columns': df.shape[1],
                    'checks_passed': len(passed),
                    'checks_failed': len(failed)
                }
            }
            
            is_valid = len(failed) == 0
            return is_valid, results, quality_score
            
        except Exception as e:
            logger.error(f"Error validating data: {str(e)}")
            return False, {
                'passed': [], 
                'failed': [str(e)], 
                'warnings': [], 
                'summary': {'quality_score': 0, 'completeness': 0}
            }, 0.0

    def calculate_quality_metrics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate data quality metrics
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with quality metrics
        """
        try:
            metrics = {
                'data_completeness': {},
                'date_range': {},
                'statistics': {}
            }
            
            # Get non-Date columns (ticker columns)
            ticker_cols = [col for col in df.columns if col != 'Date']
            
            # Data completeness for each ticker
            for col in ticker_cols:
                if col in df.columns:
                    valid_rows = df[col].notna().sum()
                    metrics['data_completeness'][col] = {
                        'total_rows': len(df),
                        'valid_rows': valid_rows,
                        'completeness_pct': round((valid_rows / len(df) * 100) if len(df) > 0 else 0, 2)
                    }
            
            # Date range
            if 'Date' in df.columns and len(df) > 0:
                metrics['date_range'] = {
                    'start_date': str(df['Date'].iloc[0].date()),
                    'end_date': str(df['Date'].iloc[-1].date()),
                    'total_days': (df['Date'].iloc[-1] - df['Date'].iloc[0]).days,
                    'trading_days': len(df)
                }
            
            # Basic statistics for each ticker
            for col in ticker_cols:
                if col in df.columns:
                    metrics['statistics'][col] = {
                        'mean_price': round(df[col].mean(), 2),
                        'median_price': round(df[col].median(), 2),
                        'min_price': round(df[col].min(), 2),
                        'max_price': round(df[col].max(), 2),
                        'std_dev': round(df[col].std(), 2)
                    }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            return {
                'data_completeness': {},
                'date_range': {},
                'statistics': {}
            }
