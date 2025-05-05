import streamlit as st
from ingestion.fx import get_currency_rates
from ingestion.news import fetch_news
from ingestion.sentiment import analyze_sentiment
from ingestion.historical import get_historical_stock_data
from ingestion.real_time import get_real_time_stock_data
from ingestion.pdf_summarizer import summarize_pdf
from dashboard.dashboard import show_dashboard
from rag.query_handler import handle_query

def main():
    st.title("RAG Analytics Portal")

    # Sidebar for user navigation
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Choose Section", ["Home", "Stock Data", "Currency Data", "News", "PDF Summarizer", "Ask a Question"])

    if selection == "Home":
        st.write("Welcome to the RAG Analytics Portal! Choose from the options in the sidebar.")
    elif selection == "Stock Data":
        st.write("Showing historical and real-time stock data.")
        stock_symbol = st.text_input("Enter stock symbol (e.g., TCS, INFY):")
        if stock_symbol:
            st.write(get_historical_stock_data(stock_symbol))
            st.write(get_real_time_stock_data(stock_symbol))
    elif selection == "Currency Data":
        st.write("Live currency rates")
        st.write(get_currency_rates())
    elif selection == "News":
        st.write("Latest deal news")
        st.write(fetch_news())
    elif selection == "PDF Summarizer":
        uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")
        if uploaded_pdf:
            st.write(summarize_pdf(uploaded_pdf))
    elif selection == "Ask a Question":
        user_query = st.text_input("Enter your query:")
        if user_query:
            response = handle_query(user_query)
            st.write(response)

if __name__ == "__main__":
    main()
