# Analytics Dashboard Guide

## Overview
The analytics page provides comprehensive analysis of India's economic indicators with real-time data, correlations, and insights.

## Features

### 1. **Overview Cards**
- **Total Indicators**: Shows the count of all economic metrics tracked
- **Average Growth Rate**: Displays average growth across all indicators
- **Time Span**: Shows years of historical data available

### 2. **Correlation Matrix**
- Interactive heatmap showing relationships between indicators
- Color-coded cells:
  - Green: Strong positive correlation (>0.7)
  - Red: Strong negative correlation (<-0.7)
  - Gray: Weak or no correlation
- Helps identify which indicators move together

### 3. **Multi-Indicator Comparison**
- Compare up to 5 indicators simultaneously
- Uses normalized z-score for fair comparison
- Interactive chart with toggleable indicators:
  - GDP Growth
  - Unemployment
  - Inflation (CPI)
  - Forex Reserves
  - IIP (Industrial Production)

### 4. **Growth Trends**
- Horizontal bar chart showing growth rates
- Automatically sorted by performance
- Green bars: Positive growth
- Red bars: Negative growth

### 5. **Category Distribution**
- Doughnut chart showing indicator distribution by category
- Categories include: Growth, Inflation, Employment, Trade, Finance, Digital, etc.

### 6. **Dynamic Insights**
Automatically generated insights including:
- Fastest growing indicator
- Slowest/declining indicators
- Strong correlations between indicators
- Overall economic health score

## How to Use

### Starting the Server

1. **Start the API Server**:
   ```bash
   python api_server.py
   ```
   This will start the server at http://localhost:5000

2. **Access the Analytics Page**:
   - Open your browser and go to: http://localhost:5000/analytics
   - Or navigate from the main dashboard using the navigation menu

### Interactive Features

#### Comparing Indicators
1. Click on indicator buttons in the "Multi-Indicator Comparison" section
2. Add or remove indicators by clicking their buttons
3. At least one indicator must remain selected

#### Refreshing Data
- Click "Refresh All" button in the header to reload all charts
- Click individual "Refresh Insights" button to update insights only

#### Exporting Data
- Click "Export Data" button to download analytics as CSV
- Includes:
  - Summary statistics for all indicators
  - Complete correlation matrix
  - Timestamped filename

## API Endpoints Used

The analytics page uses these API endpoints:

1. **`/api/indicators`** - Get list of all available indicators
2. **`/api/correlation`** - Get correlation matrix
3. **`/api/summary`** - Get summary statistics for all indicators
4. **`/api/data/<indicator>`** - Get time-series data for specific indicator

## Understanding the Data

### Correlation Values
- **1.0**: Perfect positive correlation (always move together)
- **0.7 to 1.0**: Strong positive correlation
- **0.4 to 0.7**: Moderate positive correlation
- **-0.4 to 0.4**: Weak or no correlation
- **-0.7 to -0.4**: Moderate negative correlation
- **-1.0 to -0.7**: Strong negative correlation
- **-1.0**: Perfect negative correlation (always move opposite)

### Normalization
The multi-indicator comparison uses z-score normalization:
- Mean = 0
- Standard deviation = 1
- Allows fair comparison of indicators with different scales

### Growth Rate
Calculated as: `((Latest Value - First Value) / First Value) × 100`

## Troubleshooting

### No Data Showing
1. Ensure the API server is running
2. Check browser console for errors (F12)
3. Verify data files exist in the `data/` directory

### Correlation Matrix Empty
- Requires at least 2 indicators with overlapping dates
- Check that CSV files have valid date columns

### Charts Not Loading
1. Clear browser cache
2. Refresh the page (Ctrl+F5 or Cmd+Shift+R)
3. Check network tab for failed API calls

## Best Practices

1. **Regular Refresh**: Click "Refresh All" to get latest data
2. **Export Regularly**: Save analytics data for historical comparison
3. **Analyze Trends**: Look for patterns in correlation changes over time
4. **Compare Related Indicators**: Group similar metrics (e.g., all growth indicators)

## Advanced Usage

### Custom Analysis
You can modify the analytics page to:
1. Add more indicators to comparison (edit `selectedIndicators` array)
2. Change correlation threshold colors
3. Add custom insight calculations
4. Modify chart types and visualizations

### Integration
The analytics API endpoints can be integrated with:
- Excel/Google Sheets (via CSV export)
- Other dashboards or applications
- Automated reporting systems
- Machine learning models

## Technical Details

**Frontend Technologies**:
- Chart.js 4.4.0 for visualizations
- Tailwind CSS for styling
- Font Awesome for icons
- Vanilla JavaScript for interactivity

**Backend**:
- Flask API server
- Pandas for data processing
- NumPy for calculations

**Data Format**:
- All dates in ISO format (YYYY-MM-DD)
- Numeric values with proper precision
- Missing values handled gracefully

## Support

For issues or questions:
1. Check the console logs
2. Verify API server is running
3. Ensure all data files are present
4. Review the main README.md for setup instructions
