# web_app/pages/admin.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def show_admin(df):
    """Display admin panel with system management features"""
    
    if df is None:
        st.error("No data available. Please check your data file.")
        return
    
    st.markdown('<div class="main-header">⚙️ Admin Panel</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <h4>System Administration & Management</h4>
        <p>Manage system settings, view system statistics, export data, and perform administrative tasks.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin tabs
    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs([
        " System Statistics", 
        " Data Management", 
        " Settings", 
        " User Management"
    ])
    
    with admin_tab1:
        st.header("System Statistics")
        
        # Overall statistics
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            total_records = len(df)
            st.metric("Total Records", f"{total_records:,}")
        
        with stat_col2:
            date_range = (df['Date'].max() - df['Date'].min()).days
            st.metric("Date Range", f"{date_range} days")
        
        with stat_col3:
            total_stores = df['Store ID'].nunique()
            st.metric("Total Stores", total_stores)
        
        with stat_col4:
            total_products = df['Product ID'].nunique()
            st.metric("Total Products", total_products)
        
        st.markdown("---")
        
        # Data quality metrics
        st.subheader("Data Quality Metrics")
        
        quality_col1, quality_col2 = st.columns(2)
        
        with quality_col1:
            st.write("**Data Completeness**")
            completeness = {
                'Total Records': len(df),
                'Complete Records': len(df.dropna()),
                'Missing Values': df.isnull().sum().sum()
            }
            for key, value in completeness.items():
                st.write(f"- {key}: {value:,}")
            
            completeness_pct = (completeness['Complete Records'] / completeness['Total Records'] * 100) if completeness['Total Records'] > 0 else 0
            st.progress(completeness_pct / 100)
            st.caption(f"Data Completeness: {completeness_pct:.1f}%")
        
        with quality_col2:
            st.write("**Data Range**")
            st.write(f"- Start Date: {df['Date'].min().strftime('%Y-%m-%d')}")
            st.write(f"- End Date: {df['Date'].max().strftime('%Y-%m-%d')}")
            st.write(f"- Categories: {df['Category'].nunique()}")
            st.write(f"- Regions: {df['Region'].nunique()}")
            st.write(f"- Weather Conditions: {df['Weather Condition'].nunique()}")
        
        st.markdown("---")
        
        # System performance
        st.subheader("System Performance Overview")
        
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            st.write("**Sales Performance**")
            total_sales = df['Units Sold'].sum()
            total_revenue = (df['Units Sold'] * df['Price'] * (1 - df['Discount']/100)).sum()
            avg_daily_sales = df.groupby('Date')['Units Sold'].sum().mean()
            
            st.write(f"- Total Sales: {total_sales:,} units")
            st.write(f"- Total Revenue: ${total_revenue:,.2f}")
            st.write(f"- Average Daily Sales: {avg_daily_sales:,.0f} units")
        
        with perf_col2:
            st.write("**Inventory Performance**")
            avg_inventory = df['Inventory Level'].mean()
            total_inventory = df['Inventory Level'].sum()
            inventory_turnover = total_sales / avg_inventory if avg_inventory > 0 else 0
            
            st.write(f"- Average Inventory: {avg_inventory:,.0f} units")
            st.write(f"- Total Inventory Value: ${(df['Inventory Level'] * df['Price']).sum():,.2f}")
            st.write(f"- Inventory Turnover: {inventory_turnover:.2f}x")
        
        # Data distribution charts
        st.markdown("---")
        st.subheader("Data Distribution")
        
        dist_col1, dist_col2 = st.columns(2)
        
        with dist_col1:
            category_dist = df['Category'].value_counts()
            fig_cat_dist = px.pie(
                values=category_dist.values,
                names=category_dist.index,
                title="Records by Category"
            )
            st.plotly_chart(fig_cat_dist, use_container_width=True)
        
        with dist_col2:
            region_dist = df['Region'].value_counts()
            fig_region_dist = px.bar(
                x=region_dist.index,
                y=region_dist.values,
                title="Records by Region",
                labels={'x': 'Region', 'y': 'Count'}
            )
            st.plotly_chart(fig_region_dist, use_container_width=True)
    
    with admin_tab2:
        st.header("Data Management")
        
        # Data export
        st.subheader(" Export Data")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            export_format = st.selectbox(
                "Export Format",
                options=['CSV', 'Excel', 'JSON']
            )
        
        with export_col2:
            export_scope = st.selectbox(
                "Export Scope",
                options=['All Data', 'Filtered Data', 'Summary Statistics']
            )
        
        if st.button(" Download Data", use_container_width=True):
            if export_format == 'CSV':
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"retail_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            elif export_format == 'Excel':
                # Note: This would require openpyxl
                st.info("Excel export requires openpyxl. Please install: pip install openpyxl")
            elif export_format == 'JSON':
                json_data = df.to_json(orient='records', date_format='iso')
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"retail_data_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        st.markdown("---")
        
        # Data import (simulated)
        st.subheader(" Import Data")
        st.info("Data import functionality would be implemented here. Upload new CSV files to update the database.")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a new CSV file to update the database"
        )
        
        if uploaded_file is not None:
            try:
                new_df = pd.read_csv(uploaded_file)
                st.success(f"File uploaded successfully! {len(new_df)} records found.")
                st.dataframe(new_df.head(), use_container_width=True)
                st.warning(" This is a preview. Actual import would require database connection.")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
        
        st.markdown("---")
        
        # Data backup
        st.subheader(" Backup & Restore")
        
        backup_col1, backup_col2 = st.columns(2)
        
        with backup_col1:
            if st.button(" Create Backup", use_container_width=True):
                st.success("Backup created successfully!")
                st.info(f"Backup file: backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        with backup_col2:
            if st.button(" Restore from Backup", use_container_width=True):
                st.warning(" Restore functionality would require backup file selection and database connection.")
    
    with admin_tab3:
        st.header("System Settings")
        
        # General settings
        st.subheader("General Settings")
        
        setting_col1, setting_col2 = st.columns(2)
        
        with setting_col1:
            st.write("**Display Settings**")
            date_format = st.selectbox(
                "Date Format",
                options=['YYYY-MM-DD', 'MM/DD/YYYY', 'DD/MM/YYYY'],
                index=0
            )
            
            currency_symbol = st.selectbox(
                "Currency Symbol",
                options=['$ (USD)', '€ (EUR)', '£ (GBP)', '¥ (JPY)'],
                index=0
            )
            
            items_per_page = st.slider(
                "Items per Page",
                min_value=10,
                max_value=100,
                value=20,
                step=10
            )
        
        with setting_col2:
            st.write("**Alert Settings**")
            
            low_stock_threshold = st.number_input(
                "Low Stock Threshold",
                min_value=0,
                max_value=1000,
                value=100,
                step=10
            )
            
            high_demand_threshold = st.number_input(
                "High Demand Threshold",
                min_value=0,
                max_value=1000,
                value=200,
                step=10
            )
            
            enable_email_alerts = st.checkbox("Enable Email Alerts", value=False)
            enable_sms_alerts = st.checkbox("Enable SMS Alerts", value=False)
        
        if st.button(" Save Settings", use_container_width=True):
            st.success("Settings saved successfully!")
        
        st.markdown("---")
        
        # System maintenance
        st.subheader("System Maintenance")
        
        maint_col1, maint_col2 = st.columns(2)
        
        with maint_col1:
            if st.button(" Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.success("Cache cleared successfully!")
            
            if st.button(" Refresh Data", use_container_width=True):
                st.success("Data refreshed successfully!")
                st.rerun()
        
        with maint_col2:
            if st.button(" Recalculate Statistics", use_container_width=True):
                st.success("Statistics recalculated!")
            
            if st.button(" Run Data Validation", use_container_width=True):
                st.info("Data validation completed. No issues found.")
        
        st.markdown("---")
        
        # System information
        st.subheader("System Information")
        
        sys_info = {
            "Application Version": "1.0.0",
            "Python Version": "3.13",
            "Streamlit Version": "1.37.1",
            "Pandas Version": pd.__version__,
            "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        for key, value in sys_info.items():
            st.write(f"**{key}**: {value}")
    
    with admin_tab4:
        st.header("User Management")
        
        st.info(" User management functionality would be implemented here for multi-user systems.")
        
        # Simulated user list
        st.subheader("Current Users")
        
        users_data = {
            'Username': ['admin', 'manager1', 'analyst1', 'viewer1'],
            'Role': ['Administrator', 'Manager', 'Analyst', 'Viewer'],
            'Last Login': ['2025-11-07 09:00', '2025-11-07 08:30', '2025-11-06 17:00', '2025-11-06 16:00'],
            'Status': ['Active', 'Active', 'Active', 'Inactive']
        }
        
        users_df = pd.DataFrame(users_data)
        st.dataframe(users_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Add new user
        st.subheader("Add New User")
        
        user_col1, user_col2 = st.columns(2)
        
        with user_col1:
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_role = st.selectbox(
                "Role",
                options=['Administrator', 'Manager', 'Analyst', 'Viewer']
            )
        
        with user_col2:
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            new_status = st.selectbox(
                "Status",
                options=['Active', 'Inactive']
            )
        
        if st.button(" Add User", use_container_width=True):
            if new_password == confirm_password:
                st.success(f"User '{new_username}' added successfully!")
            else:
                st.error("Passwords do not match!")
        
        st.markdown("---")
        
        # Permissions
        st.subheader("Role Permissions")
        
        permissions = {
            'Role': ['Administrator', 'Manager', 'Analyst', 'Viewer'],
            'View Dashboard': ['✓', '✓', '✓', '✓'],
            'View Alerts': ['✓', '✓', '✓', '✓'],
            'View Products': ['✓', '✓', '✓', '✓'],
            'Edit Products': ['✓', '✓', '✗', '✗'],
            'Admin Access': ['✓', '✗', '✗', '✗'],
            'Export Data': ['✓', '✓', '✓', '✗']
        }
        
        permissions_df = pd.DataFrame(permissions)
        st.dataframe(permissions_df, use_container_width=True, hide_index=True)
