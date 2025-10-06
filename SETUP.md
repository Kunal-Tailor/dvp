# IndianPulse Setup Guide

## Quick Start

### 1. Start the Backend Server

**Option A: Using the startup script (Recommended)**
```bash
python start_backend.py
```

**Option B: Manual setup**
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start the server
cd backend
python app.py
```

### 2. Open the Frontend

1. Open `frontend/index.html` in your web browser
2. The dashboard will automatically connect to the backend API

## Features

✅ **Real Data Integration**: Uses actual economic data from `data.csv`  
✅ **3 Months & Yearly Views**: Time range options as requested  
✅ **6 Key Indicators**: GDP, CPI, GST, Unemployment, Forex, IIP  
✅ **Interactive Charts**: Line, Bar, Area, and Scatter charts  
✅ **Live Statistics**: Latest, Highest, Lowest, Average values  
✅ **Responsive Design**: Works on all devices  

## Available Indicators

| Indicator | Description | Unit | Source |
|-----------|-------------|------|--------|
| GDP Growth Rate | Quarterly GDP growth | % | RBI |
| Consumer Price Index | Monthly inflation rate | % | MOSPI |
| GST Collections | Monthly GST revenue | ₹ Lakh Cr | CBIC |
| Unemployment Rate | Monthly unemployment | % | CMIE |
| Foreign Exchange Reserves | Weekly forex reserves | Billion USD | RBI |
| Index of Industrial Production | Monthly IIP growth | % | MOSPI |

## Time Ranges

- **3M**: Last 3 quarters of data
- **1Y**: Last 1 year of data (default)
- **2Y**: Last 2 years of data
- **5Y**: Last 5 years of data

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/indicators` - List all indicators
- `GET /api/data/<indicator>?range=<time_range>` - Get indicator data
- `GET /api/stats/<indicator>` - Get indicator statistics

## Troubleshooting

**Backend not starting?**
- Check if Python 3.7+ is installed
- Ensure all dependencies are installed
- Check if port 5000 is available

**Frontend not loading data?**
- Ensure backend is running on http://localhost:5000
- Check browser console for errors
- Verify CORS is enabled (it is by default)

**Data not showing?**
- Check if `backend/data.csv` exists
- Verify CSV format is correct
- Check backend logs for errors
