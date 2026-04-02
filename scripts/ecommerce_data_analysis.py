#!/usr/bin/env python3
"""
E-Commerce Business Analysis Project
Author: [Teu Nome]
Description: This script extracts e-commerce data from a MySQL database, 
processes revenue trends, and visualizes geographical and temporal performance.
"""

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

def load_data():
    # Database Credentials
    user = "root"
    password = "" 
    host = "localhost"
    database = "ecommerce_project"

    # Connection Engine
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    
    query = """
    SELECT 
        o.order_purchase_timestamp,
        p.payment_value,
        c.customer_state
    FROM orders o
    JOIN order_payments p ON o.order_id = p.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    """
    return pd.read_sql(query, engine)

def plot_revenue_trend(df):
    # Data Preprocessing
    df_sorted = df.sort_values('order_purchase_timestamp')
    df_sorted['month_year_dt'] = df_sorted['order_purchase_timestamp'].dt.to_period('M')
    
    monthly_revenue = df_sorted.groupby('month_year_dt')['payment_value'].sum().reset_index()
    monthly_revenue['month_label'] = monthly_revenue['month_year_dt'].dt.strftime('%b %y')

    # Chart Creation
    plt.figure(figsize=(16, 7), facecolor='white')
    ax = plt.gca()
    plt.plot(monthly_revenue['month_label'], monthly_revenue['payment_value'], 
             color='#2c3e50', linewidth=3, marker='o', markerfacecolor='white')

    # Formatting
    ticks_to_show = range(0, len(monthly_revenue), 2)
    plt.xticks(ticks_to_show, [monthly_revenue['month_label'][i] for i in ticks_to_show])
    
    formatter = ticker.FuncFormatter(lambda x, pos: f'${x/1e6:.1f}M')
    ax.yaxis.set_major_formatter(formatter)
    
    plt.title('E-Commerce Monthly Revenue Trend', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

def plot_top_states(df):
    # Data Aggregation
    state_revenue = df.groupby('customer_state')['payment_value'].sum().sort_values(ascending=False).head(10)

    # Chart Creation
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=state_revenue.values, y=state_revenue.index, hue=state_revenue.index, palette='viridis', legend=False)

    # Formatting
    formatter = ticker.FuncFormatter(lambda x, pos: f'${x/1e6:.1f}M')
    ax.xaxis.set_major_formatter(formatter)
    
    plt.title('Top 10 Brazilian States by Total Revenue', fontsize=15, fontweight='bold')
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Starting Analysis...")
    data = load_data()
    data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
    
    plot_revenue_trend(data)
    plot_top_states(data)
    print("Analysis Complete.")