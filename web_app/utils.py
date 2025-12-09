# web_app/utils.py
import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_data():
    """Load the retail inventory data"""
    try:
        # Try to load from notebooks directory
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notebooks', 'retail_store_inventory.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            # Try current directory
            csv_path = 'retail_store_inventory.csv'
            df = pd.read_csv(csv_path)
        
        # Convert Date to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def get_css():
    """Return custom CSS styles"""
    return """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: black;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .info-box {
        background-color: black;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    .alert-high {
        background-color: black;
        border-color: #dc3545;
    }
    .alert-medium {
        background-color: black;
        border-color: #ffc107;
    }
    .alert-low {
        background-color: black;
        border-color: #17a2b8;
    }
    </style>
    """