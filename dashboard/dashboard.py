import streamlit as st
import pandas as pd
import plotly.express as px
import os

DATA_PATH = "data/"  # Path to store CSV files (exported from modules)

# ------------------- Load Data Functions ------------------- #
def load_csv(file_name):
    file_path = os.path.join(DATA_PATH, file_name)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.warning(f"{file_name} not found.")
        return pd.DataFrame()

# ------------------- Dashboard Layout ------------------- #
def show_dashboard():
    st.set_page_config(page_title="RAG Analytics Dashboard", layout="wide")
    st.title("📊 Unified Analytics Dashboard")

    # Tabs layout
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Real-Time Stock", "🕰️ Historical Data", "💱 FX Rates", "📑 Sentiment & News"])

    # 1. Real-Time Stock
    with tab1:
        st.subheader("Live Stock Quotes")
        rt_data = load_csv("real_time_stock.csv")
        if not rt_data.empty:
            selected_ticker = st.selectbox("Select Ticker", rt_data["Ticker"].unique())
            filtered = rt_data[rt_data["Ticker"] == selected_ticker]
            st.dataframe(filtered, use_container_width=True)
            fig = px.line(filtered, x="Time", y="Price", title=f"{selected_ticker} Real-Time Movement")
            st.plotly_chart(fig, use_container_width=True)

    # 2. Historical Data
    with tab2:
        st.subheader("Historical Stock Data")
        hist_data = load_csv("historical_stock.csv")
        if not hist_data.empty:
            selected_ticker = st.selectbox("Select Historical Ticker", hist_data["Symbol"].unique())
            hdata = hist_data[hist_data["Symbol"] == selected_ticker]
            st.dataframe(hdata.tail(30), use_container_width=True)
            fig = px.line(hdata, x="Date", y="Close", title=f"{selected_ticker} - Closing Price")
            st.plotly_chart(fig, use_container_width=True)

    # 3. FX Rates
    with tab3:
        st.subheader("Live Currency Exchange Rates")
        fx_data = load_csv("fx_rates.csv")
        if not fx_data.empty:
            st.dataframe(fx_data, use_container_width=True)
            fig = px.bar(fx_data, x="Currency", y="Rate", color="Currency", title="Live FX Rates (INR)")
            st.plotly_chart(fig, use_container_width=True)

    # 4. Sentiment & News
    with tab4:
        st.subheader("Sentiment Analysis")
        sent_data = load_csv("sentiment_results.csv")
        news_data = load_csv("latest_news.csv")

        if not sent_data.empty:
            st.write("### 🧠 Sentiment Summary")
            st.dataframe(sent_data, use_container_width=True)
            fig = px.pie(sent_data, names='Sentiment', title="Sentiment Distribution")
            st.plotly_chart(fig, use_container_width=True)

        if not news_data.empty:
            st.write("### 📰 Latest News Highlights")
            for _, row in news_data.iterrows():
                st.markdown(f"**{row['title']}**\\n\\n*{row['source']}*\\n\\n[Read more]({row['link']})")

if __name__ == "__main__":
    show_dashboard()
