# 🇮🇳 India Economic Data Dashboard

A comprehensive, interactive dashboard for visualizing and analyzing India's key economic indicators. Built with **Streamlit** and **Plotly** for modern, responsive data visualization.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### 📊 11 Economic Indicators
- **GDP Growth Rate** - Quarterly GDP growth trends
- **Consumer Price Index (CPI)** - Inflation rates (Urban/Rural)
- **GST Collections** - Monthly GST revenue data
- **Unemployment Rate** - State-wise unemployment statistics
- **Foreign Exchange Reserves** - Forex reserves tracking
- **Index of Industrial Production (IIP)** - Industrial growth indicators
- **Repo Rate** - RBI policy rate changes
- **Trade Balance** - Exports, Imports, and Trade Balance
- **Financial Inclusion Index** - Banking penetration metrics
- **Digital Payment Volume** - UPI and digital transaction trends
- **Composite Leading Indicator (CLI)** - Economic forecasting index

### 🎨 Interactive Visualizations
- **Multiple Chart Types**: Line, Area, Bar, and Scatter plots
- **Dynamic Filtering**: Date range, region, state, and payment mode filters
- **Real-time Statistics**: Latest value, average, min/max with delta indicators
- **Advanced Analytics**:
  - Correlation heatmaps between indicators
  - Multi-indicator comparison with normalization
  - Trend analysis with moving averages
  - Growth rate calculations

### 🎯 User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Intuitive Interface**: Clean sidebar navigation and organized tabs
- **Data Export**: Download filtered data as CSV
- **Professional Styling**: Custom CSS with color-coded metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd /path/to/economic-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements-dashboard.txt
   ```

3. **Generate CSV data** (if not already done)
   ```bash
   python3 generate_csv_data.py
   ```

4. **Run the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

5. **Open in browser**
   - The dashboard will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in terminal

## 📁 Project Structure

```
economic-dashboard/
├── dashboard.py                    # Main Streamlit application
├── generate_csv_data.py           # CSV data generation script
├── requirements-dashboard.txt     # Python dependencies
├── DASHBOARD_README.md            # This file
├── backend/
│   └── data_processor.py         # Data processing and analytics module
└── data/                         # Generated CSV files
    ├── gdp_growth_rate.csv
    ├── consumer_price_index.csv
    ├── gst_collections.csv
    ├── unemployment_rate.csv
    ├── forex_reserves.csv
    ├── iip.csv
    ├── repo_rate.csv
    ├── trade_balance.csv
    ├── financial_inclusion_index.csv
    ├── digital_payment_volume.csv
    └── composite_leading_indicator.csv
