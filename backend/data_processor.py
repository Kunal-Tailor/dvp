"""
Data Processing Module for Economic Dashboard
Handles loading, cleaning, and transforming CSV data
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class EconomicDataProcessor:
    """Process and clean economic indicator data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.datasets = {}
        self.load_all_data()
    
    def load_all_data(self):
        """Load all CSV files into memory"""
        self.datasets['gdp'] = self.load_gdp_data()
        self.datasets['cpi'] = self.load_cpi_data()
        self.datasets['gst'] = self.load_gst_data()
        self.datasets['unemployment'] = self.load_unemployment_data()
        self.datasets['forex'] = self.load_forex_data()
        self.datasets['iip'] = self.load_iip_data()
        self.datasets['repo_rate'] = self.load_repo_rate_data()
        self.datasets['trade'] = self.load_trade_balance_data()
        self.datasets['financial_inclusion'] = self.load_financial_inclusion_data()
        self.datasets['digital_payment'] = self.load_digital_payment_data()
        self.datasets['cli'] = self.load_cli_data()
    
    def create_date_column(self, df: pd.DataFrame, year_col: str, period_col: str, 
                          period_type: str = 'month') -> pd.DataFrame:
        """Create a datetime column from year and period"""
        df = df.copy()
        
        if period_type == 'quarter':
            # Map quarters to months
            quarter_map = {'Q1': 1, 'Q2': 4, 'Q3': 7, 'Q4': 10}
            df['Month_Num'] = df[period_col].map(quarter_map)
        else:
            # Convert month names to numbers
            month_map = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            df['Month_Num'] = df[period_col].map(month_map)
        
        df['Date'] = pd.to_datetime(
            df[year_col].astype(str) + '-' + df['Month_Num'].astype(str) + '-01',
            format='%Y-%m-%d'
        )
        df = df.drop('Month_Num', axis=1)
        return df.sort_values('Date')
    
    def load_gdp_data(self) -> pd.DataFrame:
        """Load and clean GDP growth rate data"""
        df = pd.read_csv(f"{self.data_dir}/gdp_growth_rate.csv")
        df = self.create_date_column(df, 'Year', 'Quarter', 'quarter')
        df['GDP_Growth_Percent'] = pd.to_numeric(df['GDP_Growth_Percent'], errors='coerce')
        return df
    
    def load_cpi_data(self) -> pd.DataFrame:
        """Load and clean CPI data"""
        df = pd.read_csv(f"{self.data_dir}/consumer_price_index.csv")
        df = self.create_date_column(df, 'Year', 'Month', 'month')
        df['CPI'] = pd.to_numeric(df['CPI'], errors='coerce')
        df['Inflation_Rate'] = pd.to_numeric(df['Inflation_Rate'], errors='coerce')
        return df
    
    def load_gst_data(self) -> pd.DataFrame:
        """Load and clean GST collections data"""
        df = pd.read_csv(f"{self.data_dir}/gst_collections.csv")
        df = self.create_date_column(df, 'Year', 'Month', 'month')
        df['GST_Collections_Cr'] = pd.to_numeric(df['GST_Collections_Cr'], errors='coerce')
        return df
    
    def load_unemployment_data(self) -> pd.DataFrame:
        """Load and clean unemployment rate data"""
        df = pd.read_csv(f"{self.data_dir}/unemployment_rate.csv")
        df = self.create_date_column(df, 'Year', 'Month', 'month')
        df['Unemployment_Rate'] = pd.to_numeric(df['Unemployment_Rate'], errors='coerce')
        return df
    
    def load_forex_data(self) -> pd.DataFrame:
        """Load and clean forex reserves data"""
        df = pd.read_csv(f"{self.data_dir}/forex_reserves.csv")
        df = self.create_date_column(df, 'Year', 'Month', 'month')
        df['Forex_Reserves_USD_Bn'] = pd.to_numeric(df['Forex_Reserves_USD_Bn'], errors='coerce')
        return df
    
    def load_iip_data(self) -> pd.DataFrame:
        """Load and clean IIP growth data"""
        df = pd.read_csv(f"{self.data_dir}/iip.csv")
        df = self.create_date_column(df, 'Year', 'Month', 'month')
        df['IIP_YOY_Growth'] = pd.to_numeric(df['IIP_YOY_Growth'], errors='coerce')
        return df
    
    def load_repo_rate_data(self) -> pd.DataFrame:
        """Load and clean repo rate data"""
        df = pd.read_csv(f"{self.data_dir}/repo_rate.csv")
        df = self.create_date_column(df, 'Year', 'Month', 'month')
        df['Repo_Rate_Percent'] = pd.to_numeric(df['Repo_Rate_Percent'], errors='coerce')
        return df
    
    def load_trade_balance_data(self) -> pd.DataFrame:
        """Load and clean trade balance data"""
        df = pd.read_csv(f"{self.data_dir}/trade_balance.csv")
        df = self.create_date_column(df, 'Year', 'Month', 'month')
        df['Exports_USD_Bn'] = pd.to_numeric(df['Exports_USD_Bn'], errors='coerce')
        df['Imports_USD_Bn'] = pd.to_numeric(df['Imports_USD_Bn'], errors='coerce')
        df['Trade_Balance_USD_Bn'] = pd.to_numeric(df['Trade_Balance_USD_Bn'], errors='coerce')
        return df
    
    def load_financial_inclusion_data(self) -> pd.DataFrame:
        """Load and clean financial inclusion index data"""
        df = pd.read_csv(f"{self.data_dir}/financial_inclusion_index.csv")
        df = self.create_date_column(df, 'Year', 'Month', 'month')
        df['FI_Index'] = pd.to_numeric(df['FI_Index'], errors='coerce')
        return df
    
    def load_digital_payment_data(self) -> pd.DataFrame:
        """Load and clean digital payment volume data"""
        df = pd.read_csv(f"{self.data_dir}/digital_payment_volume.csv")
        df = self.create_date_column(df, 'Year', 'Month', 'month')
        df['Volume_Mn'] = pd.to_numeric(df['Volume_Mn'], errors='coerce')
        df['Value_Cr'] = pd.to_numeric(df['Value_Cr'], errors='coerce')
        return df
    
    def load_cli_data(self) -> pd.DataFrame:
        """Load and clean composite leading indicator data"""
        df = pd.read_csv(f"{self.data_dir}/composite_leading_indicator.csv")
        df = self.create_date_column(df, 'Year', 'Quarter', 'quarter')
        df['CLI_Value'] = pd.to_numeric(df['CLI_Value'], errors='coerce')
        return df
    
    def get_dataset(self, name: str) -> pd.DataFrame:
        """Get a specific dataset by name"""
        return self.datasets.get(name, pd.DataFrame())
    
    def get_date_range(self, df: pd.DataFrame) -> Tuple[datetime, datetime]:
        """Get the date range of a dataset"""
        if 'Date' in df.columns and not df.empty:
            return df['Date'].min(), df['Date'].max()
        return None, None
    
    def filter_by_date_range(self, df: pd.DataFrame, start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> pd.DataFrame:
        """Filter dataset by date range"""
        if 'Date' not in df.columns:
            return df
        
        result = df.copy()
        if start_date:
            result = result[result['Date'] >= start_date]
        if end_date:
            result = result[result['Date'] <= end_date]
        return result
    
    def calculate_statistics(self, df: pd.DataFrame, column: str) -> Dict:
        """Calculate summary statistics for a numeric column"""
        if column not in df.columns:
            return {}
        
        data = df[column].dropna()
        if data.empty:
            return {}
        
        stats = {
            'mean': float(data.mean()),
            'median': float(data.median()),
            'std': float(data.std()),
            'min': float(data.min()),
            'max': float(data.max()),
            'latest': float(data.iloc[-1]),
            'count': int(data.count())
        }
        
        # Calculate growth rate if possible
        if len(data) > 1:
            stats['growth_rate'] = float(((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100)
            stats['change'] = float(data.iloc[-1] - data.iloc[0])
        
        return stats
    
    def get_correlation_matrix(self) -> pd.DataFrame:
        """Create correlation matrix between key indicators"""
        # Merge datasets on Date
        merged = pd.DataFrame()
        
        # GDP
        gdp = self.datasets['gdp'][['Date', 'GDP_Growth_Percent']].copy()
        merged = gdp if merged.empty else merged.merge(gdp, on='Date', how='outer')
        
        # CPI - aggregate by date
        cpi = self.datasets['cpi'].groupby('Date')['Inflation_Rate'].mean().reset_index()
        merged = merged.merge(cpi, on='Date', how='outer')
        
        # Unemployment - filter India only
        unemp = self.datasets['unemployment'][
            self.datasets['unemployment']['State'] == 'India'
        ][['Date', 'Unemployment_Rate']].copy()
        merged = merged.merge(unemp, on='Date', how='outer')
        
        # Forex
        forex = self.datasets['forex'][['Date', 'Forex_Reserves_USD_Bn']].copy()
        merged = merged.merge(forex, on='Date', how='outer')
        
        # IIP
        iip = self.datasets['iip'][['Date', 'IIP_YOY_Growth']].copy()
        merged = merged.merge(iip, on='Date', how='outer')
        
        # Repo Rate
        repo = self.datasets['repo_rate'][['Date', 'Repo_Rate_Percent']].copy()
        merged = merged.merge(repo, on='Date', how='outer')
        
        # Calculate correlation
        merged = merged.drop('Date', axis=1)
        correlation = merged.corr()
        
        return correlation
    
    def export_dataset(self, name: str, filepath: str):
        """Export a dataset to CSV"""
        if name in self.datasets:
            self.datasets[name].to_csv(filepath, index=False)
            return True
        return False


if __name__ == "__main__":
    # Test the data processor
    processor = EconomicDataProcessor()
    
    print("Available datasets:")
    for name in processor.datasets.keys():
        df = processor.get_dataset(name)
        print(f"  - {name}: {len(df)} rows")
    
    print("\nGDP Statistics:")
    gdp_stats = processor.calculate_statistics(
        processor.get_dataset('gdp'), 
        'GDP_Growth_Percent'
    )
    for key, value in gdp_stats.items():
        print(f"  {key}: {value:.2f}")
    
    print("\nCorrelation Matrix:")
    print(processor.get_correlation_matrix())
