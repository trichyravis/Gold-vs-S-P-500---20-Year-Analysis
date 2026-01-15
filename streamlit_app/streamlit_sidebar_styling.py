"""
Custom Streamlit Sidebar Styling
Apply this to any page to get bright blue sidebar with gold text
"""

import streamlit as st

def apply_sidebar_styling():
    """
    Apply custom sidebar styling with bright blue background and gold text
    Add this function call to the top of any page after st.set_page_config()
    """
    st.markdown("""
        <style>
        /* Sidebar Background - Bright Blue */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #1E90FF 0%, #4169E1 100%);
        }
        
        /* Sidebar Text - Gold */
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #FFD700;
        }
        
        [data-testid="stSidebar"] label {
            color: #FFD700;
        }
        
        [data-testid="stSidebar"] div {
            color: #FFD700;
        }
        
        [data-testid="stSidebar"] p {
            color: #FFD700;
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #FFD700;
        }
        
        /* Sidebar Radio Buttons */
        [data-testid="stSidebar"] [data-baseweb="radio"] {
            color: #FFD700;
        }
        
        /* Sidebar Sliders */
        [data-testid="stSidebar"] [data-testid="stSlider"] {
            color: #FFD700;
        }
        
        /* Sidebar Checkboxes */
        [data-testid="stSidebar"] [data-testid="stCheckbox"] {
            color: #FFD700;
        }
        
        /* Sidebar Select Boxes */
        [data-testid="stSidebar"] [data-baseweb="select"] {
            color: #FFD700;
        }
        
        /* Main Sidebar Text Color Override */
        [data-testid="stSidebar"] {
            --text-color: #FFD700;
        }
        
        /* Sidebar Number Input */
        [data-testid="stSidebar"] [data-testid="stNumberInput"] {
            color: #FFD700;
        }
        
        /* Sidebar Text Input */
        [data-testid="stSidebar"] [data-testid="stTextInput"] {
            color: #FFD700;
        }
        
        /* Navigation Links in Sidebar */
        [data-testid="stSidebar"] a {
            color: #FFD700 !important;
        }
        
        /* Sidebar Background for inputs */
        [data-testid="stSidebar"] input {
            background-color: rgba(255, 215, 0, 0.1) !important;
            color: #FFD700 !important;
        }
        
        /* Sidebar Expander */
        [data-testid="stSidebar"] [data-testid="stExpander"] {
            color: #FFD700;
        }
        
        </style>
    """, unsafe_allow_html=True)

# Example usage - add this to top of each page:
# from streamlit_sidebar_styling import apply_sidebar_styling
# apply_sidebar_styling()
