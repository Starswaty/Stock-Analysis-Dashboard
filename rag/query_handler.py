import streamlit as st
from rag.faiss_index import build_faiss_index, search_faiss_index
from transformers import pipeline
from ingestion.news import fetch_news
from ingestion.sentiment import analyze_sentiment
from ingestion.fx import fetch_fx_rates
from ingestion.historical import fetch_historical_data
from ingestion.real_time import fetch_real_time_data
from ingestion.pdf_summarizer import summarize_pdf

# Initialize the question-answering model (Hugging Face pipeline)
qa_model = pipeline("question-answering")

def get_relevant_data(query):
    """
    Retrieve relevant data from different modules based on the user's query.
    This includes news, sentiment, FX rates, and stock data.
    """
    relevant_data = []

    # Fetch data based on keywords in the query
    if "deal" in query.lower() or "news" in query.lower():
        news_data = fetch_news(query)
        relevant_data.append(news_data)

    if "sentiment" in query.lower():
        sentiment_data = analyze_sentiment(query)
        relevant_data.append(sentiment_data)

    if "fx" in query.lower():
        fx_data = fetch_fx_rates()
        relevant_data.append(fx_data)

    if "stock" in query.lower() or "historical" in query.lower():
        stock_data = fetch_historical_data(query)
        relevant_data.append(stock_data)

    if "real-time" in query.lower() or "stock price" in query.lower():
        real_time_data = fetch_real_time_data(query)
        relevant_data.append(real_time_data)

    if "pdf" in query.lower():
        pdf_data = summarize_pdf(query)
        relevant_data.append(pdf_data)

    return relevant_data

def generate_synthesis(query):
    """
    Synthesize the answer to the query using relevant data retrieved from various modules.
    """
    # Retrieve relevant data
    relevant_data = get_relevant_data(query)

    # Combine the data into a single string to use as context for the model
    context = ""
    for data in relevant_data:
        context += f"\n\n{data}"

    # Use the question-answering model to generate a response based on the context
    response = qa_model(question=query, context=context)
    return response['answer']

def show_query_interface():
    """
    Streamlit interface for the user to input queries and view answers.
    """
    st.title("🔍 Unified RAG Query Interface")

    # Capture user input (query)
    user_query = st.text_input("Ask your question here:", "Latest deals, sentiment shifts, FX rates, and earnings highlights for TCS")

    # Button to trigger query processing
    if st.button("Get Answer"):
        with st.spinner("Fetching data and synthesizing answer..."):
            answer = generate_synthesis(user_query)
        
        # Display the answer
        st.subheader("📋 Synthesized Answer:")
        st.write(answer)

if __name__ == "__main__":
    show_query_interface()
