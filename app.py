# app.py
from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# -----------------------------
# Data loading utilities (CSV)
# -----------------------------

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

_MONTHS_MAP = {
    'jan': 1, 'january': 1,
    'feb': 2, 'february': 2,
    'mar': 3, 'march': 3,
    'apr': 4, 'april': 4,
    'may': 5,
    'jun': 6, 'june': 6,
    'jul': 7, 'july': 7,
    'aug': 8, 'august': 8,
    'sep': 9, 'sept': 9, 'september': 9,
    'oct': 10, 'october': 10,
    'nov': 11, 'november': 11,
    'dec': 12, 'december': 12,
}

def _to_int(x):
    try:
        return int(str(x).strip())
    except Exception:
        return None

def _parse_month(month_value):
    if pd.isna(month_value):
        return None
    m = str(month_value).strip().lower()
    return _MONTHS_MAP.get(m)

def _date_from_year_month(year_value, month_value):
    year = _to_int(year_value)
    month = _parse_month(month_value)
    if year and month:
        return datetime(year, month, 1)
    return None

def _date_from_year_quarter(year_value, quarter_value, calendar_quarter=True):
    """calendar_quarter=True: Q1=Jan; if False: Q1=Apr (financial year)."""
    year = _to_int(year_value)
    if year is None:
        return None
    q_match = re.search(r'Q(\d+)', str(quarter_value))
    if not q_match:
        return None
    q = int(q_match.group(1))
    if calendar_quarter:
        month = (q - 1) * 3 + 1
        return datetime(year, month, 1)
    # Financial year Q1 starts in April
    month = (q - 1) * 3 + 4
    full_year = year
    if month > 12:
        month -= 12
        full_year += 1
    return datetime(full_year, month, 1)

def _coerce_numeric(series):
    return pd.to_numeric(series.replace(['N/A', 'n/a', 'NA', '', 'null', None], np.nan), errors='coerce')

def _finalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if 'date' in df.columns:
        df = df[df['date'].notna()].sort_values('date')
    return df

def load_gdp_growth() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'gdp_growth_rate.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_quarter(r['Year'], r['Quarter'], calendar_quarter=True), axis=1)
    df['GDP_Growth_Percent'] = _coerce_numeric(df['GDP_Growth_Percent'])
    return _finalize_df(df)

def load_cpi() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'consumer_price_index.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_month(r['Year'], r['Month']), axis=1)
    df['CPI'] = _coerce_numeric(df['CPI'])
    df['Inflation_Rate'] = _coerce_numeric(df['Inflation_Rate'])
    return _finalize_df(df)

def load_gst() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'gst_collections.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_month(r['Year'], r['Month']), axis=1)
    df['GST_Collections_Cr'] = _coerce_numeric(df['GST_Collections_Cr'])
    return _finalize_df(df)

def load_unemployment() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'unemployment_rate.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_month(r['Year'], r['Month']), axis=1)
    df['Unemployment_Rate'] = _coerce_numeric(df['Unemployment_Rate'])
    return _finalize_df(df)

def load_forex() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'forex_reserves.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_month(r['Year'], r['Month']), axis=1)
    df['Forex_Reserves_USD_Bn'] = _coerce_numeric(df['Forex_Reserves_USD_Bn'])
    return _finalize_df(df)

def load_iip() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'iip.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_month(r['Year'], r['Month']), axis=1)
    df['IIP_YOY_Growth'] = _coerce_numeric(df['IIP_YOY_Growth'])
    return _finalize_df(df)

def load_repo() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'repo_rate.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_month(r['Year'], r['Month']), axis=1)
    df['Repo_Rate_Percent'] = _coerce_numeric(df['Repo_Rate_Percent'])
    return _finalize_df(df)

def load_trade() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'trade_balance.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_month(r['Year'], r['Month']), axis=1)
    df['Exports_USD_Bn'] = _coerce_numeric(df['Exports_USD_Bn'])
    df['Imports_USD_Bn'] = _coerce_numeric(df['Imports_USD_Bn'])
    df['Trade_Balance_USD_Bn'] = _coerce_numeric(df['Trade_Balance_USD_Bn'])
    return _finalize_df(df)

def load_inclusion() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'financial_inclusion_index.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_month(r['Year'], r['Month']), axis=1)
    df['FI_Index'] = _coerce_numeric(df['FI_Index'])
    return _finalize_df(df)

def load_digital() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'digital_payment_volume.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_month(r['Year'], r['Month']), axis=1)
    df['Volume_Mn'] = _coerce_numeric(df['Volume_Mn'])
    df['Value_Cr'] = _coerce_numeric(df['Value_Cr'])
    return _finalize_df(df)

def load_cli() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, 'composite_leading_indicator.csv')
    df = pd.read_csv(path)
    df['date'] = df.apply(lambda r: _date_from_year_quarter(r['Year'], r['Quarter'], calendar_quarter=True), axis=1)
    df['CLI_Value'] = _coerce_numeric(df['CLI_Value'])
    return _finalize_df(df)

