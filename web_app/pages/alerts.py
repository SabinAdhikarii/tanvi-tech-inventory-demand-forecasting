# web_app/pages/alerts.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def show_alerts(df):
    """Display alerts and notifications page"""
    
    if df is None:
        st.error("No data available. Please check your data file.")
        return
    
    st.markdown('<div class="main-header"> Alerts & Notifications</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <h4>Stay Informed About Your Inventory</h4>
        <p>This page shows important alerts about low stock, high demand, pricing issues, and other critical 
        information that requires your attention.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate alerts
    alerts = []
    
    # Low Stock Alerts
    st.header(" Stock Alerts")
    
    # Define thresholds
    low_stock_threshold = df['Inventory Level'].quantile(0.2)  # Bottom 20%
    high_demand_threshold = df['Units Ordered'].quantile(0.8)  # Top 20%
    
    # Low inventory alerts
    low_stock = df[df['Inventory Level'] < low_stock_threshold].copy()
    if len(low_stock) > 0:
        st.subheader(" Low Stock Alert")
        st.warning(f"**{len(low_stock)} products** have inventory levels below the threshold ({low_stock_threshold:.0f} units)")
        
        # Show top low stock items
        low_stock_summary = low_stock.groupby(['Product ID', 'Category', 'Store ID']).agg({
            'Inventory Level': 'mean',
            'Units Sold': 'mean',
            'Price': 'mean'
        }).reset_index()
        low_stock_summary = low_stock_summary.sort_values('Inventory Level').head(10)
        
        st.dataframe(
            low_stock_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Product ID": "Product",
                "Category": "Category",
                "Store ID": "Store",
                "Inventory Level": st.column_config.NumberColumn("Current Stock", format="%.0f"),
                "Units Sold": st.column_config.NumberColumn("Avg Units Sold", format="%.1f"),
                "Price": st.column_config.NumberColumn("Price", format="$%.2f")
            }
        )
    else:
        st.success(" All products have adequate stock levels")
    
    st.markdown("---")
    
    # High Demand Alerts
    st.header(" High Demand Alerts")
    
    high_demand = df[df['Units Ordered'] > high_demand_threshold].copy()
    if len(high_demand) > 0:
        st.subheader(" High Demand Products")
        st.info(f"**{len(high_demand)} product entries** show high demand (above {high_demand_threshold:.0f} units ordered)")
        
        high_demand_summary = high_demand.groupby(['Product ID', 'Category', 'Region']).agg({
            'Units Ordered': 'mean',
            'Inventory Level': 'mean',
            'Price': 'mean',
            'Discount': 'mean'
        }).reset_index()
        high_demand_summary = high_demand_summary.sort_values('Units Ordered', ascending=False).head(10)
        
        st.dataframe(
            high_demand_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Product ID": "Product",
                "Category": "Category",
                "Region": "Region",
                "Units Ordered": st.column_config.NumberColumn("Avg Demand", format="%.0f"),
                "Inventory Level": st.column_config.NumberColumn("Current Stock", format="%.0f"),
                "Price": st.column_config.NumberColumn("Price", format="$%.2f"),
                "Discount": st.column_config.NumberColumn("Discount", format="%.0f%%")
            }
        )
    else:
        st.info("No unusually high demand detected")
    
    st.markdown("---")
    
    # Price Alerts
    st.header(" Pricing Alerts")
    
    # Products with high discount but low sales
    high_discount_low_sales = df[(df['Discount'] > 15) & (df['Units Sold'] < df['Units Sold'].quantile(0.3))].copy()
    if len(high_discount_low_sales) > 0:
        st.subheader(" High Discount, Low Sales")
        st.warning(f"**{len(high_discount_low_sales)} products** have high discounts (>15%) but low sales. Consider reviewing pricing strategy.")
        
        discount_alert_summary = high_discount_low_sales.groupby(['Product ID', 'Category']).agg({
            'Discount': 'mean',
            'Units Sold': 'mean',
            'Price': 'mean'
        }).reset_index()
        discount_alert_summary = discount_alert_summary.sort_values('Discount', ascending=False).head(10)
        
        st.dataframe(
            discount_alert_summary,
            use_container_width=True,
            hide_index=True
        )
    
    # Products priced significantly above competitor
    competitor_price_diff = df[df['Price'] > df['Competitor Pricing'] * 1.2].copy()
    if len(competitor_price_diff) > 0:
        st.subheader(" Price Above Competitors")
        st.warning(f"**{len(competitor_price_diff)} products** are priced more than 20% above competitor pricing")
        
        price_alert_summary = competitor_price_diff.groupby(['Product ID', 'Category']).agg({
            'Price': 'mean',
            'Competitor Pricing': 'mean',
            'Units Sold': 'mean'
        }).reset_index()
        price_alert_summary['Price Difference'] = price_alert_summary['Price'] - price_alert_summary['Competitor Pricing']
        price_alert_summary = price_alert_summary.sort_values('Price Difference', ascending=False).head(10)
        
        st.dataframe(
            price_alert_summary,
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    
    # Store Performance Alerts
    st.header(" Store Performance Alerts")
    
    store_performance = df.groupby('Store ID').agg({
        'Units Sold': 'sum',
        'Inventory Level': 'mean'
    }).reset_index()
    store_performance = store_performance.sort_values('Units Sold')
    
    # Identify underperforming stores
    avg_sales = store_performance['Units Sold'].mean()
    underperforming_stores = store_performance[store_performance['Units Sold'] < avg_sales * 0.8]
    
    if len(underperforming_stores) > 0:
        st.subheader(" Underperforming Stores")
        st.warning(f"**{len(underperforming_stores)} stores** are performing below average")
        
        st.dataframe(
            underperforming_stores,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Store ID": "Store",
                "Units Sold": st.column_config.NumberColumn("Total Sales", format="%,.0f"),
                "Inventory Level": st.column_config.NumberColumn("Avg Inventory", format="%.0f")
            }
        )
    else:
        st.success(" All stores are performing well")
    
    st.markdown("---")
    
    # Category Alerts
    st.header(" Category Performance Alerts")
    
    category_performance = df.groupby('Category').agg({
        'Units Sold': 'sum',
        'Inventory Level': 'mean',
        'Units Ordered': 'sum'
    }).reset_index()
    category_performance['Demand vs Supply'] = category_performance['Units Ordered'] - category_performance['Units Sold']
    
    # Categories with high demand but low sales (potential stockouts)
    stockout_risk = category_performance[category_performance['Demand vs Supply'] > category_performance['Demand vs Supply'].quantile(0.75)]
    
    if len(stockout_risk) > 0:
        st.subheader(" Potential Stockout Risk")
        st.error(f"**{len(stockout_risk)} categories** show high demand relative to sales (potential stockouts)")
        
        st.dataframe(
            stockout_risk.sort_values('Demand vs Supply', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    
    # Summary Statistics
    st.markdown("---")
    st.header(" Alert Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Low Stock Items", len(low_stock) if len(low_stock) > 0 else 0)
    
    with col2:
        st.metric("High Demand Items", len(high_demand) if len(high_demand) > 0 else 0)
    
    with col3:
        st.metric("Pricing Alerts", len(high_discount_low_sales) + len(competitor_price_diff))
    
    with col4:
        st.metric("Store Alerts", len(underperforming_stores) if len(underperforming_stores) > 0 else 0)
    
    # Filter options
    st.markdown("---")
    st.subheader(" Filter Alerts")
    
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        selected_category = st.multiselect(
            "Filter by Category",
            options=df['Category'].unique(),
            default=[]
        )
    
    with filter_col2:
        selected_region = st.multiselect(
            "Filter by Region",
            options=df['Region'].unique(),
            default=[]
        )
    
    if selected_category or selected_region:
        filtered_df = df.copy()
        if selected_category:
            filtered_df = filtered_df[filtered_df['Category'].isin(selected_category)]
        if selected_region:
            filtered_df = filtered_df[filtered_df['Region'].isin(selected_region)]
        
        st.info(f"Showing alerts for {len(filtered_df)} filtered records")
        st.dataframe(filtered_df.head(20), use_container_width=True)

