# IndianPulse - Economic Dashboard

A modern, lightweight economic dashboard for India that visualizes key economic indicators using HTML/CSS/JavaScript frontend and Flask backend.

## 🚀 Features

- **11 Key Economic Indicators**: GDP, CPI, GST, Unemployment, Forex Reserves, and more
- **Interactive Charts**: Line, Area, Bar, and Scatter charts using Chart.js
- **Real-time Data**: Time-series data with filtering and statistics
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark/Light Theme**: Toggle between themes with persistent storage
- **Export Functionality**: Export charts as PNG images
- **Modern UI**: Clean, accessible interface with smooth animations

## 🛠️ Tech Stack

### Frontend
- **HTML5** + **CSS3** (with CSS Variables)
- **Vanilla JavaScript** (ES2020+)
- **Chart.js** for data visualization
- **Responsive Design** with CSS Grid and Flexbox

### Backend
- **Python 3.10+**
- **Flask** web framework
- **Pandas** for data processing
- **NumPy** for numerical operations
- **Scikit-learn** for analytics
- **Matplotlib** for server-side chart generation

## 📁 Project Structure

```
indianpulse/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   ├── indicators.py      # Indicators API endpoints
│   │   └── charts.py          # Chart generation endpoints
│   ├── data/
│   │   ├── generator.py       # Sample data generator
│   │   └── sample_data/       # Generated CSV/JSON data
│   └── analytics/
│       ├── __init__.py
│       ├── processing.py      # Data processing functions
│       └── forecasting.py     # Forecasting algorithms
├── frontend/
│   ├── index.html             # Main HTML file
│   ├── css/
│   │   └── styles.css         # Main stylesheet
│   ├── js/
│   │   ├── api.js             # API client
│   │   ├── ui.js              # UI utilities
│   │   ├── charts.js          # Chart management
│   │   └── main.js            # Main application logic
│   └── assets/
│       └── logo.svg           # Application logo
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd indianpulse
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

5. **Generate sample data**
   ```bash
   python backend/data/generator.py --generate
   ```

6. **Start the Flask server**
   ```bash
   python backend/app.py
   ```

7. **Open the application**
   
   Navigate to `http://localhost:5000` in your web browser.

## 📊 Available Indicators

| Indicator | Description | Unit | Frequency | Source |
|-----------|-------------|------|-----------|--------|
| GDP Growth Rate | Quarterly GDP growth | % | Quarterly | RBI |
| Consumer Price Index | Monthly inflation rate | Index | Monthly | MOSPI |
| GST Collections | Monthly GST revenue | ₹ Crores | Monthly | CBIC |
| Unemployment Rate | Monthly unemployment | % | Monthly | CMIE |
| Foreign Exchange Reserves | Weekly forex reserves | USD Billion | Weekly | RBI |
| Index of Industrial Production | Monthly IIP growth | Index | Monthly | MOSPI |
| Repo Rate | Monthly repo rate | % | Monthly | RBI |
| Trade Balance | Monthly trade balance | USD Million | Monthly | DGCI&S |
| Financial Inclusion Index | Quarterly inclusion index | Index | Quarterly | RBI |
| Digital Payment Volume | Monthly payment volume | ₹ Crores | Monthly | NPCI |
| Composite Leading Indicator | Monthly leading indicator | Index | Monthly | OECD |

## 🎨 Features Overview

### Interactive Dashboard
- **Indicator Selection**: Choose from 11 economic indicators
- **Category Filtering**: Filter indicators by category (Growth, Inflation, Employment, etc.)
- **Time Range Selection**: View data for 1 year, 2 years, 5 years, or custom range
- **Chart Types**: Switch between Line, Area, Bar, and Scatter charts

### Data Visualization
- **Real-time Charts**: Interactive charts with hover tooltips
- **Statistics Cards**: Key metrics including latest value, average, min/max
- **Data Table**: Recent data points with change indicators
- **Export Functionality**: Download charts as PNG images

### User Experience
- **Responsive Design**: Optimized for all screen sizes
- **Theme Switching**: Toggle between light and dark themes
- **Keyboard Shortcuts**: Ctrl+T to toggle theme
- **Loading States**: Smooth loading indicators
- **Error Handling**: User-friendly error messages

## 🔧 API Endpoints

### Indicators
- `GET /api/v1/indicators/manifest` - Get all indicators metadata
- `GET /api/v1/indicators/{id}/series` - Get time series data
- `GET /api/v1/indicators/{id}/stats` - Get statistical summary
- `GET /api/v1/indicators/compare` - Compare multiple indicators

### Charts
- `GET /api/v1/charts/{id}.png` - Generate PNG chart
- `GET /api/v1/charts/export` - Export chart data

### Health
- `GET /api/v1/health` - Health check endpoint

## 🎯 Usage Examples

### View GDP Growth Rate
1. Select "GDP Growth Rate" from the indicator list
2. Choose "5 Years" time range
3. Select "Line" chart type
4. Click "Update Chart"

### Compare Multiple Indicators
1. Select indicators from different categories
2. Use the compare functionality (coming soon)
3. View trends across different economic sectors

### Export Chart
1. Load any indicator data
2. Click the "Export" button
3. Download as PNG image

## 🛠️ Development

### Running in Development Mode

```bash
# Start Flask with debug mode
export FLASK_DEBUG=True
python backend/app.py
```

### Generating New Sample Data

```bash
# Generate fresh sample data
python backend/data/generator.py --generate
```

### Code Structure

- **Frontend**: Modular JavaScript with ES6+ features
- **Backend**: Flask with blueprints for organization
- **Data**: Pandas-based data generation and processing
- **Charts**: Chart.js integration with custom styling

## 🚀 Deployment

### Local Production

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 backend.app:app
```

### Cloud Deployment

The application can be deployed to:
- **Heroku**: Use the included `Procfile`
- **Render**: Deploy directly from GitHub
- **Railway**: One-click deployment
- **DigitalOcean**: App Platform deployment

## 📈 Data Sources

The application uses realistic synthetic data based on:
- **RBI** (Reserve Bank of India)
- **MOSPI** (Ministry of Statistics and Programme Implementation)
- **CBIC** (Central Board of Indirect Taxes and Customs)
- **CMIE** (Centre for Monitoring Indian Economy)
- **DGCI&S** (Directorate General of Commercial Intelligence and Statistics)
- **NPCI** (National Payments Corporation of India)
- **OECD** (Organisation for Economic Co-operation and Development)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Chart.js** for excellent charting capabilities
- **Flask** for the lightweight web framework
- **Pandas** for powerful data manipulation
- **Indian Government** for economic data inspiration

## 📞 Support

For support, email support@indianpulse.com or create an issue in the repository.

---

**Built with ❤️ for India's economic data visualization**
