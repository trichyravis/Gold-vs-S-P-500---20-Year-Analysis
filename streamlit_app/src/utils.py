
"""Utility functions for data formatting, metrics calculation, and exports"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List, Optional
import json
from datetime import datetime
from io import BytesIO

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False


class DataFormatter:
    """Formatting utilities for data display"""

    @staticmethod
    def format_currency(value: float, decimals: int = 2) -> str:
        """Format value as currency"""
        if pd.isna(value):
            return "N/A"
        return f"${value:,.{decimals}f}"

    @staticmethod
    def format_percentage(value: float, decimals: int = 2) -> str:
        """Format value as percentage"""
        if pd.isna(value):
            return "N/A"
        return f"{value:.{decimals}f}%"

    @staticmethod
    def format_number(value: float, decimals: int = 2) -> str:
        """Format value as number with thousand separators"""
        if pd.isna(value):
            return "N/A"
        return f"{value:,.{decimals}f}"

    @staticmethod
    def format_date(date, format_str: str = "%Y-%m-%d") -> str:
        """Format date"""
        try:
            if isinstance(date, str):
                date = pd.to_datetime(date)
            return date.strftime(format_str)
        except:
            return str(date)

    @staticmethod
    def format_returns(returns: pd.Series, decimals: int = 2) -> pd.Series:
        """Format returns series"""
        return returns.apply(lambda x: f"{x:.{decimals}f}%" if pd.notna(x) else "N/A")


class MetricsFormatter:
    """Formatting utilities for metrics display"""

    @staticmethod
    def get_quality_level(score: float) -> Tuple[str, str]:
        """Get quality level description and emoji"""
        if pd.isna(score):
            return "Unknown", "?"
        if score >= 90:
            return "Excellent", "G"
        elif score >= 75:
            return "Good", "Y"
        elif score >= 60:
            return "Fair", "O"
        else:
            return "Poor", "R"

    @staticmethod
    def format_metric(value: Any, metric_type: str = "number") -> str:
        """Format metric based on type"""
        if metric_type == "currency":
            return DataFormatter.format_currency(value)
        elif metric_type == "percentage":
            return DataFormatter.format_percentage(value)
        elif metric_type == "date":
            return DataFormatter.format_date(value)
        else:
            return DataFormatter.format_number(value)

    @staticmethod
    def calculate_volatility(returns: pd.Series) -> float:
        """Calculate volatility"""
        if returns is None or returns.empty:
            return 0.0
        return float(returns.std() * np.sqrt(252) * 100)

    @staticmethod
    def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        if returns is None or returns.empty or returns.std() == 0:
            return 0.0
        excess_returns = returns - (risk_free_rate / 252)
        return float((excess_returns.mean() / excess_returns.std()) * np.sqrt(252))

    @staticmethod
    def calculate_cumulative_return(returns: pd.Series) -> float:
        """Calculate cumulative return"""
        if returns is None or returns.empty:
            return 0.0
        return float(((1 + returns).prod() - 1) * 100)

    @staticmethod
    def calculate_max_drawdown(returns: pd.Series) -> float:
        """Calculate maximum drawdown"""
        if returns is None or returns.empty:
            return 0.0
        cum_returns = (1 + returns).cumprod()
        running_max = cum_returns.expanding().max()
        drawdown = (cum_returns - running_max) / running_max
        return float(drawdown.min() * 100)


class ExportHelper:
    """Export utilities"""

    @staticmethod
    def dataframe_to_excel_bytes(df: pd.DataFrame, sheet_name: str = "Data") -> bytes:
        """Convert DataFrame to Excel bytes"""
        if not HAS_OPENPYXL:
            raise ImportError("openpyxl required for Excel export")
        
        output = BytesIO()
        try:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            output.seek(0)
            return output.getvalue()
        except Exception as e:
            raise Exception(f"Error creating Excel: {str(e)}")

    @staticmethod
    def dataframe_to_json(df: pd.DataFrame) -> str:
        """Convert DataFrame to JSON"""
        try:
            return df.to_json(orient='records', date_format='iso')
        except Exception as e:
            raise Exception(f"Error converting to JSON: {str(e)}")

    @staticmethod
    def dataframe_to_csv(df: pd.DataFrame) -> str:
        """Convert DataFrame to CSV"""
        try:
            return df.to_csv(index=False)
        except Exception as e:
            raise Exception(f"Error converting to CSV: {str(e)}")

    @staticmethod
    def export_summary(data: Dict[str, Any], format_type: str = "json") -> str:
        """Export summary data"""
        try:
            if format_type == "json":
                return json.dumps(data, indent=2, default=str)
            else:
                return str(data)
        except Exception as e:
            raise Exception(f"Error exporting: {str(e)}")


class DataValidator:
    """Validation utilities"""

    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """Validate date range"""
        try:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            if start >= end:
                return False, "Start date must be before end date"
            return True, "Date range valid"
        except Exception as e:
            return False, f"Invalid date format: {str(e)}"

    @staticmethod
    def validate_data_completeness(df: pd.DataFrame, min_completeness: float = 0.8) -> Tuple[bool, float]:
        """Validate data completeness"""
        if df is None or df.empty:
            return False, 0.0
        
        total_values = df.shape[0] * df.shape[1]
        missing_values = df.isna().sum().sum()
        completeness = 1 - (missing_values / total_values)
        is_valid = completeness >= min_completeness
        return is_valid, completeness

    @staticmethod
    def validate_price_data(prices: pd.Series) -> Tuple[bool, str]:
        """Validate price data"""
        if prices is None or prices.empty:
            return False, "Price data is empty"
        if (prices <= 0).any():
            return False, "Price data contains non-positive values"
        if prices.isna().any():
            return False, "Price data contains NaN values"
        return True, "Price data valid"


class StatisticalHelper:
    """Statistical calculation utilities"""

    @staticmethod
    def calculate_correlation(series1: pd.Series, series2: pd.Series) -> float:
        """Calculate correlation"""
        try:
            return float(series1.corr(series2))
        except:
            return 0.0

    @staticmethod
    def calculate_beta(asset_returns: pd.Series, market_returns: pd.Series) -> float:
        """Calculate beta"""
        try:
            covariance = asset_returns.cov(market_returns)
            market_variance = market_returns.var()
            return float(covariance / market_variance) if market_variance != 0 else 0.0
        except:
            return 0.0

    @staticmethod
    def calculate_alpha(asset_return: float, risk_free_rate: float, beta: float, market_return: float) -> float:
        """Calculate alpha"""
        try:
            expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
            return float(asset_return - expected_return)
        except:
            return 0.0


class CacheHelper:
    """Cache management utilities"""

    @staticmethod
    def should_refresh_cache(last_update: datetime, max_age_hours: int = 24) -> bool:
        """Check if cache should be refreshed"""
        if last_update is None:
            return True
        age = (datetime.now() - last_update).total_seconds() / 3600
        return age > max_age_hours

    @staticmethod
    def format_cache_age(last_update: datetime) -> str:
        """Format cache age as string"""
        if last_update is None:
            return "Never"
        age = (datetime.now() - last_update).total_seconds()
        if age < 60:
            return f"{int(age)} seconds ago"
        elif age < 3600:
            return f"{int(age / 60)} minutes ago"
        elif age < 86400:
            return f"{int(age / 3600)} hours ago"
        else:
            return f"{int(age / 86400)} days ago"
