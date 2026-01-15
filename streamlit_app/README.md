# Gold & S&P 500: 20-Year Analysis
## Comprehensive Financial Data Analysis Platform

**Platform:** The Mountain Path - World of Finance  
**Author:** Prof. V. Ravichandran  
**Framework:** Streamlit + Python  
**Purpose:** Educational Financial Analysis  
**Date:** January 2026

---

## 📋 Overview

This Streamlit application provides a comprehensive analysis platform for comparing **Gold (GLD)** and **S&P 500 (SPY)** performance over 20 years (2005-2025). 

The application is designed to:
- ✅ Fetch and validate historical financial data
- ✅ Perform quality checks and generate quality reports
- ✅ Analyze statistical properties and relationships
- ✅ Support educational learning in financial analysis
- ✅ Demonstrate best practices in data engineering and Python development

---

## 🗂️ Project Structure

```
streamlit_app/
├── app.py                              # Main Streamlit entry point
├── config.py                           # Configuration & constants
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
│
├── pages/
│   └── 01_📥_data_collection.py       # Data Collection & Validation module
│
├── src/                                # Source modules
│   ├── __init__.py
│   ├── data_fetcher.py                # Yahoo Finance data fetching
│   ├── data_processor.py              # Data validation & cleaning
│   ├── cache_manager.py               # Smart caching system
│   └── utils.py                       # Utility functions
│
├── data/                               # Data directory
│   ├── gold_sp500_daily.csv           # Raw CSV data
│   ├── gold_sp500_daily.parquet       # Optimized Parquet format
│   ├── data_quality_report.json       # Quality metrics
│   └── cache/                         # Cached data
│
└── assets/                             # Static assets
    ├── logo.png                        # Mountain Path logo
    └── styles.css                      # Custom styling
```

---

## 🚀 Quick Start

### Installation

1. **Clone or download the project**
```bash
cd streamlit_app
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📊 Features

### Step 1: Data Collection & Validation

**Location:** Pages > 📥 Data Collection

**Capabilities:**
- Fetch 20 years of historical data (2005-2025)
- Real-time progress tracking
- 10 automatic quality validation checks
- Data completeness metrics
- Multiple export formats (CSV, Excel, Parquet, PDF)
- Smart 24-hour caching with manual refresh

**Quality Checks Performed:**
1. ✅ No negative prices
2. ✅ No future dates
3. ✅ Reasonable daily price changes (max 10%)
4. ✅ Complete date range (no gaps > 2 business days)
5. ✅ Same number of records for both assets
6. ✅ No duplicate dates
7. ✅ Prices are numeric
8. ✅ Date format is consistent
9. ✅ No NULL values (or properly forward-filled)
10. ✅ Data matches expected trading days

**Quality Score:** 0-100 scale
- 95+: Excellent ✅
- 85-94: Good ✅
- 70-84: Fair ⚠️
- 50-69: Poor ⚠️
- <50: Critical ❌

### Data Sources

| Asset | Ticker | Name | Type |
|-------|--------|------|------|
| Gold | GLD | SPDR Gold Shares ETF | Commodity ETF |
| S&P 500 | SPY | SPDR S&P 500 ETF | Equity ETF |

**Data Source:** Yahoo Finance (via yfinance library)  
**Period:** 2005-01-01 to Today  
**Frequency:** Daily  
**Trading Days:** ~5,000 records

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Data Configuration
TICKERS = {
    'gold': 'GLD',
    'sp500': 'SPY'
}
START_DATE = '2005-01-01'

# Cache Configuration
CACHE_ENABLED = True
CACHE_DURATION_HOURS = 24

# Color Scheme
COLORS = {
    'primary_blue': '#003366',
    'light_blue': '#ADD8E6',
    'gold': '#FFD700',
    'success': '#2ECC71',
    'warning': '#F39C12',
    'error': '#E74C3C',
}

# Validation Rules
VALIDATION_RULES = {
    'max_daily_change_pct': 10.0,
    'max_gap_business_days': 2,
    'min_price': 0,
}
```

---

## 📁 Module Documentation

### `src/data_fetcher.py`
**Purpose:** Fetch historical data from Yahoo Finance

**Key Classes:**
- `DataFetcher(tickers, start_date, end_date)`
  - `fetch_single_ticker()` - Fetch single ticker
  - `fetch_all()` - Fetch all tickers and merge
  - `validate_dates()` - Validate date range
  - `get_basic_stats()` - Calculate basic statistics

