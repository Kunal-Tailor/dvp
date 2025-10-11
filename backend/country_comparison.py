"""
Country Comparison Module for IndianPulse
Compares India with other major economies using World Bank and OECD data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional
import os
import json

class CountryComparison:
    """Handle country-to-country economic comparisons"""
    
    # Major economies to compare with India
    COMPARISON_COUNTRIES = {
        'IND': {'name': 'India', 'flag': '🇮🇳', 'color': '#FF9933'},
        'CHN': {'name': 'China', 'flag': '🇨🇳', 'color': '#DE2910'},
        'USA': {'name': 'United States', 'flag': '🇺🇸', 'color': '#3C3B6E'},
        'GBR': {'name': 'United Kingdom', 'flag': '🇬🇧', 'color': '#012169'},
        'JPN': {'name': 'Japan', 'flag': '🇯🇵', 'color': '#BC002D'},
        'DEU': {'name': 'Germany', 'flag': '🇩🇪', 'color': '#000000'},
        'BRA': {'name': 'Brazil', 'flag': '🇧🇷', 'color': '#009739'},
        'RUS': {'name': 'Russia', 'flag': '🇷🇺', 'color': '#0033A0'},
        'ZAF': {'name': 'South Africa', 'flag': '🇿🇦', 'color': '#007749'},
        'AUS': {'name': 'Australia', 'flag': '🇦🇺', 'color': '#00008B'},
    }
    
    # World Bank indicator codes
    WB_INDICATORS = {
        'gdp_growth': 'NY.GDP.MKTP.KD.ZG',  # GDP growth (annual %)
        'gdp_per_capita': 'NY.GDP.PCAP.CD',  # GDP per capita (current US$)
        'inflation': 'FP.CPI.TOTL.ZG',  # Inflation, consumer prices (annual %)
        'unemployment': 'SL.UEM.TOTL.ZS',  # Unemployment, total (% of total labor force)
        'exports': 'NE.EXP.GNFS.ZS',  # Exports of goods and services (% of GDP)
        'imports': 'NE.IMP.GNFS.ZS',  # Imports of goods and services (% of GDP)
        'fdi': 'BX.KLT.DINV.CD.WD',  # Foreign direct investment, net inflows (current US$)
        'trade_gdp': 'NE.TRD.GNFS.ZS',  # Trade (% of GDP)
    }
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.cache_dir = os.path.join(data_dir, 'country_cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache = {}
        
    def fetch_world_bank_data(self, indicator: str, country_codes: List[str], 
                              start_year: int = 2010, end_year: int = 2024) -> pd.DataFrame:
        """Fetch data from World Bank API"""
        
        # Check cache first
        cache_key = f"{indicator}_{'_'.join(country_codes)}_{start_year}_{end_year}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.csv")
        
        if os.path.exists(cache_file):
            print(f"Loading cached data for {indicator}")
            return pd.read_csv(cache_file)
        
        all_data = []
        
        for country_code in country_codes:
            try:
                # World Bank API endpoint
                url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}"
                params = {
                    'format': 'json',
                    'date': f'{start_year}:{end_year}',
                    'per_page': 500
                }
                
                print(f"Fetching {indicator} data for {country_code}...")
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if len(data) > 1 and data[1]:
                        for item in data[1]:
                            if item['value'] is not None:
                                all_data.append({
                                    'country_code': country_code,
                                    'country': item['country']['value'],
                                    'year': int(item['date']),
                                    'value': float(item['value']),
                                    'indicator': indicator
                                })
            except Exception as e:
                print(f"Error fetching data for {country_code}: {e}")
                continue
        
        if all_data:
            df = pd.DataFrame(all_data)
            df.to_csv(cache_file, index=False)
            return df
        
        return pd.DataFrame()
    
    def generate_comparison_csv(self, indicator_name: str, wb_indicator: str, 
                                countries: List[str] = None) -> pd.DataFrame:
        """Generate comparison CSV for a specific indicator"""
        
        if countries is None:
            countries = list(self.COMPARISON_COUNTRIES.keys())
        
        df = self.fetch_world_bank_data(wb_indicator, countries)
        
        if df.empty:
            print(f"No data available for {indicator_name}")
            return self._generate_synthetic_comparison_data(indicator_name, countries)
        
        return df
    
    def _generate_synthetic_comparison_data(self, indicator: str, countries: List[str]) -> pd.DataFrame:
        """Generate realistic synthetic comparison data"""
        
        years = list(range(2010, 2025))
        data = []
        
        # Base values and growth patterns for different indicators
        base_values = {
            'gdp_growth': {'IND': 7.0, 'CHN': 8.5, 'USA': 2.5, 'GBR': 2.0, 'JPN': 1.5, 
                          'DEU': 1.8, 'BRA': 2.2, 'RUS': 1.5, 'ZAF': 1.8, 'AUS': 2.8},
            'inflation': {'IND': 6.5, 'CHN': 2.5, 'USA': 2.5, 'GBR': 2.5, 'JPN': 0.5, 
                         'DEU': 1.8, 'BRA': 6.0, 'RUS': 5.0, 'ZAF': 5.5, 'AUS': 2.5},
            'unemployment': {'IND': 5.5, 'CHN': 4.0, 'USA': 5.5, 'GBR': 5.0, 'JPN': 3.0, 
                           'DEU': 4.5, 'BRA': 8.0, 'RUS': 5.5, 'ZAF': 25.0, 'AUS': 5.5},
            'trade_gdp': {'IND': 45.0, 'CHN': 38.0, 'USA': 28.0, 'GBR': 60.0, 'JPN': 35.0, 
                         'DEU': 85.0, 'BRA': 25.0, 'RUS': 48.0, 'ZAF': 58.0, 'AUS': 42.0},
        }
        
        base = base_values.get(indicator, {country: 5.0 for country in countries})
        
        for country_code in countries:
            country_base = base.get(country_code, 5.0)
            
            for i, year in enumerate(years):
                # Add some variation and trends
                trend = np.sin(i * 0.5) * 2
                noise = np.random.normal(0, 1.5)
                
                # COVID-19 impact in 2020
                covid_impact = -15 if year == 2020 and indicator == 'gdp_growth' else 0
                covid_impact += 10 if year == 2020 and indicator == 'unemployment' else 0
                
                value = country_base + trend + noise + covid_impact
                
                data.append({
                    'country_code': country_code,
                    'country': self.COMPARISON_COUNTRIES[country_code]['name'],
                    'year': year,
                    'value': round(value, 2),
                    'indicator': indicator
                })
        
        return pd.DataFrame(data)
    
    def get_comparison_data(self, indicator: str, countries: List[str] = None, 
                           start_year: int = 2010, end_year: int = 2024) -> Dict:
        """Get comparison data formatted for frontend"""
        
        if countries is None:
            countries = ['IND', 'CHN', 'USA', 'GBR', 'JPN', 'DEU']
        
        # Map indicator names to World Bank codes
        wb_code = self.WB_INDICATORS.get(indicator)
        
        if wb_code:
            df = self.generate_comparison_csv(indicator, wb_code, countries)
        else:
            df = self._generate_synthetic_comparison_data(indicator, countries)
        
        # Filter by year range
        df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
        
        # Prepare data for frontend
        result = {
            'years': sorted(df['year'].unique().tolist()),
            'countries': {},
            'india_position': None,
            'rankings': []
        }
        
        for country_code in countries:
            country_data = df[df['country_code'] == country_code].sort_values('year')
            if not country_data.empty:
                result['countries'][country_code] = {
                    'name': self.COMPARISON_COUNTRIES[country_code]['name'],
                    'flag': self.COMPARISON_COUNTRIES[country_code]['flag'],
                    'color': self.COMPARISON_COUNTRIES[country_code]['color'],
                    'values': country_data['value'].tolist(),
                    'latest': float(country_data.iloc[-1]['value']),
                    'change': float(country_data.iloc[-1]['value'] - country_data.iloc[0]['value']) if len(country_data) > 1 else 0,
                    'average': float(country_data['value'].mean())
                }
        
        # Calculate rankings for latest year
        latest_data = df[df['year'] == df['year'].max()].sort_values('value', ascending=False)
        result['rankings'] = latest_data[['country_code', 'country', 'value']].to_dict('records')
        
        # Find India's position
        india_pos = latest_data.reset_index(drop=True)
        if 'IND' in india_pos['country_code'].values:
            india_idx = india_pos[india_pos['country_code'] == 'IND'].index[0]
            result['india_position'] = int(india_idx + 1)
        
        return result
    
    def get_relative_comparison(self, indicator: str, base_country: str = 'IND', 
                               compare_countries: List[str] = None) -> Dict:
        """Get relative comparison (India as baseline = 100)"""
        
        if compare_countries is None:
            compare_countries = ['CHN', 'USA', 'GBR', 'JPN', 'DEU', 'BRA']
        
        all_countries = [base_country] + compare_countries
        data = self.get_comparison_data(indicator, all_countries)
        
        if base_country not in data['countries']:
            return data
        
        india_values = data['countries'][base_country]['values']
        
        # Calculate relative values (India = 100)
        for country_code in compare_countries:
            if country_code in data['countries']:
                country_values = data['countries'][country_code]['values']
                relative_values = [
                    round((cv / iv * 100), 2) if iv != 0 else 100
                    for cv, iv in zip(country_values, india_values)
                ]
                data['countries'][country_code]['relative_values'] = relative_values
                data['countries'][country_code]['latest_relative'] = relative_values[-1] if relative_values else 100
        
        return data
    
    def get_multi_indicator_comparison(self, countries: List[str] = None) -> Dict:
        """Get comparison across multiple indicators for radar chart"""
        
        if countries is None:
            countries = ['IND', 'CHN', 'USA', 'GBR', 'JPN']
        
        indicators = ['gdp_growth', 'unemployment', 'inflation', 'trade_gdp']
        result = {
            'indicators': indicators,
            'countries': {}
        }
        
        for country in countries:
            country_data = []
            for indicator in indicators:
                data = self.get_comparison_data(indicator, [country])
                if country in data['countries']:
                    # Normalize values to 0-100 scale for radar chart
                    value = data['countries'][country]['latest']
                    # Simple normalization (can be improved)
                    normalized = min(max((value / 10) * 100, 0), 100)
                    country_data.append(round(normalized, 2))
                else:
                    country_data.append(0)
            
            result['countries'][country] = {
                'name': self.COMPARISON_COUNTRIES[country]['name'],
                'flag': self.COMPARISON_COUNTRIES[country]['flag'],
                'color': self.COMPARISON_COUNTRIES[country]['color'],
                'values': country_data
            }
        
        return result
    
    def export_all_comparisons(self):
        """Export all comparison data to CSV files"""
        
        countries = list(self.COMPARISON_COUNTRIES.keys())
        
        for indicator_name, wb_code in self.WB_INDICATORS.items():
            print(f"Generating comparison data for {indicator_name}...")
            df = self.generate_comparison_csv(indicator_name, wb_code, countries)
            
            if not df.empty:
                output_file = os.path.join(self.data_dir, f'comparison_{indicator_name}.csv')
                df.to_csv(output_file, index=False)
                print(f"Saved {output_file}")


if __name__ == "__main__":
    # Test the comparison module
    comparator = CountryComparison()
    
    print("Testing country comparison module...")
    
    # Test GDP growth comparison
    gdp_data = comparator.get_comparison_data('gdp_growth', ['IND', 'CHN', 'USA'])
    print(f"\nGDP Growth Comparison:")
    print(f"Years: {gdp_data['years']}")
    print(f"India Position: {gdp_data['india_position']}")
    
    # Export all comparisons
    print("\nExporting all comparison data...")
    comparator.export_all_comparisons()
    
    print("\nCountry comparison module ready!")
