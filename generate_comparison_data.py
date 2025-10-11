"""
Generate country comparison CSV files
Creates comprehensive comparison datasets for India vs other major economies
"""

import sys
sys.path.append('.')
from backend.country_comparison import CountryComparison
import pandas as pd
import os

def main():
    print("=" * 60)
    print("GENERATING COUNTRY COMPARISON DATA")
    print("=" * 60)
    
    comparator = CountryComparison()
    data_dir = comparator.data_dir
    
    # Create comparison data directory
    comparison_dir = os.path.join(data_dir, 'comparisons')
    os.makedirs(comparison_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {comparison_dir}")
    print(f"🌍 Countries: {', '.join([c['name'] for c in comparator.COMPARISON_COUNTRIES.values()])}\n")
    
    # Define indicators to generate
    indicators_config = [
        {
            'name': 'gdp_growth',
            'display_name': 'GDP Growth Rate',
            'wb_code': 'gdp_growth',
            'unit': '%'
        },
        {
            'name': 'inflation',
            'display_name': 'Inflation Rate',
            'wb_code': 'inflation',
            'unit': '%'
        },
        {
            'name': 'unemployment',
            'display_name': 'Unemployment Rate',
            'wb_code': 'unemployment',
            'unit': '%'
        },
        {
            'name': 'trade_gdp',
            'display_name': 'Trade as % of GDP',
            'wb_code': 'trade_gdp',
            'unit': '%'
        },
        {
            'name': 'exports',
            'display_name': 'Exports as % of GDP',
            'wb_code': 'exports',
            'unit': '%'
        },
        {
            'name': 'imports',
            'display_name': 'Imports as % of GDP',
            'wb_code': 'imports',
            'unit': '%'
        }
    ]
    
    all_countries = list(comparator.COMPARISON_COUNTRIES.keys())
    
    # Generate data for each indicator
    for config in indicators_config:
        print(f"📊 Generating {config['display_name']}...")
        
        try:
            # Generate the comparison data
            df = comparator._generate_synthetic_comparison_data(
                config['name'], 
                all_countries
            )
            
            if not df.empty:
                # Save to CSV
                output_file = os.path.join(comparison_dir, f"{config['name']}_comparison.csv")
                df.to_csv(output_file, index=False)
                print(f"   ✅ Saved {len(df)} records to {output_file}")
                
                # Print summary statistics
                india_data = df[df['country_code'] == 'IND']
                if not india_data.empty:
                    latest_india = india_data[india_data['year'] == india_data['year'].max()]['value'].values[0]
                    print(f"   🇮🇳 India latest value: {latest_india:.2f} {config['unit']}")
            else:
                print(f"   ⚠️  No data generated")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Generate a combined comparison file
    print(f"\n📋 Generating combined comparison file...")
    try:
        combined_data = []
        
        for config in indicators_config:
            df = comparator._generate_synthetic_comparison_data(
                config['name'], 
                all_countries
            )
            df['indicator_name'] = config['display_name']
            df['unit'] = config['unit']
            combined_data.append(df)
        
        if combined_data:
            combined_df = pd.concat(combined_data, ignore_index=True)
            combined_file = os.path.join(comparison_dir, 'all_indicators_comparison.csv')
            combined_df.to_csv(combined_file, index=False)
            print(f"   ✅ Saved {len(combined_df)} records to {combined_file}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Generate India-specific comparison summary
    print(f"\n🇮🇳 Generating India comparison summary...")
    try:
        india_summary = []
        
        for config in indicators_config:
            data = comparator.get_comparison_data(config['wb_code'], all_countries)
            
            if 'IND' in data['countries']:
                india_info = data['countries']['IND']
                india_summary.append({
                    'indicator': config['display_name'],
                    'unit': config['unit'],
                    'latest_value': india_info['latest'],
                    'change': india_info['change'],
                    'average': india_info['average'],
                    'position': data.get('india_position', 'N/A')
                })
        
        if india_summary:
            summary_df = pd.DataFrame(india_summary)
            summary_file = os.path.join(comparison_dir, 'india_summary.csv')
            summary_df.to_csv(summary_file, index=False)
            print(f"   ✅ Saved India summary to {summary_file}")
            
            # Print summary table
            print("\n" + "=" * 80)
            print("INDIA PERFORMANCE SUMMARY")
            print("=" * 80)
            print(summary_df.to_string(index=False))
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ COMPARISON DATA GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\n💡 Files saved in: {comparison_dir}")
    print("🚀 You can now use these files in your frontend visualizations")
    print("\nTo start the server with comparison features, run:")
    print("   python api_server.py")
    print("\n")

if __name__ == "__main__":
    main()
