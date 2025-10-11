# 🚀 India Economic Dashboard - Run Instructions

## ✅ Quick Start (Recommended)

The easiest way to run the project:

```bash
# Make the script executable
chmod +x START_PROJECT.sh

# Run the startup script
./START_PROJECT.sh
```

That's it! The script will:
- ✅ Check Python installation
- ✅ Install required dependencies
- ✅ Verify data files
- ✅ Test data loading
- ✅ Start the Flask server

---

## 📋 Manual Setup

If you prefer to run manually, follow these steps:

### Step 1: Install Dependencies

```bash
pip3 install flask flask-cors pandas numpy --break-system-packages
```

Or use the requirements file:

```bash
pip3 install -r requirements.txt --break-system-packages
```

### Step 2: Verify Data Files

Make sure all CSV files are present in the `data/` directory:

```bash
ls -la data/*.csv
```

You should see 11 CSV files:
- `gdp_growth_rate.csv`
- `consumer_price_index.csv`
- `gst_collections.csv`
- `unemployment_rate.csv`
- `forex_reserves.csv`
- `iip.csv`
- `repo_rate.csv`
- `trade_balance.csv`
- `financial_inclusion_index.csv`
- `digital_payment_volume.csv`
- `composite_leading_indicator.csv`

### Step 3: Start the Server

```bash
python3 api_server.py
```

---

## 🌐 Accessing the Dashboard

Once the server is running, open your browser and navigate to:

### Main Pages:
- **Landing Page**: http://localhost:5000/
- **Dashboard**: http://localhost:5000/dashboard
- **Analytics**: http://localhost:5000/analytics

### API Endpoints (for testing):
- **Health Check**: http://localhost:5000/api/health
- **Indicators List**: http://localhost:5000/api/indicators
- **GDP Data**: http://localhost:5000/api/data/gdp
- **Correlation Matrix**: http://localhost:5000/api/correlation

---

## 🔍 Troubleshooting

### Problem: "Module not found" errors

**Solution**: Install missing dependencies
```bash
pip3 install flask flask-cors pandas numpy --break-system-packages
```

### Problem: "No such file or directory: data/..."

**Solution**: Make sure you're running the server from the project root directory
```bash
cd /workspace
python3 api_server.py
```

### Problem: Port 5000 already in use

**Solution**: Either stop the other process or change the port in `api_server.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Problem: Dashboard shows "Error loading data"

**Solution**: 
1. Open browser console (F12) to see the error
2. Check if the API server is running
3. Verify API endpoints work: http://localhost:5000/api/health
4. Check that data files are present in the `data/` directory

### Problem: Charts not displaying

**Solution**:
1. Make sure JavaScript is enabled in your browser
2. Check browser console for errors (F12)
3. Try refreshing the page (Ctrl+F5)
4. Clear browser cache

---

## 📊 Features Available

### Dashboard Page (`/dashboard`)
- ✅ 11 Economic Indicators
- ✅ Interactive Charts (Line, Bar, Area)
- ✅ Date Range Filtering (1Y, 3Y, 5Y, All Time)
- ✅ Statistics Cards (Latest, Average, Min, Max)
- ✅ Data Table with Export
- ✅ Responsive Design

### Analytics Page (`/analytics`)
- ✅ Correlation Matrix
- ✅ Multi-Indicator Comparison
- ✅ Growth Trends Chart
- ✅ Category Distribution
- ✅ Key Insights

---

## 🛠️ Technical Details

### Backend:
- **Framework**: Flask
- **Data Processing**: Pandas, NumPy
- **API**: RESTful endpoints with CORS enabled
- **Port**: 5000 (default)

### Frontend:
- **Framework**: Vanilla JavaScript (ES6+)
- **Styling**: Tailwind CSS
- **Charts**: Chart.js
- **Icons**: Font Awesome

### Data:
- **Format**: CSV files
- **Time Range**: 2010-2025
- **Indicators**: 11 key economic metrics
- **Frequency**: Monthly, Quarterly, Annual (varies by indicator)

---

## 📝 Project Structure

```
/workspace/
├── api_server.py              # Main Flask API server
├── backend/
│   ├── data_processor.py      # Data loading and processing
│   └── country_comparison.py  # Country comparison features
├── frontend/
│   ├── index.html             # Landing page
│   ├── dashboard.html         # Main dashboard (FIXED)
│   └── analytics.html         # Analytics page (FIXED)
├── data/                      # CSV data files
│   ├── gdp_growth_rate.csv
│   ├── consumer_price_index.csv
│   └── ... (9 more files)
├── START_PROJECT.sh           # Quick start script
└── RUN_INSTRUCTIONS.md        # This file

```

---

## ✨ What Was Fixed

### Dashboard.html Issues:
1. ✅ Fixed date range parsing (was failing on "1y", "3y", "5y" values)
2. ✅ Added better error handling for data loading
3. ✅ Improved date label formatting for charts
4. ✅ Added support for different date formats

### Analytics.html Issues:
1. ✅ Fixed normalization calculation (division by zero)
2. ✅ Added more data field mappings (volume, cpi, etc.)
3. ✅ Improved date label formatting for comparison charts
4. ✅ Better error handling

---

## 🎯 Next Steps

Once the dashboard is running:

1. **Explore Indicators**: Click on different indicators in the sidebar
2. **Change Date Ranges**: Use the dropdown to see different time periods
3. **Try Different Charts**: Switch between Line, Bar, and Area charts
4. **View Analytics**: Navigate to the Analytics page for deeper insights
5. **Export Data**: Use export buttons to download charts and CSV data

---

## 💡 Tips

- Use **Ctrl+F5** to hard refresh if you see cached data
- Check the **browser console** (F12) for debugging
- The **API health endpoint** shows server status
- All data is **loaded at startup** for better performance
- Charts are **interactive** - hover over data points for details

---

## 📞 Support

If you encounter any issues:

1. Check this troubleshooting guide
2. Review the browser console for errors
3. Verify all data files are present
4. Ensure dependencies are installed
5. Try the health check endpoint: http://localhost:5000/api/health

---

**Built with ❤️ for India's Economic Data Visualization**

*Last Updated: 2025-10-11*