**Example Usage:**
```python
from src.data_fetcher import DataFetcher

fetcher = DataFetcher(
    tickers={'gold': 'GLD', 'sp500': 'SPY'},
    start_date='2005-01-01',
    end_date='2025-01-15'
)

data, errors = fetcher.fetch_all()
```

### `src/data_processor.py`
**Purpose:** Validate, clean, and process financial data

**Key Classes:**
- `DataProcessor(validation_rules)`
  - `process_data()` - Main processing pipeline
  - `validate_data()` - Comprehensive validation (10 checks)
  - `calculate_quality_metrics()` - Quality metrics
  - `get_summary_stats()` - Summary statistics

**Example Usage:**
```python
from src.data_processor import DataProcessor

processor = DataProcessor(config.VALIDATION_RULES)
processed_data = processor.process_data(raw_data)
is_valid, results, quality_score = processor.validate_data(processed_data)
```

### `src/cache_manager.py`
**Purpose:** Smart data caching with auto-refresh

**Key Classes:**
- `CacheManager(cache_dir, cache_duration_hours)`
  - `save_cache()` - Save data to cache
  - `load_cache()` - Load from cache if valid
  - `is_cache_valid()` - Check cache expiration
  - `get_cache_age()` - Get age information
  - `clear_cache()` - Clear all cached data
  - `export_data()` - Export to various formats

**Example Usage:**
```python
from src.cache_manager import CacheManager

cache = CacheManager('data/cache', cache_duration_hours=24)

# Load cached data
data, is_valid, metadata = cache.load_cache()

# Save data
cache.save_cache(data, metadata={'source': 'yahoo'})

# Export
success, filepath = cache.export_data(data, format='csv')
```

### `src/utils.py`
**Purpose:** Utility functions for formatting, validation, and analysis

**Key Classes:**
- `DataFormatter` - Format data for display
  - `format_currency()` - Format as currency
  - `format_percentage()` - Format as percentage
  - `format_dataframe_display()` - Format DataFrame

- `DataValidator` - Validation utilities
  - `validate_date_range()` - Validate dates
  - `validate_ticker()` - Validate ticker symbols

- `StatsCalculator` - Statistical calculations
  - `calculate_returns()` - Simple/log returns
  - `calculate_volatility()` - Annualized volatility
  - `calculate_sharpe_ratio()` - Sharpe ratio
  - `calculate_max_drawdown()` - Maximum drawdown
  - `calculate_correlation()` - Correlation matrix

- `ExportHelper` - Export utilities
  - `create_quality_report()` - Create quality report
  - `dataframe_to_excel_bytes()` - Convert to Excel
  - `dataframe_to_csv_bytes()` - Convert to CSV

**Example Usage:**
```python
from src.utils import DataFormatter, StatsCalculator

# Format currency
price_str = DataFormatter.format_currency(2150.45)  # "$2,150.45"

# Calculate statistics
returns = StatsCalculator.calculate_returns(prices)
volatility = StatsCalculator.calculate_volatility(returns)
sharpe = StatsCalculator.calculate_sharpe_ratio(returns)
```

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] **Data Fetch**
  - [ ] Fetch completes successfully
  - [ ] Progress bar shows real-time progress
  - [ ] Correct number of records (should be ~5,000)
  - [ ] Data date range is 2005-2025

- [ ] **Data Validation**
  - [ ] 10 quality checks complete
  - [ ] Quality score displayed correctly
  - [ ] No errors in validation results
  - [ ] Metrics calculated properly

- [ ] **Caching**
  - [ ] First fetch: ~30 seconds
  - [ ] Second load: <1 second (cached)
  - [ ] Cache refresh button works
  - [ ] Manual refresh fetches new data

- [ ] **Export**
  - [ ] CSV export works
  - [ ] Excel export works (if openpyxl available)
  - [ ] Data integrity preserved
  - [ ] Correct number of rows exported

- [ ] **Display**
  - [ ] UI renders correctly
  - [ ] All sections visible
  - [ ] Tables format properly
  - [ ] Colors match Mountain Path scheme

---

## 📈 Data Quality Metrics

The application calculates:

**Completeness Metrics:**
- Total rows per asset
- Non-null counts
- Completeness percentage

**Duplicate Checks:**
- Duplicate date detection
- Unique date count
- Duplicate-free status

**Outlier Checks:**
- Maximum daily price change
- Percentage returns ranges
- Anomaly detection

