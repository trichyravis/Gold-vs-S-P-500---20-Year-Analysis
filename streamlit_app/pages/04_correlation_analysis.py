"""
Correlation Analysis Page
Analyze relationships and diversification benefits
Author: Prof. V. Ravichandran
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from src.utils import StatisticalHelper

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Correlation Analysis",
    page_icon="🔗",
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
    <h1 class="header-title">🔗 Correlation Analysis</h1>
    <p class="header-subtitle">Examine relationships and diversification benefits</p>
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
gld_returns = data_copy[gld_col].pct_change() * 100
spy_returns = data_copy[spy_col].pct_change() * 100

# ==================== CORRELATION METRICS ====================
st.markdown("### 📊 Correlation Metrics")

correlation = StatisticalHelper.calculate_correlation(gld_returns.dropna(), spy_returns.dropna())
beta = StatisticalHelper.calculate_beta(gld_returns.dropna(), spy_returns.dropna())
covariance = gld_returns.cov(spy_returns)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Correlation", f"{correlation:.4f}")
    st.caption("Measure of co-movement (-1 to 1)")

with col2:
    st.metric("Beta", f"{beta:.4f}")
    st.caption("Sensitivity to market (SPY)")

with col3:
    st.metric("Covariance", f"{covariance:.4f}")
    st.caption("Joint variability")

with col4:
    diversification_benefit = (1 - correlation) * 100
    st.metric("Diversification Benefit", f"{diversification_benefit:.2f}%")
    st.caption("Risk reduction potential")

# ==================== INTERPRETATION ====================
st.markdown("### 📖 Interpretation")

if correlation > 0.7:
    corr_interpretation = "🔴 **High Positive Correlation**: Assets move together. Limited diversification benefit."
elif correlation > 0.3:
    corr_interpretation = "🟡 **Moderate Positive Correlation**: Assets tend to move together but with some independence."
elif correlation > -0.3:
    corr_interpretation = "🟢 **Low Correlation**: Assets move relatively independently. Good diversification."
elif correlation > -0.7:
    corr_interpretation = "🟢 **Moderate Negative Correlation**: Assets often move in opposite directions. Excellent diversification."
else:
    corr_interpretation = "🟢 **High Negative Correlation**: Assets strongly hedge each other. Perfect diversification."

st.markdown(corr_interpretation)

# ==================== SCATTER PLOT ====================
st.markdown("### 📊 Returns Scatter Plot")

fig_scatter = go.Figure()

fig_scatter.add_trace(go.Scatter(
    x=gld_returns.dropna(),
    y=spy_returns.dropna(),
    mode='markers',
    marker=dict(
        size=5,
        color=gld_returns.dropna(),
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="GLD Returns (%)")
    ),
    text=[f"GLD: {g:.2f}%<br>SPY: {s:.2f}%" for g, s in zip(gld_returns.dropna(), spy_returns.dropna())],
    hovertemplate='%{text}<extra></extra>'
))

# Add trend line
z = np.polyfit(gld_returns.dropna(), spy_returns.dropna(), 1)
p = np.poly1d(z)
x_line = np.linspace(gld_returns.min(), gld_returns.max(), 100)
fig_scatter.add_trace(go.Scatter(
    x=x_line,
    y=p(x_line),
    mode='lines',
    name='Trend',
    line=dict(color='red', width=2)
))

fig_scatter.update_layout(
    title=f'Daily Returns Correlation (r = {correlation:.4f})',
    xaxis_title='Gold (GLD) Daily Return (%)',
    yaxis_title='S&P 500 (SPY) Daily Return (%)',
    template='plotly_white',
    height=500
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ==================== ROLLING CORRELATION ====================
st.markdown("### 📈 Rolling Correlation (252-day window)")

rolling_correlation = gld_returns.rolling(window=252).corr(spy_returns)

fig_rolling_corr = go.Figure()

fig_rolling_corr.add_trace(go.Scatter(
    x=data_copy[date_col] if date_col else data_copy.index,
    y=rolling_correlation,
    name='Rolling Correlation (252-day)',
    line=dict(color='#003366', width=2),
    fill='tozeroy',
    fillcolor='rgba(0, 51, 102, 0.3)'
))

fig_rolling_corr.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zero Correlation")
fig_rolling_corr.add_hline(y=correlation, line_dash="dash", line_color="green", annotation_text="Overall Correlation")

fig_rolling_corr.update_layout(
    title='Rolling Correlation Over Time',
    xaxis_title='Date',
    yaxis_title='Correlation',
    template='plotly_white',
    height=400
)
st.plotly_chart(fig_rolling_corr, use_container_width=True)

# ==================== BETA ANALYSIS ====================
st.markdown("### 📊 Beta Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### What is Beta?")
    st.write(f"""
    Beta measures how sensitive Gold is to S&P 500 movements:
    - **Beta = {beta:.4f}**
    - If beta > 1: Gold is MORE volatile than SPY
    - If beta < 1: Gold is LESS volatile than SPY
    - If beta < 0: Gold moves opposite to SPY (hedge)
    
    **Interpretation:** For every 1% move in SPY, Gold tends to move {beta:.4f}%
    """)

with col2:
    # Beta visualization
    fig_beta = go.Figure()
    
    fig_beta.add_trace(go.Bar(
        x=['Gold (GLD)'],
        y=[beta],
        marker_color='#FFD700',
        name='Beta',
        text=[f"{beta:.4f}"],
        textposition='outside'
    ))
    
    fig_beta.add_hline(y=1, line_dash="dash", line_color="red", annotation_text="Beta = 1 (Market)")
    
    fig_beta.update_layout(
        title='Beta Coefficient',
        yaxis_title='Beta Value',
        template='plotly_white',
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig_beta, use_container_width=True)

# ==================== COVARIANCE MATRIX ====================
st.markdown("### 📊 Covariance & Correlation Matrix")

returns_df = pd.DataFrame({
    'GLD': gld_returns.dropna(),
    'SPY': spy_returns.dropna()
})

col1, col2 = st.columns(2)

with col1:
    st.write("**Correlation Matrix:**")
    corr_matrix = returns_df.corr()
    
    fig_corr_heatmap = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=['GLD', 'SPY'],
        y=['GLD', 'SPY'],
        text=corr_matrix.values,
        texttemplate='%{text:.4f}',
        colorscale='RdBu',
        zmid=0,
        zmin=-1,
        zmax=1
    ))
    fig_corr_heatmap.update_layout(height=300)
    st.plotly_chart(fig_corr_heatmap, use_container_width=True)

with col2:
    st.write("**Covariance Matrix:**")
    cov_matrix = returns_df.cov()
    
    fig_cov_heatmap = go.Figure(data=go.Heatmap(
        z=cov_matrix.values,
        x=['GLD', 'SPY'],
        y=['GLD', 'SPY'],
        text=cov_matrix.values,
        texttemplate='%{text:.4f}',
        colorscale='Viridis'
    ))
    fig_cov_heatmap.update_layout(height=300)
    st.plotly_chart(fig_cov_heatmap, use_container_width=True)

# ==================== PORTFOLIO DIVERSIFICATION ====================
st.markdown("### 💼 Portfolio Diversification Analysis")

st.write("""
**Diversification Benefits:**

