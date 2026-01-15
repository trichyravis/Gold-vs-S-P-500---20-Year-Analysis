"""
Descriptive Analysis Page
Analyze statistical properties and visualize trends
Author: Prof. V. Ravichandran
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from src.utils import DataFormatter, MetricsFormatter

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Descriptive Analysis",
    page_icon="📊",
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
    <h1 class="header-title">📊 Descriptive Analysis</h1>
    <p class="header-subtitle">Analyze statistical properties and visualize trends in Gold vs S&P 500</p>
</div>
""", unsafe_allow_html=True)

# ==================== CHECK FOR DATA ====================
if 'data' not in st.session_state or st.session_state.data is None:
    st.error("❌ No data available. Please go to 'Data Collection' step first and fetch data.")
    st.stop()

data = st.session_state.data

# Get column names
all_cols = list(data.columns)
date_col = None
for col in all_cols:
    if col.lower() == 'date':
        date_col = col
        break

ticker_cols = [col for col in all_cols if col.lower() != 'date']

if len(ticker_cols) < 2:
    st.error("❌ Need at least 2 assets (GLD and SPY). Please fetch data first.")
    st.stop()

# Get GLD and SPY columns (case-insensitive)
gld_col = None
spy_col = None

for col in ticker_cols:
    if col.upper() == 'GLD':
        gld_col = col
    elif col.upper() == 'SPY':
        spy_col = col

if gld_col is None or spy_col is None:
    st.warning(f"⚠️ Could not find GLD and SPY columns. Found: {ticker_cols}")
    gld_col = ticker_cols[0]
    spy_col = ticker_cols[1]

# ==================== SIDEBAR SETTINGS ====================
st.sidebar.markdown("### ⚙️ Analysis Settings")

statistics_type = st.sidebar.radio(
    "Select Analysis Type:",
    ["Summary Statistics", "Price Charts", "Returns Distribution", "All Analysis"]
)

# ==================== CALCULATE RETURNS ====================
data_copy = data.copy()
gld_returns = data_copy[gld_col].pct_change() * 100
spy_returns = data_copy[spy_col].pct_change() * 100

