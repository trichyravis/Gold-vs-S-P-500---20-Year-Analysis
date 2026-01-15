"""
═══════════════════════════════════════════════════════════════════════════════
STREAMLIT PROFESSIONAL DESIGN TEMPLATE - CONFIGURATION
═══════════════════════════════════════════════════════════════════════════════

Centralized configuration for colors, typography, spacing, and theme.
Change values here and ALL pages automatically update!

Usage:
    from config import COLORS, TYPOGRAPHY, SIDEBAR_CONFIG
    color = COLORS['primary_dark']
    font = TYPOGRAPHY['font_primary']
"""

# ═══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE - THE MOUNTAIN PATH BRANDING
# ═══════════════════════════════════════════════════════════════════════════════

COLORS = {
    # Primary Colors - Mountain Path Blue & Gold
    'primary_dark': '#003366',          # Dark Blue (main)
    'primary_light': '#1E90FF',         # Bright Blue (accents)
    'accent_gold': '#FFD700',           # Gold (highlights)
    
    # Secondary Colors
    'secondary_blue': '#4169E1',        # Royal Blue
    'text_dark': '#003366',             # Dark Blue text
    'text_light': '#FFD700',            # Gold text
    'text_muted': '#666666',            # Gray text
    'bg_light': '#F5F5F5',              # Light gray background
    
    # Status Colors
    'success': '#28A745',               # Green
    'warning': '#FFC107',               # Yellow/Amber
    'danger': '#DC3545',                # Red
    'info': '#17A2B8',                  # Cyan
    
    # Gradients (used in sidebar)
    'gradient_primary': 'linear-gradient(135deg, #003366 0%, #1E90FF 100%)',
}

# ═══════════════════════════════════════════════════════════════════════════════
# TYPOGRAPHY
# ═══════════════════════════════════════════════════════════════════════════════

TYPOGRAPHY = {
    'font_primary': "'Segoe UI', 'Helvetica Neue', sans-serif",
    'font_secondary': "'Segoe UI', 'Helvetica Neue', sans-serif",
    
    # Font Sizes
    'h1_size': '48px',
    'h2_size': '36px',
    'h3_size': '24px',
    'h4_size': '20px',
    'body_size': '16px',
    'small_size': '14px',
    
    # Font Weights
    'normal': '400',
    'semibold': '600',
    'bold': '700',
    'extra_bold': '800',
}

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SIDEBAR_CONFIG = {
    'background_gradient': 'linear-gradient(135deg, #003366 0%, #1E90FF 100%)',
    'background_color': '#003366',
    'text_color': '#FFD700',            # Gold text
    'header_text_color': '#FFFFFF',     # White for headers
    'divider_color': 'rgba(255, 215, 0, 0.3)',
    'link_color': '#FFD700',
    'link_hover_color': '#FFFFFF',
}

# ═══════════════════════════════════════════════════════════════════════════════
# HERO HEADER CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

HERO_HEADER = {
    'background_gradient': 'linear-gradient(135deg, #003366 0%, #1E90FF 100%)',
    'padding': '2rem 2.5rem',
    'border_radius': '12px',
    'box_shadow': '0 8px 24px rgba(0, 51, 102, 0.3)',
    'border_width': '3px',
    'border_color': '#FFD700',
    'max_width': '1200px',
    'emoji_size': '120px',
    'title_font_size': '48px',
    'title_font_weight': '800',
    'title_color': '#FFFFFF',
    'title_letter_spacing': '2px',
    'subtitle_font_size': '24px',
    'subtitle_font_weight': '600',
    'subtitle_color': '#FFD700',
    'description_font_size': '16px',
    'description_color': '#E8E8E8',
}

# ═══════════════════════════════════════════════════════════════════════════════
# METRIC CARD CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

METRIC_CARD = {
    'background_gradient': 'linear-gradient(135deg, #F5F5F5 0%, #FFFFFF 100%)',
    'padding': '1.5rem',
    'border_radius': '8px',
    'text_color': '#003366',
    'box_shadow': '0 4px 12px rgba(0, 51, 102, 0.1)',
    'highlight_border_width': '2px',
    'highlight_border_color': '#FFD700',
}

# ═══════════════════════════════════════════════════════════════════════════════
# BUTTONS CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

BUTTONS = {
    'primary_background': '#003366',
    'primary_text_color': '#FFFFFF',
    'primary_padding': '12px 24px',
    'primary_border_radius': '6px',
    'primary_font_weight': '600',
    'secondary_background': '#E8E8E8',
    'secondary_text_color': '#003366',
    'accent_background': '#FFD700',
    'accent_text_color': '#003366',
}

# ═══════════════════════════════════════════════════════════════════════════════
# SPACING
# ═══════════════════════════════════════════════════════════════════════════════

SPACING = {
    'xs': '0.25rem',
    'sm': '0.5rem',
    'md': '1rem',
    'lg': '1.5rem',
    'xl': '2rem',
    'xxl': '3rem',
}

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

FOOTER_CONFIG = {
    'text_color': '#666666',
    'padding': '3rem 1rem',
}

# ═══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════

"""
USAGE IN CODE:

from config import COLORS, TYPOGRAPHY, SIDEBAR_CONFIG

# In your styles or components:
color = COLORS['primary_dark']        # #003366
font = TYPOGRAPHY['h1_size']          # 48px
sidebar_bg = SIDEBAR_CONFIG['background_gradient']

# Update entire app theme by changing values here!
# All pages that use these configs will update automatically.
"""
