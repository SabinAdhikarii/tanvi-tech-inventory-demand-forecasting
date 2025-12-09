# web_app/pages/dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show_dashboard(df):
    """Display the main dashboard with visualizations"""
    
    if df is None:
        st.error("No data available. Please check your data file.")
        return
    
    # Title
    st.markdown('<div class="main-header"> Dashboard Overview</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <h4>Welcome to Your Retail Analytics Dashboard!</h4>
        <p>This dashboard provides comprehensive insights into your retail business performance, 
        sales trends, inventory levels, and demand patterns. Use the sidebar to make predictions 
        and explore the charts below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for predictions
    st.sidebar.header(" Demand Prediction Tool")
    st.sidebar.markdown("**Enter product details to predict demand:**")
    
    category = st.sidebar.selectbox("Product Category", ["Electronics", "Clothing", "Groceries", "Toys", "Furniture"])
    price = st.sidebar.slider("Price ($)", 10.0, 100.0, 55.0)
    discount = st.sidebar.slider("Discount (%)", 0, 20, 10)
    inventory = st.sidebar.slider("Current Inventory Level", 50, 500, 200)
    region = st.sidebar.selectbox("Region", ["North", "South", "East", "West"])
    weather = st.sidebar.selectbox("Weather Condition", ["Sunny", "Rainy", "Cloudy", "Snowy"])
    holiday = st.sidebar.checkbox("Holiday/Promotion Period")
    season = st.sidebar.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])
    
    # Prediction function
    def predict_demand():
        score = 0
        factors = []
        if price < 40: 
            score += 2
            factors.append("✓ Competitive pricing attracts more customers")
        if discount > 15: 
            score += 2
            factors.append("✓ Strong discount driving high demand")
        if holiday: 
            score += 1
            factors.append("✓ Holiday/promotion period increases sales")
        if category in ["Electronics", "Toys"]: 
            score += 1
            factors.append("✓ Popular category with high demand")
        if inventory < 150:
            score += 1
            factors.append("✓ Low inventory may indicate high demand")
        
        if score >= 4: 
            return "HIGH", "#000000", "🟢", factors
        elif score >= 2: 
            return "MEDIUM", "#000000", "🟡", factors
        else: 
            return "LOW", "#000000", "🔴", factors
    
    # Predict button
    if st.sidebar.button(" Predict Demand", use_container_width=True):
        demand, color, emoji, factors = predict_demand()
        st.sidebar.markdown(f"""
        <div style='padding: 15px; border-radius: 10px; background-color: {color}; margin-top: 20px;'>
            <h3 style='text-align: center; margin: 0;'>{emoji} Predicted Demand: {demand}</h3>
        </div>
        """, unsafe_allow_html=True)
        if factors:
            st.sidebar.markdown("**Key Factors:**")
            for factor in factors:
                st.sidebar.markdown(f"• {factor}")
    
    st.sidebar.markdown("---")
    st.sidebar.info(" **Tip:** Lower prices and higher discounts typically increase demand.")
    
    # Key Metrics Section
    st.header(" Key Business Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df['Units Sold'].sum()
        st.metric("Total Units Sold", f"{total_sales:,}", help="Total number of products sold")
    
    with col2:
        avg_daily_sales = df.groupby('Date')['Units Sold'].sum().mean()
        st.metric("Average Daily Sales", f"{avg_daily_sales:,.0f}", help="Average units sold per day")
    
    with col3:
        total_revenue = (df['Units Sold'] * df['Price'] * (1 - df['Discount']/100)).sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}", help="Total revenue (after discounts)")
    
    with col4:
        unique_products = df['Product ID'].nunique()
        st.metric("Total Products", f"{unique_products}", help="Number of unique products")
    
    st.markdown("---")
    
    # Visualization Section
    st.header(" Data Visualizations & Insights")
    
    # Tabs for different visualization categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs([" Sales Overview", " Store & Region", " Time Trends", " Inventory", " Demand Patterns"])
    
    with tab1:
        st.subheader("Sales Distribution by Category")
        category_sales = df.groupby('Category')['Units Sold'].sum().reset_index()
        fig_pie = px.pie(
            category_sales, 
            values='Units Sold', 
            names='Category',
            title="Total Sales by Product Category",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("""
        <div class="info-box">
            <strong> What this tells you:</strong> This shows which product categories contribute most to your total sales. 
            Use this to identify best-performing categories and allocate inventory accordingly.
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Average Sales per Category")
        category_avg = df.groupby('Category')['Units Sold'].mean().reset_index().sort_values('Units Sold', ascending=False)
        fig_bar = px.bar(
            category_avg,
            x='Category',
            y='Units Sold',
            title="Average Units Sold per Category",
            color='Units Sold',
            color_continuous_scale='Blues',
            text='Units Sold'
        )
        fig_bar.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        st.subheader("Sales Performance by Region")
        region_sales = df.groupby('Region')['Units Sold'].sum().reset_index()
        fig_region_pie = px.pie(
            region_sales,
            values='Units Sold',
            names='Region',
            title="Sales Distribution Across Regions",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_region_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_region_pie, use_container_width=True)
        
        st.subheader("Store Performance Comparison")
        store_sales = df.groupby('Store ID')['Units Sold'].sum().reset_index().sort_values('Units Sold', ascending=False)
        fig_store = px.bar(
            store_sales,
            x='Store ID',
            y='Units Sold',
            title="Total Sales by Store",
            color='Units Sold',
            color_continuous_scale='Greens',
            text='Units Sold'
        )
        fig_store.update_traces(texttemplate='%{text:,}', textposition='outside')
        st.plotly_chart(fig_store, use_container_width=True)
        
        st.subheader("Sales Heatmap: Region vs Category")
        region_category = df.groupby(['Region', 'Category'])['Units Sold'].sum().reset_index()
        region_category_pivot = region_category.pivot(index='Category', columns='Region', values='Units Sold')
        fig_heatmap = px.imshow(
            region_category_pivot,
            labels=dict(x="Region", y="Category", color="Units Sold"),
            title="Which categories sell best in which regions?",
            color_continuous_scale='YlOrRd',
            aspect="auto"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab3:
        st.subheader("Sales Trends Over Time")
        daily_sales = df.groupby('Date')['Units Sold'].sum().reset_index()
        fig_line = px.line(
            daily_sales,
            x='Date',
            y='Units Sold',
            title="Daily Sales Trend Over Time",
            markers=True
        )
        fig_line.update_traces(line_color='#1f77b4', line_width=2)
        st.plotly_chart(fig_line, use_container_width=True)
        
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        monthly_sales = df.groupby('Month')['Units Sold'].sum().reset_index()
        fig_monthly = px.bar(
            monthly_sales,
            x='Month',
            y='Units Sold',
            title="Monthly Sales Comparison",
            color='Units Sold',
            color_continuous_scale='Viridis',
            text='Units Sold'
        )
        fig_monthly.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_monthly.update_xaxes(tickangle=45)
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        st.subheader("Seasonal Sales Patterns")
        seasonal_sales = df.groupby('Seasonality')['Units Sold'].sum().reset_index()
        fig_seasonal = px.bar(
            seasonal_sales,
            x='Seasonality',
            y='Units Sold',
            title="Total Sales by Season",
            color='Seasonality',
            color_discrete_map={
                'Spring': '#90EE90',
                'Summer': '#FFD700',
                'Autumn': '#FF8C00',
                'Winter': '#87CEEB'
            },
            text='Units Sold'
        )
        fig_seasonal.update_traces(texttemplate='%{text:,}', textposition='outside')
        st.plotly_chart(fig_seasonal, use_container_width=True)
    
    with tab4:
        st.subheader("Inventory Level Analysis")
        fig_inv_hist = px.histogram(
            df,
            x='Inventory Level',
            nbins=30,
            title="Distribution of Inventory Levels",
            color_discrete_sequence=['#FF6B6B']
        )
        st.plotly_chart(fig_inv_hist, use_container_width=True)
        
        st.subheader("Inventory Level vs Sales Relationship")
        sample_df = df.sample(min(5000, len(df)))
        fig_scatter = px.scatter(
            sample_df,
            x='Inventory Level',
            y='Units Sold',
            color='Category',
            size='Price',
            hover_data=['Product ID', 'Discount'],
            title="How does inventory level relate to sales?",
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab5:
        st.subheader("Demand Level Distribution")
        df['Demand_Level'] = pd.qcut(df['Units Ordered'], q=3, labels=['Low', 'Medium', 'High'])
        demand_dist = df['Demand_Level'].value_counts().reset_index()
        demand_dist.columns = ['Demand Level', 'Count']
        
        fig_demand_pie = px.pie(
            demand_dist,
            values='Count',
            names='Demand Level',
            title="Distribution of Demand Levels",
            color='Demand Level',
            color_discrete_map={
                'Low': '#f8d7da',
                'Medium': '#fff3cd',
                'High': '#d4edda'
            }
        )
        fig_demand_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_demand_pie, use_container_width=True)
        
        st.subheader("Demand Levels by Category")
        demand_category = pd.crosstab(df['Category'], df['Demand_Level'])
        fig_demand_cat = px.bar(
            demand_category.reset_index().melt(id_vars='Category', var_name='Demand Level', value_name='Count'),
            x='Category',
            y='Count',
            color='Demand Level',
            title="Demand Level Distribution Across Categories",
            color_discrete_map={
                'Low': '#f8d7da',
                'Medium': '#fff3cd',
                'High': '#d4edda'
            },
            barmode='group'
        )
        st.plotly_chart(fig_demand_cat, use_container_width=True)
    
    # Summary Insights
    st.markdown("---")
    st.header(" Key Business Insights")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.subheader(" Top Performing Categories")
        top_categories = df.groupby('Category')['Units Sold'].sum().sort_values(ascending=False).head(3)
        for i, (cat, sales) in enumerate(top_categories.items(), 1):
            st.write(f"{i}. **{cat}**: {sales:,} units sold")
        
        st.subheader(" Best Performing Regions")
        top_regions = df.groupby('Region')['Units Sold'].sum().sort_values(ascending=False)
        for i, (region, sales) in enumerate(top_regions.items(), 1):
            st.write(f"{i}. **{region}**: {sales:,} units sold")
    
    with insight_col2:
        st.subheader(" Seasonal Insights")
        seasonal_avg = df.groupby('Seasonality')['Units Sold'].mean()
        best_season = seasonal_avg.idxmax()
        worst_season = seasonal_avg.idxmin()
        st.write(f"**Best Season**: {best_season} (Avg: {seasonal_avg[best_season]:.0f} units/day)")
        st.write(f"**Slowest Season**: {worst_season} (Avg: {seasonal_avg[worst_season]:.0f} units/day)")
        
        st.subheader(" Pricing Insights")
        avg_price = df['Price'].mean()
        avg_discount = df['Discount'].mean()
        st.write(f"**Average Price**: ${avg_price:.2f}")
        st.write(f"**Average Discount**: {avg_discount:.1f}%")
        st.write(f"**Products with Discount**: {(df['Discount'] > 0).sum() / len(df) * 100:.1f}%")