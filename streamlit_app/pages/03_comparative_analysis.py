"""
Comparative Analysis Page
Compare performance metrics between Gold and S&P 500
Author: Prof. V. Ravichandran
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from src.utils import MetricsFormatter

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Comparative Analysis",
    page_icon="📈",
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
    <h1 class="header-title">📈 Comparative Analysis</h1>
    <p class="header-subtitle">Compare performance metrics between Gold (GLD) vs S&P 500 (SPY)</p>
</div>
""", unsafe_allow_html=True)

# ==================== CHECK FOR DATA ====================
if 'data' not in st.session_state or st.session_state.data is None:
    st.error("❌ No data available. Please go to 'Data Collection' step first.")
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

# Get GLD and SPY columns
gld_col = None
spy_col = None

for col in ticker_cols:
    if col.upper() == 'GLD':
        gld_col = col
    elif col.upper() == 'SPY':
        spy_col = col

if gld_col is None or spy_col is None:
    gld_col = ticker_cols[0]
    spy_col = ticker_cols[1]

# ==================== CALCULATE METRICS ====================
data_copy = data.copy()
gld_returns = data_copy[gld_col].pct_change() * 100
spy_returns = data_copy[spy_col].pct_change() * 100

# Calculate all metrics
gld_total_return = ((data_copy[gld_col].iloc[-1] / data_copy[gld_col].iloc[0]) - 1) * 100
spy_total_return = ((data_copy[spy_col].iloc[-1] / data_copy[spy_col].iloc[0]) - 1) * 100

gld_volatility = MetricsFormatter.calculate_volatility(gld_returns)
spy_volatility = MetricsFormatter.calculate_volatility(spy_returns)

gld_sharpe = MetricsFormatter.calculate_sharpe_ratio(gld_returns)
spy_sharpe = MetricsFormatter.calculate_sharpe_ratio(spy_returns)

gld_dd = MetricsFormatter.calculate_max_drawdown(gld_returns)
spy_dd = MetricsFormatter.calculate_max_drawdown(spy_returns)

gld_annual_return = gld_returns.mean() * 252
spy_annual_return = spy_returns.mean() * 252

# ==================== METRICS COMPARISON TABLE ====================
st.markdown("### 📊 Performance Metrics Comparison")

comparison_data = {
    'Metric': [
        'Total Return (%)',
        'Annual Return (%)',
        'Volatility (Annual %)',
        'Sharpe Ratio',
        'Max Drawdown (%)',
        'Mean Daily Return (%)',
        'Median Daily Return (%)',
        'Std Dev Daily Return (%)',
        'Skewness',
        'Kurtosis'
    ],
    'Gold (GLD)': [
        f"{gld_total_return:.2f}",
        f"{gld_annual_return:.2f}",
        f"{gld_volatility:.2f}",
        f"{gld_sharpe:.2f}",
        f"{gld_dd:.2f}",
        f"{gld_returns.mean():.4f}",
        f"{gld_returns.median():.4f}",
        f"{gld_returns.std():.4f}",
        f"{gld_returns.skew():.4f}",
        f"{gld_returns.kurtosis():.4f}"
    ],
    'S&P 500 (SPY)': [
        f"{spy_total_return:.2f}",
        f"{spy_annual_return:.2f}",
        f"{spy_volatility:.2f}",
        f"{spy_sharpe:.2f}",
        f"{spy_dd:.2f}",
        f"{spy_returns.mean():.4f}",
        f"{spy_returns.median():.4f}",
        f"{spy_returns.std():.4f}",
        f"{spy_returns.skew():.4f}",
        f"{spy_returns.kurtosis():.4f}"
    ]
}

comparison_df = pd.DataFrame(comparison_data)
st.dataframe(comparison_df, use_container_width=True)

# ==================== METRICS COMPARISON CHARTS ====================
st.markdown("### 📈 Visual Comparison")

col1, col2 = st.columns(2)

with col1:
    # Total Return Comparison
    fig_returns = go.Figure(data=[
        go.Bar(name='Gold (GLD)', x=['Gold'], y=[gld_total_return], marker_color='#FFD700'),
        go.Bar(name='S&P 500 (SPY)', x=['S&P 500'], y=[spy_total_return], marker_color='#003366')
    ])
    fig_returns.update_layout(
        title='Total Return Comparison',
        yaxis_title='Return (%)',
        template='plotly_white',
        barmode='group',
        height=400
    )
    st.plotly_chart(fig_returns, use_container_width=True)

