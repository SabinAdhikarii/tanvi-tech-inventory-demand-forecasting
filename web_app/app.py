# web_app/app.py
import streamlit as st
import sys
import os

# Page config
st.set_page_config(
    page_title="Retail Management System",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛍️"
)

# Import utilities
from utils import load_data, get_css

# Apply custom CSS
st.markdown(get_css(), unsafe_allow_html=True)
# Hide Streamlit's default multipage navigation
st.markdown("""
    <style>
        /* Hide the built-in multipage app navigation */
        div[data-testid="stSidebarNav"] {display: none !important;}
        /* Optional: hide Streamlit branding at the bottom */
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

# Sidebar Navigation
st.sidebar.title(" Retail Management")
st.sidebar.markdown("---")

# Navigation menu
pages = {
    ' Dashboard': 'Dashboard',
    ' Alerts': 'Alerts',
    ' Products List': 'Products',
    ' Admin': 'Admin'
}

# Create navigation buttons
selected = st.sidebar.radio(
    "Navigate to:",
    list(pages.keys()),
    index=list(pages.values()).index(st.session_state.current_page) if st.session_state.current_page in pages.values() else 0
)

# Update current page
st.session_state.current_page = pages[selected]

# Load data once (cached)
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Route to appropriate page
if st.session_state.current_page == 'Dashboard':
    from pages.dashboard import show_dashboard
    show_dashboard(st.session_state.df)
elif st.session_state.current_page == 'Alerts':
    from pages.alerts import show_alerts
    show_alerts(st.session_state.df)
elif st.session_state.current_page == 'Products':
    from pages.products import show_products
    show_products(st.session_state.df)
elif st.session_state.current_page == 'Admin':
    from pages.admin import show_admin
    show_admin(st.session_state.df)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8rem; padding: 1rem 0;'>
    <p>Retail Management System v1.0</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    # Helpful message when someone runs `python app.py` directly.
    try:
        import streamlit  # noqa: F401  # type: ignore
    except ModuleNotFoundError:
        exe = sys.executable
        print("Streamlit is not installed in the current Python interpreter:", exe)
        print()
        print("To run the app using the environment that has Streamlit installed (recommended):")
        print("  1) Activate your conda env that has streamlit, e.g.:")
        print("       conda activate retail-forecast")
        print("  2) Run the app with Streamlit:")
        print("       streamlit run web_app\\app.py")
        print()
        print("If you want to install Streamlit into this Python interpreter, run:")
        print(f"  {exe} -m pip install streamlit")
        sys.exit(1)
    else:
        print("It looks like you're running this file with 'python app.py'.")
        print("Use the Streamlit CLI to run the app so the web server starts:")
        print("  streamlit run web_app\\app.py")
        print("(Or run: python -m streamlit run web_app\\app.py)")