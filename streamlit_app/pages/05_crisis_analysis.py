"""
Crisis Analysis Page
Analyze performance during market stress periods
Author: Prof. V. Ravichandran
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Crisis Analysis",
    page_icon="⚡",
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
    <h1 class="header-title">⚡ Crisis Analysis</h1>
    <p class="header-subtitle">Performance during market stress periods and recovery patterns</p>
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

# ==================== CALCULATE STRESS PERIODS ====================
data_copy = data.copy()
gld_returns = data_copy[gld_col].pct_change() * 100
spy_returns = data_copy[spy_col].pct_change() * 100

# Define stress periods (bottom 10% volatility days for SPY)
spy_volatility = spy_returns.rolling(window=20).std()
stress_threshold = spy_volatility.quantile(0.9)
stress_periods = spy_volatility > stress_threshold

st.markdown("### 📊 Market Stress Identification")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Stress Days", stress_periods.sum())

with col2:
    stress_pct = (stress_periods.sum() / len(stress_periods)) * 100
    st.metric("Stress Period %", f"{stress_pct:.2f}%")

with col3:
    st.metric("Volatility Threshold", f"{stress_threshold:.2f}%")

# ==================== CRISIS VS NORMAL PERFORMANCE ====================
st.markdown("### 📈 Performance in Crisis vs Normal Periods")

crisis_gld_returns = gld_returns[stress_periods].dropna()
crisis_spy_returns = spy_returns[stress_periods].dropna()
normal_gld_returns = gld_returns[~stress_periods].dropna()
normal_spy_returns = spy_returns[~stress_periods].dropna()

crisis_comparison = {
    'Metric': [
        'Mean Daily Return (%)',
        'Median Daily Return (%)',
        'Volatility (Daily %)',
        'Min Daily Return (%)',
        'Max Daily Return (%)',
        'Downside Days (%)'
    ],
    'GLD (Crisis)': [
        f"{crisis_gld_returns.mean():.4f}",
        f"{crisis_gld_returns.median():.4f}",
        f"{crisis_gld_returns.std():.4f}",
        f"{crisis_gld_returns.min():.4f}",
        f"{crisis_gld_returns.max():.4f}",
        f"{(crisis_gld_returns < 0).sum() / len(crisis_gld_returns) * 100:.2f}"
    ],
    'GLD (Normal)': [
        f"{normal_gld_returns.mean():.4f}",
        f"{normal_gld_returns.median():.4f}",
        f"{normal_gld_returns.std():.4f}",
        f"{normal_gld_returns.min():.4f}",
        f"{normal_gld_returns.max():.4f}",
        f"{(normal_gld_returns < 0).sum() / len(normal_gld_returns) * 100:.2f}"
    ],
    'SPY (Crisis)': [
        f"{crisis_spy_returns.mean():.4f}",
        f"{crisis_spy_returns.median():.4f}",
        f"{crisis_spy_returns.std():.4f}",
        f"{crisis_spy_returns.min():.4f}",
        f"{crisis_spy_returns.max():.4f}",
        f"{(crisis_spy_returns < 0).sum() / len(crisis_spy_returns) * 100:.2f}"
    ],
    'SPY (Normal)': [
        f"{normal_spy_returns.mean():.4f}",
        f"{normal_spy_returns.median():.4f}",
        f"{normal_spy_returns.std():.4f}",
        f"{normal_spy_returns.min():.4f}",
        f"{normal_spy_returns.max():.4f}",
        f"{(normal_spy_returns < 0).sum() / len(normal_spy_returns) * 100:.2f}"
    ]
}

crisis_df = pd.DataFrame(crisis_comparison)
st.dataframe(crisis_df, use_container_width=True)

# ==================== VOLATILITY DURING CRISES ====================
st.markdown("### 📊 Volatility Analysis")

col1, col2 = st.columns(2)

with col1:
    gld_crisis_vol = crisis_gld_returns.std()
    gld_normal_vol = normal_gld_returns.std()
    
    fig_gld_vol = go.Figure(data=[
        go.Bar(name='Crisis', x=['Gold (GLD)'], y=[gld_crisis_vol], marker_color='#FF6B6B'),
        go.Bar(name='Normal', x=['Gold (GLD)'], y=[gld_normal_vol], marker_color='#FFD700')
    ])
    fig_gld_vol.update_layout(
        title='Gold Volatility: Crisis vs Normal',
        yaxis_title='Daily Volatility (%)',
        barmode='group',
        template='plotly_white',
        height=400
    )
    st.plotly_chart(fig_gld_vol, use_container_width=True)

with col2:
    spy_crisis_vol = crisis_spy_returns.std()
    spy_normal_vol = normal_spy_returns.std()
    
    fig_spy_vol = go.Figure(data=[
        go.Bar(name='Crisis', x=['S&P 500 (SPY)'], y=[spy_crisis_vol], marker_color='#FF6B6B'),
        go.Bar(name='Normal', x=['S&P 500 (SPY)'], y=[spy_normal_vol], marker_color='#003366')
    ])
    fig_spy_vol.update_layout(
        title='S&P 500 Volatility: Crisis vs Normal',
        yaxis_title='Daily Volatility (%)',
        barmode='group',
        template='plotly_white',
        height=400
    )
    st.plotly_chart(fig_spy_vol, use_container_width=True)

# ==================== DRAWDOWN ANALYSIS ====================
st.markdown("### 📉 Drawdown Analysis")

def calculate_drawdown(returns):
    cumulative = (1 + returns / 100).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max * 100
    return drawdown

gld_dd = calculate_drawdown(gld_returns)
spy_dd = calculate_drawdown(spy_returns)

fig_dd = go.Figure()

fig_dd.add_trace(go.Scatter(
    x=data_copy[date_col] if date_col else data_copy.index,
    y=gld_dd,
    name='Gold (GLD)',
    line=dict(color='#FFD700'),
    fill='tozeroy'
))

fig_dd.add_trace(go.Scatter(
    x=data_copy[date_col] if date_col else data_copy.index,
    y=spy_dd,
    name='S&P 500 (SPY)',
    line=dict(color='#003366'),
    fill='tozeroy'
))

fig_dd.update_layout(
    title='Drawdown Analysis Over Time',
    xaxis_title='Date',
    yaxis_title='Drawdown (%)',
    hovermode='x unified',
    template='plotly_white',
    height=500
)
st.plotly_chart(fig_dd, use_container_width=True)

# ==================== RECOVERY TIME ====================
st.markdown("### 🔄 Recovery Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Gold (GLD)")
    gld_max_dd = gld_dd.min()
    gld_max_dd_idx = gld_dd.idxmin()
    st.metric("Max Drawdown", f"{gld_max_dd:.2f}%")
    st.caption(f"Date: {gld_max_dd_idx}")

with col2:
    st.markdown("#### S&P 500 (SPY)")
    spy_max_dd = spy_dd.min()
    spy_max_dd_idx = spy_dd.idxmin()
    st.metric("Max Drawdown", f"{spy_max_dd:.2f}%")
    st.caption(f"Date: {spy_max_dd_idx}")

# ==================== CRISIS PERIODS HEATMAP ====================
st.markdown("### 🔥 Market Stress Heatmap")

# Create rolling correlation during stress
rolling_20d = gld_returns.rolling(window=20).corr(spy_returns)

fig_stress = go.Figure()

fig_stress.add_trace(go.Scatter(
    x=data_copy[date_col] if date_col else data_copy.index,
    y=rolling_20d,
    fill='tozeroy',
    name='20-day Rolling Correlation',
    line=dict(color='#003366')
))

# Highlight stress periods
for idx, is_stress in enumerate(stress_periods):
    if is_stress and (idx == 0 or not stress_periods.iloc[idx-1]):
        fig_stress.add_vrect(
            x0=data_copy[date_col].iloc[idx] if date_col else idx,
            x1=data_copy[date_col].iloc[min(idx+20, len(data_copy)-1)] if date_col else idx+20,
            fillcolor="red", opacity=0.1, layer="below"
        )

fig_stress.update_layout(
    title='Market Stress Periods (Red Background)',
    xaxis_title='Date',
    yaxis_title='Rolling 20-day Correlation',
    template='plotly_white',
    height=400
)
st.plotly_chart(fig_stress, use_container_width=True)

# ==================== INSIGHTS ====================
st.markdown("### 🎯 Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### During Crisis Periods:")
    st.write(f"""
    - **Gold Mean Return:** {crisis_gld_returns.mean():.4f}%
    - **S&P 500 Mean Return:** {crisis_spy_returns.mean():.4f}%
    - **Gold Volatility:** {crisis_gld_returns.std():.4f}%
    - **S&P 500 Volatility:** {crisis_spy_returns.std():.4f}%
    """)

with col2:
    st.markdown("#### During Normal Periods:")
    st.write(f"""
    - **Gold Mean Return:** {normal_gld_returns.mean():.4f}%
    - **S&P 500 Mean Return:** {normal_spy_returns.mean():.4f}%
    - **Gold Volatility:** {normal_gld_returns.std():.4f}%
    - **S&P 500 Volatility:** {normal_spy_returns.std():.4f}%
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence</p>
    <p>The Mountain Path - World of Finance</p>
</div>
""", unsafe_allow_html=True)
