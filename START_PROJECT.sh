#!/bin/bash

# =======================================================
# India Economic Dashboard - Project Startup Script
# =======================================================

echo "🇮🇳 Starting India Economic Dashboard..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Check if dependencies are installed
echo ""
echo "📦 Checking dependencies..."

if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask not found. Installing dependencies..."
    pip3 install flask flask-cors pandas numpy requests --break-system-packages
else
    echo "✅ Dependencies installed"
fi

# Check for requests module
if ! python3 -c "import requests" 2>/dev/null; then
    echo "Installing requests module..."
    pip3 install requests --break-system-packages
fi

# Verify data files
echo ""
echo "📊 Verifying data files..."
if [ -d "data" ]; then
    echo "✅ Data directory found ($(ls data/*.csv 2>/dev/null | wc -l) CSV files)"
else
    echo "❌ Data directory not found!"
    exit 1
fi

# Test data loading
echo ""
echo "🔍 Testing data processor..."
python3 -c "
from backend.data_processor import EconomicDataProcessor
processor = EconomicDataProcessor()
print(f'✅ Successfully loaded {len(processor.datasets)} datasets')
for name, df in processor.datasets.items():
    print(f'   - {name}: {len(df)} rows')
" || exit 1

# Start the server
echo ""
echo "=========================================="
echo "🚀 Starting Flask API Server..."
echo "=========================================="
echo ""
echo "Server will be available at:"
echo "  📍 Main Page:    http://localhost:5000"
echo "  📊 Dashboard:    http://localhost:5000/dashboard"
echo "  📈 Analytics:    http://localhost:5000/analytics"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the API server
python3 api_server.py
