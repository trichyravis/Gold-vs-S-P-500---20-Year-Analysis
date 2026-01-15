"""
Portfolio Impact Page
Optimize allocation and diversification strategy
Author: Prof. V. Ravichandran
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import minimize

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Portfolio Impact",
    page_icon="💼",
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
    <h1 class="header-title">💼 Portfolio Impact Analysis</h1>
    <p class="header-subtitle">Optimize allocation and diversification strategy</p>
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

# ==================== CALCULATE RETURNS ====================
data_copy = data.copy()
gld_returns = data_copy[gld_col].pct_change().dropna()
spy_returns = data_copy[spy_col].pct_change().dropna()

returns_df = pd.DataFrame({
    'GLD': gld_returns,
    'SPY': spy_returns
})

# ==================== PORTFOLIO ALLOCATION SLIDER ====================
st.markdown("### 🎯 Portfolio Allocation")

col1, col2 = st.columns(2)

with col1:
    gld_weight = st.slider("Gold (GLD) Weight (%)", 0, 100, 50) / 100
    spy_weight = 1 - gld_weight
    
    st.write(f"**S&P 500 (SPY) Weight: {spy_weight*100:.0f}%**")

with col2:
    st.metric("Total Allocation", f"{(gld_weight + spy_weight)*100:.0f}%")

# ==================== PORTFOLIO METRICS ====================
st.markdown("### 📊 Portfolio Metrics")

mean_returns = returns_df.mean()
cov_matrix = returns_df.cov()

portfolio_return = gld_weight * mean_returns['GLD'] + spy_weight * mean_returns['SPY']
portfolio_variance = (gld_weight ** 2 * returns_df['GLD'].var() + 
                     spy_weight ** 2 * returns_df['SPY'].var() + 
                     2 * gld_weight * spy_weight * returns_df['GLD'].cov(returns_df['SPY']))
portfolio_std = np.sqrt(portfolio_variance)

annual_return = portfolio_return * 252 * 100
annual_volatility = portfolio_std * np.sqrt(252) * 100
sharpe_ratio = (portfolio_return * 252) / (portfolio_std * np.sqrt(252))

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Annual Return", f"{annual_return:.2f}%")

with col2:
    st.metric("Annual Volatility", f"{annual_volatility:.2f}%")

with col3:
    st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

with col4:
    st.metric("Risk-Return Ratio", f"{annual_return/annual_volatility:.2f}")

# ==================== EFFICIENT FRONTIER ====================
st.markdown("### 📈 Efficient Frontier Analysis")

# Generate random portfolios
np.random.seed(42)
n_portfolios = 5000
results = np.zeros((3, n_portfolios))

for i in range(n_portfolios):
    weights = np.random.random(2)
    weights /= np.sum(weights)
    
    p_return = np.sum(weights * mean_returns) * 252
    p_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
    p_sharpe = p_return / p_std
    
    results[0,i] = p_std * 100
    results[1,i] = p_return * 100
    results[2,i] = p_sharpe

# Find minimum variance portfolio
min_var_idx = results[0].argmin()
max_sharpe_idx = results[2].argmax()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=results[0],
    y=results[1],
    mode='markers',
    marker=dict(
        size=5,
        color=results[2],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title='Sharpe Ratio')
    ),
    text=[f"Vol: {v:.2f}%, Return: {r:.2f}%" for v, r in zip(results[0], results[1])],
    hovertemplate='%{text}<extra></extra>',
    name='Random Portfolios'
))

# Add current portfolio
fig.add_trace(go.Scatter(
    x=[annual_volatility],
    y=[annual_return],
    mode='markers+text',
    marker=dict(size=15, color='red'),
    text=['Current'],
    textposition='top center',
    name='Current Portfolio',
    hovertemplate='Current: Vol: %{x:.2f}%, Return: %{y:.2f}%<extra></extra>'
))

# Add minimum variance
fig.add_trace(go.Scatter(
    x=[results[0, min_var_idx]],
    y=[results[1, min_var_idx]],
    mode='markers+text',
    marker=dict(size=12, color='green'),
    text=['Min Var'],
    textposition='top center',
    name='Minimum Variance',
    hovertemplate='Min Var: Vol: %{x:.2f}%, Return: %{y:.2f}%<extra></extra>'
))

# Add maximum Sharpe
fig.add_trace(go.Scatter(
    x=[results[0, max_sharpe_idx]],
    y=[results[1, max_sharpe_idx]],
    mode='markers+text',
    marker=dict(size=12, color='gold'),
    text=['Max Sharpe'],
    textposition='top center',
    name='Maximum Sharpe',
    hovertemplate='Max Sharpe: Vol: %{x:.2f}%, Return: %{y:.2f}%<extra></extra>'
))

fig.update_layout(
    title='Efficient Frontier: All Possible Allocations',
    xaxis_title='Annual Volatility (%)',
    yaxis_title='Annual Return (%)',
    template='plotly_white',
    height=600
)
st.plotly_chart(fig, use_container_width=True)

# ==================== ALLOCATION COMPARISON ====================
st.markdown("### 🎯 Allocation Comparison")

allocation_scenarios = {
    '100% Gold': (1.0, 0.0),
    '75% Gold / 25% S&P': (0.75, 0.25),
    'Current (50/50)': (gld_weight, spy_weight),
    '25% Gold / 75% S&P': (0.25, 0.75),
    '100% S&P 500': (0.0, 1.0),
}

scenario_results = []

for scenario_name, (gld_w, spy_w) in allocation_scenarios.items():
    p_return = gld_w * mean_returns['GLD'] + spy_w * mean_returns['SPY']
    p_variance = (gld_w ** 2 * returns_df['GLD'].var() + 
                 spy_w ** 2 * returns_df['SPY'].var() + 
                 2 * gld_w * spy_w * returns_df['GLD'].cov(returns_df['SPY']))
    p_std = np.sqrt(p_variance)
    p_sharpe = (p_return * 252) / (p_std * np.sqrt(252))
    
    scenario_results.append({
        'Allocation': scenario_name,
        'Annual Return (%)': f"{p_return * 252 * 100:.2f}",
        'Annual Volatility (%)': f"{p_std * np.sqrt(252) * 100:.2f}",
        'Sharpe Ratio': f"{p_sharpe:.2f}"
    })

scenario_df = pd.DataFrame(scenario_results)
st.dataframe(scenario_df, use_container_width=True)

# ==================== PORTFOLIO WEIGHT PIE CHART ====================
st.markdown("### 🥧 Current Portfolio Allocation")

col1, col2 = st.columns(2)

with col1:
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Gold (GLD)', 'S&P 500 (SPY)'],
        values=[gld_weight * 100, spy_weight * 100],
        marker=dict(colors=['#FFD700', '#003366']),
        hole=0.4
    )])
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.markdown("#### Asset Allocation Details")
    st.write(f"""
    **Gold (GLD):** {gld_weight * 100:.1f}%
    - Expected Annual Return: {gld_weight * mean_returns['GLD'] * 252 * 100:.2f}%
    
    **S&P 500 (SPY):** {spy_weight * 100:.1f}%
    - Expected Annual Return: {spy_weight * mean_returns['SPY'] * 252 * 100:.2f}%
    
    **Total Portfolio Return:** {annual_return:.2f}%
    """)

# ==================== DIVERSIFICATION METRICS ====================
st.markdown("### 📊 Diversification Metrics")

col1, col2, col3 = st.columns(3)

correlation = returns_df['GLD'].corr(returns_df['SPY'])

with col1:
    st.metric("Correlation", f"{correlation:.4f}")

with col2:
    weighted_vol = gld_weight * returns_df['GLD'].std() * np.sqrt(252) * 100 + spy_weight * returns_df['SPY'].std() * np.sqrt(252) * 100
    diversification_benefit = (weighted_vol - annual_volatility) / weighted_vol * 100
    st.metric("Diversification Benefit", f"{diversification_benefit:.2f}%")

with col3:
    herfindahl_index = gld_weight ** 2 + spy_weight ** 2
    st.metric("Herfindahl Index", f"{herfindahl_index:.4f}")
    st.caption("Lower is better (max 1.0)")

# ==================== INSIGHTS ====================
st.markdown("### 🎯 Key Insights & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Risk Considerations:")
    if annual_volatility < 10:
        st.write("✅ **Low Risk Portfolio** - Suitable for conservative investors")
    elif annual_volatility < 15:
        st.write("🟡 **Moderate Risk Portfolio** - Balanced approach")
    else:
        st.write("🔴 **High Risk Portfolio** - For aggressive investors")

with col2:
    st.markdown("#### Return Considerations:")
    if annual_return < 5:
        st.write("⚠️ **Low Expected Return** - Below historical averages")
    elif annual_return < 10:
        st.write("✅ **Moderate Expected Return** - In line with historical performance")
    else:
        st.write("📈 **High Expected Return** - Above historical averages")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence</p>
    <p>The Mountain Path - World of Finance</p>
</div>
""", unsafe_allow_html=True)
