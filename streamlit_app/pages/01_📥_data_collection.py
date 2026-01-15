
"""
Data Collection & Validation Page
Fetch and validate 20 years of Gold (GLD) vs S&P 500 (SPY) data
Author: Prof. V. Ravichandran
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.data_fetcher import DataFetcher
from src.data_processor import DataProcessor
from src.cache_manager import CacheManager
from src.utils import DataFormatter, MetricsFormatter, ExportHelper

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Data Collection & Validation",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM STYLING ====================
st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(135deg, #003366 0%, #004d80 100%);
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .header-title {
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        margin: 0;
    }
    .header-subtitle {
        color: #FFD700;
        font-size: 1.1em;
        margin: 10px 0 0 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== PAGE HEADER ====================
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📥 Data Collection & Validation</h1>
    <p class="header-subtitle">Fetch and validate 20 years of Gold (GLD) vs S&P 500 (SPY) data</p>
</div>
""", unsafe_allow_html=True)

# ==================== INITIALIZE SESSION STATE ====================
if 'data' not in st.session_state:
    st.session_state.data = None
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'validation_results' not in st.session_state:
    st.session_state.validation_results = None
if 'fetch_errors' not in st.session_state:
    st.session_state.fetch_errors = []

# ==================== FETCH CONTROLS ====================
st.markdown("### 🔧 Fetch Controls")

col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.date_input(
        "Start Date",
        value=datetime(2005, 1, 1),
        key="start_date"
    )

with col2:
    end_date = st.date_input(
        "End Date",
        value=datetime.now(),
        key="end_date"
    )

with col3:
    period_days = (end_date - start_date).days
    period_years = period_days / 365.25
    st.metric("Period", f"~{period_years:.1f} years")

# ==================== ASSETS SELECTION ====================
st.markdown("### 📊 Assets to Fetch:")

col1, col2 = st.columns(2)

with col1:
    fetch_gold = st.checkbox("Gold (GLD) - SPDR Gold Shares", value=True)

with col2:
    fetch_sp500 = st.checkbox("S&P 500 (SPY) - SPDR S&P 500 ETF", value=True)

# ==================== FETCH BUTTONS ====================
button_col1, button_col2, button_col3 = st.columns(3)

with button_col1:
    fetch_button = st.button("📥 FETCH DATA", key="fetch_btn", use_container_width=True)

with button_col2:
    refresh_button = st.button("🔄 REFRESH DATA", key="refresh_btn", use_container_width=True)

with button_col3:
    clear_button = st.button("🗑️ CLEAR CACHE", key="clear_btn", use_container_width=True)

# ==================== DATA FETCHING LOGIC ====================
if fetch_button or refresh_button:
    try:
        # Prepare tickers
        tickers = []
        if fetch_gold:
            tickers.append('GLD')
        if fetch_sp500:
            tickers.append('SPY')
        
        if not tickers:
            st.error("❌ Please select at least one asset")
        else:
            # Convert dates to strings
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            # Fetch data
            progress_placeholder = st.empty()
            with progress_placeholder.container():
                st.info(f"📥 Fetching data from Yahoo Finance...")
                
                fetcher = DataFetcher(tickers, start_date_str, end_date_str)
                raw_data, fetch_errors = fetcher.fetch_all()
                
                st.session_state.raw_data = raw_data
                st.session_state.fetch_errors = fetch_errors
            
            if raw_data is None:
                st.error(f"❌ Failed to fetch data. Errors: {fetch_errors}")
            else:
                # Process data
                st.info("📊 Processing and validating data...")
                processor = DataProcessor()
                processed_data = processor.process_data(raw_data)
                
                if processed_data is None or processed_data.empty:
                    st.error("❌ Failed to process data")
                else:
                    # Validate data
                    is_valid, validation_results, quality_score = processor.validate_data(processed_data)
                    
                    st.session_state.data = processed_data
                    st.session_state.validation_results = validation_results
                    
                    # Show success message
                    st.success(f"✅ Data fetched and validated successfully! Quality Score: {quality_score:.1f}%")
                    
                    # Rerun to show data preview
                    st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error during data fetch: {str(e)}")
        import traceback
        st.error(traceback.format_exc())