def _format_label(date: datetime, is_quarter: bool = False) -> str:
    if pd.isna(date):
        return ''
    if is_quarter:
        q = (date.month - 1) // 3 + 1
        return f"{date.year} Q{q}"
    return date.strftime('%Y-%b')

def _compute_stats(values):
    clean = [float(x) for x in values if pd.notna(x)]
    if not clean:
        return {
            'latest': 0,
            'highest': 0,
            'lowest': 0,
            'average': 0,
            'change': 0,
        }
    return {
        'latest': round(clean[-1], 2),
        'highest': round(max(clean), 2),
        'lowest': round(min(clean), 2),
        'average': round(sum(clean) / len(clean), 2),
        'change': round(clean[-1] - clean[0], 2) if len(clean) > 1 else 0,
    }

def _apply_range(df: pd.DataFrame, end_date_col: str = 'date', range_param: str = '1Y') -> pd.DataFrame:
    if df.empty:
        return df
    end_date = df[end_date_col].max()
    if pd.isna(end_date):
        return df
    if range_param == '3M':
        start_date = end_date - timedelta(days=90)
    elif range_param == '1Y':
        start_date = end_date - timedelta(days=365)
    elif range_param == '2Y':
        start_date = end_date - timedelta(days=730)
    elif range_param == '5Y':
        start_date = end_date - timedelta(days=1825)
    else:
        start_date = df[end_date_col].min()
    return df[(df[end_date_col] >= start_date) & (df[end_date_col] <= end_date)].copy()

def load_all_datasets():
    return {
        'gdp': load_gdp_growth(),
        'cpi': load_cpi(),
        'gst': load_gst(),
        'unemployment': load_unemployment(),
        'forex': load_forex(),
        'iip': load_iip(),
        'repo': load_repo(),
        'trade': load_trade(),
        'inclusion': load_inclusion(),
        'digital': load_digital(),
        'cli': load_cli(),
    }

# Load datasets at startup
DATASETS = load_all_datasets()

# Metadata for indicators
INDICATOR_META = {
    'gdp': {
        'name': 'GDP Growth Rate', 'unit': '%', 'value_col': 'GDP_Growth_Percent', 'frequency': 'Quarterly', 'is_quarter': True,
    },
    'cpi': {
        'name': 'Consumer Price Inflation', 'unit': '%', 'value_col': 'Inflation_Rate', 'frequency': 'Monthly', 'is_quarter': False,
        'filters': {'region': 'Region'},
    },
    'gst': {
        'name': 'GST Collections', 'unit': '₹ Cr', 'value_col': 'GST_Collections_Cr', 'frequency': 'Monthly', 'is_quarter': False,
    },
    'unemployment': {
        'name': 'Unemployment Rate', 'unit': '%', 'value_col': 'Unemployment_Rate', 'frequency': 'Monthly', 'is_quarter': False,
        'filters': {'state': 'State'},
    },
    'forex': {
        'name': 'Forex Reserves', 'unit': 'USD Bn', 'value_col': 'Forex_Reserves_USD_Bn', 'frequency': 'Monthly', 'is_quarter': False,
    },
    'iip': {
        'name': 'IIP YoY Growth', 'unit': '%', 'value_col': 'IIP_YOY_Growth', 'frequency': 'Monthly', 'is_quarter': False,
    },
    'repo': {
        'name': 'Repo Rate', 'unit': '%', 'value_col': 'Repo_Rate_Percent', 'frequency': 'Monthly', 'is_quarter': False,
    },
    'trade': {
        'name': 'Trade Balance', 'unit': 'USD Bn', 'value_col': 'Trade_Balance_USD_Bn', 'frequency': 'Monthly', 'is_quarter': False,
    },
    'inclusion': {
        'name': 'Financial Inclusion Index', 'unit': 'Index', 'value_col': 'FI_Index', 'frequency': 'Annual', 'is_quarter': False,
    },
    'digital': {
        'name': 'Digital Payments (UPI)', 'unit': 'Mn', 'value_col': 'Volume_Mn', 'frequency': 'Monthly', 'is_quarter': False,
        'filters': {'payment_mode': 'Payment_Mode', 'metric': ['Volume_Mn', 'Value_Cr']},
    },
    'cli': {
        'name': 'Composite Leading Indicator', 'unit': 'Index', 'value_col': 'CLI_Value', 'frequency': 'Quarterly', 'is_quarter': True,
    },
}

