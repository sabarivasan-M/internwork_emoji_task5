"""
Generate synthetic business performance data for Task 5 dashboard.
Creates realistic business metrics: sales, revenue, customer satisfaction, regional performance.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def generate_sales_data(n_records=500):
    """Generate synthetic daily sales data."""
    dates = [datetime(2025, 1, 1) + timedelta(days=x) for x in range(365)]
    
    data = {
        'date': dates,
        'sales_revenue': np.random.normal(50000, 15000, 365).clip(10000),
        'units_sold': np.random.poisson(250, 365),
        'customer_acquisition': np.random.poisson(45, 365),
        'customer_churn': np.random.poisson(12, 365),
        'avg_order_value': np.random.normal(350, 80, 365).clip(100),
    }
    
    df = pd.DataFrame(data)
    return df

def generate_regional_performance():
    """Generate synthetic regional sales performance."""
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    quarters = ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025']
    
    data = []
    for region in regions:
        for quarter in quarters:
            data.append({
                'region': region,
                'quarter': quarter,
                'revenue': np.random.normal(500000, 150000, 1)[0],
                'growth_rate': np.random.normal(15, 8, 1)[0],
                'market_share': np.random.uniform(10, 35, 1)[0],
            })
    
    return pd.DataFrame(data)

def generate_product_performance():
    """Generate synthetic product category performance."""
    categories = ['Electronics', 'Apparel', 'Home & Garden', 'Sports', 'Beauty', 'Food & Beverage']
    
    data = []
    for month in range(1, 13):
        for category in categories:
            data.append({
                'month': month,
                'category': category,
                'sales': np.random.normal(120000, 40000, 1)[0].clip(20000),
                'margin': np.random.normal(28, 8, 1)[0].clip(5),
                'satisfaction_score': np.random.normal(4.2, 0.5, 1)[0].clip(1, 5),
            })
    
    return pd.DataFrame(data)

def generate_customer_metrics():
    """Generate synthetic customer lifetime value and retention metrics."""
    data = {
        'segment': ['Premium', 'Standard', 'Economy', 'New'],
        'customer_count': [2500, 8500, 15000, 3200],
        'avg_ltv': [8500, 3200, 1200, 500],
        'retention_rate': [92, 78, 65, 45],
        'satisfaction': [4.7, 4.1, 3.5, 3.2],
    }
    return pd.DataFrame(data)

def generate_operational_metrics():
    """Generate synthetic operational efficiency metrics."""
    metrics = {
        'metric': [
            'Order Fulfillment Time (hours)',
            'Return Rate (%)',
            'Website Uptime (%)',
            'Avg Response Time (sec)',
            'Cost per Order ($)',
            'Net Promoter Score',
        ],
        'current': [24, 3.2, 99.8, 1.2, 12.50, 72],
        'target': [18, 2.5, 99.95, 0.8, 10, 80],
        'trend': ['↓ Improving', '↓ Improving', '→ Stable', '↓ Improving', '↑ Rising', '↓ Declining'],
    }
    return pd.DataFrame(metrics)

if __name__ == '__main__':
    base_path = "c:/Users/HP/Music/data_anal_inter/task5/"
    
    # Generate and save datasets
    sales_df = generate_sales_data()
    sales_df.to_csv(base_path + 'daily_sales.csv', index=False)
    print(f"✓ Generated daily sales data: {len(sales_df)} records")
    
    regional_df = generate_regional_performance()
    regional_df.to_csv(base_path + 'regional_performance.csv', index=False)
    print(f"✓ Generated regional performance: {len(regional_df)} records")
    
    product_df = generate_product_performance()
    product_df.to_csv(base_path + 'product_performance.csv', index=False)
    print(f"✓ Generated product performance: {len(product_df)} records")
    
    customer_df = generate_customer_metrics()
    customer_df.to_csv(base_path + 'customer_segments.csv', index=False)
    print(f"✓ Generated customer metrics: {len(customer_df)} records")
    
    operational_df = generate_operational_metrics()
    operational_df.to_csv(base_path + 'operational_metrics.csv', index=False)
    print(f"✓ Generated operational metrics: {len(operational_df)} records")
    
    print("\n✅ All synthetic datasets generated!")