```

## 📊 Dashboard Sections

### 1. Sidebar Controls
- **Dataset Selection**: Choose from 11 economic indicators
- **Visualization Type**: Select chart type (Line/Area/Bar/Scatter)
- **Date Range Filter**: All Time, Last 5/3/1 Years
- **Additional Filters**: Region, State, Payment Mode (context-specific)

### 2. Main Dashboard
- **Key Metrics Cards**: Latest value, average, maximum, minimum
- **Interactive Chart**: Main visualization with hover tooltips
- **Data Table**: Sortable, filterable data grid
- **Statistics**: Descriptive stats and distribution histogram

### 3. Advanced Analysis
- **Correlation Analysis**: Heatmap showing relationships between indicators
- **Comparative View**: Normalized comparison of multiple indicators
- **Trend Analysis**: Moving averages and growth rate calculations

## 🎯 Use Cases

### Economic Research
- Analyze GDP growth patterns during COVID-19
- Study correlation between inflation and unemployment
- Track digital payment adoption trends

### Policy Analysis
- Monitor impact of repo rate changes on economic indicators
- Analyze state-wise unemployment disparities
- Evaluate GST collection trends

### Financial Analysis
- Forex reserves management insights
- Trade balance and export-import trends
- Industrial production monitoring

### Education & Presentations
- Visual teaching tool for economics
- Data for research papers and reports
- Professional presentation charts

## 🛠️ Technical Details

### Backend Architecture
- **Data Processing**: Pandas-based ETL pipeline
- **Date Handling**: Automatic date parsing for quarters and months
- **Statistics**: Built-in statistical calculations and correlations
- **Caching**: Streamlit resource caching for performance

### Frontend Components
- **Streamlit**: Dashboard framework
- **Plotly**: Interactive charting library
- **Custom CSS**: Enhanced styling and responsiveness
- **Tab Navigation**: Organized content structure

### Data Pipeline
```
CSV Files → Data Processor → Pandas DataFrames → Streamlit Cache → Plotly Charts → Dashboard
```

## 📈 Data Details

### Data Timeframes
- **GDP**: Quarterly data (2010-2024)
- **CPI**: Annual data by region (2010-2024)
- **GST**: Monthly data (2017-2024)
- **Unemployment**: Monthly/State-wise (2012-2024)
- **Forex**: Monthly data (2010-2024)
- **IIP**: Monthly data (2010-2024)
- **Repo Rate**: Policy change dates (2010-2024)
- **Trade**: Monthly data (2010-2024)
- **FI Index**: Annual data (2011-2025)
- **Digital Payments**: Annual UPI data (2016-2024)
- **CLI**: Quarterly data (2010-2025)

### Data Quality
- All numeric columns properly typed (float/int)
- Date columns standardized to datetime format
- Missing values handled appropriately
- Outliers preserved for transparency

## 🎨 Customization

### Adding New Indicators
1. Add CSV file to `data/` directory
2. Create loader method in `data_processor.py`
3. Add dataset to dashboard selector
4. Configure visualization in `dashboard.py`

### Modifying Visualizations
- Edit chart configurations in respective sections
- Update color schemes in Plotly figure definitions
- Modify CSS in the `st.markdown()` style block

### Adjusting Filters
- Add new filter widgets in sidebar
- Implement filtering logic in main content area
- Update dataset queries accordingly

## 🔧 Troubleshooting

### Dashboard won't start
```bash
# Ensure all dependencies are installed
pip install --upgrade streamlit pandas plotly

# Check Python version
python3 --version  # Should be 3.8+

# Run with verbose logging
streamlit run dashboard.py --logger.level=debug
```

### Data not loading
```bash
# Regenerate CSV files
python3 generate_csv_data.py

# Verify files exist
ls -la data/
```

### Charts not displaying
- Clear Streamlit cache: Press 'C' in dashboard
- Check browser console for JavaScript errors
- Try different browser (Chrome/Firefox recommended)

## 📚 Resources

### Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Data Sources (Inspiration)
- Reserve Bank of India (RBI)
- Ministry of Statistics (MOSPI)
- Central Board of Indirect Taxes and Customs (CBIC)
- Centre for Monitoring Indian Economy (CMIE)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed description
2. **Suggest Features**: Share ideas for new indicators or visualizations
3. **Submit PRs**: Fork, create feature branch, and submit pull request
4. **Improve Docs**: Help enhance documentation and examples

## 📝 Future Enhancements

- [ ] Add forecasting models (ARIMA, Prophet)
- [ ] Implement real-time data updates via APIs
- [ ] Add export to PDF/PNG functionality
- [ ] Create custom indicator combinations
- [ ] Add state-wise map visualizations
- [ ] Implement user authentication
- [ ] Add data version control
- [ ] Create mobile app version

## ⚠️ Disclaimer

This dashboard uses **synthetic/sample data** for demonstration purposes. While the data patterns are inspired by actual Indian economic indicators, they should not be used for real economic analysis or decision-making.

For official economic data, please refer to:
- [Reserve Bank of India](https://www.rbi.org.in/)
- [Ministry of Statistics and Programme Implementation](https://mospi.gov.in/)
- [National Statistical Office](https://www.mospi.gov.in/web/mospi/home)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit Team** for the amazing dashboard framework
- **Plotly** for powerful visualization capabilities
- **Pandas** for robust data processing
- **Indian Government** for economic data inspiration

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Email: support@example.com
- Documentation: See this README

---

**Built with ❤️ for India's Economic Data Visualization**

*Last Updated: October 2024*
