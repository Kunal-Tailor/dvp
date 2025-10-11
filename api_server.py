"""
Enhanced Flask API Server for Economic Dashboard Frontend
Provides RESTful API endpoints for all economic data
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys
sys.path.append('.')
from backend.data_processor import EconomicDataProcessor
from backend.country_comparison import CountryComparison
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# Initialize data processor and country comparison
processor = EconomicDataProcessor()
comparator = CountryComparison()

@app.route('/')
def index():
    """Serve the main landing page"""
    return send_from_directory('frontend', 'index.html')

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard page"""
    return send_from_directory('frontend', 'dashboard.html')

@app.route('/analytics')
def analytics():
    """Serve the analytics page"""
    return send_from_directory('frontend', 'analytics.html')

@app.route('/api/indicators')
def get_indicators():
    """Get list of all available indicators"""
    indicators = [
        {
            'id': 'gdp',
            'name': 'GDP Growth Rate',
            'description': 'Quarterly GDP growth percentage',
            'category': 'Growth',
            'unit': '%',
            'icon': '📈'
        },
        {
            'id': 'cpi',
            'name': 'Consumer Price Index',
            'description': 'Urban and Rural inflation rates',
            'category': 'Inflation',
            'unit': 'Index',
            'icon': '💰'
        },
        {
            'id': 'gst',
            'name': 'GST Collections',
            'description': 'Monthly GST revenue collections',
            'category': 'Revenue',
            'unit': '₹ Crores',
            'icon': '💼'
        },
        {
            'id': 'unemployment',
            'name': 'Unemployment Rate',
            'description': 'State-wise unemployment percentage',
            'category': 'Employment',
            'unit': '%',
            'icon': '👥'
        },
        {
            'id': 'forex',
            'name': 'Forex Reserves',
            'description': 'Foreign exchange reserves',
            'category': 'Reserves',
            'unit': 'USD Billion',
            'icon': '💵'
        },
        {
            'id': 'iip',
            'name': 'IIP Growth',
            'description': 'Industrial production index growth',
            'category': 'Production',
            'unit': '%',
            'icon': '🏭'
        },
        {
            'id': 'repo_rate',
            'name': 'Repo Rate',
            'description': 'RBI benchmark interest rate',
            'category': 'Monetary',
            'unit': '%',
            'icon': '🏦'
        },
        {
            'id': 'trade',
            'name': 'Trade Balance',
            'description': 'Exports, Imports, and Balance',
            'category': 'Trade',
            'unit': 'USD Billion',
            'icon': '🌐'
        },
        {
            'id': 'financial_inclusion',
            'name': 'Financial Inclusion',
            'description': 'Banking penetration index',
            'category': 'Finance',
            'unit': 'Index',
            'icon': '🏧'
        },
        {
            'id': 'digital_payment',
            'name': 'Digital Payments',
            'description': 'UPI transaction volumes',
            'category': 'Digital',
            'unit': 'Million',
            'icon': '📱'
        },
        {
            'id': 'cli',
            'name': 'Composite Leading Indicator',
            'description': 'Economic forecasting indicator',
            'category': 'Forecast',
            'unit': 'Index',
            'icon': '🔮'
        }
    ]
    return jsonify(indicators)

@app.route('/api/data/<indicator>')
def get_indicator_data(indicator):
    """Get data for a specific indicator"""
    
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    region = request.args.get('region')
    state = request.args.get('state')
    
    # Map indicator to dataset
    dataset_map = {
        'gdp': 'gdp',
        'cpi': 'cpi',
        'gst': 'gst',
        'unemployment': 'unemployment',
        'forex': 'forex',
        'iip': 'iip',
        'repo_rate': 'repo_rate',
        'trade': 'trade',
        'financial_inclusion': 'financial_inclusion',
        'digital_payment': 'digital_payment',
        'cli': 'cli'
    }
    
    if indicator not in dataset_map:
        return jsonify({'error': 'Invalid indicator'}), 404
    
    # Get dataset
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
        item = {
            'date': row['Date'].strftime('%Y-%m-%d'),
            'year': row['Year'],
        }
        
        # Add indicator-specific fields
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

@app.route('/api/correlation')
def get_correlation():
    """Get correlation matrix"""
    try:
        corr_matrix = processor.get_correlation_matrix()
        
        # Convert to JSON-friendly format
        result = {
            'indicators': corr_matrix.columns.tolist(),
            'matrix': corr_matrix.values.tolist()
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

# ============================================
# COUNTRY COMPARISON ENDPOINTS
# ============================================

@app.route('/api/comparison/countries')
def get_available_countries():
    """Get list of available countries for comparison"""
    countries = [
        {
            'code': code,
            'name': info['name'],
            'flag': info['flag'],
            'color': info['color']
        }
        for code, info in comparator.COMPARISON_COUNTRIES.items()
    ]
    return jsonify(countries)

@app.route('/api/comparison/<indicator>')
def get_country_comparison(indicator):
    """Get comparison data for a specific indicator"""
    
    # Get query parameters
    countries = request.args.get('countries', 'IND,CHN,USA,GBR,JPN,DEU').split(',')
    start_year = int(request.args.get('start_year', 2010))
    end_year = int(request.args.get('end_year', 2024))
    
    try:
        data = comparator.get_comparison_data(
            indicator, 
            countries, 
            start_year, 
            end_year
        )
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comparison/relative/<indicator>')
def get_relative_comparison(indicator):
    """Get relative comparison with India as baseline (100)"""
    
    base_country = request.args.get('base', 'IND')
    compare_countries = request.args.get('countries', 'CHN,USA,GBR,JPN,DEU,BRA').split(',')
    
    try:
        data = comparator.get_relative_comparison(
            indicator, 
            base_country, 
            compare_countries
        )
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comparison/multi-indicator')
def get_multi_indicator_comparison():
    """Get multi-indicator comparison for radar chart"""
    
    countries = request.args.get('countries', 'IND,CHN,USA,GBR,JPN').split(',')
    
    try:
        data = comparator.get_multi_indicator_comparison(countries)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comparison/rankings/<indicator>')
def get_country_rankings(indicator):
    """Get country rankings for a specific indicator"""
    
    countries = request.args.get('countries', None)
    if countries:
        countries = countries.split(',')
    
    try:
        data = comparator.get_comparison_data(indicator, countries)
        
        # Return just the rankings
        return jsonify({
            'indicator': indicator,
            'rankings': data['rankings'],
            'india_position': data['india_position']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comparison/export')
def export_comparison_data():
    """Export all comparison data"""
    try:
        comparator.export_all_comparisons()
        return jsonify({
            'status': 'success',
            'message': 'Comparison data exported successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Economic Dashboard API Server...")
    print("📊 Loaded datasets:", len(processor.datasets))
    print("🌍 Country comparison enabled with", len(comparator.COMPARISON_COUNTRIES), "countries")
    print("🌐 Server running at: http://localhost:5000")
    print("📱 Frontend available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
