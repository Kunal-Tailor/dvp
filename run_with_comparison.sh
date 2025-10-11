#!/bin/bash

echo "=============================================="
echo "🇮🇳 IndianPulse - Country Comparison Setup"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "⚠️  Some dependencies may have failed to install"
fi

# Generate comparison data
echo ""
echo "📊 Generating country comparison data..."
python3 generate_comparison_data.py

if [ $? -eq 0 ]; then
    echo "✅ Comparison data generated successfully"
else
    echo "⚠️  Using fallback synthetic data generation"
fi

# Create necessary directories
echo ""
echo "📁 Creating necessary directories..."
mkdir -p data/comparisons
mkdir -p data/country_cache
echo "✅ Directories created"

# Display available features
echo ""
echo "=============================================="
echo "🎉 Setup Complete!"
echo "=============================================="
echo ""
echo "📱 Available Features:"
echo "   • Main Dashboard (India economic data)"
echo "   • Analytics Dashboard (correlations & trends)"
echo "   • 🆕 Country Comparison (India vs World)"
echo ""
echo "🌐 Starting server..."
echo ""
echo "Access your dashboards at:"
echo "   📊 Main: http://localhost:5000"
echo "   📈 Dashboard: http://localhost:5000/dashboard.html"
echo "   📉 Analytics: http://localhost:5000/analytics.html"
echo "   🌍 Comparison: http://localhost:5000/comparison.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=============================================="
echo ""

# Start the server
python3 api_server.py
