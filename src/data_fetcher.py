
"""
Data Collection & Validation Page
Streamlit app for fetching and validating Gold vs S&P 500 data
Author: Prof. V. Ravichandran
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# ==================== IMPORT CONFIGURATION ====================
# Get absolute paths to required directories
current_file = os.path.abspath(__file__)  # /mount/src/.../streamlit_app/pages/01_📥_data_collection.py
current_dir = os.path.dirname(current_file)  # /mount/src/.../streamlit_app/pages/
parent_dir = os.path.dirname(current_dir)  # /mount/src/.../streamlit_app/
root_dir = os.path.dirname(parent_dir)  # /mount/src/.../

# Ensure parent_dir (streamlit_app/) is in path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing config from streamlit_app level
    import importlib.util
    config_path = os.path.join(parent_dir, 'config.py')
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    
    # Import src modules
    src_path = os.path.join(parent_dir, 'src')
    sys.path.insert(0, src_path)
    
    from data_fetcher import DataFetcher
    from data_processor import DataProcessor
    from cache_manager import CacheManager
    from utils import DataFormatter, MetricsFormatter, ExportHelper
    
except Exception as e:
    st.error(f"❌ Error importing modules: {str(e)}")
    st.stop()

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state=config.INITIAL_SIDEBAR_STATE
)

# ==================== CUSTOM STYLING ====================
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #003366 0%, #004d80 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 12px;
        opacity: 0.8;
        font-weight: bold;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        margin-top: 5px;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 15px;
        border-radius: 5px;
        color: #155724;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeeba;
        padding: 15px;
        border-radius: 5px;
        color: #856404;
    }
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 15px;
        border-radius: 5px;
        color: #721c24;
    }
    .header-main {
        color: #003366;
        border-bottom: 3px solid #FFD700;
        padding-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== INITIALIZE SESSION STATE ====================
if 'data' not in st.session_state:
    st.session_state.data = None
if 'validation_results' not in st.session_state:
    st.session_state.validation_results = None
if 'quality_metrics' not in st.session_state:
    st.session_state.quality_metrics = None
if 'fetch_timestamp' not in st.session_state:
    st.session_state.fetch_timestamp = None
if 'fetch_status' not in st.session_state:
    st.session_state.fetch_status = None

# ==================== HELPER FUNCTIONS ====================

@st.cache_resource
def get_cache_manager():
    """Get cache manager instance"""
    return CacheManager(config.CACHE_DIR, config.CACHE_DURATION_HOURS)

@st.cache_resource
def get_data_processor():
    """Get data processor instance"""
    return DataProcessor(config.VALIDATION_RULES)

def fetch_and_process_data(use_cache=True):
    """Fetch data from Yahoo Finance and process it"""
    cache_manager = get_cache_manager()
    processor = get_data_processor()
    
    # Try to load from cache first
    if use_cache:
        cached_data, is_valid, cache_info = cache_manager.load_cache()
        if is_valid and cached_data is not None:
            st.session_state.fetch_status = 'cache'
            st.session_state.fetch_timestamp = cache_info.get('cached_at', 'Unknown')
            st.session_state.data = cached_data
            return cached_data, cache_info
    
    # Fetch fresh data
    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    
    try:
        # Fetch data
        status_placeholder.info("📥 Fetching data from Yahoo Finance...")
        progress_bar.progress(30)
        
        fetcher = DataFetcher(
            tickers=config.TICKERS,
            start_date=config.START_DATE,
            end_date=None
        )
        
        raw_data, errors = fetcher.fetch_all()
        
        if raw_data is None:
            st.error("❌ Failed to fetch data from Yahoo Finance")
            return None, None
        
        progress_bar.progress(60)
        status_placeholder.info("📊 Processing and validating data...")
        
        # Process data
        processed_data = processor.process_data(raw_data)
        
        # Validate data
        is_valid, validation_results, quality_score = processor.validate_data(processed_data)
        quality_metrics = processor.calculate_quality_metrics(processed_data)
        
        st.session_state.validation_results = validation_results
        st.session_state.quality_metrics = quality_metrics
        
        progress_bar.progress(85)
        
        # Save to cache
        cache_manager.save_cache(processed_data, {'quality_score': quality_score})
        
        progress_bar.progress(100)
        status_placeholder.success("✅ Data fetched, processed, and cached successfully!")
        
        st.session_state.fetch_status = 'fresh'
        st.session_state.fetch_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.data = processed_data
        
        return processed_data, {
            'rows': len(processed_data),
            'quality_score': quality_score,
            'validation': validation_results
        }
        
    except Exception as e:
        st.error(f"❌ Error during data fetch: {str(e)}")
        return None, None

def display_header():
    """Display page header"""
    st.markdown("""
        <div style='background: linear-gradient(135deg, #003366 0%, #004d80 100%); padding: 30px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: white; margin: 0; display: flex; align-items: center;'>
                <span style='font-size: 40px; margin-right: 15px;'>📥</span>
                Data Collection & Validation
            </h1>
            <p style='color: #FFD700; margin: 10px 0 0 0; font-size: 16px;'>
                Fetch and validate 20 years of Gold (GLD) vs S&P 500 (SPY) data
            </p>
        </div>
    """, unsafe_allow_html=True)

def display_controls():
    """Display fetch controls section"""
    st.markdown("### 🔧 Fetch Controls")
    
    col1, col2, col3 = st.columns([2, 2, 1.5])
    
    with col1:
        st.date_input(
            "Start Date",
            value=pd.to_datetime(config.START_DATE),
            disabled=True,
            help="Fixed at 2005-01-01 for consistent analysis"
        )
    
    with col2:
        st.date_input(
            "End Date",
            value=datetime.today(),
            disabled=True,
            help="Updates automatically to today"
        )
    
    with col3:
        st.info(f"📊 Period: ~20 years")
    
    # Assets selection
    st.markdown("**Assets to Fetch:**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Gold (GLD) - SPDR Gold Shares", value=True, disabled=True)
    
    with col2:
        st.checkbox("S&P 500 (SPY) - SPDR S&P 500", value=True, disabled=True)
    
    # Fetch buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fetch_button = st.button("🔄 FETCH DATA", use_container_width=True, type="primary")
    
    with col2:
        refresh_button = st.button("♻️ REFRESH DATA", use_container_width=True)
    
    with col3:
        clear_button = st.button("🗑️ CLEAR CACHE", use_container_width=True)
    
    return fetch_button, refresh_button, clear_button

def display_progress_section(data):
    """Display fetch progress and status section"""
    if data is None:
        return
    
    st.markdown("### ⏳ Fetch Progress & Status")
    
    # Status information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_type = st.session_state.get('fetch_status', 'unknown')
        if status_type == 'cache':
            st.info("📦 Using cached data")
        else:
            st.success("✅ Fresh data fetched")
    
    with col2:
        timestamp = st.session_state.get('fetch_timestamp', 'Unknown')
        st.info(f"⏱️ {timestamp}")
    
    with col3:
        st.info(f"📊 {len(data)} records")
    
    # Cache information
    cache_manager = get_cache_manager()
    cache_info = cache_manager.get_cache_info()
    
    if cache_info.get('exists'):
        age_info = cache_info.get('age_info', {})
        if age_info:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Cache Status", "✅ Active", f"{age_info.get('age_hours', 0)}h old")
            with col2:
                st.metric("Expires in", f"{age_info.get('time_remaining_hours', 0)}h", "24h cycle")

def display_quality_dashboard(validation_results, quality_metrics):
    """Display data quality dashboard"""
    if validation_results is None or quality_metrics is None:
        return
    
    st.markdown("### 📊 Data Quality Summary Dashboard")
    
    # Quality score
    quality_score = validation_results.get('summary', {}).get('quality_score', 0)
    level_desc, emoji = MetricsFormatter.get_quality_level(quality_score)
    
    # Metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gold_metrics = quality_metrics.get('data_completeness', {}).get('gold', {})
        st.metric(
            "Gold (GLD)",
            f"{gold_metrics.get('total_rows', 0):,} rows",
            f"{gold_metrics.get('completeness_pct', 0):.1f}% complete"
        )
    
    with col2:
        sp500_metrics = quality_metrics.get('data_completeness', {}).get('sp500', {})
        st.metric(
            "S&P 500 (SPY)",
            f"{sp500_metrics.get('total_rows', 0):,} rows",
            f"{sp500_metrics.get('completeness_pct', 0):.1f}% complete"
        )
    
    with col3:
        date_range = quality_metrics.get('date_range', {})
        st.metric(
            "Period",
            f"{date_range.get('total_days', 0):,} days",
            f"{date_range.get('start_date')} to {date_range.get('end_date')}"
        )
    
    with col4:
        st.metric(
            "Quality Score",
            f"{quality_score:.0f}/100",
            f"{emoji} {level_desc}"
        )
    
    # Validation checks
    st.markdown("**Data Quality Checks:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("✅ **Passed Checks:**")
        for check in validation_results.get('passed', []):
            st.write(f"  ✅ {check}")
    
    with col2:
        failed = validation_results.get('failed', [])
        warnings = validation_results.get('warnings', [])
        
        if failed:
            st.markdown("❌ **Failed Checks:**")
            for check in failed:
                st.write(f"  ❌ {check}")
        
        if warnings:
            st.markdown("⚠️ **Warnings:**")
            for check in warnings:
                st.write(f"  ⚠️ {check}")

def display_data_preview(data):
    """Display data preview section"""
    if data is None or len(data) == 0:
        return
    
    st.markdown("### 📊 Data Preview")
    
    # Prepare display data
    display_cols = ['date', 'gold', 'sp500', 'gold_return', 'sp500_return']
    
    col1, col2 = st.tabs(["Latest Data (Top 5)", "Oldest Data (Bottom 5)"])
    
    with col1:
        latest = data[display_cols].tail(5).copy()
        latest['date'] = latest['date'].dt.strftime('%Y-%m-%d')
        latest.columns = ['Date', 'Gold ($)', 'S&P 500 ($)', 'Gold Return (%)', 'SP500 Return (%)']
        st.dataframe(latest.iloc[::-1], use_container_width=True, hide_index=True)
    
    with col2:
        oldest = data[display_cols].head(5).copy()
        oldest['date'] = oldest['date'].dt.strftime('%Y-%m-%d')
        oldest.columns = ['Date', 'Gold ($)', 'S&P 500 ($)', 'Gold Return (%)', 'SP500 Return (%)']
        st.dataframe(oldest, use_container_width=True, hide_index=True)
    
    # Show all rows button
    if st.checkbox("Show all rows"):
        st.dataframe(data[display_cols], use_container_width=True)

def display_export_section(data):
    """Display export options"""
    if data is None:
        return
    
    st.markdown("### 💾 Export & Download Options")
    
    col1, col2, col3 = st.columns(3)
    
    # CSV Export
    with col1:
        csv_data = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name=f"gold_sp500_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Excel Export
    with col2:
        try:
            excel_data = ExportHelper.dataframe_to_excel_bytes(data, 'Gold vs S&P 500')
            st.download_button(
                label="📥 Download as Excel",
                data=excel_data,
                file_name=f"gold_sp500_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"Excel export not available: {str(e)}")
    
    # Copy to clipboard
    with col3:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.write("Data format (first 5 rows):")
            st.code(data.head().to_csv(index=False))

def display_advanced_options():
    """Display advanced options section"""
    st.markdown("### ⚙️ Advanced Options")
    
    with st.expander("Cache Settings", expanded=False):
        cache_manager = get_cache_manager()
        cache_info = cache_manager.get_cache_info()
        
        if cache_info.get('exists'):
            st.info(f"✅ Cache exists with {cache_info.get('rows', 0):,} rows")
            age_info = cache_info.get('age_info', {})
            if age_info:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Cached at:** {age_info.get('cached_at', 'Unknown')}")
                with col2:
                    st.write(f"**Expires at:** {age_info.get('expires_at', 'Unknown')}")
        else:
            st.info("ℹ️ No cache available")
    
    with st.expander("Data Processing Options", expanded=False):
        st.checkbox("Handle missing values: Forward Fill", value=True, disabled=True)
        st.checkbox("Remove outliers", value=False, disabled=True)
        st.checkbox("Adjust for splits/dividends", value=True, disabled=True, help="Already handled by Yahoo Finance")
    
    with st.expander("Validation Rules", expanded=False):
        rules = config.VALIDATION_RULES
        for rule, value in rules.items():
            st.write(f"• **{rule}:** {value}")

def display_next_steps(data):
    """Display next steps and progress"""
    if data is None:
        return
    
    st.markdown("### 📈 Next Steps")
    
    # Progress indicator
    st.markdown("**Progress:**")
    
    progress_data = config.PROGRESS_STAGES
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    cols = [col1, col2, col3, col4, col5, col6]
    
    for idx, (emoji, title, desc) in enumerate(progress_data):
        with cols[idx]:
            if idx == 0:  # Current step
                st.markdown(f"<div style='text-align: center;'><h3>{emoji} ✅</h3><small>{title}</small></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: center; opacity: 0.6;'><h3>{emoji}</h3><small>{title}</small></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➡️ GO TO DESCRIPTIVE ANALYSIS", use_container_width=True):
            st.info("This page will be available in Step 2")
    
    with col2:
        if st.button("📊 SAVE PROGRESS", use_container_width=True):
            st.success("Progress saved to cache")
    
    with col3:
        if st.button("🔄 RE-FETCH DATA", use_container_width=True):
            st.session_state.data = None
            st.rerun()

def display_footer():
    """Display footer with disclaimers and credits"""
    st.markdown("---")
    
    st.markdown("### ⚠️ Disclaimer")
    st.info(config.DISCLAIMER)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**{config.FOOTER_CONTENT['author']}**")
        st.markdown(f"*{config.FOOTER_CONTENT['experience']}*")
    
    with col2:
        st.markdown(f"**{config.FOOTER_CONTENT['platform']}**")
        st.markdown(f"[🔗 LinkedIn]({config.FOOTER_CONTENT['linkedin']})")
    
    with col3:
        st.markdown("**Data Source**")
        st.markdown("[📊 Yahoo Finance](https://finance.yahoo.com/)")

# ==================== MAIN APP ====================

def main():
    """Main application"""
    
    # Display header
    display_header()
    
    # Display controls
    fetch_button, refresh_button, clear_button = display_controls()
    
    # Handle button clicks
    if fetch_button:
        with st.spinner("Fetching data..."):
            data, result = fetch_and_process_data(use_cache=True)
    
    if refresh_button:
        st.session_state.data = None
        with st.spinner("Refreshing data..."):
            data, result = fetch_and_process_data(use_cache=False)
            st.rerun()
    
    if clear_button:
        cache_manager = get_cache_manager()
        if cache_manager.clear_cache():
            st.success("✅ Cache cleared successfully")
            st.session_state.data = None
            st.rerun()
    
    # Load cached data by default
    if st.session_state.data is None:
        with st.spinner("Loading data..."):
            cache_manager = get_cache_manager()
            cached_data, is_valid, cache_info = cache_manager.load_cache()
            
            if is_valid and cached_data is not None:
                st.session_state.data = cached_data
                st.session_state.fetch_status = 'cache'
                st.session_state.fetch_timestamp = cache_info.get('cached_at', 'Unknown')
    
    # Display sections if data available
    if st.session_state.data is not None:
        st.success(f"✅ Data loaded ({len(st.session_state.data):,} records)")
        
        display_progress_section(st.session_state.data)
        display_quality_dashboard(st.session_state.validation_results, st.session_state.quality_metrics)
        display_data_preview(st.session_state.data)
        display_export_section(st.session_state.data)
        display_advanced_options()
        display_next_steps(st.session_state.data)
    else:
        st.info("📥 Click 'FETCH DATA' to load data from Yahoo Finance")
    
    # Display footer
    display_footer()

if __name__ == "__main__":
    main()
