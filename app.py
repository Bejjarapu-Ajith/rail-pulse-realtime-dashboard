import streamlit as st
import pandas as pd
from pydruid.db import connect
import altair as alt
from datetime import datetime
import time

# ---------- Streamlit Page Config ----------
st.set_page_config(
    page_title="🚄 Live Train Dashboard",
    page_icon="🚄",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    h1, h2, h3, h4, h5, h6, p {
        color: #66fcf1;
        font-family: 'Arial Black', sans-serif;
    }
    .stButton>button {
        background-color: #1f2833;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .stTextInput>div>div>input {
        background-color: #1f2833;
        color: white;
    }
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("<h1 style='text-align: center;'>🚂 RailPulse: Real-Time Train Dashboard 🚂</h1>", unsafe_allow_html=True)
clock_placeholder = st.empty()

# ---------- Connect to Druid ----------
conn = connect(
    host='localhost',
    port=8888,
    path='/druid/v2/sql/',
    scheme='http'
)
cursor = conn.cursor()

# ---------- Load Data from Druid ----------
def load_data():
    sql = """
    SELECT *
    FROM trains_data
    WHERE __time >= CURRENT_TIMESTAMP - INTERVAL '12' HOUR
    ORDER BY __time DESC
    LIMIT 100
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    return pd.DataFrame(result, columns=cols)

# ---------- Highlight Train Status ----------
def highlight_status(val):
    if val == "On Time":
        return "background-color: #28a745; color: white"
    elif val == "Delayed":
        return "background-color: #dc3545; color: white"
    elif val == "Cancelled":
        return "background-color: #ffc107; color: black"
    return ""

# ---------- Main App ----------
def main():
    clock_placeholder.markdown(
        f"<h3 style='text-align: center; color: #45a29e;'>{datetime.now().strftime('%A, %d %B %Y - %H:%M:%S')}</h3>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    df = load_data()

    # Filters
    col1, col2 = st.columns([3, 1])
    train_search = col1.text_input("🔍 Search Train Number")
    platform_filter = col2.selectbox(
        "🛤️ Filter by Platform",
        options=["All"] + sorted(df['platform'].dropna().astype(str).unique().tolist())
    )

    if train_search:
        df = df[df['train_number'].astype(str).str.contains(train_search)]
    if platform_filter != "All":
        df = df[df['platform'].astype(str) == platform_filter]

    # ---------- KPIs ----------
    st.markdown("## 📊 Train Metrics")
    k1, k2, k3 = st.columns(3)
    k1.metric("🚆 Total Trains", len(df))
    k2.metric("✅ On Time", df[df['status'] == "On Time"].shape[0])
    k3.metric("⚠️ Delayed", df[df['status'] == "Delayed"].shape[0])

    st.markdown("---")

    # ---------- Live Train Data Table ----------
    st.markdown("## 📋 Latest Train Records")
    if not df.empty:
        styled_df = df.style.applymap(highlight_status, subset=["status"])
        st.dataframe(styled_df, use_container_width=True, height=600)
    else:
        st.warning("No live train data available.")

    st.markdown("---")

    # ---------- Platform-wise Train Count ----------
    st.markdown("## 📈 Platform-wise Distribution")
    if not df.empty:
        platform_df = df['platform'].value_counts().reset_index()
        platform_df.columns = ["Platform", "Train Count"]

        chart = alt.Chart(platform_df).mark_bar(size=40).encode(
            x=alt.X('Platform:N', title="Platform Number"),
            y=alt.Y('Train Count:Q', title="Number of Trains"),
            color=alt.Color('Platform:N', scale=alt.Scale(scheme='category20b'), legend=None),
            tooltip=['Platform', 'Train Count']
        ).properties(
            width=800,
            height=400,
            title="Train Count per Platform"
        )

        st.altair_chart(chart, use_container_width=True)

# ---------- Run App with 1-Second Auto Refresh ----------
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

main()

# Auto-refresh every 1 second
refresh_interval = 4
time.sleep(refresh_interval)
st.rerun()
