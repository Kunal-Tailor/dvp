#!/bin/bash

# =======================================================
# Test Script - Verify All Fixes
# =======================================================

echo "🧪 Running comprehensive tests..."
echo ""

# Test 1: Python version
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Python Version"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 --version && echo "✅ Python OK" || echo "❌ Python FAILED"
echo ""

# Test 2: Dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: Required Dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

modules=("flask" "flask_cors" "pandas" "numpy" "requests")
all_ok=true

for module in "${modules[@]}"; do
    if python3 -c "import $module" 2>/dev/null; then
        echo "✅ $module installed"
    else
        echo "❌ $module MISSING"
        all_ok=false
    fi
done
echo ""

# Test 3: Data files
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 3: Data Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

csv_count=$(ls data/*.csv 2>/dev/null | wc -l)
echo "Found $csv_count CSV files"

if [ "$csv_count" -eq 11 ]; then
    echo "✅ All 11 data files present"
else
    echo "❌ Expected 11 data files, found $csv_count"
    all_ok=false
fi
echo ""

# Test 4: Data processor
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 4: Data Processor Module"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 -c "
from backend.data_processor import EconomicDataProcessor
processor = EconomicDataProcessor()
if len(processor.datasets) == 11:
    print('✅ Data processor loaded 11 datasets')
    for name, df in processor.datasets.items():
        print(f'   - {name}: {len(df)} rows')
    exit(0)
else:
    print(f'❌ Expected 11 datasets, got {len(processor.datasets)}')
    exit(1)
" || all_ok=false
echo ""

# Test 5: Frontend files
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 5: Frontend Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

files=("frontend/index.html" "frontend/dashboard.html" "frontend/analytics.html")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file MISSING"
        all_ok=false
    fi
done
echo ""

# Test 6: Check for fixes in dashboard.html
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 6: Verify Dashboard Fixes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if grep -q "if (dateRange === '5y') years = 5;" frontend/dashboard.html; then
    echo "✅ Date range parsing fix applied"
else
    echo "❌ Date range fix NOT found"
    all_ok=false
fi

if grep -q "d.year && d.quarter" frontend/dashboard.html; then
    echo "✅ Date label formatting fix applied"
else
    echo "❌ Date label fix NOT found"
    all_ok=false
fi
echo ""

# Test 7: Check for fixes in analytics.html
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 7: Verify Analytics Fixes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if grep -q "|| 1;" frontend/analytics.html; then
    echo "✅ Division by zero fix applied"
else
    echo "❌ Division by zero fix NOT found"
    all_ok=false
fi

if grep -q "d.volume || d.cpi" frontend/analytics.html; then
    echo "✅ Complete field mapping fix applied"
else
    echo "❌ Field mapping fix NOT found"
    all_ok=false
fi
echo ""

# Final summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "FINAL RESULT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$all_ok" = true ]; then
    echo "✅ ALL TESTS PASSED!"
    echo ""
    echo "🚀 You can now run: ./START_PROJECT.sh"
    echo "📍 Then visit: http://localhost:5000/dashboard"
    exit 0
else
    echo "❌ SOME TESTS FAILED"
    echo ""
    echo "Please review the output above and fix any issues."
    echo "For help, see: RUN_INSTRUCTIONS.md"
    exit 1
fi
