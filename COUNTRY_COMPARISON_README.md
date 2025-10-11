# 🌍 Country Comparison Feature - IndianPulse

## Overview

The Country Comparison feature allows you to compare India's economic performance with major world economies including China, USA, UK, Japan, Germany, Brazil, Russia, South Africa, and Australia.

## 🚀 Features

### 1. **Multi-Country Comparison**
- Compare India with up to 10 major economies simultaneously
- View trends over 15+ years (2010-2024)
- Interactive country selection with flag badges

### 2. **Economic Indicators**
The comparison includes 8 key economic indicators:

| Indicator | Description | Unit |
|-----------|-------------|------|
| **GDP Growth** | Annual GDP growth rate | % |
| **Inflation** | Consumer price inflation | % |
| **Unemployment** | Total unemployment rate | % |
| **Trade** | Trade as % of GDP | % |
| **Exports** | Exports as % of GDP | % |
| **Imports** | Imports as % of GDP | % |
| **FDI** | Foreign Direct Investment | USD |
| **GDP per Capita** | GDP per capita | Current US$ |

### 3. **Advanced Visualizations**

#### 📈 Trend Comparison Chart
- Line chart showing historical trends (2010-2024)
- India's data is highlighted with a thicker line and filled area
- Interactive tooltips with detailed values

#### 📊 Bar Comparison Chart
- Compare latest values across all selected countries
- Color-coded bars for easy identification
- Sorted by value for quick analysis

#### 🎯 Radar Chart (Multi-Indicator Analysis)
- Compare multiple indicators simultaneously
- Spider/radar chart visualization
- Shows relative performance across different metrics

#### 🏆 Country Rankings
- Ranked list of countries by selected indicator
- 🥇🥈🥉 Medal icons for top 3 positions
- India's position is highlighted in orange

### 4. **India Performance Summary**
Special dashboard showing:
- Current value of selected indicator
- India's global rank
- Change since 2010
- Color-coded positive/negative changes

## 📡 API Endpoints

### Get Available Countries
```
GET /api/comparison/countries
```
Returns list of all available countries with their codes, names, flags, and colors.

### Get Comparison Data
```
GET /api/comparison/{indicator}?countries=IND,CHN,USA&start_year=2010&end_year=2024
```
Returns comparison data for specified indicator and countries.

**Parameters:**
- `indicator`: One of `gdp_growth`, `inflation`, `unemployment`, `trade_gdp`, `exports`, `imports`, `fdi`, `gdp_per_capita`
- `countries`: Comma-separated country codes (default: IND,CHN,USA,GBR,JPN,DEU)
- `start_year`: Starting year (default: 2010)
- `end_year`: Ending year (default: 2024)

### Get Relative Comparison
```
GET /api/comparison/relative/{indicator}?base=IND&countries=CHN,USA
```
Returns comparison data with India as baseline (100).

### Get Multi-Indicator Comparison
```
GET /api/comparison/multi-indicator?countries=IND,CHN,USA,GBR,JPN
```
Returns data for radar chart with multiple indicators.

### Get Country Rankings
```
GET /api/comparison/rankings/{indicator}?countries=IND,CHN,USA
```
Returns ranked list of countries for specified indicator.

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- Flask==2.3.3
- Flask-CORS==4.0.0
- pandas==2.0.3
- numpy==1.24.3
- requests==2.31.0

### 2. Generate Comparison Data (Optional)
```bash
python3 generate_comparison_data.py
```

This script generates synthetic comparison data for all indicators. The data is saved in `data/comparisons/` directory.

### 3. Start the Server
```bash
python3 api_server.py
```

The server will start on `http://localhost:5000`

### 4. Access the Comparison Page
Open your browser and navigate to:
```
http://localhost:5000/comparison.html
```

## 💻 Usage Guide

### Basic Usage

1. **Select Countries**: Click on country badges to select/deselect countries for comparison (India is always selected)

2. **Choose Indicator**: Click on one of the 8 indicator cards to view comparison for that metric

