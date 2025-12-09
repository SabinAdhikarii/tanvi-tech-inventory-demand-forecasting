# web_app/pages/products.py
import streamlit as st
import pandas as pd
import plotly.express as px

def show_products(df):
    """Display products list and inventory management page"""
    
    if df is None:
        st.error("No data available. Please check your data file.")
        return
    
    st.markdown('<div class="main-header">📦 Products List & Inventory</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <h4>Manage Your Product Inventory</h4>
        <p>View and manage all your products, check inventory levels, pricing, and performance metrics. 
        Use filters to find specific products quickly.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    st.header("🔍 Filter Products")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        selected_categories = st.multiselect(
            "Categories",
            options=sorted(df['Category'].unique()),
            default=[]
        )
    
    with filter_col2:
        selected_regions = st.multiselect(
            "Regions",
            options=sorted(df['Region'].unique()),
            default=[]
        )
    
    with filter_col3:
        selected_stores = st.multiselect(
            "Stores",
            options=sorted(df['Store ID'].unique()),
            default=[]
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
    if selected_stores:
        filtered_df = filtered_df[filtered_df['Store ID'].isin(selected_stores)]
    
    st.markdown("---")
    
    # Product Summary Statistics
    st.header("📊 Product Summary")
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        unique_products = filtered_df['Product ID'].nunique()
        st.metric("Total Products", unique_products)
    
    with summary_col2:
        total_inventory = filtered_df['Inventory Level'].sum()
        st.metric("Total Inventory", f"{total_inventory:,}")
    
    with summary_col3:
        avg_price = filtered_df['Price'].mean()
        st.metric("Average Price", f"${avg_price:.2f}")
    
    with summary_col4:
        total_sales = filtered_df['Units Sold'].sum()
        st.metric("Total Sales", f"{total_sales:,}")
    
    st.markdown("---")
    
    # Product Details Table
    st.header("📋 Product Details")
    
    # Create aggregated product view
    product_summary = filtered_df.groupby(['Product ID', 'Category']).agg({
        'Inventory Level': 'mean',
        'Units Sold': 'sum',
        'Units Ordered': 'sum',
        'Price': 'mean',
        'Discount': 'mean',
        'Store ID': 'nunique',
        'Region': lambda x: ', '.join(x.unique()[:3])  # Show first 3 regions
    }).reset_index()
    
    product_summary.columns = [
        'Product ID', 'Category', 'Avg Inventory', 'Total Units Sold', 
        'Total Units Ordered', 'Avg Price', 'Avg Discount', 'Stores', 'Regions'
    ]
    
    # Add demand level
    product_summary['Demand Level'] = pd.qcut(
        product_summary['Total Units Ordered'], 
        q=3, 
        labels=['Low', 'Medium', 'High']
    )
    
    # Sort options
    sort_col1, sort_col2 = st.columns(2)
    
    with sort_col1:
        sort_by = st.selectbox(
            "Sort by",
            options=['Total Units Sold', 'Total Units Ordered', 'Avg Inventory', 'Avg Price'],
            index=0
        )
    
    with sort_col2:
        sort_order = st.selectbox(
            "Order",
            options=['Descending', 'Ascending'],
            index=0
        )
    
    ascending = sort_order == 'Ascending'
    product_summary = product_summary.sort_values(sort_by, ascending=ascending)
    
    # Display table
    st.dataframe(
        product_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Product ID": "Product",
            "Category": "Category",
            "Avg Inventory": st.column_config.NumberColumn("Avg Inventory", format="%.0f"),
            "Total Units Sold": st.column_config.NumberColumn("Total Sold", format="%,.0f"),
            "Total Units Ordered": st.column_config.NumberColumn("Total Ordered", format="%,.0f"),
            "Avg Price": st.column_config.NumberColumn("Avg Price", format="$%.2f"),
            "Avg Discount": st.column_config.NumberColumn("Avg Discount", format="%.1f%%"),
            "Stores": "No. Stores",
            "Regions": "Regions",
            "Demand Level": st.column_config.TextColumn("Demand")
        },
        height=400
    )
    
    st.markdown("---")
    
    # Product Performance Charts
    st.header("📈 Product Performance Analysis")
    
    chart_tab1, chart_tab2, chart_tab3 = st.tabs(["By Category", "By Store", "Price Analysis"])
    
    with chart_tab1:
        st.subheader("Product Performance by Category")
        
        category_stats = filtered_df.groupby('Category').agg({
            'Units Sold': 'sum',
            'Inventory Level': 'mean',
            'Price': 'mean'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_sales = px.bar(
                category_stats,
                x='Category',
                y='Units Sold',
                title="Total Sales by Category",
                color='Units Sold',
                color_continuous_scale='Blues',
                text='Units Sold'
            )
            fig_sales.update_traces(texttemplate='%{text:,}', textposition='outside')
            st.plotly_chart(fig_sales, use_container_width=True)
        
        with col2:
            fig_inv = px.bar(
                category_stats,
                x='Category',
                y='Inventory Level',
                title="Average Inventory by Category",
                color='Inventory Level',
                color_continuous_scale='Greens',
                text='Inventory Level'
            )
            fig_inv.update_traces(texttemplate='%{text:.0f}', textposition='outside')
            st.plotly_chart(fig_inv, use_container_width=True)
    
    with chart_tab2:
        st.subheader("Product Performance by Store")
        
        store_stats = filtered_df.groupby('Store ID').agg({
            'Units Sold': 'sum',
            'Product ID': 'nunique',
            'Inventory Level': 'mean'
        }).reset_index()
        store_stats.columns = ['Store ID', 'Total Sales', 'Unique Products', 'Avg Inventory']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_store_sales = px.bar(
                store_stats,
                x='Store ID',
                y='Total Sales',
                title="Total Sales by Store",
                color='Total Sales',
                color_continuous_scale='Purples',
                text='Total Sales'
            )
            fig_store_sales.update_traces(texttemplate='%{text:,}', textposition='outside')
            st.plotly_chart(fig_store_sales, use_container_width=True)
        
        with col2:
            fig_store_products = px.bar(
                store_stats,
                x='Store ID',
                y='Unique Products',
                title="Number of Products by Store",
                color='Unique Products',
                color_continuous_scale='Oranges',
                text='Unique Products'
            )
            fig_store_products.update_traces(texttemplate='%{text:.0f}', textposition='outside')
            st.plotly_chart(fig_store_products, use_container_width=True)
    
    with chart_tab3:
        st.subheader("Price Analysis")
        
        price_analysis = filtered_df.groupby('Category').agg({
            'Price': ['mean', 'min', 'max'],
            'Discount': 'mean',
            'Units Sold': 'sum'
        }).reset_index()
        price_analysis.columns = ['Category', 'Avg Price', 'Min Price', 'Max Price', 'Avg Discount', 'Total Sales']
        
        fig_price_range = px.scatter(
            price_analysis,
            x='Avg Price',
            y='Total Sales',
            size='Avg Discount',
            color='Category',
            hover_data=['Min Price', 'Max Price'],
            title="Price vs Sales Performance",
            labels={'Avg Price': 'Average Price ($)', 'Total Sales': 'Total Units Sold'}
        )
        st.plotly_chart(fig_price_range, use_container_width=True)
        
        st.dataframe(
            price_analysis,
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    
    # Detailed Product View
    st.header("🔎 Detailed Product View")
    
    selected_product = st.selectbox(
        "Select a product to view details",
        options=sorted(filtered_df['Product ID'].unique())
    )
    
    if selected_product:
        product_details = filtered_df[filtered_df['Product ID'] == selected_product]
        
        detail_col1, detail_col2 = st.columns(2)
        
        with detail_col1:
            st.subheader("Product Information")
            st.write(f"**Product ID**: {selected_product}")
            st.write(f"**Category**: {product_details['Category'].iloc[0]}")
            st.write(f"**Average Price**: ${product_details['Price'].mean():.2f}")
            st.write(f"**Average Discount**: {product_details['Discount'].mean():.1f}%")
            st.write(f"**Available in**: {product_details['Store ID'].nunique()} stores")
            st.write(f"**Regions**: {', '.join(product_details['Region'].unique())}")
        
        with detail_col2:
            st.subheader("Performance Metrics")
            st.write(f"**Total Units Sold**: {product_details['Units Sold'].sum():,}")
            st.write(f"**Total Units Ordered**: {product_details['Units Ordered'].sum():,}")
            st.write(f"**Average Inventory**: {product_details['Inventory Level'].mean():.0f}")
            st.write(f"**Total Revenue**: ${(product_details['Units Sold'] * product_details['Price'] * (1 - product_details['Discount']/100)).sum():,.2f}")
        
        # Product timeline
        st.subheader("Sales Timeline")
        product_timeline = product_details.groupby('Date').agg({
            'Units Sold': 'sum',
            'Inventory Level': 'mean',
            'Price': 'mean'
        }).reset_index().sort_values('Date')
        
        fig_timeline = px.line(
            product_timeline,
            x='Date',
            y='Units Sold',
            title=f"Sales Over Time for {selected_product}",
            markers=True
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Product details table
        st.subheader("All Records for This Product")
        st.dataframe(
            product_details[['Date', 'Store ID', 'Region', 'Inventory Level', 'Units Sold', 'Units Ordered', 'Price', 'Discount', 'Weather Condition', 'Seasonality']],
            use_container_width=True,
            hide_index=True
        )
