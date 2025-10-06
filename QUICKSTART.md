# 🚀 Quick Start Guide - India Economic Dashboard

This guide will get you up and running with the Economic Dashboard in 5 minutes!

## ⚡ One-Command Launch

### On Linux/Mac:
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

### On Windows:
```bash
python3 generate_csv_data.py
streamlit run dashboard.py
```

## 📋 Step-by-Step Setup

### Step 1: Install Dependencies (2 minutes)

```bash
# Install required Python packages
pip install pandas numpy matplotlib seaborn plotly streamlit

# Or use the requirements file
pip install -r requirements-dashboard.txt
```

### Step 2: Generate Data (30 seconds)

```bash
# Run the data generation script
python3 generate_csv_data.py
```

You should see: `All CSV files saved!`

### Step 3: Launch Dashboard (10 seconds)

```bash
# Start the Streamlit server
streamlit run dashboard.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## 🎯 First Time Usage

### 1. Explore the Sidebar
- **Select Dataset**: Choose from 11 economic indicators
- **Chart Type**: Try different visualization types
- **Date Range**: Filter data by time period
- **Filters**: Use context-specific filters (Region, State, etc.)

### 2. View Key Metrics
- See latest values, averages, and extremes at the top
- Green/red arrows show changes over time

### 3. Interactive Charts
- Hover over charts for detailed information
- Zoom in/out using the chart controls
- Pan across the timeline

### 4. Explore Tabs
- **Main Chart**: Primary visualization
- **Data Table**: View and download raw data
- **Statistics**: Detailed statistical analysis

### 5. Advanced Analysis
- **Correlation Analysis**: See how indicators relate
- **Comparative View**: Compare multiple indicators
- **Trend Analysis**: View moving averages and growth rates

## 📊 Example Workflows

### Analyzing GDP Growth
1. Select "GDP Growth Rate" from sidebar
2. Choose "Line Chart" visualization
3. Set date range to "Last 5 Years"
4. View the impact of COVID-19 in 2020
5. Check correlation with other indicators

### Comparing Inflation (Urban vs Rural)
1. Select "Consumer Price Index"
2. Keep both Urban and Rural selected in filters
3. Choose "Line Chart" to see trends
4. Use "Bar Chart" to compare specific periods
5. Download data for further analysis

### Tracking Digital Payment Growth
1. Select "Digital Payment Volume"
2. View exponential growth from 2016-2024
3. Check both Volume and Value metrics
4. Export chart for presentations

## 🎨 Customization Tips

### Change Color Themes
The dashboard uses Plotly's default theme, but you can modify colors in `dashboard.py`:

```python
# Look for color_continuous_scale parameters
color_continuous_scale='RdBu_r'  # Change to 'Viridis', 'Blues', etc.
```

### Adjust Chart Sizes
```python
# Find update_layout() calls and modify height
fig.update_layout(height=500)  # Change to desired height
```

### Add More Metrics
Edit the metrics section in `dashboard.py` to add custom calculations:

```python
col5, col6 = st.columns(2)
with col5:
    st.metric("Your Custom Metric", value="...")
```

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Install dependencies
```bash
pip install streamlit pandas plotly
```

### Issue: "FileNotFoundError: data/gdp_growth_rate.csv"
**Solution**: Generate CSV files
```bash
python3 generate_csv_data.py
```

### Issue: Dashboard shows blank charts
**Solution**: 
1. Check browser console (F12)
2. Clear Streamlit cache (press 'C' in dashboard)
3. Restart the server

### Issue: Port 8501 already in use
**Solution**: Use a different port
```bash
streamlit run dashboard.py --server.port 8502
```

## 📱 Accessing from Mobile

1. Find your computer's IP address:
   ```bash
   # On Mac/Linux
   ifconfig | grep "inet "
   
   # On Windows
   ipconfig
   ```

2. On mobile browser, navigate to:
   ```
   http://YOUR_IP_ADDRESS:8501
   ```

3. Ensure your phone is on the same network

## 🎓 Learning Resources

### Streamlit Basics
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)

### Plotly Charts
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [Plotly Tutorials](https://plotly.com/python/)

### Data Analysis
- [Pandas Tutorials](https://pandas.pydata.org/docs/getting_started/tutorials.html)
- [NumPy Basics](https://numpy.org/doc/stable/user/quickstart.html)

## 💡 Pro Tips

1. **Keyboard Shortcuts**
   - `R`: Rerun the app
   - `C`: Clear cache
   - `Ctrl+C` (in terminal): Stop server

2. **Performance**
   - The first load might be slower (data caching)
   - Subsequent loads are much faster
   - Use date filters to improve responsiveness

3. **Data Export**
   - Download filtered data as CSV from Data Table tab
   - Use browser's print to save charts as PDF

4. **Multi-User Access**
   - Multiple people can access the dashboard simultaneously
   - Each user gets their own session

5. **Auto-Reload**
   - Streamlit watches for file changes
   - Edit `dashboard.py` and it auto-reloads
   - Great for development and customization

## 🎯 Next Steps

1. ✅ Explore all 11 economic indicators
2. ✅ Try different chart types and filters
3. ✅ Use advanced analysis features
4. ✅ Download and analyze data
5. ✅ Customize visualizations
6. ✅ Share with colleagues

## 📞 Need Help?

- Check `DASHBOARD_README.md` for detailed documentation
- Review the troubleshooting section above
- Open an issue on GitHub
- Email support team

---

**Happy Analyzing! 📊🇮🇳**
