# E-commerce Analytics Dashboard

A professional Streamlit dashboard for analyzing e-commerce business performance, featuring interactive visualizations and real-time data filtering.

## Overview

This project provides a comprehensive business intelligence solution featuring both Jupyter notebook analysis and a professional Streamlit dashboard for e-commerce sales data with configurable time periods and reusable business metrics calculations.

## Features

### Dashboard Layout Structure

- **Header**: Clean title with date range filter (top-left: title, top-right: date filter)
- **KPI Row**: Four key performance indicators with year-over-year trend analysis
  - Total Revenue with trend indicator
  - Monthly Growth percentage
  - Average Order Value with trend indicator
  - Total Orders with trend indicator
- **Charts Grid**: 2×2 visualization layout
  - **Revenue Trend Chart**: Line chart comparing current and previous year
    - Solid line for current period
    - Dashed line for previous period
    - Grid lines for easier reading
    - Y-axis formatted as $300K instead of $300,000
  - **Top 10 Categories**: Horizontal bar chart sorted descending
    - Blue gradient coloring (lighter for lower values)
    - Values formatted as $300K and $2M
  - **Revenue by State**: US choropleth map
    - Blue gradient color-coding by revenue amount
  - **Satisfaction vs Delivery Time**: Bar chart analysis
    - X-axis: Delivery time buckets (1-3 days, 4-7 days, 8+ days)
    - Y-axis: Average review score
- **Bottom Row**: Customer experience metrics
  - Average delivery time with trend indicator
  - Review Score card with star rating and subtitle

### Key Features

- **Interactive Filtering**: Year-based filtering that updates all metrics and visualizations
- **Trend Indicators**: Color-coded arrows showing performance changes
  - Green for positive trends
  - Red for negative trends
  - All trends show 2 decimal places
- **Professional Styling**: Clean, modern design with uniform card heights for each row
- **Responsive Charts**: Plotly-based interactive charts with hover details
- **Smart Formatting**: Currency values displayed as $300K, $2M for better readability

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify data files**: Ensure the `ecommerce_data/` directory contains:
   - orders_dataset.csv
   - order_items_dataset.csv
   - products_dataset.csv
   - customers_dataset.csv
   - order_reviews_dataset.csv
   - order_payments_dataset.csv

## Usage

### Running the Dashboard

1. **Navigate to the project directory**:
   ```bash
   cd lesson7_files
   ```

2. **Launch the Streamlit dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

3. **Access the dashboard**:
   - The dashboard will automatically open in your default web browser
   - Default URL: http://localhost:8501

### Using the Dashboard

1. **Select Date Range**: Use the dropdown in the top-right to filter data by year
2. **View KPIs**: Monitor key metrics with trend indicators showing year-over-year changes (2 decimal places)
3. **Analyze Charts**: Interact with visualizations to explore:
   - Monthly revenue trends compared to previous year
   - Top performing product categories with blue gradient
   - Geographic revenue distribution across US states
   - Relationship between delivery time and customer satisfaction
4. **Customer Experience**: Review delivery performance and customer ratings at the bottom

### Running the Jupyter Notebook

1. **Launch Jupyter**:
   ```bash
   jupyter notebook EDA_Refactored.ipynb
   ```

2. **Configure analysis parameters** in the first code cell:
   ```python
   ANALYSIS_YEAR = 2023        # Year to analyze
   COMPARISON_YEAR = 2022      # Comparison year (optional)
   ANALYSIS_MONTH = None       # Specific month or None for full year
   DATA_PATH = 'ecommerce_data/'
   ```

3. **Run all cells** to generate the complete analysis

## Project Structure

```
lesson7_files/
├── dashboard.py              # Main Streamlit dashboard application
├── data_loader.py           # Data loading and processing utilities
├── business_metrics.py      # Business metrics calculation module
├── EDA_Refactored.ipynb    # Source analysis notebook
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── ecommerce_data/         # Data directory
    ├── orders_dataset.csv
    ├── order_items_dataset.csv
    ├── products_dataset.csv
    ├── customers_dataset.csv
    ├── order_reviews_dataset.csv
    └── order_payments_dataset.csv
```

## Technical Details

### Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualizations
- **streamlit**: Web dashboard framework
- **matplotlib**: Additional plotting support
- **seaborn**: Statistical visualizations

### Data Processing Architecture

The dashboard uses a modular architecture:

1. **Data Loader** (`data_loader.py`):
   - Loads and cleans raw CSV files
   - Joins multiple datasets
   - Calculates delivery metrics
   - Provides filtered datasets based on user selection