# ==================== SUMMARY STATISTICS ====================
if statistics_type in ["Summary Statistics", "All Analysis"]:
    st.markdown("### 📈 Summary Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Gold (GLD)")
        gld_stats = {
            'Mean Price': data_copy[gld_col].mean(),
            'Median Price': data_copy[gld_col].median(),
            'Std Dev': data_copy[gld_col].std(),
            'Min Price': data_copy[gld_col].min(),
            'Max Price': data_copy[gld_col].max(),
            'Current Price': data_copy[gld_col].iloc[-1],
            'Mean Return (%)': gld_returns.mean(),
            'Return Std Dev (%)': gld_returns.std(),
            'Volatility (Annual %)': MetricsFormatter.calculate_volatility(gld_returns)
        }
        
        stats_df_gld = pd.DataFrame({
            'Metric': gld_stats.keys(),
            'Value': [f"{v:.2f}" if isinstance(v, (int, float)) else str(v) for v in gld_stats.values()]
        })
        st.dataframe(stats_df_gld, use_container_width=True)
    
    with col2:
        st.markdown("#### S&P 500 (SPY)")
        spy_stats = {
            'Mean Price': data_copy[spy_col].mean(),
            'Median Price': data_copy[spy_col].median(),
            'Std Dev': data_copy[spy_col].std(),
            'Min Price': data_copy[spy_col].min(),
            'Max Price': data_copy[spy_col].max(),
            'Current Price': data_copy[spy_col].iloc[-1],
            'Mean Return (%)': spy_returns.mean(),
            'Return Std Dev (%)': spy_returns.std(),
            'Volatility (Annual %)': MetricsFormatter.calculate_volatility(spy_returns)
        }
        
        stats_df_spy = pd.DataFrame({
            'Metric': spy_stats.keys(),
            'Value': [f"{v:.2f}" if isinstance(v, (int, float)) else str(v) for v in spy_stats.values()]
        })
        st.dataframe(stats_df_spy, use_container_width=True)
    
    # Performance Metrics
    st.markdown("### 🎯 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    gld_total_return = ((data_copy[gld_col].iloc[-1] / data_copy[gld_col].iloc[0]) - 1) * 100
    spy_total_return = ((data_copy[spy_col].iloc[-1] / data_copy[spy_col].iloc[0]) - 1) * 100
    gld_sharpe = MetricsFormatter.calculate_sharpe_ratio(gld_returns)
    spy_sharpe = MetricsFormatter.calculate_sharpe_ratio(spy_returns)
    
    with col1:
        st.metric("GLD Total Return (%)", f"{gld_total_return:.2f}%")
    
    with col2:
        st.metric("SPY Total Return (%)", f"{spy_total_return:.2f}%")
    
    with col3:
        st.metric("GLD Sharpe Ratio", f"{gld_sharpe:.2f}")
    
    with col4:
        st.metric("SPY Sharpe Ratio", f"{spy_sharpe:.2f}")
    
    # Max Drawdown
    st.markdown("### 📉 Maximum Drawdown Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gld_dd = MetricsFormatter.calculate_max_drawdown(gld_returns)
        st.metric("GLD Max Drawdown (%)", f"{gld_dd:.2f}%")
    
    with col2:
        spy_dd = MetricsFormatter.calculate_max_drawdown(spy_returns)
        st.metric("SPY Max Drawdown (%)", f"{spy_dd:.2f}%")

# ==================== PRICE CHARTS ====================
if statistics_type in ["Price Charts", "All Analysis"]:
    st.markdown("### 📈 Price Trends")
    
    # Normalize prices to 100 at start
    gld_normalized = (data_copy[gld_col] / data_copy[gld_col].iloc[0]) * 100
    spy_normalized = (data_copy[spy_col] / data_copy[spy_col].iloc[0]) * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data_copy[date_col] if date_col else data_copy.index,
        y=gld_normalized,
        name='Gold (GLD)',
        line=dict(color='#FFD700', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=data_copy[date_col] if date_col else data_copy.index,
        y=spy_normalized,
        name='S&P 500 (SPY)',
        line=dict(color='#003366', width=2)
    ))
    
    fig.update_layout(
        title='Normalized Price Trends (Base = 100)',
        xaxis_title='Date',
        yaxis_title='Normalized Value',
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Actual Prices
    st.markdown("### 💰 Actual Price Charts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_gld = go.Figure()
        fig_gld.add_trace(go.Scatter(
            x=data_copy[date_col] if date_col else data_copy.index,
            y=data_copy[gld_col],
            name='GLD',
            line=dict(color='#FFD700', width=2),
            fill='tozeroy'
        ))
        fig_gld.update_layout(
            title='Gold (GLD) Price',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig_gld, use_container_width=True)
    
    with col2:
        fig_spy = go.Figure()
        fig_spy.add_trace(go.Scatter(
            x=data_copy[date_col] if date_col else data_copy.index,
            y=data_copy[spy_col],
            name='SPY',
            line=dict(color='#003366', width=2),
            fill='tozeroy'
        ))
        fig_spy.update_layout(
            title='S&P 500 (SPY) Price',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig_spy, use_container_width=True)

# ==================== RETURNS DISTRIBUTION ====================
if statistics_type in ["Returns Distribution", "All Analysis"]:
    st.markdown("### 📊 Returns Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_gld_dist = go.Figure()
        fig_gld_dist.add_trace(go.Histogram(
            x=gld_returns.dropna(),
            name='GLD Returns',
            nbinsx=50,
            marker_color='#FFD700'
        ))
        fig_gld_dist.update_layout(
            title='Gold (GLD) Daily Returns Distribution',
            xaxis_title='Daily Return (%)',
            yaxis_title='Frequency',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig_gld_dist, use_container_width=True)
    
    with col2:
        fig_spy_dist = go.Figure()
        fig_spy_dist.add_trace(go.Histogram(
            x=spy_returns.dropna(),
            name='SPY Returns',
            nbinsx=50,
            marker_color='#003366'
        ))
        fig_spy_dist.update_layout(
            title='S&P 500 (SPY) Daily Returns Distribution',
            xaxis_title='Daily Return (%)',
            yaxis_title='Frequency',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig_spy_dist, use_container_width=True)
    
    # Returns Time Series
    st.markdown("### 📈 Daily Returns Over Time")
    
    fig_returns = go.Figure()
    
    fig_returns.add_trace(go.Scatter(
        x=data_copy[date_col] if date_col else data_copy.index,
        y=gld_returns,
        name='GLD Daily Returns',
        line=dict(color='#FFD700')
    ))
    
    fig_returns.add_trace(go.Scatter(
        x=data_copy[date_col] if date_col else data_copy.index,
        y=spy_returns,
        name='SPY Daily Returns',
        line=dict(color='#003366')
    ))
    
    fig_returns.update_layout(
        title='Daily Returns Comparison',
        xaxis_title='Date',
        yaxis_title='Daily Return (%)',
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    st.plotly_chart(fig_returns, use_container_width=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence</p>
    <p>The Mountain Path - World of Finance</p>
</div>
""", unsafe_allow_html=True)
