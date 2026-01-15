"""
Utilities Module - Helper functions and formatting utilities
Author: Prof. V. Ravichandran
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List
import io
import json

class DataFormatter:
    """Format data for display and export"""
    
    @staticmethod
    def format_currency(value: float, decimals: int = 2) -> str:
        """Format number as currency"""
        if pd.isna(value):
            return "N/A"
        return f"${value:,.{decimals}f}"
    
    @staticmethod
    def format_percentage(value: float, decimals: int = 2) -> str:
        """Format number as percentage"""
        if pd.isna(value):
            return "N/A"
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def format_number(value: float, decimals: int = 2) -> str:
        """Format number with commas"""
        if pd.isna(value):
            return "N/A"
        return f"{value:,.{decimals}f}"
    
    @staticmethod
    def format_date(date_obj, format_str: str = '%Y-%m-%d') -> str:
        """Format date object"""
        if isinstance(date_obj, str):
            date_obj = pd.to_datetime(date_obj)
        return date_obj.strftime(format_str)
    
    @staticmethod
    def format_dataframe_display(df: pd.DataFrame, display_cols: List[str] = None, max_rows: int = None) -> pd.DataFrame:
        """
        Format DataFrame for Streamlit display
        
        Args:
            df: DataFrame to format
            display_cols: Specific columns to display
            max_rows: Maximum rows to show
            
        Returns:
            Formatted DataFrame
        """
        # Select columns if specified
        if display_cols:
            df = df[[col for col in display_cols if col in df.columns]]
        
        # Limit rows if specified
        if max_rows:
            df = df.head(max_rows)
        
        # Format numeric columns
        formatted = df.copy()
        
        for col in formatted.columns:
            if col == 'date':
                formatted[col] = formatted[col].dt.strftime('%Y-%m-%d')
            elif col in ['gold', 'sp500']:
                formatted[col] = formatted[col].apply(lambda x: DataFormatter.format_currency(x))
            elif 'return' in col.lower():
                formatted[col] = formatted[col].apply(lambda x: DataFormatter.format_percentage(x, 4))
            elif 'cumulative' in col.lower():
                formatted[col] = formatted[col].apply(lambda x: DataFormatter.format_percentage(x, 2))
        
        return formatted


class DataValidator:
    """Validation utilities"""
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """
        Validate date range
        
        Args:
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            
            if start >= end:
                return False, "Start date must be before end date"
            
            if end > datetime.now():
                return False, "End date cannot be in the future"
            
            return True, "Valid date range"
            
        except Exception as e:
            return False, f"Invalid date format: {str(e)}"
    
    @staticmethod
    def validate_ticker(ticker: str) -> Tuple[bool, str]:
        """
        Basic ticker validation
        
        Args:
            ticker: Ticker symbol
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not ticker or not isinstance(ticker, str):
            return False, "Ticker must be a non-empty string"
        
        ticker = ticker.upper().strip()
        
        if len(ticker) < 1 or len(ticker) > 5:
            return False, "Ticker must be 1-5 characters"
        
        if not ticker.isalpha():
            return False, "Ticker must contain only letters"
        
        return True, "Valid ticker"


class StatsCalculator:
    """Calculate statistics and metrics"""
    
    @staticmethod
    def calculate_returns(prices: pd.Series, return_type: str = 'simple') -> pd.Series:
        """
        Calculate returns from price series
        
        Args:
            prices: Price series
            return_type: 'simple' or 'log'
            
        Returns:
            Series of returns (as percentages)
        """
        if return_type == 'simple':
            return prices.pct_change() * 100
        elif return_type == 'log':
            return np.log(prices / prices.shift(1)) * 100
        else:
            raise ValueError("return_type must be 'simple' or 'log'")
    
    @staticmethod
    def calculate_cumulative_returns(prices: pd.Series) -> pd.Series:
        """
        Calculate cumulative returns
        
        Args:
            prices: Price series
            
        Returns:
            Series of cumulative returns (as percentages)
        """
        return ((prices / prices.iloc[0]) - 1) * 100
    
    @staticmethod
    def calculate_volatility(returns: pd.Series, periods: int = 252) -> float:
        """
        Calculate annualized volatility
        
        Args:
            returns: Series of returns (as decimals)
            periods: Trading periods per year (default 252)
            
        Returns:
            Annualized volatility (as percentage)
        """
        return returns.std() * np.sqrt(periods)
    
    @staticmethod
    def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02, periods: int = 252) -> float:
        """
        Calculate Sharpe ratio
        
        Args:
            returns: Series of returns (as decimals)
            risk_free_rate: Annual risk-free rate (default 2%)
            periods: Trading periods per year (default 252)
            
        Returns:
            Sharpe ratio
        """
        excess_return = returns.mean() - (risk_free_rate / periods)
        volatility = returns.std()
        
        if volatility == 0:
            return 0
        
        return (excess_return / volatility) * np.sqrt(periods)
    
    @staticmethod
    def calculate_max_drawdown(prices: pd.Series) -> float:
        """
        Calculate maximum drawdown
        
        Args:
            prices: Price series
            
        Returns:
            Maximum drawdown (as percentage)
        """
        cumulative = (1 + prices.pct_change()).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        
        return drawdown.min() * 100
    
    @staticmethod
    def calculate_correlation(series1: pd.Series, series2: pd.Series) -> float:
        """
        Calculate correlation between two series
        
        Args:
            series1: First price series
            series2: Second price series
            
        Returns:
            Correlation coefficient (-1 to 1)
        """
        returns1 = series1.pct_change()
        returns2 = series2.pct_change()
        
        return returns1.corr(returns2)
    
    @staticmethod
    def calculate_beta(asset_returns: pd.Series, market_returns: pd.Series) -> float:
        """
        Calculate beta (asset volatility relative to market)
        
        Args:
            asset_returns: Asset returns (as decimals)
            market_returns: Market returns (as decimals)
            
        Returns:
            Beta coefficient
        """
        covariance = asset_returns.cov(market_returns)
        market_variance = market_returns.var()
        
        if market_variance == 0:
            return 0
        
        return covariance / market_variance


class ExportHelper:
    """Help with data export operations"""
    
    @staticmethod
    def create_quality_report(validation_results: Dict, quality_metrics: Dict) -> Dict:
        """
        Create a quality report dictionary
        
        Args:
            validation_results: Results from data validation
            quality_metrics: Quality metrics calculated
            
        Returns:
            Dictionary representing the quality report
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'validation_summary': validation_results.get('summary', {}),
            'validation_details': {
                'passed': validation_results.get('passed', []),
                'failed': validation_results.get('failed', []),
                'warnings': validation_results.get('warnings', []),
            },
            'quality_metrics': quality_metrics
        }
        
        return report
    
    @staticmethod
    def dataframe_to_excel_bytes(df: pd.DataFrame, sheet_name: str = 'Data') -> bytes:
        """
        Convert DataFrame to Excel bytes
        
        Args:
            df: DataFrame to convert
            sheet_name: Excel sheet name
            
        Returns:
            Bytes of Excel file
        """
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        output.seek(0)
        return output.getvalue()
    
    @staticmethod
    def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
        """
        Convert DataFrame to CSV bytes
        
        Args:
            df: DataFrame to convert
            
        Returns:
            Bytes of CSV file
        """
        return df.to_csv(index=False).encode('utf-8')


