
"""
Custom Sidebar Styling - POWERFUL CSS
Add this to the TOP of every page file for bright blue sidebar with gold text
"""

import streamlit as st

def apply_custom_sidebar():
    """
    Apply POWERFUL custom sidebar styling
    Call this at the very top of each page after st.set_page_config()
    """
    st.markdown("""
        <style>
        /* ============ SIDEBAR BACKGROUND ============ */
        section[data-testid="stSidebar"] {
            background: linear-gradient(135deg, #1E90FF 0%, #4169E1 100%) !important;
            background-color: #1E90FF !important;
        }
        
        section[data-testid="stSidebar"] > div {
            background: linear-gradient(135deg, #1E90FF 0%, #4169E1 100%) !important;
            background-color: #1E90FF !important;
        }
        
        section[data-testid="stSidebar"] > div > div {
            background: linear-gradient(135deg, #1E90FF 0%, #4169E1 100%) !important;
        }
        
        /* ============ ALL TEXT IN SIDEBAR ============ */
        section[data-testid="stSidebar"] * {
            color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] p {
            color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] label {
            color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6 {
            color: #FFD700 !important;
        }
        
        /* ============ SIDEBAR MARKDOWN TEXT ============ */
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
            color: #FFD700 !important;
        }
        
        /* ============ SIDEBAR INPUTS & CONTROLS ============ */
        section[data-testid="stSidebar"] input {
            color: #FFD700 !important;
            background-color: rgba(255, 215, 0, 0.2) !important;
            border-color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] input::placeholder {
            color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] input:focus {
            color: #FFD700 !important;
            background-color: rgba(255, 215, 0, 0.3) !important;
            border-color: #FFD700 !important;
        }
        
        /* ============ SIDEBAR RADIO BUTTONS ============ */
        section[data-testid="stSidebar"] [role="radio"] {
            color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] [role="radio"] span {
            color: #FFD700 !important;
        }
        
        /* ============ SIDEBAR CHECKBOXES ============ */
        section[data-testid="stSidebar"] [role="checkbox"] {
            color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] [role="checkbox"] span {
            color: #FFD700 !important;
        }
        
        /* ============ SIDEBAR BUTTONS ============ */
        section[data-testid="stSidebar"] button {
            color: #FFD700 !important;
            background-color: rgba(30, 144, 255, 0.8) !important;
            border-color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] button:hover {
            color: #FFFFFF !important;
            background-color: #4169E1 !important;
        }
        
        /* ============ SIDEBAR SELECTS ============ */
        section[data-testid="stSidebar"] select {
            color: #FFD700 !important;
            background-color: rgba(255, 215, 0, 0.1) !important;
            border-color: #FFD700 !important;
        }
        
        /* ============ SIDEBAR SLIDERS ============ */
        section[data-testid="stSidebar"] [data-testid="stSlider"] {
            color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] [data-testid="stSlider"] span {
            color: #FFD700 !important;
        }
        
        /* ============ SIDEBAR METRICS ============ */
        section[data-testid="stSidebar"] [data-testid="stMetricContainer"] {
            color: #FFD700 !important;
        }
        
        /* ============ SIDEBAR EXPANDABLE ============ */
        section[data-testid="stSidebar"] [data-testid="stExpander"] {
            background-color: rgba(255, 215, 0, 0.1) !important;
        }
        
        section[data-testid="stSidebar"] [data-testid="stExpander"] button {
            color: #FFD700 !important;
        }
        
        /* ============ SIDEBAR LINKS ============ */
        section[data-testid="stSidebar"] a {
            color: #FFD700 !important;
        }
        
        section[data-testid="stSidebar"] a:hover {
            color: #FFFFFF !important;
        }
        
        /* ============ ENSURE NO WHITE TEXT ============ */
        section[data-testid="stSidebar"] .stMarkdown {
            color: #FFD700 !important;
        }
        
        /* ============ FIX FOR LIGHT TEXT ============ */
        section[data-testid="stSidebar"] {
            --text-color: #FFD700;
            --background-color: #1E90FF;
        }
        </style>
    """, unsafe_allow_html=True)
