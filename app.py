# app.py
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load and preprocess the CSV data
def load_economic_data():
    df = pd.read_csv('data.csv')
    
    # Clean column names
    df.columns = [col.strip() for col in df.columns]
    
    # Convert financial year quarters to datetime objects
    def fy_to_date(fy_str):
        if 'FY' in fy_str and 'Q' in fy_str:
            # Handle quarterly data (e.g., "FY18 Q1")
            match = re.search(r'FY(\d+)\s*Q(\d+)', fy_str)
            if match:
                year = int(match.group(1))
                quarter = int(match.group(2))
                # Convert 2-digit year to 4-digit (assuming 2000s)
                full_year = 2000 + year if year < 50 else 1900 + year
                # Calculate month based on quarter (April is start of FY in India)
                month = (quarter - 1) * 3 + 4
                if month > 12:
                    month -= 12
                    full_year += 1
                return datetime(full_year, month, 1)
        elif 'FY' in fy_str and '-' in fy_str:
            # Handle yearly data (e.g., "FY 2017-18")
            match = re.search(r'FY\s*(\d+)-(\d+)', fy_str)
            if match:
                start_year = int(match.group(1))
                # Use the start of the financial year (April 1)
                return datetime(start_year, 4, 1)
        return None
    
    df['date'] = df['Year / Quarter'].apply(fy_to_date)
    
    # Filter out rows without valid dates
    df = df[df['date'].notna()].copy()
    df = df.sort_values('date')
    
    # Convert numeric columns to proper numeric types, handling N/A values
    numeric_columns = [
        'GDP Growth Rate (YoY %)',
        'CPI Inflation (YoY %)',
        'Gross GST Collections (₹ Lakh Crore)',
        'Unemployment Rate (%)',
        'Foreign Exchange Reserves (Billion USD, End of Period)',
        'Index of Industrial Production (IIP) Growth (YoY %)'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            # Replace N/A with NaN and convert to numeric
            df[col] = df[col].replace(['N/A', 'n/a', 'NA', ''], np.nan)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# Global variable to store the data
economic_data = load_economic_data()

# API endpoint to get indicator data
@app.route('/api/data/<indicator>')
def get_indicator_data(indicator):
    range_param = request.args.get('range', '1Y')
    
    # Map indicator keys to column names
    indicator_map = {
        'gdp': 'GDP Growth Rate (YoY %)',
        'cpi': 'CPI Inflation (YoY %)',
        'gst': 'Gross GST Collections (₹ Lakh Crore)',
        'unemployment': 'Unemployment Rate (%)',
        'forex': 'Foreign Exchange Reserves (Billion USD, End of Period)',
        'iip': 'Index of Industrial Production (IIP) Growth (YoY %)',
        'repo': 'Repo Rate',
        'trade': 'Trade Balance',
        'inclusion': 'Financial Inclusion Index',
        'digital': 'Digital Payment Volume',
        'cli': 'Composite Leading Indicator'
    }
    
    column_name = indicator_map.get(indicator)
    if not column_name or column_name not in economic_data.columns:
        return jsonify({'error': 'Indicator not found'}), 404
    
    # Filter data based on time range
    end_date = economic_data['date'].max()
    
    if range_param == '3M':
        start_date = end_date - timedelta(days=90)
    elif range_param == '1Y':
        start_date = end_date - timedelta(days=365)
    elif range_param == '2Y':
        start_date = end_date - timedelta(days=730)
    elif range_param == '5Y':
        start_date = end_date - timedelta(days=1825)
    else:
        start_date = economic_data['date'].min()
    
    filtered_data = economic_data[
        (economic_data['date'] >= start_date) & 
        (economic_data['date'] <= end_date)
    ].copy()
    
    # Prepare response - filter out NaN values
    filtered_data = filtered_data[filtered_data[column_name].notna()].copy()
    labels = filtered_data['Year / Quarter'].tolist()
    data = filtered_data[column_name].tolist()
    
    # Calculate statistics - ensure data is numeric
    valid_data = []
    for x in data:
        if pd.notna(x) and isinstance(x, (int, float)):
            valid_data.append(float(x))
    
    if valid_data:
        stats = {
            'latest': round(valid_data[-1], 2),
            'highest': round(max(valid_data), 2),
            'lowest': round(min(valid_data), 2),
            'average': round(sum(valid_data) / len(valid_data), 2),
            'change': round(valid_data[-1] - valid_data[0], 2) if len(valid_data) > 1 else 0
        }
    else:
        stats = {
            'latest': 0,
            'highest': 0,
            'lowest': 0,
            'average': 0,
            'change': 0
        }
    
    return jsonify({
        'labels': labels,
        'data': data,
        'stats': stats,
        'indicator': indicator_map[indicator]
    })

# Serve the main pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)