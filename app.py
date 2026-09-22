"""
NovaMart Analytics — app.py
----------------------------
Folder structure expected:

novamart-streamlit/
├── app.py
├── requirements.txt
└── data/
    └── novamart_cleaned_master.csv   <-- put your CSV here (check the exact filename!)

RUN:
    pip install -r requirements.txt
    streamlit run app.py
"""

import os
import pandas as pd
import streamlit as st
import plotly.express as px

# ======================================================================
# PAGE CONFIG
# ======================================================================
st.set_page_config(
    page_title="NovaMart Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================================
# NUDE THEME + SMOOTH TRANSITIONS (custom CSS)
# ======================================================================
st.markdown(
    """
    <style>
    :root{
        --nude-bg:#F3E7DA;
        --nude-panel:#FBF4EC;
        --nude-card:#FFFDFB;
        --nude-accent:#B08968;
        --nude-accent-dark:#8A5A44;
        --nude-text:#3E2C23;
        --nude-border:#E4D4C3;
    }

    .stApp{
        background-color: var(--nude-bg);
        color: var(--nude-text);
    }

    section[data-testid="stSidebar"]{
        background-color: var(--nude-panel);
        border-right: 1px solid var(--nude-border);
    }

    h1, h2, h3, h4, h5, h6 { color: var(--nude-accent-dark) !important; }

    /* Force dark, readable text everywhere on the nude background */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li,
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricDelta"],
    div[data-testid="stCaptionContainer"],
    .stSelectbox div, .stMultiSelect div, .stRadio div,
    .stDateInput div, .stSlider div,
    section[data-testid="stSidebar"] * {
        color: var(--nude-text) !important;
    }

    /* Keep the header banner text light since its background is dark */
    .project-header, .project-header h1, .project-header p{
        color: #FFF8F0 !important;
    }

    /* Keep buttons' own text light against their accent background */
    .stButton>button, .stDownloadButton>button{
        color: #FFF8F0 !important;
    }

    /* Header banner */
    .project-header{
        background: linear-gradient(90deg, var(--nude-accent) 0%, var(--nude-accent-dark) 100%);
        padding: 22px 30px;
        border-radius: 14px;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px rgba(139, 90, 68, 0.25);
        transition: box-shadow .25s ease, transform .25s ease;
    }
    .project-header:hover{
        box-shadow: 0 8px 22px rgba(139, 90, 68, 0.35);
        transform: translateY(-2px);
    }
    .project-header h1{
        color: #FFF8F0 !important;
        margin: 0;
        font-size: 28px;
        letter-spacing: .5px;
    }
    .project-header p{
        color: #F3E3D3;
        margin: 4px 0 0 0;
        font-size: 14px;
    }

    /* KPI cards */
    div[data-testid="stMetric"]{
        background-color: var(--nude-card);
        border: 1px solid var(--nude-border);
        border-radius: 12px;
        padding: 16px 14px 10px 14px;
        box-shadow: 0 2px 6px rgba(62, 44, 35, 0.06);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    div[data-testid="stMetric"]:hover{
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(62, 44, 35, 0.14);
    }
    div[data-testid="stMetricLabel"]{ color: var(--nude-accent-dark) !important; }

    /* Panels (chart card / options card) */
    .panel-card{
        background-color: var(--nude-panel);
        border: 1px solid var(--nude-border);
        border-radius: 14px;
        padding: 18px 20px;
        transition: box-shadow .2s ease;
    }
    .panel-card:hover{ box-shadow: 0 6px 18px rgba(62, 44, 35, 0.10); }

    /* Buttons */
    .stButton>button, .stDownloadButton>button{
        background-color: var(--nude-accent);
        color: #FFF8F0;
        border: none;
        border-radius: 8px;
        padding: 8px 18px;
        transition: background-color .18s ease, transform .12s ease;
    }
    .stButton>button:hover, .stDownloadButton>button:hover{
        background-color: var(--nude-accent-dark);
        transform: translateY(-1px);
    }

    /* Dataframe container */
    div[data-testid="stDataFrame"]{
        border: 1px solid var(--nude-border);
        border-radius: 10px;
        overflow: hidden;
    }

    /* Smooth scroll + general transitions */
    * { transition: background-color .15s ease, color .15s ease; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ======================================================================
# LOAD DATA
# ======================================================================
CANDIDATE_PATHS = [
    "data/novamart_cleaned_master.csv",
    "data/novamart_cleand_master.csv",   # fallback in case of the typo'd filename
    "novamart_cleaned_master.csv",
]

@st.cache_data
def load_data(path):
    return pd.read_csv(path, parse_dates=["order_date", "signup_date", "launch_date"])

csv_path = next((p for p in CANDIDATE_PATHS if os.path.exists(p)), None)

if csv_path is None:
    st.error(
        "Couldn't find the CSV. Place it at `data/novamart_cleaned_master.csv` "
        "(double check the spelling) and rerun the app."
    )
    st.stop()

df = load_data(csv_path)

# ======================================================================
# HEADER
# ======================================================================
st.markdown(
    """
    <div class="project-header">
        <h1>🛍️ NovaMart Analytics</h1>
        <p>Interactive sales, profitability & operations dashboard</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ======================================================================
# LEFT SIDEBAR — "all tables where we can select from here"
# ======================================================================
st.sidebar.header("📊 Select View")

VIEW_OPTIONS = {
    "Category":            "category",
    "Sub-category":        "subcategory",
    "State":                "state",
    "City":                 "city",
    "Sales Channel":        "sales_channel",
    "Payment Method":       "payment_method",
    "Customer Segment":     "segment",
    "Gender":               "gender",
    "Acquisition Channel":  "acquisition_channel",
    "Discount Band":        "discount_band",
    "Delivery Bucket":      "delivery_bucket",
    "Monthly Trend":        "month_year",
}

view_label = st.sidebar.radio("Table / dimension", list(VIEW_OPTIONS.keys()), index=0)
view_col = VIEW_OPTIONS[view_label]

st.sidebar.divider()
st.sidebar.header("🧰 Filters")

min_date, max_date = df["order_date"].min(), df["order_date"].max()
date_range = st.sidebar.date_input("Order date range", (min_date, max_date), min_date, max_date)

status_filter = st.sidebar.multiselect("Order status", sorted(df["order_status"].dropna().unique()))
category_filter = st.sidebar.multiselect("Category", sorted(df["category"].dropna().unique()))

filtered = df.copy()
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[(filtered["order_date"] >= start) & (filtered["order_date"] <= end)]
if status_filter:
    filtered = filtered[filtered["order_status"].isin(status_filter)]
if category_filter:
    filtered = filtered[filtered["category"].isin(category_filter)]

st.sidebar.caption(f"{len(filtered):,} rows match current filters")

# ======================================================================
# KPI CARDS
# ======================================================================
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Net Revenue", f"₹{filtered['net_revenue'].sum():,.0f}")
k2.metric("Profit", f"₹{filtered['profit'].sum():,.0f}")
k3.metric("Avg Margin", f"{filtered['profit_margin'].mean():.1f}%")
k4.metric("Orders", f"{filtered['order_id'].nunique():,}")
k5.metric("Avg Rating", f"{filtered['rating'].mean():.2f} ★")

st.write("")

# ======================================================================
# CENTER (chart + table) | RIGHT (chart/analysis options)
# ======================================================================
center, right = st.columns((3, 1))

with right:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.subheader("⚙️ Analysis Options")

    METRIC_OPTIONS = {
        "Net Revenue (Sum)":    ("net_revenue", "sum"),
        "Profit (Sum)":         ("profit", "sum"),
        "Profit Margin (Avg)":  ("profit_margin", "mean"),
        "Quantity (Sum)":       ("quantity", "sum"),
        "Orders (Count)":       ("order_id", "nunique"),
        "Avg Rating":           ("rating", "mean"),
        "Avg Delivery Days":    ("delivery_days", "mean"),
    }
    metric_label = st.selectbox("Metric", list(METRIC_OPTIONS.keys()))
    metric_col, agg_func = METRIC_OPTIONS[metric_label]

    chart_type = st.selectbox("Chart type", ["Bar", "Line", "Area", "Pie", "Donut"])
    top_n = st.slider("Show top N categories", 5, 30, 12)
    st.markdown("</div>", unsafe_allow_html=True)

with center:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.subheader(f"{view_label} — {metric_label}")

    grouped = (
        filtered.groupby(view_col)[metric_col]
        .agg(agg_func)
        .reset_index()
        .rename(columns={metric_col: metric_label})
    )

    # keep chronological order for the monthly trend view, otherwise sort by value
    if view_col == "month_year":
        grouped = grouped.sort_values(view_col)
    else:
        grouped = grouped.sort_values(metric_label, ascending=False).head(top_n)

    DARK_TEXT = "#3E2C23"
    BAR_COLOR = "#A9714E"          # solid muted terracotta — reads clearly on nude bg, doesn't wash out
    PIE_PALETTE = ["#A9714E", "#C9986B", "#8A5A44", "#D8B48F", "#6E4A38", "#E3C6A3", "#5C3C2E"]

    if chart_type == "Bar":
        fig = px.bar(
            grouped, x=view_col, y=metric_label,
            color_discrete_sequence=[BAR_COLOR],
            text_auto=".2s",
        )
        fig.update_traces(
            textposition="outside",
            textfont=dict(color=DARK_TEXT, size=12),
            marker_line_color="#8A5A44",
            marker_line_width=1,
        )
    elif chart_type == "Line":
        fig = px.line(grouped, x=view_col, y=metric_label, markers=True,
                       color_discrete_sequence=[BAR_COLOR])
    elif chart_type == "Area":
        fig = px.area(grouped, x=view_col, y=metric_label,
                       color_discrete_sequence=[BAR_COLOR])
    elif chart_type == "Pie":
        fig = px.pie(grouped, names=view_col, values=metric_label,
                      color_discrete_sequence=PIE_PALETTE)
    else:  # Donut
        fig = px.pie(grouped, names=view_col, values=metric_label, hole=0.5,
                      color_discrete_sequence=PIE_PALETTE)

    if chart_type in ("Pie", "Donut"):
        fig.update_traces(textfont=dict(color="#FFF8F0", size=12))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=DARK_TEXT, size=13),
        title_font_color=DARK_TEXT,
        legend=dict(font=dict(color=DARK_TEXT)),
        xaxis=dict(
            title_font=dict(color=DARK_TEXT),
            tickfont=dict(color=DARK_TEXT),
            gridcolor="#E4D4C3",
            linecolor="#C9AF95",
        ),
        yaxis=dict(
            title_font=dict(color=DARK_TEXT),
            tickfont=dict(color=DARK_TEXT),
            gridcolor="#E4D4C3",
            linecolor="#C9AF95",
        ),
        margin=dict(t=30, l=10, r=10, b=10),
        transition_duration=400,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### Summary table")
    st.dataframe(grouped, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ======================================================================
# BOTTOM — "select columns from here" (detailed raw data table)
# ======================================================================
st.markdown('<div class="panel-card">', unsafe_allow_html=True)
st.subheader("📋 Detailed Data")

default_cols = [
    "order_id", "order_date", "category", "subcategory", "product_name",
    "state", "quantity", "net_revenue", "profit", "profit_margin",
]
default_cols = [c for c in default_cols if c in filtered.columns]

selected_cols = st.multiselect(
    "Select columns from here",
    options=list(filtered.columns),
    default=default_cols,
)

if selected_cols:
    detail_df = filtered[selected_cols]
    st.dataframe(detail_df, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download this table as CSV",
        detail_df.to_csv(index=False).encode("utf-8"),
        "novamart_filtered_data.csv",
        "text/csv",
    )
else:
    st.info("Pick at least one column above to preview and download the data.")

st.markdown("</div>", unsafe_allow_html=True)