**Date Range Checks:**
- Start and end dates
- Total calendar days
- Trading days count
- Gap analysis

---

## 🎨 Design System

### Color Scheme (Mountain Path)
- **Primary Blue:** #003366 (RGB 0, 51, 102)
- **Light Blue:** #ADD8E6 (RGB 173, 216, 230)
- **Gold:** #FFD700 (RGB 255, 215, 0)
- **Success:** #2ECC71 (Green)
- **Warning:** #F39C12 (Orange)
- **Error:** #E74C3C (Red)

### Typography
- Font: Streamlit default (good readability)
- Headers: Bold, Dark Blue
- Body: Regular weight

### UI Components
- Metric cards with blue/gold theme
- Progress bars with animations
- Status indicators (✅ ❌ ⚠️)
- Expandable sections for details

---

## ⚠️ Disclaimers

**Educational Purpose Only**

This tool is designed for educational purposes in learning financial analysis, data science, and Python development. It is NOT financial advice and should not be used for investment decisions.

**Not Investment Advice**
- Always consult with qualified financial advisors
- Past performance does not guarantee future results
- Does not include taxes, fees, or transaction costs
- Market conditions and data may change

**Data Accuracy**
- Data sourced from Yahoo Finance
- Subject to data errors or delays
- Historical data may be adjusted retroactively
- Always verify important data independently

---

## 🛠️ Troubleshooting

### Common Issues

**Issue:** "No module named yfinance"
```bash
pip install yfinance
```

**Issue:** "No module named openpyxl" (Excel export)
```bash
pip install openpyxl
```

**Issue:** "Network connection error"
- Check internet connection
- Yahoo Finance might be temporarily unavailable
- Try using cached data
- Wait a few minutes and retry

**Issue:** "Cache not loading"
- Delete `data/cache/` folder
- Restart the app
- Fetch data again

**Issue:** "Slow performance"
- First load will be ~30 seconds (fetching 5,000 rows)
- Subsequent loads <1 second (using cache)
- If still slow, check internet speed

---

## 📝 Future Enhancements

**Planned Features:**
- [ ] Step 2: Descriptive Analysis (Charts, statistics)
- [ ] Step 3: Comparative Analysis (Performance metrics)
- [ ] Step 4: Correlation Analysis (Relationships)
- [ ] Step 5: Crisis Analysis (Drawdowns, volatility)
- [ ] Step 6: Portfolio Optimization (Asset allocation)
- [ ] Dashboard with multi-page analysis
- [ ] Custom date range selection
- [ ] API endpoint for data access
- [ ] Automated report generation
- [ ] Machine learning predictions

---

## 📚 Learning Resources

### Python Concepts Demonstrated
- Object-oriented programming (Classes, inheritance)
- File I/O and caching mechanisms
- Error handling and logging
- Data structures (DataFrames, dictionaries)
- Type hints and documentation

### Financial Concepts Covered
- Asset pricing and data collection
- Data quality metrics
- Risk analysis metrics
- Time series analysis
- Portfolio analysis

### Libraries Used
- **Streamlit:** Web app framework
- **Pandas:** Data manipulation
- **NumPy:** Numerical computing
- **yfinance:** Financial data
- **Openpyxl:** Excel export
- **PyArrow:** Parquet format

---

## 📞 Support & Contact

**Author:** Prof. V. Ravichandran
- **Experience:** 28+ Years Corporate Finance & Banking | 10+ Years Academic Excellence
- **Specialization:** Risk Management, Financial Modeling, Data Science
- **LinkedIn:** https://www.linkedin.com/in/trichyravis/
- **GitHub:** https://github.com/trichyravis

**Platform:** The Mountain Path - World of Finance

---

## 📄 License

This project is for educational purposes. Use and modify freely for learning.

---

## 🙏 Acknowledgments

- Yahoo Finance for historical data
- Streamlit for web framework
- Pandas for data processing
- Open-source community for tools and libraries

---

**Created:** January 2026  
**Last Updated:** January 15, 2026

---

## 📖 Additional Documentation

For detailed technical specifications, see:
- `DATA_COLLECTION_DESIGN_DOCUMENT.md` - Full technical design
- `00_DESIGN_REVIEW_SUMMARY.txt` - Design overview and decisions
- `DATA_COLLECTION_APPROVAL_CHECKLIST.md` - Feature checklist

---

**The Mountain Path - World of Finance**  
*Making Complex Finance Simple*