2. **Business Metrics** (`business_metrics.py`):
   - Calculates revenue metrics and growth rates
   - Analyzes product and geographic performance
   - Computes customer satisfaction metrics
   - Generates delivery performance statistics

3. **Dashboard** (`dashboard.py`):
   - Renders interactive UI with Streamlit
   - Creates Plotly visualizations with specific formatting
   - Manages state and filtering
   - Applies professional styling with CSS

### Key Metrics Explained

- **Total Revenue**: Sum of all order item prices for delivered orders
- **Monthly Growth**: Average month-over-month revenue growth percentage
- **Average Order Value (AOV)**: Mean total value per order
- **Total Orders**: Count of unique delivered orders
- **Trend Indicators**: Year-over-year percentage change with 2 decimal precision
- **Delivery Time**: Days between order placement and customer delivery
- **Review Score**: Average customer rating (1-5 stars)

## Customization

### Changing the Default Year

Edit line 381 in `dashboard.py`:
```python
if 2023 in available_years:  # Change 2023 to your preferred default year
    default_year_index = available_years.index(2023)
```

### Modifying Color Schemes

Chart colors can be customized in the respective chart functions:
- **Revenue trend**: Lines 158, 173 (colors: #1f77b4, #ff7f0e)
- **Category chart**: Lines 228-231 (blue gradient RGB values)
- **State map**: Line 275 (colorscale='Blues')
- **Satisfaction chart**: Line 335 (color='#1f77b4')

### Adjusting Card Heights

Modify CSS in `dashboard.py`:
- **KPI cards**: Line 41 (`height: 140px`)
- **Bottom cards**: Line 82 (`height: 180px`)

### Adding New Metrics

1. Extend the `BusinessMetricsCalculator` class in `business_metrics.py`
2. Add visualization methods to create new charts
3. Update dashboard.py to display new metrics

## Troubleshooting

### Common Issues

1. **Module not found errors**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Data loading errors**:
   - Verify all CSV files exist in `ecommerce_data/` directory
   - Check file permissions
   - Ensure CSV files are not corrupted

3. **Port already in use**:
   ```bash
   streamlit run dashboard.py --server.port 8502
   ```

4. **Charts not displaying**:
   - Clear browser cache
   - Restart the Streamlit server
   - Check browser console for JavaScript errors

5. **Empty Results**:
   - Verify date filters match available data range
   - Check order status filtering (defaults to 'delivered')

## Performance Optimization

- **Data Caching**: The `@st.cache_data` decorator caches loaded data for faster filtering
- **Efficient Queries**: Groupby operations are optimized for large datasets
- **Lazy Loading**: Charts are only rendered when data is available
- **Modular Processing**: Data is processed only when filters change

## Module Usage

### Data Loading Module
```python
from data_loader import EcommerceDataLoader, load_and_process_data

# Quick start
loader, processed_data = load_and_process_data('ecommerce_data/')

# Create filtered dataset
sales_data = loader.create_sales_dataset(
    year_filter=2023,
    month_filter=None,
    status_filter='delivered'
)
```

### Business Metrics Module
```python
from business_metrics import BusinessMetricsCalculator, MetricsVisualizer

# Calculate metrics
metrics_calc = BusinessMetricsCalculator(sales_data)
report = metrics_calc.generate_comprehensive_report(
    current_year=2023,
    previous_year=2022
)

# Create visualizations
visualizer = MetricsVisualizer(report)
revenue_fig = visualizer.plot_revenue_trend()
```

## Future Enhancements

Potential improvements:
- Month-level filtering option
- Product-level drill-down capability
- Export functionality (PDF/Excel reports)
- Predictive analytics and forecasting
- Customer segmentation analysis
- Real-time data refresh capability
- A/B testing framework integration
- Mobile-responsive improvements

## Contributing

To extend this analysis framework:

1. Follow the existing code structure and documentation patterns
2. Add comprehensive docstrings to new functions
3. Include error handling for edge cases
4. Update this README with new features
5. Test with different data ranges

## License

This project is provided as-is for educational and business analysis purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the Streamlit documentation: https://docs.streamlit.io
3. Review the Plotly documentation: https://plotly.com/python/
4. Verify data format matches expected schema

---

**Dashboard Version**: 1.0
**Last Updated**: February 2026
**Built with**: Streamlit, Plotly, Pandas

**Note**: This framework is designed to be easily maintained and extended for ongoing business intelligence needs. The modular architecture ensures that updates to data sources or metric calculations can be made without affecting the overall analysis structure.