class MetricsFormatter:
    """Format metrics for display"""
    
    @staticmethod
    def format_metric_card(label: str, value: Any, suffix: str = '', color_code: str = None) -> Dict:
        """
        Format a metric for card display
        
        Args:
            label: Metric label
            value: Metric value
            suffix: Suffix to add (e.g., '%', '$')
            color_code: Optional color code
            
        Returns:
            Dictionary with formatted metric
        """
        return {
            'label': label,
            'value': value,
            'suffix': suffix,
            'color': color_code
        }
    
    @staticmethod
    def get_quality_level(score: float) -> Tuple[str, str]:
        """
        Get quality level description and emoji
        
        Args:
            score: Quality score (0-100)
            
        Returns:
            Tuple of (level_description, emoji)
        """
        if score >= 95:
            return 'Excellent', '✅'
        elif score >= 85:
            return 'Good', '✅'
        elif score >= 70:
            return 'Fair', '⚠️'
        elif score >= 50:
            return 'Poor', '⚠️'
        else:
            return 'Critical', '❌'
    
    @staticmethod
    def get_status_indicator(condition: bool, true_text: str = 'OK', false_text: str = 'ERROR') -> str:
        """
        Get status indicator with emoji
        
        Args:
            condition: Boolean condition
            true_text: Text for true condition
            false_text: Text for false condition
            
        Returns:
            Formatted status string
        """
        emoji = '✅' if condition else '❌'
        text = true_text if condition else false_text
        return f"{emoji} {text}"
