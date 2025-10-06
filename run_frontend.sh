#!/bin/bash

# Economic Dashboard Frontend Launcher
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🇮🇳 India Economic Dashboard - Frontend Launcher 🎨        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
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
        echo "❌ Error generating CSV files."
        exit 1
    fi
else
    echo "✅ CSV data files found!"
fi

echo ""
echo "🚀 Starting Flask API Server..."
echo "📍 Frontend will be available at: http://localhost:5000"
echo "📊 Dashboard: http://localhost:5000/dashboard"
echo "📈 Analytics: http://localhost:5000/analytics"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Flask API server
python3 api_server.py
