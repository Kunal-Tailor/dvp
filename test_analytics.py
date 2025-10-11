#!/usr/bin/env python3
"""
Test script for Analytics API endpoints
Verifies all endpoints used by analytics.html are working correctly
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_endpoint(name, url, expected_keys=None):
    """Test a single endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response received")
        
        if expected_keys:
            for key in expected_keys:
                if key in data:
                    print(f"✅ Key '{key}' found")
                    if isinstance(data[key], list):
                        print(f"   - Contains {len(data[key])} items")
                    elif isinstance(data[key], dict):
                        print(f"   - Contains {len(data[key])} keys")
                else:
                    print(f"❌ Key '{key}' NOT found")
        
        # Print sample data
        if isinstance(data, list) and len(data) > 0:
            print(f"\n📊 Sample data (first item):")
            print(json.dumps(data[0], indent=2))
        elif isinstance(data, dict):
            print(f"\n📊 Sample data:")
            sample = {k: v for i, (k, v) in enumerate(data.items()) if i < 3}
            print(json.dumps(sample, indent=2))
        
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Server not running at {BASE_URL}")
        print(f"   Please start the server with: python api_server.py")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("ANALYTICS API ENDPOINT TESTS")
    print(f"Testing server at: {BASE_URL}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = []
    
    # Test 1: Health check
    results.append(test_endpoint(
        "Health Check",
        f"{BASE_URL}/api/health",
        expected_keys=["status", "datasets", "timestamp"]
    ))
    
    # Test 2: Get indicators list
    results.append(test_endpoint(
        "Indicators List",
        f"{BASE_URL}/api/indicators",
        expected_keys=None  # It's a list
    ))
    
    # Test 3: Get correlation matrix
    results.append(test_endpoint(
        "Correlation Matrix",
        f"{BASE_URL}/api/correlation",
        expected_keys=["indicators", "matrix"]
    ))
    
    # Test 4: Get summary
    results.append(test_endpoint(
        "Summary Statistics",
        f"{BASE_URL}/api/summary",
        expected_keys=None  # It's a list
    ))
    
    # Test 5: Get GDP data
    results.append(test_endpoint(
        "GDP Data",
        f"{BASE_URL}/api/data/gdp",
        expected_keys=None  # It's a list
    ))
    
    # Test 6: Get CPI data
    results.append(test_endpoint(
        "CPI/Inflation Data",
        f"{BASE_URL}/api/data/cpi",
        expected_keys=None  # It's a list
    ))
    
    # Test 7: Get unemployment data
    results.append(test_endpoint(
        "Unemployment Data",
        f"{BASE_URL}/api/data/unemployment",
        expected_keys=None  # It's a list
    ))
    
    # Test 8: Get forex data
    results.append(test_endpoint(
        "Forex Reserves Data",
        f"{BASE_URL}/api/data/forex",
        expected_keys=None  # It's a list
    ))
    
    # Test 9: Get IIP data
    results.append(test_endpoint(
        "IIP Data",
        f"{BASE_URL}/api/data/iip",
        expected_keys=None  # It's a list
    ))
    
    # Test 10: Get statistics for GDP
    results.append(test_endpoint(
        "GDP Statistics",
        f"{BASE_URL}/api/statistics/gdp",
        expected_keys=["latest", "mean", "max", "min", "growth_rate"]
    ))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! Analytics page should work correctly.")
    else:
        print(f"\n❌ Some tests failed. Please check the server and data files.")
    
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("1. If tests passed, open: http://localhost:5000/analytics")
    print("2. Check browser console (F12) for any JavaScript errors")
    print("3. Use 'Export Data' button to download analytics CSV")
    print("4. Try comparing different indicators")
    print("="*60)

if __name__ == "__main__":
    main()
