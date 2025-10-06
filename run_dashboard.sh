#!/bin/bash

# Economic Dashboard Launcher Script
echo "🇮🇳 India Economic Dashboard"
echo "============================"
echo ""

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "📁 Creating data directory..."
    mkdir -p data
fi

# Check if CSV files exist
if [ ! -f "data/gdp_growth_rate.csv" ]; then
    echo "📊 Generating CSV data files..."
    python3 generate_csv_data.py
    if [ $? -eq 0 ]; then
        echo "✅ CSV files generated successfully!"
    else
        echo "❌ Error generating CSV files. Please check your Python installation."
        exit 1
    fi
else
    echo "✅ CSV data files found!"
fi

echo ""
echo "🚀 Starting Streamlit dashboard..."
echo "📍 Dashboard will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

# Run Streamlit
streamlit run dashboard.py
