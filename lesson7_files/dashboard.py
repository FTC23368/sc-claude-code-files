"""
E-commerce Business Analytics Dashboard
A professional Streamlit dashboard for business performance analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings

# Import custom modules
from data_loader import EcommerceDataLoader, load_and_process_data
from business_metrics import BusinessMetricsCalculator

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }

    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        margin: 0.3rem 0;
        color: #1f1f1f;
    }

    .metric-label {
        font-size: 0.95rem;
        color: #666;
        margin: 0;
        margin-bottom: 0.3rem;
        font-weight: 500;
    }

    .metric-trend {
        font-size: 0.85rem;
        margin: 0;
        margin-top: 0.3rem;
    }

    .trend-positive {
        color: #28a745;
    }

    .trend-negative {
        color: #dc3545;
    }

    .bottom-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .bottom-card .metric-value {
        font-size: 2.5rem;
    }

    .bottom-card .metric-label {
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    .stars {
        color: #ffc107;
        font-size: 1.5rem;
        margin-top: 0.5rem;
    }

    .stSelectbox > div > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_dashboard_data():
    """Load and cache data for dashboard"""
    try:
        loader, processed_data = load_and_process_data('ecommerce_data/')
        return loader, processed_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None


def format_currency(value):
    """Format currency values with K/M suffixes"""
    if abs(value) >= 1e6:
        return f"${value/1e6:.1f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.0f}K"
    else:
        return f"${value:.0f}"


def format_trend(current, previous):
    """Format trend indicators with arrows and colors (2 decimal places)"""
    if previous == 0 or pd.isna(previous):
        return "N/A"

    change_pct = ((current - previous) / previous) * 100
    arrow = "↗" if change_pct > 0 else "↘"
    color_class = "trend-positive" if change_pct > 0 else "trend-negative"

    return f'<span class="{color_class}">{arrow} {abs(change_pct):.2f}%</span>'


def create_revenue_trend_chart(current_data, previous_data, current_year, previous_year):
    """Create revenue trend line chart with current and previous period"""
    fig = go.Figure()

    # Current period - solid line
    current_monthly = current_data.groupby('purchase_month')['price'].sum().reset_index()
    current_monthly = current_monthly.sort_values('purchase_month')

    fig.add_trace(go.Scatter(
        x=current_monthly['purchase_month'],
        y=current_monthly['price'],
        mode='lines+markers',
        name=f'{current_year}',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8),
        hovertemplate='Month %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ))

    # Previous period - dashed line
    if previous_data is not None and not previous_data.empty:
        previous_monthly = previous_data.groupby('purchase_month')['price'].sum().reset_index()
        previous_monthly = previous_monthly.sort_values('purchase_month')

        fig.add_trace(go.Scatter(
            x=previous_monthly['purchase_month'],
            y=previous_monthly['price'],
            mode='lines+markers',
            name=f'{previous_year}',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            marker=dict(size=8),
            hovertemplate='Month %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        ))

    fig.update_layout(
        title="Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue",
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            tickmode='linear',
            dtick=1
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            tickformat='$,.0s',
            ticksuffix='',
        ),
        height=350,
        margin=dict(t=50, b=50, l=60, r=50),
        font=dict(size=12)
    )

    # Custom format for y-axis to show $300K format
    fig.update_yaxes(tickformat='$.2s')

    return fig


def create_category_chart(sales_data):
    """Create top 10 categories bar chart sorted descending with blue gradient"""
    if 'product_category_name' not in sales_data.columns:
        return go.Figure().add_annotation(
            text="Product category data not available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )

    # Get top 10 categories sorted descending
    category_revenue = sales_data.groupby('product_category_name')['price'].sum().sort_values(ascending=True).tail(10)

    # Create blue gradient colors (light for lower values, darker for higher)
    colors = []
    min_val = category_revenue.min()
    max_val = category_revenue.max()

    for val in category_revenue.values:
        # Normalize value between 0 and 1
        normalized = (val - min_val) / (max_val - min_val) if max_val != min_val else 0.5
        # Create RGB color from light blue to dark blue
        r = int(173 - (173 - 31) * normalized)
        g = int(216 - (216 - 119) * normalized)
        b = int(230 - (230 - 180) * normalized)
        colors.append(f'rgb({r},{g},{b})')

    fig = go.Figure(data=[
        go.Bar(
            y=category_revenue.index,
            x=category_revenue.values,
            orientation='h',
            marker=dict(color=colors),
            text=[format_currency(x) for x in category_revenue.values],
            textposition='outside',
            hovertemplate='%{y}<br>Revenue: %{text}<extra></extra>'
        )
    ])

    fig.update_layout(
        title="Top 10 Product Categories",
        xaxis_title="Revenue",
        yaxis_title="",
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', tickformat='$.2s'),
        yaxis=dict(showgrid=False),
        height=350,
        margin=dict(t=50, b=50, l=150, r=80),
        font=dict(size=12)
    )

    return fig


def create_state_map(sales_data):
    """Create US choropleth map with blue gradient"""
    if 'customer_state' not in sales_data.columns:
        return go.Figure().add_annotation(
            text="Geographic data not available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )

    state_revenue = sales_data.groupby('customer_state')['price'].sum().reset_index()
    state_revenue.columns = ['state', 'revenue']

    fig = go.Figure(data=go.Choropleth(
        locations=state_revenue['state'],
        z=state_revenue['revenue'],
        locationmode='USA-states',
        colorscale='Blues',
        showscale=True,
        colorbar=dict(
            title="Revenue",
            tickformat='$.2s',
            len=0.7
        ),
        hovertemplate='%{location}<br>Revenue: $%{z:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title="Revenue by State",
        geo_scope='usa',
        height=350,
        margin=dict(t=50, b=20, l=20, r=20),
        font=dict(size=12)
    )

    return fig


def create_satisfaction_delivery_chart(sales_data):
    """Create satisfaction vs delivery time bar chart"""
    if 'delivery_days' not in sales_data.columns or 'review_score' not in sales_data.columns:
        return go.Figure().add_annotation(
            text="Delivery or review data not available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )

    # Categorize delivery days
    def categorize_delivery(days):
        if pd.isna(days):
            return 'Unknown'
        elif days <= 3:
            return '1-3 days'
        elif days <= 7:
            return '4-7 days'
        else:
            return '8+ days'

    sales_data_copy = sales_data.copy()
    sales_data_copy['delivery_category'] = sales_data_copy['delivery_days'].apply(categorize_delivery)

    # Calculate average review score by delivery category
    delivery_satisfaction = sales_data_copy.groupby('delivery_category')['review_score'].mean().reset_index()
    delivery_satisfaction = delivery_satisfaction[delivery_satisfaction['delivery_category'] != 'Unknown']

    # Order categories properly
    category_order = ['1-3 days', '4-7 days', '8+ days']
    delivery_satisfaction['delivery_category'] = pd.Categorical(
        delivery_satisfaction['delivery_category'],
        categories=category_order,
        ordered=True
    )
    delivery_satisfaction = delivery_satisfaction.sort_values('delivery_category')

    fig = go.Figure(data=[
        go.Bar(
            x=delivery_satisfaction['delivery_category'],
            y=delivery_satisfaction['review_score'],
            marker=dict(color='#1f77b4'),
            text=[f'{x:.2f}' for x in delivery_satisfaction['review_score']],
            textposition='outside',
            hovertemplate='%{x}<br>Avg Review: %{y:.2f}<extra></extra>'
        )
    ])

    fig.update_layout(
        title="Customer Satisfaction vs Delivery Time",
        xaxis_title="Delivery Time",
        yaxis_title="Average Review Score",
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', range=[0, 5]),
        height=350,
        margin=dict(t=50, b=50, l=50, r=50),
        font=dict(size=12)
    )

    return fig


def main():
    """Main dashboard function"""

    # Load data
    loader, processed_data = load_dashboard_data()

    if loader is None:
        st.error("Failed to load data. Please check your data files.")
        return

    # Header with title and date filters
    header_col1, header_col2 = st.columns([3, 1])

    with header_col1:
        st.title("E-commerce Analytics Dashboard")

    with header_col2:
        # Get available years from data
        orders_data = processed_data['orders']
        available_years = sorted(orders_data['purchase_year'].unique(), reverse=True)

        # Set default year to 2023 if available
        default_year_index = 0
        if 2023 in available_years:
            default_year_index = available_years.index(2023)

        selected_year = st.selectbox(
            "Date Range",
            options=available_years,
            index=default_year_index,
            key="year_filter"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Create datasets based on selected year
    current_data = loader.create_sales_dataset(
        year_filter=selected_year,
        status_filter='delivered'
    )

    previous_year = selected_year - 1
    previous_data = None
    if previous_year in available_years:
        previous_data = loader.create_sales_dataset(
            year_filter=previous_year,
            status_filter='delivered'
        )

    # Calculate metrics
    total_revenue = current_data['price'].sum()
    total_orders = current_data['order_id'].nunique()
    avg_order_value = current_data.groupby('order_id')['price'].sum().mean()

    # Calculate previous year metrics for trends
    prev_revenue = previous_data['price'].sum() if previous_data is not None and not previous_data.empty else 0
    prev_orders = previous_data['order_id'].nunique() if previous_data is not None and not previous_data.empty else 0
    prev_aov = previous_data.groupby('order_id')['price'].sum().mean() if previous_data is not None and not previous_data.empty else 0

    # Monthly growth calculation
    monthly_data = current_data.groupby('purchase_month')['price'].sum()
    if len(monthly_data) > 1:
        monthly_growth = monthly_data.pct_change().mean() * 100
    else:
        # If only one month, compare with previous year same month
        if previous_data is not None and not previous_data.empty:
            current_month = current_data['purchase_month'].iloc[0]
            prev_same_month = previous_data[previous_data['purchase_month'] == current_month]['price'].sum()
            current_month_revenue = current_data['price'].sum()
            monthly_growth = ((current_month_revenue - prev_same_month) / prev_same_month * 100) if prev_same_month > 0 else 0
        else:
            monthly_growth = 0

    # KPI Row - 4 cards with uniform height
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        trend_html = format_trend(total_revenue, prev_revenue)
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Total Revenue</p>
            <p class="metric-value">{format_currency(total_revenue)}</p>
            <p class="metric-trend">{trend_html}</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        color_class = "trend-positive" if monthly_growth > 0 else "trend-negative"
        arrow = "↗" if monthly_growth > 0 else "↘"
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Monthly Growth</p>
            <p class="metric-value">{monthly_growth:.2f}%</p>
            <p class="metric-trend"><span class="{color_class}">{arrow}</span></p>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        trend_html = format_trend(avg_order_value, prev_aov)
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Average Order Value</p>
            <p class="metric-value">{format_currency(avg_order_value)}</p>
            <p class="metric-trend">{trend_html}</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        trend_html = format_trend(total_orders, prev_orders)
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Total Orders</p>
            <p class="metric-value">{total_orders:,}</p>
            <p class="metric-trend">{trend_html}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Grid - 2x2 layout
    chart_row1_col1, chart_row1_col2 = st.columns(2)

    with chart_row1_col1:
        revenue_fig = create_revenue_trend_chart(current_data, previous_data, selected_year, previous_year)
        st.plotly_chart(revenue_fig, width='stretch')

    with chart_row1_col2:
        category_fig = create_category_chart(current_data)
        st.plotly_chart(category_fig, width='stretch')

    chart_row2_col1, chart_row2_col2 = st.columns(2)

    with chart_row2_col1:
        map_fig = create_state_map(current_data)
        st.plotly_chart(map_fig, width='stretch')

    with chart_row2_col2:
        satisfaction_fig = create_satisfaction_delivery_chart(current_data)
        st.plotly_chart(satisfaction_fig, width='stretch')

    st.markdown("<br>", unsafe_allow_html=True)

    # Bottom Row - 2 cards with uniform height
    bottom_col1, bottom_col2 = st.columns(2)

    with bottom_col1:
        # Average delivery time with trend
        if 'delivery_days' in current_data.columns:
            avg_delivery = current_data['delivery_days'].mean()
            prev_delivery = previous_data['delivery_days'].mean() if previous_data is not None and not previous_data.empty else 0
            delivery_trend = format_trend(avg_delivery, prev_delivery)

            st.markdown(f"""
            <div class="bottom-card">
                <p class="metric-label">Average Delivery Time</p>
                <p class="metric-value">{avg_delivery:.1f} days</p>
                <p class="metric-trend">{delivery_trend}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="bottom-card">
                <p class="metric-label">Average Delivery Time</p>
                <p class="metric-value">N/A</p>
                <p class="metric-trend">Data not available</p>
            </div>
            """, unsafe_allow_html=True)

    with bottom_col2:
        # Review score with stars
        if 'review_score' in current_data.columns:
            avg_review = current_data['review_score'].mean()
            stars = "★" * int(round(avg_review))

            st.markdown(f"""
            <div class="bottom-card">
                <p class="metric-value">{avg_review:.1f}/5.0</p>
                <p class="stars">{stars}</p>
                <p class="metric-label">Average Review Score</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="bottom-card">
                <p class="metric-value">N/A</p>
                <p class="metric-label">Average Review Score</p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
