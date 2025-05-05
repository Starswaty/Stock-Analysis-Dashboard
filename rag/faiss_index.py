import faiss
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch

# Initialize the transformer model and tokenizer for vector embedding
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def encode_text(texts):
    """
    Encode text using BERT model to get embeddings (vector representation).
    """
    # Tokenize the text
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    # Get the embeddings from the model
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()  # Mean pooling for sentence embeddings
    
    return embeddings

def build_faiss_index(data):
    """
    Build a FAISS index from the provided data.
    The data should be a list of text documents (strings).
    """
    # Step 1: Encode the text data into vectors
    print("Encoding text data into vectors...")
    embeddings = encode_text(data)
    
    # Step 2: Initialize FAISS index (using L2 distance for similarity search)
    dimension = embeddings.shape[1]  # This should match the embedding size (e.g., 768 for BERT)
    index = faiss.IndexFlatL2(dimension)
    
    # Step 3: Add the encoded embeddings to the FAISS index
    index.add(embeddings)
    
    return index

def search_faiss_index(query, index, top_k=5):
    """
    Search the FAISS index for the top-k most similar documents to the query.
    """
    query_vector = encode_text([query])
    
    # Perform the search
    _, indices = index.search(query_vector, top_k)
    
    return indices

# Example to test FAISS
if __name__ == "__main__":
    # Sample data for testing
    data = ["The stock price of TCS rose by 5% today.", "Nifty index saw a decline in the past week.", "Sentiment for TCS is positive in the market."]
    
    # Build FAISS index
    index = build_faiss_index(data)
    
    # Query to search
    query = "TCS stock performance"
    
    # Search FAISS index
    results = search_faiss_index(query, index)
    print("Top matches for the query:", results)
