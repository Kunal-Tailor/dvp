import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

# Backend endpoints
API_BASE = os.environ.get("API_BASE", "http://localhost:5000/api")

@st.cache_data(show_spinner=False)
def fetch_json(path: str, params: dict | None = None):
    import requests
    try:
        resp = requests.get(f"{API_BASE}{path}", params=params, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.warning(f"API error: {e}")
        return None

st.set_page_config(
    page_title="IndianPulse - Streamlit",
    page_icon="📊",
    layout="wide",
)

st.sidebar.title("IndianPulse 📊")

# Sidebar - indicator selection
meta = fetch_json("/metadata") or {}
indicator_keys = list(meta.keys())
name_by_key = {k: meta[k]["name"] for k in indicator_keys}
key_by_name = {v: k for k, v in name_by_key.items()}

selected_name = st.sidebar.selectbox("Dataset", [name_by_key[k] for k in indicator_keys]) if indicator_keys else None
selected_key = key_by_name.get(selected_name)

# Sidebar - time range
range_label_to_value = {"3M": "3M", "1Y": "1Y", "2Y": "2Y", "5Y": "5Y", "Max": "MAX"}
selected_range = st.sidebar.select_slider("Time Range", options=list(range_label_to_value.keys()), value="1Y")

# Sidebar - chart type
chart_type = st.sidebar.selectbox("Chart Type", ["Line", "Bar", "Area", "Scatter"], index=0)

# Optional filters depending on dataset
params: dict[str, str] = {}
filters = {}
if selected_key and selected_key in meta and "filters" in meta[selected_key]:
    filters = meta[selected_key]["filters"]
    regions = filters.get("regions")
    states = filters.get("states")
    payment_modes = filters.get("payment_modes")
    metrics = filters.get("metrics")
    if regions:
        region = st.sidebar.selectbox("Region", ["All"] + regions)
        if region and region != "All":
            params["region"] = region
    if states:
        state = st.sidebar.selectbox("State", ["All"] + states)
        if state and state != "All":
            params["state"] = state
    if payment_modes:
        mode = st.sidebar.selectbox("Payment Mode", ["All"] + payment_modes)
        if mode and mode != "All":
            params["payment_mode"] = mode
    if metrics:
        metric = st.sidebar.radio("Metric", metrics, horizontal=True)
        params["metric"] = metric

# Fetch data
if selected_key:
    params["range"] = range_label_to_value[selected_range]
    data = fetch_json(f"/data/{selected_key}", params=params)
else:
    data = None

st.title("IndianPulse - Economic Dashboard (Streamlit)")

col1, col2 = st.columns([2, 1])

with col1:
    if data and data.get("labels"):
        df = pd.DataFrame({"date": data["labels"], "value": data["data"]})
        title = f"{selected_name}"
        unit = data.get("unit", "")
        if chart_type == "Line":
            fig = px.line(df, x="date", y="value", title=title)
        elif chart_type == "Bar":
            fig = px.bar(df, x="date", y="value", title=title)
        elif chart_type == "Area":
            fig = px.area(df, x="date", y="value", title=title)
        else:
            fig = px.scatter(df, x="date", y="value", title=title)
        fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
        fig.update_yaxes(title=unit)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select a dataset to view the chart.")

with col2:
    st.subheader("Summary Metrics")
    if data and data.get("stats"):
        stats = data["stats"]
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Latest", f"{stats['latest']}")
            st.metric("Highest", f"{stats['highest']}")
        with c2:
            st.metric("Lowest", f"{stats['lowest']}")
            st.metric("Average", f"{stats['average']}")
        st.metric("Change", f"{stats['change']}")
    else:
        st.write("No stats available.")

st.divider()

# Correlation Heatmap
st.subheader("Correlation Heatmap (select indicators)")
all_names = [name_by_key[k] for k in indicator_keys]
selected_compare = st.multiselect("Indicators", all_names, default=[name_by_key.get("gdp"), name_by_key.get("cpi"), name_by_key.get("iip")])
sel_keys = [key_by_name[n] for n in selected_compare if n in key_by_name]
if sel_keys:
    corr_resp = fetch_json("/correlation", params={"indicators": ",".join(sel_keys)})
    if corr_resp and corr_resp.get("correlation"):
        corr_df = pd.DataFrame(corr_resp["correlation"]).reindex(index=corr_resp["columns"], columns=corr_resp["columns"])  # square
        fig = px.imshow(corr_df, text_auto=True, color_continuous_scale="RdBu", zmin=-1, zmax=1)
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Correlation unavailable for selection.")

# Data export
if selected_key:
    csv_url = f"{API_BASE}/export/{selected_key}"
    st.download_button("Download CSV", data=csv_url, file_name=f"{selected_key}_export.csv")
