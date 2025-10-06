"""
Economic Data Dashboard - Interactive Visualization Platform
Built with Streamlit and Plotly for India's Economic Indicators
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import sys
sys.path.append('.')
from backend.data_processor import EconomicDataProcessor

# Page configuration
st.set_page_config(
    page_title="India Economic Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    h1 {
        color: #1f77b4;
        font-weight: 700;
        margin-bottom: 10px;
    }
    h2 {
        color: #ff7f0e;
        font-weight: 600;
        margin-top: 20px;
    }
    h3 {
        color: #2ca02c;
        margin-top: 15px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize data processor
@st.cache_resource
def load_data_processor():
    """Load and cache the data processor"""
    return EconomicDataProcessor()

processor = load_data_processor()

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Flag_of_India.svg/200px-Flag_of_India.svg.png", 
             width=100)
    st.title("🇮🇳 India Economic Dashboard")
    st.markdown("---")
    
    # Dataset selection
    st.subheader("📈 Select Dataset")
    dataset_options = {
        "GDP Growth Rate": "gdp",
        "Consumer Price Index": "cpi",
        "GST Collections": "gst",
        "Unemployment Rate": "unemployment",
        "Foreign Exchange Reserves": "forex",
        "Index of Industrial Production": "iip",
        "Repo Rate": "repo_rate",
        "Trade Balance": "trade",
        "Financial Inclusion Index": "financial_inclusion",
        "Digital Payment Volume": "digital_payment",
        "Composite Leading Indicator": "cli"
    }
    
    selected_dataset_name = st.selectbox(
        "Choose an indicator:",
        list(dataset_options.keys()),
        index=0
    )
    selected_dataset = dataset_options[selected_dataset_name]
    
    st.markdown("---")
    
    # Chart type selection
    st.subheader("📊 Visualization Type")
    chart_type = st.radio(
        "Select chart type:",
        ["Line Chart", "Area Chart", "Bar Chart", "Scatter Plot"],
        index=0
    )
    
    st.markdown("---")
    
    # Date range filter
    st.subheader("📅 Date Range")
    date_filter = st.select_slider(
        "Select time period:",
        options=["All Time", "Last 5 Years", "Last 3 Years", "Last Year"],
        value="All Time"
    )
    
    st.markdown("---")
    
    # Additional filters based on dataset
    st.subheader("🔍 Filters")
    region_filter = None
    state_filter = None
    payment_mode_filter = None
    
    if selected_dataset == 'cpi':
        region_filter = st.multiselect(
            "Select Region:",
            ["Urban", "Rural"],
            default=["Urban", "Rural"]
        )
    
    if selected_dataset == 'unemployment':
        df_unemp = processor.get_dataset('unemployment')
        states = df_unemp['State'].unique().tolist()
        state_filter = st.multiselect(
            "Select State:",
            states,
            default=["India"] if "India" in states else states[:1]
        )
    
    if selected_dataset == 'digital_payment':
        df_digi = processor.get_dataset('digital_payment')
        modes = df_digi['Payment_Mode'].unique().tolist()
        payment_mode_filter = st.multiselect(
            "Select Payment Mode:",
            modes,
            default=modes
        )
    
    st.markdown("---")
    st.info("💡 **Tip**: Hover over charts for detailed information and use controls to zoom and pan.")

# Main content
st.title(f"📊 {selected_dataset_name} Analysis")
st.markdown(f"*Comprehensive analysis and visualization of India's {selected_dataset_name.lower()}*")

# Load dataset
df = processor.get_dataset(selected_dataset)

# Apply date filter
if date_filter != "All Time":
    end_date = df['Date'].max()
    if date_filter == "Last Year":
        start_date = end_date - timedelta(days=365)
    elif date_filter == "Last 3 Years":
        start_date = end_date - timedelta(days=1095)
    else:  # Last 5 Years
        start_date = end_date - timedelta(days=1825)
    df = df[df['Date'] >= start_date]

# Apply additional filters
if selected_dataset == 'cpi' and region_filter:
    df = df[df['Region'].isin(region_filter)]

if selected_dataset == 'unemployment' and state_filter:
    df = df[df['State'].isin(state_filter)]

if selected_dataset == 'digital_payment' and payment_mode_filter:
    df = df[df['Payment_Mode'].isin(payment_mode_filter)]

# Display metrics
st.markdown("### 📈 Key Metrics")

# Determine the main metric column
metric_columns = {
    'gdp': 'GDP_Growth_Percent',
    'cpi': 'Inflation_Rate',
    'gst': 'GST_Collections_Cr',
    'unemployment': 'Unemployment_Rate',
    'forex': 'Forex_Reserves_USD_Bn',
    'iip': 'IIP_YOY_Growth',
    'repo_rate': 'Repo_Rate_Percent',
    'trade': 'Trade_Balance_USD_Bn',
    'financial_inclusion': 'FI_Index',
    'digital_payment': 'Volume_Mn',
    'cli': 'CLI_Value'
}

main_column = metric_columns.get(selected_dataset)

if main_column and main_column in df.columns:
    # Calculate statistics
    stats = processor.calculate_statistics(df, main_column)
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Latest Value",
            value=f"{stats.get('latest', 0):.2f}",
            delta=f"{stats.get('change', 0):.2f}" if 'change' in stats else None
        )
    
    with col2:
        st.metric(
            label="Average",
            value=f"{stats.get('mean', 0):.2f}"
        )
    
    with col3:
        st.metric(
            label="Maximum",
            value=f"{stats.get('max', 0):.2f}"
        )
    
    with col4:
        st.metric(
            label="Minimum",
            value=f"{stats.get('min', 0):.2f}"
        )

st.markdown("---")

# Create visualizations
st.markdown("### 📊 Interactive Visualization")

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["📈 Main Chart", "📊 Data Table", "📉 Statistics"])

with tab1:
    if not df.empty:
        # Create the appropriate chart based on dataset and selection
        if selected_dataset == 'gdp':
            if chart_type == "Line Chart":
                fig = px.line(df, x='Date', y='GDP_Growth_Percent',
                            title='GDP Growth Rate Over Time',
                            labels={'GDP_Growth_Percent': 'Growth Rate (%)', 'Date': 'Date'})
            elif chart_type == "Area Chart":
                fig = px.area(df, x='Date', y='GDP_Growth_Percent',
                            title='GDP Growth Rate Over Time',
                            labels={'GDP_Growth_Percent': 'Growth Rate (%)', 'Date': 'Date'})
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x='Date', y='GDP_Growth_Percent',
                           title='GDP Growth Rate Over Time',
                           labels={'GDP_Growth_Percent': 'Growth Rate (%)', 'Date': 'Date'})
            else:
                fig = px.scatter(df, x='Date', y='GDP_Growth_Percent',
                               title='GDP Growth Rate Over Time',
                               labels={'GDP_Growth_Percent': 'Growth Rate (%)', 'Date': 'Date'})
        
        elif selected_dataset == 'cpi':
            if chart_type == "Line Chart":
                fig = px.line(df, x='Date', y='Inflation_Rate', color='Region',
                            title='Inflation Rate by Region',
                            labels={'Inflation_Rate': 'Inflation Rate (%)', 'Date': 'Date'})
            elif chart_type == "Area Chart":
                fig = px.area(df, x='Date', y='CPI', color='Region',
                            title='Consumer Price Index by Region',
                            labels={'CPI': 'CPI', 'Date': 'Date'})
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x='Date', y='Inflation_Rate', color='Region',
                           title='Inflation Rate by Region',
                           labels={'Inflation_Rate': 'Inflation Rate (%)', 'Date': 'Date'},
                           barmode='group')
            else:
                fig = px.scatter(df, x='Date', y='Inflation_Rate', color='Region',
                               title='Inflation Rate by Region',
                               labels={'Inflation_Rate': 'Inflation Rate (%)', 'Date': 'Date'})
        
        elif selected_dataset == 'gst':
            if chart_type == "Line Chart":
                fig = px.line(df, x='Date', y='GST_Collections_Cr',
                            title='GST Collections Over Time',
                            labels={'GST_Collections_Cr': 'Collections (₹ Crores)', 'Date': 'Date'})
            elif chart_type == "Area Chart":
                fig = px.area(df, x='Date', y='GST_Collections_Cr',
                            title='GST Collections Over Time',
                            labels={'GST_Collections_Cr': 'Collections (₹ Crores)', 'Date': 'Date'})
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x='Date', y='GST_Collections_Cr',
                           title='GST Collections Over Time',
                           labels={'GST_Collections_Cr': 'Collections (₹ Crores)', 'Date': 'Date'})
            else:
                fig = px.scatter(df, x='Date', y='GST_Collections_Cr',
                               title='GST Collections Over Time',
                               labels={'GST_Collections_Cr': 'Collections (₹ Crores)', 'Date': 'Date'})
        
        elif selected_dataset == 'unemployment':
            if chart_type == "Line Chart":
                fig = px.line(df, x='Date', y='Unemployment_Rate', color='State',
                            title='Unemployment Rate by State',
                            labels={'Unemployment_Rate': 'Unemployment Rate (%)', 'Date': 'Date'})
            elif chart_type == "Area Chart":
                fig = px.area(df, x='Date', y='Unemployment_Rate', color='State',
                            title='Unemployment Rate by State',
                            labels={'Unemployment_Rate': 'Unemployment Rate (%)', 'Date': 'Date'})
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x='Date', y='Unemployment_Rate', color='State',
                           title='Unemployment Rate by State',
                           labels={'Unemployment_Rate': 'Unemployment Rate (%)', 'Date': 'Date'},
                           barmode='group')
            else:
                fig = px.scatter(df, x='Date', y='Unemployment_Rate', color='State',
                               title='Unemployment Rate by State',
                               labels={'Unemployment_Rate': 'Unemployment Rate (%)', 'Date': 'Date'})
        
        elif selected_dataset == 'forex':
            if chart_type == "Line Chart":
                fig = px.line(df, x='Date', y='Forex_Reserves_USD_Bn',
                            title='Foreign Exchange Reserves Over Time',
                            labels={'Forex_Reserves_USD_Bn': 'Reserves (USD Billion)', 'Date': 'Date'})
            elif chart_type == "Area Chart":
                fig = px.area(df, x='Date', y='Forex_Reserves_USD_Bn',
                            title='Foreign Exchange Reserves Over Time',
                            labels={'Forex_Reserves_USD_Bn': 'Reserves (USD Billion)', 'Date': 'Date'})
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x='Date', y='Forex_Reserves_USD_Bn',
                           title='Foreign Exchange Reserves Over Time',
                           labels={'Forex_Reserves_USD_Bn': 'Reserves (USD Billion)', 'Date': 'Date'})
            else:
                fig = px.scatter(df, x='Date', y='Forex_Reserves_USD_Bn',
                               title='Foreign Exchange Reserves Over Time',
                               labels={'Forex_Reserves_USD_Bn': 'Reserves (USD Billion)', 'Date': 'Date'})
        
        elif selected_dataset == 'iip':
            if chart_type == "Line Chart":
                fig = px.line(df, x='Date', y='IIP_YOY_Growth',
                            title='Index of Industrial Production Growth',
                            labels={'IIP_YOY_Growth': 'YoY Growth (%)', 'Date': 'Date'})
            elif chart_type == "Area Chart":
                fig = px.area(df, x='Date', y='IIP_YOY_Growth',
                            title='Index of Industrial Production Growth',
                            labels={'IIP_YOY_Growth': 'YoY Growth (%)', 'Date': 'Date'})
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x='Date', y='IIP_YOY_Growth',
                           title='Index of Industrial Production Growth',
                           labels={'IIP_YOY_Growth': 'YoY Growth (%)', 'Date': 'Date'})
            else:
                fig = px.scatter(df, x='Date', y='IIP_YOY_Growth',
                               title='Index of Industrial Production Growth',
                               labels={'IIP_YOY_Growth': 'YoY Growth (%)', 'Date': 'Date'})
        
        elif selected_dataset == 'repo_rate':
            if chart_type == "Line Chart":
                fig = px.line(df, x='Date', y='Repo_Rate_Percent',
                            title='Repo Rate Over Time',
                            labels={'Repo_Rate_Percent': 'Repo Rate (%)', 'Date': 'Date'})
            elif chart_type == "Area Chart":
                fig = px.area(df, x='Date', y='Repo_Rate_Percent',
                            title='Repo Rate Over Time',
                            labels={'Repo_Rate_Percent': 'Repo Rate (%)', 'Date': 'Date'})
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x='Date', y='Repo_Rate_Percent',
                           title='Repo Rate Over Time',
                           labels={'Repo_Rate_Percent': 'Repo Rate (%)', 'Date': 'Date'})
            else:
                fig = px.scatter(df, x='Date', y='Repo_Rate_Percent',
                               title='Repo Rate Over Time',
                               labels={'Repo_Rate_Percent': 'Repo Rate (%)', 'Date': 'Date'})
        
        elif selected_dataset == 'trade':
            # Special visualization for trade balance
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Scatter(x=df['Date'], y=df['Exports_USD_Bn'], 
                          name="Exports", mode='lines+markers'),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=df['Date'], y=df['Imports_USD_Bn'], 
                          name="Imports", mode='lines+markers'),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Bar(x=df['Date'], y=df['Trade_Balance_USD_Bn'], 
                      name="Trade Balance", opacity=0.6),
                secondary_y=True,
            )
            
            fig.update_xaxes(title_text="Date")
            fig.update_yaxes(title_text="Exports/Imports (USD Bn)", secondary_y=False)
            fig.update_yaxes(title_text="Trade Balance (USD Bn)", secondary_y=True)
            fig.update_layout(title_text="Trade Balance: Exports vs Imports")
        
        elif selected_dataset == 'financial_inclusion':
            if chart_type == "Line Chart":
                fig = px.line(df, x='Date', y='FI_Index',
                            title='Financial Inclusion Index Over Time',
                            labels={'FI_Index': 'FI Index', 'Date': 'Date'})
            elif chart_type == "Area Chart":
                fig = px.area(df, x='Date', y='FI_Index',
                            title='Financial Inclusion Index Over Time',
                            labels={'FI_Index': 'FI Index', 'Date': 'Date'})
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x='Date', y='FI_Index',
                           title='Financial Inclusion Index Over Time',
                           labels={'FI_Index': 'FI Index', 'Date': 'Date'})
            else:
                fig = px.scatter(df, x='Date', y='FI_Index',
                               title='Financial Inclusion Index Over Time',
                               labels={'FI_Index': 'FI Index', 'Date': 'Date'})
        
        elif selected_dataset == 'digital_payment':
            # Special visualization for digital payments
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(x=df['Date'], y=df['Volume_Mn'], 
                      name="Volume (Million)", opacity=0.7),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=df['Date'], y=df['Value_Cr'], 
                          name="Value (₹ Crores)", mode='lines+markers', 
                          line=dict(width=3)),
                secondary_y=True,
            )
            
            fig.update_xaxes(title_text="Date")
            fig.update_yaxes(title_text="Volume (Million)", secondary_y=False)
            fig.update_yaxes(title_text="Value (₹ Crores)", secondary_y=True)
            fig.update_layout(title_text="Digital Payment Volume and Value")
        
        elif selected_dataset == 'cli':
            if chart_type == "Line Chart":
                fig = px.line(df, x='Date', y='CLI_Value',
                            title='Composite Leading Indicator Over Time',
                            labels={'CLI_Value': 'CLI Value', 'Date': 'Date'})
            elif chart_type == "Area Chart":
                fig = px.area(df, x='Date', y='CLI_Value',
                            title='Composite Leading Indicator Over Time',
                            labels={'CLI_Value': 'CLI Value', 'Date': 'Date'})
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x='Date', y='CLI_Value',
                           title='Composite Leading Indicator Over Time',
                           labels={'CLI_Value': 'CLI Value', 'Date': 'Date'})
            else:
                fig = px.scatter(df, x='Date', y='CLI_Value',
                               title='Composite Leading Indicator Over Time',
                               labels={'CLI_Value': 'CLI Value', 'Date': 'Date'})
        
        # Update layout for better appearance
        fig.update_layout(
            height=500,
            hovermode='x unified',
            template='plotly_white',
            font=dict(size=12),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

with tab2:
    st.markdown("#### 📋 Data Table")
    st.dataframe(df, use_container_width=True, height=400)
    
    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"{selected_dataset}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

with tab3:
    st.markdown("#### 📊 Statistical Summary")
    
    # Display detailed statistics
    if main_column and main_column in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Descriptive Statistics**")
            describe_df = df[main_column].describe().to_frame()
            describe_df.columns = ['Value']
            st.dataframe(describe_df, use_container_width=True)
        
        with col2:
            st.markdown("**Distribution**")
            fig_hist = px.histogram(df, x=main_column, nbins=20,
                                   title=f'Distribution of {selected_dataset_name}',
                                   labels={main_column: selected_dataset_name})
            fig_hist.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_hist, use_container_width=True)

# Additional Analysis Section
st.markdown("---")
st.markdown("### 🔬 Advanced Analysis")

analysis_tabs = st.tabs(["📈 Correlation Analysis", "🎯 Comparative View", "📊 Trend Analysis"])

with analysis_tabs[0]:
    st.markdown("#### Correlation Matrix")
    st.markdown("*Analyzing relationships between different economic indicators*")
    
    try:
        corr_matrix = processor.get_correlation_matrix()
        
        # Create heatmap
        fig_corr = px.imshow(corr_matrix,
                            text_auto='.2f',
                            aspect="auto",
                            color_continuous_scale='RdBu_r',
                            title='Correlation Between Economic Indicators')
        fig_corr.update_layout(height=500)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.info("💡 **Interpretation**: Values close to 1 indicate strong positive correlation, " 
               "values close to -1 indicate strong negative correlation.")
    except Exception as e:
        st.error(f"Error generating correlation matrix: {str(e)}")

with analysis_tabs[1]:
    st.markdown("#### Compare Multiple Indicators")
    
    # Multi-select for comparison
    compare_datasets = st.multiselect(
        "Select indicators to compare:",
        list(dataset_options.keys()),
        default=[selected_dataset_name]
    )
    
    if len(compare_datasets) > 1:
        fig_compare = go.Figure()
        
        for dataset_name in compare_datasets:
            ds = dataset_options[dataset_name]
            temp_df = processor.get_dataset(ds)
            col = metric_columns.get(ds)
            
            if col and col in temp_df.columns:
                # Normalize data for comparison
                normalized = (temp_df[col] - temp_df[col].mean()) / temp_df[col].std()
                fig_compare.add_trace(go.Scatter(
                    x=temp_df['Date'],
                    y=normalized,
                    name=dataset_name,
                    mode='lines'
                ))
        
        fig_compare.update_layout(
            title='Normalized Comparison of Economic Indicators',
            xaxis_title='Date',
            yaxis_title='Normalized Value (Standard Deviations)',
            height=500,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig_compare, use_container_width=True)
        st.info("💡 **Note**: Values are normalized (standardized) for fair comparison.")
    else:
        st.info("Please select at least 2 indicators to compare.")

with analysis_tabs[2]:
    st.markdown("#### Trend Analysis")
    
    if main_column and main_column in df.columns and len(df) > 1:
        # Calculate moving average
        window_size = st.slider("Moving Average Window (periods):", 2, 12, 4)
        
        df_trend = df.copy()
        df_trend['Moving_Avg'] = df_trend[main_column].rolling(window=window_size).mean()
        
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=df_trend['Date'],
            y=df_trend[main_column],
            name='Actual',
            mode='lines+markers',
            opacity=0.6
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=df_trend['Date'],
            y=df_trend['Moving_Avg'],
            name=f'{window_size}-Period Moving Average',
            mode='lines',
            line=dict(width=3, color='red')
        ))
        
        fig_trend.update_layout(
            title=f'Trend Analysis with Moving Average',
            xaxis_title='Date',
            yaxis_title=selected_dataset_name,
            height=500,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Growth rate analysis
        if len(df) > 1:
            st.markdown("#### Growth Rate Analysis")
            df_growth = df.copy()
            df_growth['YoY_Change'] = df_growth[main_column].pct_change() * 100
            
            fig_growth = px.bar(df_growth, x='Date', y='YoY_Change',
                              title='Period-over-Period Percentage Change',
                              labels={'YoY_Change': 'Change (%)', 'Date': 'Date'})
            fig_growth.update_layout(height=400)
            st.plotly_chart(fig_growth, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>India Economic Dashboard</strong> | Built with ❤️ using Streamlit & Plotly</p>
        <p>Data sources: RBI, MOSPI, CBIC, CMIE | Last updated: October 2024</p>
        <p style='font-size: 12px;'>⚠️ This dashboard uses synthetic data for demonstration purposes</p>
    </div>
    """, unsafe_allow_html=True)
