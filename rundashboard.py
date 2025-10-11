#!/usr/bin/env python3
"""
Run Dashboard - Simplified launcher for the Economic Dashboard
This script starts the Flask API server which serves the dashboard frontend
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from backend.data_processor import EconomicDataProcessor
from backend.country_comparison import CountryComparison
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# Initialize data processor and country comparison
processor = EconomicDataProcessor()
comparator = CountryComparison()

print("=" * 60)
print("🚀 STARTING INDIA ECONOMIC DASHBOARD")
print("=" * 60)
print(f"📊 Loaded {len(processor.datasets)} datasets")
print(f"🌍 Country comparison enabled ({len(comparator.COMPARISON_COUNTRIES)} countries)")
print("=" * 60)

@app.route('/')
def index():
    """Serve the main landing page"""
    return send_from_directory('frontend', 'index.html')

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard page"""
    return send_from_directory('frontend', 'dashboard.html')


@app.route('/comparison')
def comparison():
    """Serve the comparison page"""
    return send_from_directory('frontend', 'comparison.html')

@app.route('/api/indicators')
def get_indicators():
    """Get list of all available indicators"""
    indicators = [
        {'id': 'gdp', 'name': 'GDP Growth Rate', 'description': 'Quarterly GDP growth percentage', 'category': 'Growth', 'unit': '%', 'icon': '📈'},
        {'id': 'cpi', 'name': 'Consumer Price Index', 'description': 'Urban and Rural inflation rates', 'category': 'Inflation', 'unit': 'Index', 'icon': '💰'},
        {'id': 'gst', 'name': 'GST Collections', 'description': 'Monthly GST revenue collections', 'category': 'Revenue', 'unit': '₹ Crores', 'icon': '💼'},
        {'id': 'unemployment', 'name': 'Unemployment Rate', 'description': 'State-wise unemployment percentage', 'category': 'Employment', 'unit': '%', 'icon': '👥'},
        {'id': 'forex', 'name': 'Forex Reserves', 'description': 'Foreign exchange reserves', 'category': 'Reserves', 'unit': 'USD Billion', 'icon': '💵'},
        {'id': 'iip', 'name': 'IIP Growth', 'description': 'Industrial production index growth', 'category': 'Production', 'unit': '%', 'icon': '🏭'},
        {'id': 'repo_rate', 'name': 'Repo Rate', 'description': 'RBI benchmark interest rate', 'category': 'Monetary', 'unit': '%', 'icon': '🏦'},
        {'id': 'trade', 'name': 'Trade Balance', 'description': 'Exports, Imports, and Balance', 'category': 'Trade', 'unit': 'USD Billion', 'icon': '🌐'},
        {'id': 'financial_inclusion', 'name': 'Financial Inclusion', 'description': 'Banking penetration index', 'category': 'Finance', 'unit': 'Index', 'icon': '🏧'},
        {'id': 'digital_payment', 'name': 'Digital Payments', 'description': 'UPI transaction volumes', 'category': 'Digital', 'unit': 'Million', 'icon': '📱'},
        {'id': 'cli', 'name': 'Composite Leading Indicator', 'description': 'Economic forecasting indicator', 'category': 'Forecast', 'unit': 'Index', 'icon': '🔮'}
    ]
    return jsonify(indicators)