3. **Analyze Visualizations**: 
   - View trend chart for historical comparison
   - Check bar chart for latest values
   - Use radar chart for multi-indicator analysis
   - Review rankings to see India's position

### Advanced Features

#### Filter by Date Range
The comparison automatically shows data from 2010-2024. You can modify the date range by adjusting the API call parameters.

#### Export Data
You can export comparison data by calling:
```
GET /api/comparison/export
```

This generates CSV files for all indicators in the `data/comparisons/` directory.

#### Customize Colors
Each country has a predefined color scheme. You can modify colors in `backend/country_comparison.py`:
```python
COMPARISON_COUNTRIES = {
    'IND': {'name': 'India', 'flag': '🇮🇳', 'color': '#FF9933'},
    # Add or modify countries here
}
```

## 📊 Data Sources

The comparison module supports two data sources:

### 1. World Bank API (Recommended)
The module automatically fetches data from the World Bank API for accurate, real-time comparisons. Data is cached locally to improve performance.

### 2. Synthetic Data (Fallback)
If World Bank API is unavailable, the module generates realistic synthetic data based on historical patterns and trends.

## 🎨 Customization

### Adding New Countries
Edit `backend/country_comparison.py`:
```python
COMPARISON_COUNTRIES = {
    'IND': {'name': 'India', 'flag': '🇮🇳', 'color': '#FF9933'},
    'NEW': {'name': 'New Country', 'flag': '🆕', 'color': '#123456'},
}
```

### Adding New Indicators
1. Add World Bank indicator code in `backend/country_comparison.py`:
```python
WB_INDICATORS = {
    'new_indicator': 'WB.INDICATOR.CODE',
}
```

2. Update frontend indicator pills in `frontend/comparison.html`

3. Update synthetic data generator if needed

## 🔧 Troubleshooting

### Issue: No data showing
**Solution**: Run `python3 generate_comparison_data.py` to generate synthetic data

### Issue: World Bank API errors
**Solution**: The module automatically falls back to synthetic data. Check your internet connection or wait for API to become available.

### Issue: Charts not rendering
**Solution**: Ensure Chart.js is loaded. Check browser console for JavaScript errors.

### Issue: Countries not showing
**Solution**: Verify that `/api/comparison/countries` endpoint is accessible

## 📈 Performance Tips

1. **Caching**: Data from World Bank API is automatically cached in `data/country_cache/`
2. **Limit Countries**: Comparing fewer countries improves chart readability
3. **Date Range**: Smaller date ranges load faster

## 🤝 Contributing

To add more features to the comparison module:

1. Fork the repository
2. Create a feature branch
3. Add your enhancements to `backend/country_comparison.py` or `frontend/comparison.html`
4. Test thoroughly
5. Submit a pull request

## 📝 Example API Responses

### Get Comparison Data Response
```json
{
  "years": [2010, 2011, 2012, ...],
  "countries": {
    "IND": {
      "name": "India",
      "flag": "🇮🇳",
      "color": "#FF9933",
      "values": [8.5, 6.6, 5.2, ...],
      "latest": 7.8,
      "change": -0.7,
      "average": 6.5
    },
    "CHN": { ... }
  },
  "india_position": 2,
  "rankings": [
    {"country_code": "CHN", "country": "China", "value": 8.1},
    {"country_code": "IND", "country": "India", "value": 7.8}
  ]
}
```

## 🎯 Future Enhancements

Planned features for future releases:

- [ ] Real-time data updates from multiple sources
- [ ] Export charts as PDF
- [ ] Custom date range selector in UI
- [ ] Comparison templates (e.g., "BRICS countries", "G7 countries")
- [ ] Historical event annotations on charts
- [ ] Forecasting and projections
- [ ] Download comparison reports

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review API endpoints
3. Check browser console for errors
4. Verify backend is running
5. Create an issue on GitHub

## 🎉 Credits

- **Chart.js**: For beautiful, responsive charts
- **Tailwind CSS**: For modern, utility-first styling
- **World Bank API**: For international economic data
- **Font Awesome**: For icons
- **Flask**: For the backend API

---

**Built with ❤️ for comparing India's economic performance with the world**