# ==================== CLEAR CACHE ====================
if clear_button:
    try:
        cache_manager = CacheManager()
        cache_manager.clear_cache()
        st.session_state.data = None
        st.session_state.raw_data = None
        st.session_state.validation_results = None
        st.session_state.fetch_errors = []
        st.success("✅ Cache cleared successfully")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error clearing cache: {str(e)}")

# ==================== DATA PREVIEW ====================
def display_data_preview(data):
    """Display preview of fetched data"""
    if data is None or data.empty:
        st.info("📥 Click 'FETCH DATA' to load data from Yahoo Finance")
        return
    
    st.markdown("### 📋 Data Preview")
    
    # Get column names safely
    all_cols = list(data.columns)
    
    # Try to find Date column (case-insensitive)
    date_col = None
    for col in all_cols:
        if col.lower() == 'date':
            date_col = col
            break
    
    # Get ticker columns (non-date columns)
    ticker_cols = [col for col in all_cols if col.lower() != 'date']
    
    # Display columns for preview
    if date_col:
        display_cols = [date_col] + ticker_cols
    else:
        display_cols = all_cols
    
    # Only use columns that exist in the data
    display_cols = [col for col in display_cols if col in data.columns]
    
    if display_cols:
        # Show latest rows
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Latest Data:**")
            latest = data[display_cols].tail(5).copy()
            st.dataframe(latest, use_container_width=True)
        
        with col2:
            st.write("**Data Statistics:**")
            stats = pd.DataFrame({
                'Metric': ['Total Rows', 'Total Columns', 'Date Range'],
                'Value': [
                    len(data),
                    len(data.columns),
                    f"{data[date_col].min() if date_col else 'N/A'} to {data[date_col].max() if date_col else 'N/A'}"
                ]
            })
            st.dataframe(stats, use_container_width=True)
        
        # Show download options
        st.markdown("### 💾 Export Data")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = DataFormatter.format_returns(data[ticker_cols].pct_change())
            csv_download = data[[date_col] + ticker_cols].copy() if date_col else data[ticker_cols].copy()
            
            st.download_button(
                label="📥 Download CSV",
                data=ExportHelper.dataframe_to_csv(csv_download),
                file_name=f"gold_sp500_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            try:
                st.download_button(
                    label="📊 Download Excel",
                    data=ExportHelper.dataframe_to_excel_bytes(data[display_cols]),
                    file_name=f"gold_sp500_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.warning(f"Excel export not available: {str(e)}")
        
        with col3:
            st.info("📌 JSON export available in advanced options")
    else:
        st.warning("⚠️ No data columns available for preview")

# ==================== VALIDATION RESULTS ====================
def display_validation_results(validation_results):
    """Display validation results"""
    if validation_results is None:
        return
    
    st.markdown("### ✅ Data Validation Results")
    
    # Show summary
    summary = validation_results.get('summary', {})
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Quality Score", f"{summary.get('quality_score', 0):.1f}%")
    
    with col2:
        st.metric("Completeness", f"{summary.get('completeness', 0):.1f}%")
    
    with col3:
        st.metric("Checks Passed", f"{summary.get('checks_passed', 0)}/{summary.get('checks_passed', 0) + summary.get('checks_failed', 0)}")
    
    # Show detailed results in expander
    with st.expander("📊 Detailed Validation Results"):
        # Passed checks
        if validation_results.get('passed'):
            st.success("✅ Passed Checks:")
            for check in validation_results['passed']:
                st.write(f"  • {check}")
        
        # Failed checks
        if validation_results.get('failed'):
            st.error("❌ Failed Checks:")
            for check in validation_results['failed']:
                st.write(f"  • {check}")
        
        # Warnings
        if validation_results.get('warnings'):
            st.warning("⚠️ Warnings:")
            for warning in validation_results['warnings']:
                st.write(f"  • {warning}")

# ==================== MAIN DISPLAY ====================
if st.session_state.data is not None:
    display_data_preview(st.session_state.data)
    display_validation_results(st.session_state.validation_results)
else:
    st.info("📥 Click 'FETCH DATA' to load data from Yahoo Finance")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence</p>
    <p>The Mountain Path - World of Finance</p>
</div>
""", unsafe_allow_html=True)
