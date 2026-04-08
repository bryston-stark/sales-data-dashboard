# Retail Data Dashboard (Streamlit)

## Overview
This project is an interactive data dashboard built using **Streamlit** and **Plotly**.  
It analyzes retail data across customers, orders, and returns to provide insights into sales performance, profitability, and return behavior.

---

## Features
- Interactive dashboard with sidebar filters:
  - Region
  - Category
  - Date range
- KPI metrics:
  - Total Sales
  - Total Profit
  - Unique Orders
  - Return Rate
  - Average Discount
- Visualizations:
  - Monthly Sales Trend (Line Chart)
  - Profit by Category (Box Plot)
  - Sales by Region (Bar Chart)
  - Sales by Segment (Pie Chart)
  - Return Rate by Category
  - Top Sub-Categories by Sales
- Summary table and filtered data preview

---

## Files Included
- `app.py` → Streamlit dashboard application  
- `customers.csv`, `orders.csv`, `returns.csv` → Dataset files  
- `requirements.txt` → Required Python packages  
- `README.md` → Project documentation  

---

## Installation & Setup

1. Clone or download the project folder

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

---

## Usage
- Use the sidebar to filter data by region, category, and date range
- Interact with charts (hover, zoom, click)
- View updated KPIs and tables based on selected filters

---

## Notes
- Ensure all CSV files are in the same directory as `app.py`
- No database or server setup required
- Designed for local execution

---

## Author
Created for academic data analysis and dashboarding assignment.
