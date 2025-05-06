from textblob import TextBlob

# Function to analyze sentiment
def sentiment_analysis(text):
    # Create a TextBlob object
    blob = TextBlob(text)
    
    # Get the polarity of the text
    polarity = blob.sentiment.polarity
    
    # Classify polarity into sentiment categories
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment
