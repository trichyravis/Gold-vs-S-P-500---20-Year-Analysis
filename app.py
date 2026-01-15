"""
Main Streamlit Application Entry Point
Gold & S&P 500: 20-Year Analysis Dashboard
Author: Prof. V. Ravichandran
"""

import streamlit as st
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Gold & S&P 500: 20-Year Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #004d80 100%);
        color: white;
        padding: 40px;
        border-radius: 10px;
        margin-bottom: 30px;
        text-align: center;
    }
    .main-header h1 {
        margin: 0;
        font-size: 48px;
        color: white;
    }
    .main-header p {
        margin: 10px 0 0 0;
        font-size: 18px;
        color: #FFD700;
    }
    .step-card {
        background: #f8f9fa;
        border-left: 4px solid #003366;
        padding: 20px;
        margin: 15px 0;
        border-radius: 5px;
    }
    .step-card h3 {
        color: #003366;
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
    <div class="main-header">
        <h1>📊 Gold & S&P 500: 20-Year Analysis</h1>
        <p>Comprehensive Financial Data Analysis Platform</p>
    </div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("## Welcome to The Mountain Path")
st.markdown("""
This comprehensive analysis platform compares **Gold (GLD)** and **S&P 500 (SPY)** performance 
over the past 20 years. Explore the data, analyze trends, and understand the relationship 
between these two important asset classes.

**Platform:** The Mountain Path - World of Finance  
**Instructor:** Prof. V. Ravichandran  
**Purpose:** Educational Analysis | Financial Research
""")

st.markdown("---")

# Navigation guide
st.markdown("## 📍 Navigation Guide")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="step-card">
    <h3>📥 Step 1: Data Collection</h3>
    <p>Fetch and validate 20 years of historical price data from Yahoo Finance</p>
    <ul>
    <li>Download GLD & SPY prices</li>
    <li>Validate data quality</li>
    <li>Export for analysis</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
    <h3>📊 Step 2: Descriptive Analysis</h3>
    <p>Analyze statistical properties and visualize trends</p>
    <ul>
    <li>Summary statistics</li>
    <li>Price charts & trends</li>
    <li>Returns distribution</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
    <h3>📈 Step 3: Comparative Analysis</h3>
    <p>Compare performance metrics between assets</p>
    <ul>
    <li>Total returns</li>
    <li>Risk metrics</li>
    <li>Drawdowns</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="step-card">
    <h3>🔗 Step 4: Correlation Analysis</h3>
    <p>Examine relationships and diversification benefits</p>
    <ul>
    <li>Correlation matrix</li>
    <li>Beta analysis</li>
    <li>Covariance</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
    <h3>⚡ Step 5: Crisis Analysis</h3>
    <p>Analyze performance during market stress periods</p>
    <ul>
    <li>Volatility analysis</li>
    <li>Drawdown periods</li>
    <li>Recovery patterns</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
    <h3>💼 Step 6: Portfolio Impact</h3>
    <p>Optimize allocation and diversification strategy</p>
    <ul>
    <li>Asset allocation</li>
    <li>Risk parity</li>
    <li>Optimization</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Getting Started
st.markdown("## 🚀 Getting Started")

st.markdown("""
### Step 1: Start with Data Collection
Click on **"📥 Data Collection"** in the sidebar to begin:

1. **Fetch Data** - Download 20 years of Gold and S&P 500 prices
2. **Validate Quality** - Automatic data quality checks (10 validations)
3. **Review Summary** - See data completeness and quality metrics
4. **Export Data** - Download as CSV, Excel, or other formats

The data is automatically cached for 24 hours to speed up subsequent loads.

### Step 2: Explore the Analysis
Once data is collected, additional analysis pages will be available:
- Descriptive statistics and charts
- Performance comparisons
- Correlation and relationship analysis
- Crisis period analysis
- Portfolio optimization

### Features
✅ **Real-time Data** - Fetches latest prices from Yahoo Finance  
✅ **Smart Caching** - 24-hour automatic refresh with manual override  
✅ **Quality Checks** - 10 automatic validation checks  
✅ **Multiple Formats** - Export as CSV, Excel, Parquet, or PDF  
✅ **Educational Focus** - Clear, documented code for learning  

### Data Source
- **Gold:** GLD (SPDR Gold Shares ETF)
- **S&P 500:** SPY (SPDR S&P 500 ETF)
- **Period:** 2005-01-01 to Today
- **Source:** Yahoo Finance (yfinance library)
""")

st.markdown("---")

# Sidebar information
st.sidebar.markdown("## About This Tool")
st.sidebar.markdown("""
**The Mountain Path - World of Finance**

An educational platform for learning financial analysis and data science.

**Instructor:** Prof. V. Ravichandran
- 28+ Years Corporate Finance & Banking Experience
- 10+ Years Academic Excellence
- Specialization: Risk Management & Financial Modeling

**Skills Covered:**
- Financial data collection & validation
- Time series analysis
- Risk metrics & performance analysis
- Portfolio optimization
- Python & Streamlit development
""")

st.sidebar.markdown("---")

st.sidebar.markdown("""
**Quick Links:**
- [LinkedIn](https://www.linkedin.com/in/trichyravis/)
- [GitHub](https://github.com/trichyravis)
- [Yahoo Finance](https://finance.yahoo.com/)
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>The Mountain Path - World of Finance</strong></p>
    <p>Educational Purpose Only | Not Financial Advice</p>
    <p>Created: January 2026</p>
</div>
""", unsafe_allow_html=True)
