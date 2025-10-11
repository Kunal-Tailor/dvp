# 🚀 Analytics Quick Start Guide

## Start in 3 Simple Steps

### Step 1: Start the Server
```bash
./run_analytics.sh
```
**OR**
```bash
python3 api_server.py
```

### Step 2: Open in Browser
Go to: **http://localhost:5000/analytics**

### Step 3: Explore!
✅ You're ready to analyze India's economic data!

---

## 📊 What You'll See

### Top Section - Overview
- **Total Indicators**: Number of economic metrics
- **Average Growth**: Overall economic growth
- **Time Span**: Years of historical data

### Correlation Matrix
- **Green cells**: Indicators move together (positive correlation)
- **Red cells**: Indicators move opposite (negative correlation)
- **Gray cells**: Weak or no relationship

### Multi-Indicator Comparison
- Click indicator buttons to add/remove
- Compares different metrics on the same scale
- Normalized for fair comparison

### Growth Trends
- Shows which indicators are growing fastest
- Green = positive growth
- Red = declining

### Category Distribution
- Pie chart of indicator categories
- Helps understand data composition

### Key Insights
- Automatically generated from your data
- Updates with "Refresh Insights" button

---

## 🎮 Quick Actions

| Button | What It Does |
|--------|-------------|
| **Export Data** | Download analytics as CSV file |
| **Refresh All** | Reload all charts with latest data |
| **Refresh Insights** | Update the insights section only |
| **Indicator Buttons** | Toggle indicators in comparison chart |

---

## 🔧 Troubleshooting

### Nothing loads?
1. Check server is running: Look for "Running on http://127.0.0.1:5000"
2. Press F12 in browser → Check Console tab for errors
3. Verify data files exist in `data/` folder

### Charts show errors?
1. Click "Refresh All" button
2. Clear browser cache (Ctrl+F5)
3. Restart the server

### Need help?
1. Read: `ANALYTICS_GUIDE.md` for detailed help
2. Run tests: `python3 test_analytics.py`
3. Check console logs

---

## 💡 Pro Tips

1. **Export regularly** - Save snapshots for comparison
2. **Check correlations** - Find hidden relationships
3. **Watch growth trends** - Identify opportunities
4. **Compare indicators** - Get complete picture
5. **Refresh often** - Stay updated

---

## 📱 Mobile Users

The analytics page works on mobile! Just use the same URL on your phone:
- Swipe to see full correlation matrix
- Tap to interact with charts
- All features work on touch screens

---

## 🎯 Common Use Cases

### Economic Research
1. Export correlation matrix
2. Analyze strongest relationships
3. Track trends over time

### Policy Analysis
1. Compare growth indicators
2. Check declining metrics
3. Identify areas needing attention

### Investment Decisions
1. Monitor forex and inflation
2. Track GDP vs unemployment
3. Export data for models

### Academic Projects
1. Use correlation data
2. Generate charts
3. Export for reports

---

## 🌟 Features at a Glance

✅ Real-time data loading  
✅ Interactive visualizations  
✅ One-click export to CSV  
✅ Auto-generated insights  
✅ Mobile responsive  
✅ Professional design  
✅ Error handling  
✅ Loading indicators  

---

## 📚 Learn More

- **Full Guide**: See `ANALYTICS_GUIDE.md`
- **Technical Details**: See `ANALYTICS_IMPROVEMENTS_SUMMARY.md`
- **Test API**: Run `python3 test_analytics.py`

---

## ⚡ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **F5** | Refresh page |
| **Ctrl+F5** | Hard refresh (clear cache) |
| **F12** | Open developer console |
| **Ctrl+S** | Save page (not recommended, use Export instead) |

---

## 🆘 Need Help?

**Can't start server?**
```bash
pip install -r requirements.txt
python3 api_server.py
```

**Port 5000 in use?**
Edit `api_server.py` line 411:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

**Missing data files?**
Ensure these files exist in `data/` folder:
- gdp_growth_rate.csv
- consumer_price_index.csv
- unemployment_rate.csv
- forex_reserves.csv
- iip.csv
- (and others)

---

## 🎉 You're All Set!

The analytics page is now your go-to tool for India economic analysis!

**Happy Analyzing! 📊🇮🇳**
