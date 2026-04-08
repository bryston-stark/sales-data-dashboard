import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Retail Dashboard", layout="wide")

@st.cache_data
def load_data():
    customers = pd.read_csv("customers.csv")
    orders = pd.read_csv("orders.csv")
    returns = pd.read_csv("returns.csv")

    df = orders.merge(customers, on="Customer ID", how="left")
    df = df.merge(returns.assign(Returned_Flag=1), on="Order ID", how="left")

    df["Returned_Flag"] = df["Returned_Flag"].fillna(0).astype(int)
    df["Returned"] = df["Returned"].fillna("No")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%y", errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%y", errors="coerce")
    return df

df = load_data()

st.title("Retail Data Dashboard")
st.caption("Streamlit app with Plotly charts and sidebar filters for region, category, and date range.")

st.sidebar.header("Filters")

region_options = ["All"] + sorted(df["Region"].dropna().unique().tolist())
category_options = ["All"] + sorted(df["Category"].dropna().unique().tolist())

selected_region = st.sidebar.selectbox("Region", region_options)
selected_category = st.sidebar.selectbox("Category", category_options)

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df.copy()

if selected_region != "All":
    filtered = filtered[filtered["Region"] == selected_region]

if selected_category != "All":
    filtered = filtered[filtered["Category"] == selected_category]

filtered = filtered[
    (filtered["Order Date"].dt.date >= start_date) &
    (filtered["Order Date"].dt.date <= end_date)
]

unique_orders = filtered["Order ID"].nunique()
returned_orders = filtered.loc[filtered["Returned_Flag"] == 1, "Order ID"].nunique()
return_rate = (returned_orders / unique_orders) if unique_orders else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
k2.metric("Total Profit", f"${filtered['Profit'].sum():,.0f}")
k3.metric("Unique Orders", f"{unique_orders:,}")
k4.metric("Return Rate", f"{return_rate:.1%}")
k5.metric("Avg Discount", f"{filtered['Discount'].mean():.1%}" if len(filtered) else "0.0%")

monthly_sales = (
    filtered
    .dropna(subset=["Order Date"])
    .set_index("Order Date")
    .resample("ME")["Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Over Time"
)

fig_box = px.box(
    filtered,
    x="Category",
    y="Profit",
    points="outliers",
    title="Profit by Category"
)

sales_by_region = filtered.groupby("Region", as_index=False)["Sales"].sum()
fig_region = px.bar(
    sales_by_region,
    x="Region",
    y="Sales",
    title="Total Sales by Region"
)

sales_by_segment = filtered.groupby("Segment", as_index=False)["Sales"].sum()
fig_segment = px.pie(
    sales_by_segment,
    names="Segment",
    values="Sales",
    hole=0.45,
    title="Sales by Segment"
)

returns_by_category = (
    filtered.groupby("Category")
    .agg(
        rows=("Order ID", "count"),
        returned=("Returned_Flag", "sum")
    )
    .reset_index()
)
returns_by_category["Return Rate"] = returns_by_category["returned"] / returns_by_category["rows"]

fig_returns = px.bar(
    returns_by_category,
    x="Category",
    y="Return Rate",
    title="Return Rate by Category"
)

top_subcats = (
    filtered.groupby("Sub-Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_subcats = px.bar(
    top_subcats.sort_values("Sales"),
    x="Sales",
    y="Sub-Category",
    orientation="h",
    title="Top 10 Sub-Categories by Sales"
)

row1_col1, row1_col2 = st.columns([2, 1])
with row1_col1:
    st.plotly_chart(fig_monthly, use_container_width=True)
with row1_col2:
    st.plotly_chart(fig_region, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.plotly_chart(fig_box, use_container_width=True)
with row2_col2:
    st.plotly_chart(fig_segment, use_container_width=True)

row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    st.plotly_chart(fig_returns, use_container_width=True)
with row3_col2:
    st.plotly_chart(fig_subcats, use_container_width=True)

st.subheader("Filtered Summary Table")
summary_table = (
    filtered.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Avg_Discount=("Discount", "mean"),
        Return_Rate=("Returned_Flag", "mean")
    )
    .reset_index()
)

st.dataframe(summary_table, use_container_width=True)

st.subheader("Filtered Data Preview")
st.dataframe(filtered.head(50), use_container_width=True)

st.markdown(
    '''
    **Run locally**
    1. Put `app.py`, `customers.csv`, `orders.csv`, and `returns.csv` in the same folder  
    2. Install dependencies: `pip install streamlit plotly pandas`  
    3. Start the app: `streamlit run app.py`
    '''
)
