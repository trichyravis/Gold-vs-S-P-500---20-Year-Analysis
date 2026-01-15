"""
Configuration file for Gold & S&P 500 Analysis Streamlit App
Author: Prof. V. Ravichandran
Date: January 2026
"""

import os
from datetime import datetime, timedelta

# ==================== DATA CONFIGURATION ====================
TICKERS = {
    'gold': 'GLD',
    'sp500': 'SPY'
}

START_DATE = '2005-01-01'
# END_DATE is set to today automatically in the app

DATA_FREQUENCY = 'daily'
DATA_INTERVAL = '1d'  # For yfinance

# ==================== CACHE CONFIGURATION ====================
CACHE_ENABLED = True
CACHE_DURATION_HOURS = 24
CACHE_DIR = 'data/cache'

# ==================== FILE PATHS ====================
DATA_DIR = 'data'
CSV_FILE = os.path.join(DATA_DIR, 'gold_sp500_daily.csv')
PARQUET_FILE = os.path.join(DATA_DIR, 'gold_sp500_daily.parquet')
REPORT_FILE = os.path.join(DATA_DIR, 'data_quality_report.json')
CACHE_METADATA_FILE = os.path.join(CACHE_DIR, 'cache_metadata.json')

# ==================== STREAMLIT CONFIGURATION ====================
PAGE_TITLE = "Gold & S&P 500: 20-Year Analysis"
PAGE_ICON = "📊"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# ==================== DESIGN - COLOR SCHEME ====================
COLORS = {
    'primary_blue': '#003366',      # Dark Blue (RGB 0, 51, 102)
    'light_blue': '#ADD8E6',        # Light Blue (RGB 173, 216, 230)
    'gold': '#FFD700',              # Gold (RGB 255, 215, 0)
    'success': '#2ECC71',           # Green
    'warning': '#F39C12',           # Orange
    'error': '#E74C3C',             # Red
    'loading': '#3498DB',           # Bright Blue
    'white': '#FFFFFF',
    'light_gray': '#F5F5F5',
    'dark_gray': '#333333'
}

# ==================== DATA VALIDATION RULES ====================
VALIDATION_RULES = {
    'max_daily_change_pct': 10.0,          # Max 10% daily change
    'max_gap_business_days': 2,            # Max 2 business day gap
    'min_price': 0,                        # Prices must be positive
    'future_date_tolerance_days': 1,       # Allow 1 day in future for timezone
}

# ==================== QUALITY SCORE WEIGHTS ====================
QUALITY_SCORE_WEIGHTS = {
    'completeness': 0.40,           # 40% - Data completeness
    'duplicates': 0.20,             # 20% - No duplicates
    'outliers': 0.20,               # 20% - No outliers/anomalies
    'null_values': 0.20              # 20% - No missing values
}

# ==================== DATA QUALITY CHECKS ====================
QUALITY_CHECKS = [
    "No negative prices",
    "No future dates",
    "Reasonable daily price changes (max 10%)",
    "Complete date range (no gaps > 2 business days)",
    "Same number of records for both assets",
    "No duplicate dates",
    "Prices are numeric",
    "Date format is consistent",
    "No NULL values (or forward-filled)",
    "Data matches expected trading days"
]

# ==================== ERROR MESSAGES ====================
ERROR_MESSAGES = {
    'network_error': "❌ Network Error: Unable to fetch data from Yahoo Finance. Using cached data if available.",
    'missing_data': "⚠️ Warning: Some data is missing. Forward-filling with last known values.",
    'date_mismatch': "⚠️ Warning: Assets have different dates. Merging on common dates.",
    'corrupted_cache': "❌ Cache Error: Cached file is corrupted. Refetching from source.",
    'timeout': "⚠️ Timeout: Data fetching is taking longer than expected. Please wait...",
    'invalid_ticker': "❌ Error: Invalid ticker symbol."
}

# ==================== SUCCESS MESSAGES ====================
SUCCESS_MESSAGES = {
    'data_fetched': "✅ Data successfully fetched from Yahoo Finance!",
    'cache_used': "✅ Using cached data (last updated: {timestamp})",
    'validation_passed': "✅ All data quality checks passed!",
    'exported': "✅ Data successfully exported!"
}

# ==================== DISCLAIMER ====================
DISCLAIMER = """
⚠️ **DISCLAIMER:** This tool is for educational purposes only. It is NOT financial advice.

Always consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results. This tool does not include taxes, fees, or transaction costs. The author assumes no responsibility for investment decisions made using this tool.

**Educational Use Only** | **Not a Substitute for Professional Advice**
"""

# ==================== FOOTER CONTENT ====================
FOOTER_CONTENT = {
    'author': 'Prof. V. Ravichandran',
    'experience': '28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence',
    'platform': 'The Mountain Path - World of Finance',
    'linkedin': 'https://www.linkedin.com/in/trichyravis/',
    'github': 'https://github.com/trichyravis'
}

# ==================== PROGRESS STAGES ====================
PROGRESS_STAGES = [
    ('📥', 'Data Collection', 'Fetch and validate financial data'),
    ('📊', 'Descriptive Analysis', 'Statistical summary and visualizations'),
    ('📈', 'Comparative Analysis', 'Compare Gold vs S&P 500 performance'),
    ('🔗', 'Correlation Analysis', 'Analyze relationships and correlations'),
    ('⚡', 'Crisis Analysis', 'Performance during market downturns'),
    ('💼', 'Portfolio Impact', 'Asset allocation and diversification benefits')
]

# ==================== EXPORT FORMATS ====================
EXPORT_FORMATS = {
    'csv': {'extension': '.csv', 'mime': 'text/csv'},
    'excel': {'extension': '.xlsx', 'mime': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'},
    'parquet': {'extension': '.parquet', 'mime': 'application/octet-stream'}
}

# ==================== NUMERIC PRECISION ====================
DECIMAL_PLACES = {
    'price': 2,
    'return': 4,
    'percentage': 2,
    'correlation': 4
}
