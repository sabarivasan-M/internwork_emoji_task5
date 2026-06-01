"""
Business Performance Interactive Dashboard — Task 5
Visualizes sales trends, regional performance, product metrics, customer segments, and operational KPIs.
Outputs: business_dashboard.html (interactive dashboard)
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

BASE_PATH = "c:/Users/HP/Music/data_anal_inter/task5/"

def load_business_data():
    """Load synthetic business performance datasets."""
    try:
        sales = pd.read_csv(BASE_PATH + "daily_sales.csv")
        print(f"✓ Loaded daily sales: {len(sales)} records")
    except Exception as e:
        print(f"⚠ Sales data not found: {e}")
        sales = None
    
    try:
        regional = pd.read_csv(BASE_PATH + "regional_performance.csv")
        print(f"✓ Loaded regional performance: {len(regional)} records")
    except Exception as e:
        print(f"⚠ Regional data not found: {e}")
        regional = None
    
    try:
        products = pd.read_csv(BASE_PATH + "product_performance.csv")
        print(f"✓ Loaded product performance: {len(products)} records")
    except Exception as e:
        print(f"⚠ Product data not found: {e}")
        products = None
    
    try:
        customers = pd.read_csv(BASE_PATH + "customer_segments.csv")
        print(f"✓ Loaded customer segments: {len(customers)} records")
    except Exception as e:
        print(f"⚠ Customer data not found: {e}")
        customers = None
    
    try:
        operations = pd.read_csv(BASE_PATH + "operational_metrics.csv")
        print(f"✓ Loaded operational metrics: {len(operations)} records")
    except Exception as e:
        print(f"⚠ Operational data not found: {e}")
        operations = None
    
    return sales, regional, products, customers, operations

def create_overview_dashboard(sales, regional, products, customers, operations):
    """Create main overview dashboard."""
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=(
            "Daily Sales Revenue Trend",
            "Revenue by Region (Q4 2025)",
            "Units Sold vs Revenue",
            "Sales by Product Category",
            "Customer Segment Value",
            "Fulfillment vs Target"
        ),
        specs=[[{"type": "scatter"}, {"type": "pie"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
    )
    
    # Row 1, Col 1: Daily Sales Trend
    if sales is not None:
        sales['date'] = pd.to_datetime(sales['date'])
        fig.add_trace(
            go.Scatter(x=sales['date'], y=sales['sales_revenue'], mode='lines', name='Revenue', 
                      line=dict(color='steelblue', width=2), fill='tozeroy'),
            row=1, col=1
        )
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    
    # Row 1, Col 2: Regional Revenue Pie
    if regional is not None:
        q4_data = regional[regional['quarter'] == 'Q4 2025']
        fig.add_trace(
            go.Pie(labels=q4_data['region'], values=q4_data['revenue'], name="Revenue"),
            row=1, col=2
        )
    
    # Row 1, Col 3: Units vs Revenue
    if sales is not None:
        fig.add_trace(
            go.Scatter(x=sales['units_sold'], y=sales['sales_revenue'], mode='markers',
                      name='Daily', marker=dict(size=5, color=sales['avg_order_value'], colorscale='Viridis', showscale=False)),
            row=1, col=3
        )
        fig.update_xaxes(title_text="Units Sold", row=1, col=3)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=3)
    
    # Row 2, Col 1: Product Category Sales
    if products is not None:
        prod_monthly = products.groupby('category')['sales'].sum().sort_values(ascending=True)
        fig.add_trace(
            go.Bar(y=prod_monthly.index, x=prod_monthly.values, orientation='h', 
                   name="Sales", marker=dict(color='mediumpurple')),
            row=2, col=1
        )
        fig.update_xaxes(title_text="Total Sales ($)", row=2, col=1)
    
    # Row 2, Col 2: Customer Segment Value
    if customers is not None:
        fig.add_trace(
            go.Bar(x=customers['segment'], y=customers['avg_ltv'], 
                   name="Avg LTV", marker=dict(color='mediumseagreen')),
            row=2, col=2
        )
        fig.update_yaxes(title_text="Avg Lifetime Value ($)", row=2, col=2)
    
    # Row 2, Col 3: Fulfillment Performance
    if operations is not None:
        ops_metrics = operations[['metric', 'current']].head(3)
        fig.add_trace(
            go.Bar(x=ops_metrics['metric'].str.replace(' (hours)', '').str.replace(' (%)', ''), 
                   y=ops_metrics['current'], name='Current',
                   marker=dict(color='coral')),
            row=2, col=3
        )
        fig.update_yaxes(title_text="Value", row=2, col=3)
    
    fig.update_layout(height=900, showlegend=False, title_text="Business Performance Dashboard", hovermode='closest')
    return fig

def create_sales_detail_dashboard(sales):
    """Create detailed sales analytics dashboard."""
    if sales is None:
        return None
    
    sales['date'] = pd.to_datetime(sales['date'])
    sales['month'] = sales['date'].dt.month
    sales['week'] = sales['date'].dt.isocalendar().week
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Daily Revenue Trend", "Monthly Sales Total", "Units Sold Daily", "Avg Order Value Trend"),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "scatter"}]]
    )
    
    fig.add_trace(go.Scatter(x=sales['date'], y=sales['sales_revenue'], mode='lines', 
                            name='Revenue', line=dict(color='steelblue', width=2)), row=1, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    
    monthly_sales = sales.groupby('month')['sales_revenue'].sum()
    fig.add_trace(go.Bar(x=monthly_sales.index, y=monthly_sales.values, name='Monthly Sales', 
                        marker_color='mediumpurple'), row=1, col=2)
    fig.update_xaxes(title_text="Month", row=1, col=2)
    fig.update_yaxes(title_text="Sales ($)", row=1, col=2)
    
    fig.add_trace(go.Scatter(x=sales['date'], y=sales['units_sold'], mode='lines+markers',
                            name='Units', line=dict(color='mediumseagreen')), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Units Sold", row=2, col=1)
    
    fig.add_trace(go.Scatter(x=sales['date'], y=sales['avg_order_value'], mode='lines',
                            name='AOV', line=dict(color='coral', width=2)), row=2, col=2)
    fig.update_xaxes(title_text="Date", row=2, col=2)
    fig.update_yaxes(title_text="Avg Order Value ($)", row=2, col=2)
    
    fig.update_layout(height=900, showlegend=False, title_text="Sales Analytics Dashboard")
    return fig

def create_regional_dashboard(regional):
    """Create regional performance dashboard."""
    if regional is None:
        return None
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Revenue by Region & Quarter", "Market Share by Region"),
        specs=[[{"type": "bar"}, {"type": "scatter"}]]
    )
    
    for region in regional['region'].unique():
        region_data = regional[regional['region'] == region]
        fig.add_trace(
            go.Bar(x=region_data['quarter'], y=region_data['revenue'], name=region),
            row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(x=regional['region'], y=regional['market_share'], mode='markers+text',
                  name='Market Share', marker=dict(size=15, color=regional['growth_rate'], colorscale='Viridis', showscale=True)),
        row=1, col=2
    )
    fig.update_xaxes(title_text="Region", row=1, col=2)
    fig.update_yaxes(title_text="Market Share (%)", row=1, col=2)
    
    fig.update_layout(height=500, showlegend=True, title_text="Regional Performance Dashboard")
    return fig

def create_product_dashboard(products):
    """Create product performance dashboard."""
    if products is None:
        return None
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Sales by Category", "Profit Margin by Category", "Satisfaction by Category", "Sales Trend by Category"),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    prod_sales = products.groupby('category')['sales'].sum().sort_values(ascending=False)
    fig.add_trace(go.Bar(x=prod_sales.index, y=prod_sales.values, name='Sales', marker_color='steelblue'), row=1, col=1)
    fig.update_yaxes(title_text="Sales ($)", row=1, col=1)
    
    prod_margin = products.groupby('category')['margin'].mean().sort_values(ascending=False)
    fig.add_trace(go.Bar(x=prod_margin.index, y=prod_margin.values, name='Margin', marker_color='coral'), row=1, col=2)
    fig.update_yaxes(title_text="Margin (%)", row=1, col=2)
    
    prod_satisfaction = products.groupby('category')['satisfaction_score'].mean().sort_values(ascending=False)
    fig.add_trace(go.Bar(x=prod_satisfaction.index, y=prod_satisfaction.values, name='Satisfaction', marker_color='mediumseagreen'), row=2, col=1)
    fig.update_yaxes(title_text="Satisfaction Score", row=2, col=1)
    
    for cat in products['category'].unique():
        cat_data = products[products['category'] == cat].sort_values('month')
        fig.add_trace(go.Scatter(x=cat_data['month'], y=cat_data['sales'], mode='lines', name=cat), row=2, col=2)
    fig.update_xaxes(title_text="Month", row=2, col=2)
    fig.update_yaxes(title_text="Sales ($)", row=2, col=2)
    
    fig.update_layout(height=900, showlegend=True, title_text="Product Performance Dashboard")
    return fig

def create_kpi_summary(sales, regional, products, customers, operations):
    """Create KPI summary HTML."""
    kpi_html = "<h2>📊 Key Business Metrics</h2><div style='display:grid;grid-template-columns:repeat(3,1fr);gap:15px;'>"
    
    if sales is not None:
        total_revenue = sales['sales_revenue'].sum()
        total_units = sales['units_sold'].sum()
        avg_revenue = sales['sales_revenue'].mean()
        kpi_html += f"""<div style='background:#e3f2fd;padding:15px;border-radius:8px;border-left:4px solid #1976d2;'>
            <div style='font-size:24px;font-weight:bold;color:#1976d2;'>${total_revenue:,.0f}</div>
            <div style='font-size:12px;color:#555;'>Total Annual Revenue</div>
        </div>
        <div style='background:#f3e5f5;padding:15px;border-radius:8px;border-left:4px solid #7b1fa2;'>
            <div style='font-size:24px;font-weight:bold;color:#7b1fa2;'>{total_units:,.0f}</div>
            <div style='font-size:12px;color:#555;'>Total Units Sold</div>
        </div>
        <div style='background:#e0f2f1;padding:15px;border-radius:8px;border-left:4px solid #00796b;'>
            <div style='font-size:24px;font-weight:bold;color:#00796b;'>${avg_revenue:,.0f}</div>
            <div style='font-size:12px;color:#555;'>Daily Avg Revenue</div>
        </div>"""
    
    if regional is not None:
        q4_revenue = regional[regional['quarter'] == 'Q4 2025']['revenue'].sum()
        avg_growth = regional['growth_rate'].mean()
        kpi_html += f"""<div style='background:#fff3e0;padding:15px;border-radius:8px;border-left:4px solid #f57c00;'>
            <div style='font-size:24px;font-weight:bold;color:#f57c00;'>${q4_revenue:,.0f}</div>
            <div style='font-size:12px;color:#555;'>Q4 2025 Revenue</div>
        </div>
        <div style='background:#fce4ec;padding:15px;border-radius:8px;border-left:4px solid #c2185b;'>
            <div style='font-size:24px;font-weight:bold;color:#c2185b;'>{avg_growth:.1f}%</div>
            <div style='font-size:12px;color:#555;'>Avg Growth Rate</div>
        </div>"""
    
    if customers is not None:
        total_customers = customers['customer_count'].sum()
        avg_satisfaction = customers['satisfaction'].mean()
        kpi_html += f"""<div style='background:#e8f5e9;padding:15px;border-radius:8px;border-left:4px solid #388e3c;'>
            <div style='font-size:24px;font-weight:bold;color:#388e3c;'>{total_customers:,.0f}</div>
            <div style='font-size:12px;color:#555;'>Total Customers</div>
        </div>
        <div style='background:#fbe9e7;padding:15px;border-radius:8px;border-left:4px solid #d84315;'>
            <div style='font-size:24px;font-weight:bold;color:#d84315;'>{avg_satisfaction:.1f}/5.0</div>
            <div style='font-size:12px;color:#555;'>Avg Satisfaction</div>
        </div>"""
    
    kpi_html += "</div>"
    return kpi_html

def generate_html_dashboard(sales, regional, products, customers, operations):
    """Generate comprehensive HTML dashboard."""
    overview_fig = create_overview_dashboard(sales, regional, products, customers, operations)
    sales_fig = create_sales_detail_dashboard(sales)
    regional_fig = create_regional_dashboard(regional)
    product_fig = create_product_dashboard(products)
    kpi_html = create_kpi_summary(sales, regional, products, customers, operations)
    
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Business Performance Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0;}
        body {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh;}
        .container {max-width: 1500px; margin: auto; background: white; border-radius: 10px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); padding: 30px;}
        h1 {color: #333; margin-bottom: 10px; text-align: center; font-size: 32px;}
        .subtitle {text-align: center; color: #666; margin-bottom: 30px; font-size: 14px;}
        .kpi-section {margin-bottom: 40px;}
        .nav-tabs {display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #ddd; flex-wrap: wrap;}
        .nav-tabs button {padding: 12px 24px; background: #f0f0f0; border: none; border-radius: 4px 4px 0 0; cursor: pointer; font-weight: 500; transition: all 0.3s; font-size: 14px;}
        .nav-tabs button.active {background: #667eea; color: white;}
        .nav-tabs button:hover {background: #667eea; color: white;}
        .tab-content {display: none; animation: fadeIn 0.3s;}
        .tab-content.active {display: block;}
        @keyframes fadeIn {from {opacity: 0;} to {opacity: 1;}}
        .footer {text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #999; font-size: 12px;}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Business Performance Dashboard</h1>
        <div class="subtitle">Real-time analytics for sales, revenue, regional performance, and customer insights</div>
        
        <div class="kpi-section">""" + kpi_html + """</div>
        
        <div class="nav-tabs">
            <button class="tab-button active" onclick="switchTab('overview')">📈 Overview</button>
            <button class="tab-button" onclick="switchTab('sales')">💰 Sales Analytics</button>
            <button class="tab-button" onclick="switchTab('regional')">🌍 Regional Performance</button>
            <button class="tab-button" onclick="switchTab('products')">📦 Product Analysis</button>
        </div>
        
        <div id="overview" class="tab-content active">
            <div id="overview-dashboard"></div>
        </div>
        <div id="sales" class="tab-content">
            <div id="sales-dashboard"></div>
        </div>
        <div id="regional" class="tab-content">
            <div id="regional-dashboard"></div>
        </div>
        <div id="products" class="tab-content">
            <div id="products-dashboard"></div>
        </div>
        
        <div class="footer">
            <p>Business Performance Dashboard | Generated with Plotly | Real-time Synthetic Data</p>
        </div>
    </div>
    
    <script>
        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(el => el.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
    </script>
"""
    
    html += "<script>\n" + "Plotly.newPlot('overview-dashboard', " + overview_fig.to_json() + ", {responsive: true});\n</script>\n"
    
    if sales_fig:
        html += "<script>\nPlotly.newPlot('sales-dashboard', " + sales_fig.to_json() + ", {responsive: true});\n</script>\n"
    if regional_fig:
        html += "<script>\nPlotly.newPlot('regional-dashboard', " + regional_fig.to_json() + ", {responsive: true});\n</script>\n"
    if product_fig:
        html += "<script>\nPlotly.newPlot('products-dashboard', " + product_fig.to_json() + ", {responsive: true});\n</script>\n"
    
    html += "</body></html>"
    
    out_path = BASE_PATH + "business_dashboard.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ Business dashboard saved: {out_path}")

if __name__ == '__main__':
    sales, regional, products, customers, operations = load_business_data()
    generate_html_dashboard(sales, regional, products, customers, operations)
    print("\n✅ Business dashboard created successfully!")
