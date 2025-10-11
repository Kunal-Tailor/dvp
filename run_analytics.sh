#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  India Economic Analytics Dashboard  ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed${NC}"
    echo "Please install Python 3.7+ to continue"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python3 found"

# Check if required packages are installed
echo -e "\n${YELLOW}Checking dependencies...${NC}"
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠ Flask not found. Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

python3 -c "import pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠ Pandas not found. Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

echo -e "${GREEN}✓${NC} All dependencies installed"

# Check if data directory exists
if [ ! -d "data" ]; then
    echo -e "${RED}❌ Data directory not found${NC}"
    echo "Please ensure the 'data' folder exists with CSV files"
    exit 1
fi

echo -e "${GREEN}✓${NC} Data directory found"

# Count CSV files
CSV_COUNT=$(find data -name "*.csv" | wc -l)
echo -e "${GREEN}✓${NC} Found $CSV_COUNT CSV data files"

echo ""
echo -e "${BLUE}Starting Analytics API Server...${NC}"
echo ""
echo -e "${GREEN}📊 Analytics will be available at:${NC}"
echo -e "   ${YELLOW}http://localhost:5000/analytics${NC}"
echo ""
echo -e "${BLUE}Other available pages:${NC}"
echo -e "   • Home: ${YELLOW}http://localhost:5000/${NC}"
echo -e "   • Dashboard: ${YELLOW}http://localhost:5000/dashboard${NC}"
echo -e "   • Comparison: ${YELLOW}http://localhost:5000/comparison.html${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Start the server
python3 api_server.py