@app.route('/api/data/<indicator>')
def get_indicator_data(indicator):
    range_param = request.args.get('range', '1Y')
    meta = INDICATOR_META.get(indicator)
    if not meta or indicator not in DATASETS:
        return jsonify({'error': 'Indicator not found'}), 404

    df = DATASETS[indicator]

    # Apply optional filters based on indicator
    filters = meta.get('filters', {})
    if 'region' in filters:
        region = request.args.get('region')
        if region and region.lower() != 'all' and 'Region' in df.columns:
            df = df[df['Region'].str.lower() == region.lower()]
    if 'state' in filters:
        state = request.args.get('state')
        if state and state.lower() != 'all' and 'State' in df.columns:
            df = df[df['State'].str.lower() == state.lower()]
    if 'payment_mode' in filters:
        mode = request.args.get('payment_mode')
        if mode and mode.lower() != 'all' and 'Payment_Mode' in df.columns:
            df = df[df['Payment_Mode'].str.lower() == mode.lower()]
    # For digital metric selection
    value_col = meta['value_col']
    if indicator == 'digital':
        metric = request.args.get('metric')
        if metric in ['Volume_Mn', 'Value_Cr']:
            value_col = metric

    # Apply range
    df_range = _apply_range(df, 'date', range_param)
    # Drop NA values of the selected value column
    series_df = df_range[[ 'date', value_col ]].dropna().copy()
    # If multiple rows per date (e.g., CPI Urban/Rural, unemployment states), aggregate by mean
    if not series_df.empty and series_df.duplicated(subset=['date']).any():
        series_df = (
            series_df.groupby('date', as_index=False)[value_col]
            .mean()
            .sort_values('date')
        )

    # Labels and values
    is_quarter = bool(meta.get('is_quarter'))
    labels = [ _format_label(d, is_quarter=is_quarter) for d in series_df['date'] ]
    values = series_df[value_col].astype(float).tolist()

    stats = _compute_stats(values)

    # Allow dynamic unit override (e.g., digital metric Value_Cr)
    unit = meta['unit']
    if indicator == 'digital' and value_col == 'Value_Cr':
        unit = 'Cr'

    return jsonify({
        'labels': labels,
        'data': values,
        'stats': stats,
        'indicator': meta['name'],
        'unit': unit,
        'frequency': meta['frequency'],
    })

@app.route('/api/metadata')
def get_metadata():
    meta = {}
    for key, m in INDICATOR_META.items():
        entry = {
            'name': m['name'],
            'unit': m['unit'],
            'frequency': m['frequency'],
        }
        filters = m.get('filters')
        if filters:
            filt_values = {}
            df = DATASETS.get(key)
            if df is not None:
                if 'region' in filters and 'Region' in df.columns:
                    filt_values['regions'] = sorted(df['Region'].dropna().unique().tolist())
                if 'state' in filters and 'State' in df.columns:
                    filt_values['states'] = sorted(df['State'].dropna().unique().tolist())
                if 'payment_mode' in filters and 'Payment_Mode' in df.columns:
                    filt_values['payment_modes'] = sorted(df['Payment_Mode'].dropna().unique().tolist())
                if key == 'digital':
                    filt_values['metrics'] = ['Volume_Mn', 'Value_Cr']
            entry['filters'] = filt_values
        meta[key] = entry
    return jsonify(meta)

@app.route('/api/export/<indicator>')
def export_indicator(indicator):
    meta = INDICATOR_META.get(indicator)
    if not meta or indicator not in DATASETS:
        return jsonify({'error': 'Indicator not found'}), 404
    df = DATASETS[indicator].copy()
    # Reapply same filters as data endpoint
    if 'Region' in df.columns:
        region = request.args.get('region')
        if region and region.lower() != 'all':
            df = df[df['Region'].str.lower() == region.lower()]
    if 'State' in df.columns:
        state = request.args.get('state')
        if state and state.lower() != 'all':
            df = df[df['State'].str.lower() == state.lower()]
    if 'Payment_Mode' in df.columns:
        mode = request.args.get('payment_mode')
        if mode and mode.lower() != 'all':
            df = df[df['Payment_Mode'].str.lower() == mode.lower()]

    csv_data = df.to_csv(index=False)
    filename = f"{indicator}_export.csv"
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': f'attachment; filename={filename}'})

@app.route('/api/correlation')
def correlation():
    indicators_param = request.args.get('indicators', 'gdp,cpi,iip,forex,gst')
    keys = [k.strip() for k in indicators_param.split(',') if k.strip() in DATASETS]
    if not keys:
        return jsonify({'error': 'No valid indicators provided'}), 400
    # Build merged frame on date
    merged = None
    for k in keys:
        meta = INDICATOR_META[k]
        df = DATASETS[k][['date', meta['value_col']]].rename(columns={meta['value_col']: meta['name']}).copy()
        if merged is None:
            merged = df
        else:
            merged = pd.merge(merged, df, on='date', how='inner')
    if merged is None or merged.empty:
        return jsonify({'correlation': {}, 'dates': []})
    corr = merged.drop(columns=['date']).corr(numeric_only=True)
    corr_dict = corr.round(3).to_dict()
    return jsonify({'correlation': corr_dict, 'columns': list(corr.columns)})

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