@app.route('/api/data/<indicator>')
def get_indicator_data(indicator):
    """Get data for a specific indicator"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    region = request.args.get('region')
    state = request.args.get('state')
    
    dataset_map = {
        'gdp': 'gdp', 'cpi': 'cpi', 'gst': 'gst', 'unemployment': 'unemployment',
        'forex': 'forex', 'iip': 'iip', 'repo_rate': 'repo_rate', 'trade': 'trade',
        'financial_inclusion': 'financial_inclusion', 'digital_payment': 'digital_payment', 'cli': 'cli'
    }
    
    if indicator not in dataset_map:
        return jsonify({'error': 'Invalid indicator'}), 404
    
    df = processor.get_dataset(dataset_map[indicator])
    
    # Apply filters
    if start_date:
        df = df[df['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['Date'] <= pd.to_datetime(end_date)]
    if indicator == 'cpi' and region:
        df = df[df['Region'] == region]
    if indicator == 'unemployment' and state:
        df = df[df['State'] == state]
    
    # Prepare response
    data = []
    for _, row in df.iterrows():
        item = {'date': row['Date'].strftime('%Y-%m-%d'), 'year': row['Year']}
        
        if indicator == 'gdp':
            item['value'] = float(row['GDP_Growth_Percent'])
            item['quarter'] = row['Quarter']
        elif indicator == 'cpi':
            item['cpi'] = float(row['CPI'])
            item['inflation'] = float(row['Inflation_Rate'])
            item['region'] = row['Region']
        elif indicator == 'gst':
            item['value'] = float(row['GST_Collections_Cr'])
        elif indicator == 'unemployment':
            item['value'] = float(row['Unemployment_Rate'])
            item['state'] = row['State']
        elif indicator == 'forex':
            item['value'] = float(row['Forex_Reserves_USD_Bn'])
        elif indicator == 'iip':
            item['value'] = float(row['IIP_YOY_Growth'])
        elif indicator == 'repo_rate':
            item['value'] = float(row['Repo_Rate_Percent'])
        elif indicator == 'trade':
            item['exports'] = float(row['Exports_USD_Bn'])
            item['imports'] = float(row['Imports_USD_Bn'])
            item['balance'] = float(row['Trade_Balance_USD_Bn'])
        elif indicator == 'financial_inclusion':
            item['value'] = float(row['FI_Index'])
        elif indicator == 'digital_payment':
            item['volume'] = float(row['Volume_Mn'])
            item['value'] = float(row['Value_Cr'])
            item['mode'] = row['Payment_Mode']
        elif indicator == 'cli':
            item['value'] = float(row['CLI_Value'])
            item['quarter'] = row['Quarter']
        
        data.append(item)
    
    return jsonify(data)

@app.route('/api/statistics/<indicator>')
def get_statistics(indicator):
    """Get statistical summary for an indicator"""
    dataset_map = {
        'gdp': ('gdp', 'GDP_Growth_Percent'),
        'cpi': ('cpi', 'Inflation_Rate'),
        'gst': ('gst', 'GST_Collections_Cr'),
        'unemployment': ('unemployment', 'Unemployment_Rate'),
        'forex': ('forex', 'Forex_Reserves_USD_Bn'),
        'iip': ('iip', 'IIP_YOY_Growth'),
        'repo_rate': ('repo_rate', 'Repo_Rate_Percent'),
        'trade': ('trade', 'Trade_Balance_USD_Bn'),
        'financial_inclusion': ('financial_inclusion', 'FI_Index'),
        'digital_payment': ('digital_payment', 'Volume_Mn'),
        'cli': ('cli', 'CLI_Value')
    }
    
    if indicator not in dataset_map:
        return jsonify({'error': 'Invalid indicator'}), 404
    
    dataset_name, column = dataset_map[indicator]
    df = processor.get_dataset(dataset_name)
    stats = processor.calculate_statistics(df, column)
    
    return jsonify(stats)

@app.route('/api/summary')
def get_summary():
    """Get summary of all indicators"""
    summary = []
    indicators = [
        ('gdp', 'GDP_Growth_Percent', 'GDP Growth'),
        ('cpi', 'Inflation_Rate', 'Inflation'),
        ('gst', 'GST_Collections_Cr', 'GST Collections'),
        ('unemployment', 'Unemployment_Rate', 'Unemployment'),
        ('forex', 'Forex_Reserves_USD_Bn', 'Forex Reserves'),
        ('iip', 'IIP_YOY_Growth', 'IIP Growth'),
        ('repo_rate', 'Repo_Rate_Percent', 'Repo Rate'),
        ('trade', 'Trade_Balance_USD_Bn', 'Trade Balance'),
        ('financial_inclusion', 'FI_Index', 'FI Index'),
        ('digital_payment', 'Volume_Mn', 'Digital Payments'),
        ('cli', 'CLI_Value', 'CLI')
    ]
    
    for dataset_name, column, display_name in indicators:
        df = processor.get_dataset(dataset_name)
        if not df.empty and column in df.columns:
            stats = processor.calculate_statistics(df, column)
            summary.append({
                'id': dataset_name,
                'name': display_name,
                'latest': stats.get('latest', 0),
                'change': stats.get('change', 0),
                'growth_rate': stats.get('growth_rate', 0)
            })
    
    return jsonify(summary)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'datasets': len(processor.datasets),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("\n🌐 Dashboard URLs:")
    print("   - Main Page:    http://localhost:5000")
    print("   - Dashboard:    http://localhost:5000/dashboard")
    
    print("   - Comparison:   http://localhost:5000/comparison")
    print("\n📡 API Endpoints:")
    print("   - Health:       http://localhost:5000/api/health")
    print("   - Indicators:   http://localhost:5000/api/indicators")
    print("   - Summary:      http://localhost:5000/api/summary")
    print("\n" + "=" * 60)
    print("✅ Server starting on http://0.0.0.0:5000")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
