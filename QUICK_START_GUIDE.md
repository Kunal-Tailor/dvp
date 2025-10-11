# 🚀 Quick Start Guide - IndianPulse with Country Comparison

## Welcome! 🎉

Your IndianPulse project now has **country comparison features** that let you compare India's economic performance with 10 major world economies!

---

## 📋 Table of Contents
1. [Installation](#installation)
2. [Running the Application](#running-the-application)
3. [Features Overview](#features-overview)
4. [Using Country Comparison](#using-country-comparison)
5. [API Usage](#api-usage)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Installation

### Option 1: Automated Setup (Recommended) ⚡

```bash
# Make the script executable
chmod +x run_with_comparison.sh

# Run it!
./run_with_comparison.sh
```

This script will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Generate comparison data
- ✅ Start the server

### Option 2: Manual Setup 🛠️

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. (Optional) Generate comparison data
python3 generate_comparison_data.py

# 3. Start the server
python3 api_server.py
```

---

## 🌐 Running the Application

Once the server is running, access these URLs:

| Page | URL | Description |
|------|-----|-------------|
| **🏠 Home** | http://localhost:5000 | Landing page |
| **📊 Dashboard** | http://localhost:5000/dashboard.html | Main economic indicators |
| **📈 Analytics** | http://localhost:5000/analytics.html | Correlation & trends |
| **🌍 Comparison** | http://localhost:5000/comparison.html | **NEW! Country comparison** |

---

## ✨ Features Overview

### 1. Main Dashboard (Existing)
- View 11 Indian economic indicators
- Interactive charts (Line, Bar, Area)
- Time range selection (3M, 1Y, 2Y, 5Y, All)
- Statistics cards (Latest, Average, Max, Min)
- Export functionality

### 2. Analytics (Existing)
- Correlation matrix
- Multi-indicator comparisons
- Advanced statistical analysis
- Relationship insights

### 3. 🆕 Country Comparison (NEW!)
**Compare India with 10 countries:**
- 🇮🇳 India (always selected)
- 🇨🇳 China
- 🇺🇸 United States
- 🇬🇧 United Kingdom
- 🇯🇵 Japan
- 🇩🇪 Germany
- 🇧🇷 Brazil
- 🇷🇺 Russia
- 🇿🇦 South Africa
- 🇦🇺 Australia

**8 Economic Indicators:**
- 📈 GDP Growth Rate
- 💰 Inflation Rate
- 👥 Unemployment Rate
- 🌐 Trade (% of GDP)
- 📦 Exports (% of GDP)
- 📥 Imports (% of GDP)
- 💼 Foreign Direct Investment
- 💵 GDP per Capita

**4 Visualization Types:**
- 📈 **Trend Chart**: Line chart showing 15 years of data
- 📊 **Bar Chart**: Compare latest values
- 🎯 **Radar Chart**: Multi-indicator analysis
- 🏆 **Rankings**: Medal-based country rankings

---

## 🌍 Using Country Comparison

### Step-by-Step Guide

#### 1. **Open the Comparison Page**
Navigate to: http://localhost:5000/comparison.html

#### 2. **Select Countries**
- Click on country badges to select/deselect
- India 🇮🇳 is always selected (you can't deselect it)
- You can select up to 10 countries

#### 3. **Choose an Indicator**
Click on one of the 8 indicator cards:
- GDP Growth
- Inflation
- Unemployment
- Trade
- Exports
- Imports
- FDI
- GDP per Capita

#### 4. **Analyze the Visualizations**

**Trend Chart (Top Left)**
- Shows historical trends from 2010-2024
- India's line is thicker and highlighted
- Hover to see exact values
- Compare growth patterns

**Bar Chart (Top Right)**
- Shows latest values for all countries
- Easy side-by-side comparison
- Color-coded by country

**Radar Chart (Bottom Left)**
- Shows multiple indicators at once
- Good for overall performance comparison
- Values normalized to 0-100 scale

**Rankings Table (Bottom Right)**
- Countries ranked by selected indicator
- 🥇🥈🥉 Medals for top 3
- India's row highlighted in orange

#### 5. **Check India's Performance**
At the bottom, see India's:
- Current value
- Global rank
- Change since 2010

---

## 🔌 API Usage

### Basic Examples

#### Get Available Countries
```bash
curl http://localhost:5000/api/comparison/countries
```

Response:
```json
[
  {
    "code": "IND",
    "name": "India",
    "flag": "🇮🇳",
    "color": "#FF9933"
  },
  ...
]
```

#### Get Comparison Data
```bash
curl "http://localhost:5000/api/comparison/gdp_growth?countries=IND,CHN,USA"
```

Response:
```json
{
  "years": [2010, 2011, ...],
  "countries": {
    "IND": {
      "name": "India",
      "values": [8.3, 6.6, ...],
      "latest": 7.8,
      "change": -0.5,
      "average": 6.5
    },
    ...
  },
  "india_position": 1,
  "rankings": [...]
}
```

#### Get Rankings Only
```bash
curl "http://localhost:5000/api/comparison/rankings/gdp_growth"
```

#### Multi-Indicator Comparison
```bash
curl "http://localhost:5000/api/comparison/multi-indicator?countries=IND,CHN,USA"
```

### API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/comparison/countries` | GET | List all countries |
| `/api/comparison/{indicator}` | GET | Get comparison data |
| `/api/comparison/relative/{indicator}` | GET | India as baseline (100) |
| `/api/comparison/multi-indicator` | GET | Multi-indicator data |
| `/api/comparison/rankings/{indicator}` | GET | Ranked list |
| `/api/comparison/export` | GET | Export CSV files |

---

## 📊 Example Use Cases

### Use Case 1: Compare BRICS Nations
```bash
# API Call
curl "http://localhost:5000/api/comparison/gdp_growth?countries=IND,CHN,BRA,RUS,ZAF"

# Or use the frontend:
# 1. Select: India, China, Brazil, Russia, South Africa
# 2. Choose: GDP Growth
# 3. Analyze trends
```

### Use Case 2: Analyze G7 Unemployment
```bash
# Select: India, USA, UK, Japan, Germany
# Choose: Unemployment
# Compare with radar chart
```

### Use Case 3: Trade Performance
```bash
# Select: India, China, USA
# Choose: Trade (% of GDP)
# View trend chart for historical patterns
```

---

## 🐛 Troubleshooting

### Problem: Server won't start

**Solution 1**: Check if port 5000 is already in use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port in api_server.py
```

**Solution 2**: Install dependencies
```bash
pip3 install -r requirements.txt
```

### Problem: Charts not showing

**Solution**: Check browser console (F12)
- Ensure Chart.js is loading
- Check for JavaScript errors
- Try refreshing the page

### Problem: No comparison data

**Solution**: Generate comparison data
```bash
python3 generate_comparison_data.py
```

### Problem: World Bank API not working

**Solution**: The system automatically falls back to synthetic data. Check:
- Internet connection
- Firewall settings
- Or just use the synthetic data (already generated)

### Problem: Import errors

**Solution**: Ensure you're in the right directory
```bash
# Navigate to project root
cd /path/to/IndianPulse

# Run from root
python3 api_server.py
```

---

## 📁 Project Structure

```
IndianPulse/
│
├── 🔧 Backend
│   ├── backend/
│   │   ├── country_comparison.py      # Comparison logic
│   │   └── data_processor.py          # Data processing
│   └── api_server.py                  # Flask API server
│
├── 🎨 Frontend
│   └── frontend/
│       ├── comparison.html            # NEW! Comparison page
│       ├── dashboard.html             # Main dashboard
│       ├── analytics.html             # Analytics page
│       └── index.html                 # Landing page
│
├── 📊 Data
│   └── data/
│       ├── comparisons/               # Comparison CSV files
│       ├── country_cache/             # API cache
│       └── [indicator].csv            # Indian data
│
├── 📝 Documentation
│   ├── QUICK_START_GUIDE.md          # This file
│   ├── COUNTRY_COMPARISON_README.md  # Detailed docs
│   ├── FEATURES_SUMMARY.md           # Features overview
│   └── README.md                      # Main README
│
└── 🚀 Scripts
    ├── run_with_comparison.sh         # Quick start script
    ├── generate_comparison_data.py    # Data generator
    └── requirements.txt               # Dependencies
```

---

## 🎯 Next Steps

### Explore the Features
1. ✅ Try different country combinations
2. ✅ Switch between indicators
3. ✅ Analyze trends and rankings
4. ✅ Use the API for custom analysis

### Customize
1. Add more countries
2. Add new indicators
3. Modify visualizations
4. Create custom reports

### Share
1. Deploy to a server
2. Share with colleagues
3. Use in presentations
4. Contribute improvements

---

## 📚 Additional Resources

- **Detailed Documentation**: See `COUNTRY_COMPARISON_README.md`
- **Features Summary**: See `FEATURES_SUMMARY.md`
- **API Reference**: Check API endpoints in docs
- **Data Sources**: World Bank, OECD (cached locally)

---

## 💡 Tips & Tricks

### Performance
- Data is cached locally for faster loading
- First load might be slower (fetching from API)
- Subsequent loads are much faster

### Best Practices
- Select 4-6 countries for best visualization
- Use radar chart for multi-indicator comparison
- Export data for offline analysis
- Check rankings for quick insights

### Keyboard Shortcuts
- `Ctrl + R`: Refresh page
- `F11`: Fullscreen mode
- `F12`: Developer console

---

## 🎉 You're All Set!

Your IndianPulse project is now ready with:
- ✅ 11 Indian economic indicators
- ✅ Advanced analytics
- ✅ **Country comparison with 10 countries**
- ✅ 8 economic indicators for comparison
- ✅ 4 advanced visualization types
- ✅ REST API for custom analysis

### Start Exploring!

```bash
# If server is not running:
./run_with_comparison.sh

# Then visit:
http://localhost:5000/comparison.html
```

---

**Happy Analyzing! 🇮🇳📊🌍**

*Made with ❤️ for India's economic data visualization*