with col2:
    # Volatility vs Return
    fig_risk_return = go.Figure()
    fig_risk_return.add_trace(go.Scatter(
        x=[gld_volatility],
        y=[gld_total_return],
        mode='markers+text',
        name='Gold (GLD)',
        marker=dict(size=15, color='#FFD700'),
        text=['GLD'],
        textposition='top center'
    ))
    fig_risk_return.add_trace(go.Scatter(
        x=[spy_volatility],
        y=[spy_total_return],
        mode='markers+text',
        name='S&P 500 (SPY)',
        marker=dict(size=15, color='#003366'),
        text=['SPY'],
        textposition='top center'
    ))
    fig_risk_return.update_layout(
        title='Risk vs Return',
        xaxis_title='Volatility (Annual %)',
        yaxis_title='Total Return (%)',
        template='plotly_white',
        height=400
    )
    st.plotly_chart(fig_risk_return, use_container_width=True)

# ==================== ROLLING METRICS COMPARISON ====================
st.markdown("### 📊 Rolling Metrics Comparison (252-day window)")

col1, col2 = st.columns(2)

with col1:
    # Rolling Volatility
    gld_rolling_vol = gld_returns.rolling(window=252).std() * np.sqrt(252) * 100
    spy_rolling_vol = spy_returns.rolling(window=252).std() * np.sqrt(252) * 100
    
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(
        x=data_copy[date_col] if date_col else data_copy.index,
        y=gld_rolling_vol,
        name='Gold (GLD)',
        line=dict(color='#FFD700')
    ))
    fig_vol.add_trace(go.Scatter(
        x=data_copy[date_col] if date_col else data_copy.index,
        y=spy_rolling_vol,
        name='S&P 500 (SPY)',
        line=dict(color='#003366')
    ))
    fig_vol.update_layout(
        title='Rolling Annual Volatility',
        xaxis_title='Date',
        yaxis_title='Volatility (%)',
        template='plotly_white',
        height=400
    )
    st.plotly_chart(fig_vol, use_container_width=True)

with col2:
    # Rolling Sharpe Ratio
    gld_rolling_sharpe = (gld_returns.rolling(window=252).mean() / gld_returns.rolling(window=252).std()) * np.sqrt(252)
    spy_rolling_sharpe = (spy_returns.rolling(window=252).mean() / spy_returns.rolling(window=252).std()) * np.sqrt(252)
    
    fig_sharpe = go.Figure()
    fig_sharpe.add_trace(go.Scatter(
        x=data_copy[date_col] if date_col else data_copy.index,
        y=gld_rolling_sharpe,
        name='Gold (GLD)',
        line=dict(color='#FFD700')
    ))
    fig_sharpe.add_trace(go.Scatter(
        x=data_copy[date_col] if date_col else data_copy.index,
        y=spy_rolling_sharpe,
        name='S&P 500 (SPY)',
        line=dict(color='#003366')
    ))
    fig_sharpe.update_layout(
        title='Rolling Sharpe Ratio (252-day)',
        xaxis_title='Date',
        yaxis_title='Sharpe Ratio',
        template='plotly_white',
        height=400
    )
    st.plotly_chart(fig_sharpe, use_container_width=True)

# ==================== CUMULATIVE RETURNS ====================
st.markdown("### 💰 Cumulative Returns Comparison")

gld_cumulative = (1 + gld_returns / 100).cumprod() * 100 - 100
spy_cumulative = (1 + spy_returns / 100).cumprod() * 100 - 100

fig_cumulative = go.Figure()
fig_cumulative.add_trace(go.Scatter(
    x=data_copy[date_col] if date_col else data_copy.index,
    y=gld_cumulative,
    name='Gold (GLD)',
    line=dict(color='#FFD700', width=2),
    fill='tozeroy'
))
fig_cumulative.add_trace(go.Scatter(
    x=data_copy[date_col] if date_col else data_copy.index,
    y=spy_cumulative,
    name='S&P 500 (SPY)',
    line=dict(color='#003366', width=2),
    fill='tozeroy'
))
fig_cumulative.update_layout(
    title='Cumulative Returns Over Time',
    xaxis_title='Date',
    yaxis_title='Cumulative Return (%)',
    hovermode='x unified',
    template='plotly_white',
    height=500
)
st.plotly_chart(fig_cumulative, use_container_width=True)

# ==================== SUMMARY INSIGHTS ====================
st.markdown("### 🎯 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    better_return = "GLD" if gld_total_return > spy_total_return else "SPY"
    st.metric("Better Return", better_return, f"{max(gld_total_return, spy_total_return):.2f}%")

with col2:
    lower_volatility = "GLD" if gld_volatility < spy_volatility else "SPY"
    st.metric("Lower Risk", lower_volatility, f"{min(gld_volatility, spy_volatility):.2f}%")

with col3:
    higher_sharpe = "GLD" if gld_sharpe > spy_sharpe else "SPY"
    st.metric("Better Risk-Adjusted", higher_sharpe, f"{max(gld_sharpe, spy_sharpe):.2f}")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence</p>
    <p>The Mountain Path - World of Finance</p>
</div>
""", unsafe_allow_html=True)