With a correlation of **{:.4f}** between Gold and S&P 500:

1. **Risk Reduction Potential:** {:.2f}%
   - The lower the correlation, the more risk reduction from diversification
   
2. **Portfolio Construction:** A 50/50 portfolio would have:
""".format(correlation, (1 - correlation) * 100))

# Calculate 50/50 portfolio metrics
w_gld = 0.5
w_spy = 0.5

portfolio_return = w_gld * gld_returns.mean() + w_spy * spy_returns.mean()
portfolio_var = (w_gld ** 2 * gld_returns.var() + 
                 w_spy ** 2 * spy_returns.var() + 
                 2 * w_gld * w_spy * covariance)
portfolio_std = np.sqrt(portfolio_var)
portfolio_volatility = portfolio_std * np.sqrt(252) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Portfolio Annual Return", f"{portfolio_return * 252:.2f}%")

with col2:
    st.metric("Portfolio Volatility", f"{portfolio_volatility:.2f}%")

with col3:
    gld_vol = gld_returns.std() * np.sqrt(252) * 100
    spy_vol = spy_returns.std() * np.sqrt(252) * 100
    weighted_avg_vol = w_gld * gld_vol + w_spy * spy_vol
    diversification_benefit_pct = ((weighted_avg_vol - portfolio_volatility) / weighted_avg_vol) * 100
    st.metric("Diversification Benefit", f"{diversification_benefit_pct:.2f}%")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>Prof. V. Ravichandran | 28+ Years Corporate Finance & Banking Experience | 10+ Years Academic Excellence</p>
    <p>The Mountain Path - World of Finance</p>
</div>
""", unsafe_allow_html=True)
