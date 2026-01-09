import nltk
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import time
import re

# Download VADER lexicon for sentiment analysis
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def clean_text(text):
    """Cleans text for better sentiment analysis (basic cleaning)."""
    if not isinstance(text, str):
        return ""
    # Remove HTML tags and punctuation
    text = re.sub('<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def get_sentiment(text):
    """
    Performs sentiment analysis using NLTK's VADER.
    Returns the compound score and a classification (Positive/Negative/Neutral).
    """
    cleaned_text = clean_text(text)
    if not cleaned_text:
        return {'VADER Score': 0.0, 'Sentiment': 'Neutral'}

    # Get VADER compound score
    score = sia.polarity_scores(cleaned_text)['compound']

    # Simple classification based on thresholds
    if score >= 0.05:
        sentiment = "Positive"
    elif score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
        
    return {
        'VADER Score': score,
        'Sentiment': sentiment
    }

def analyze_articles(articles):
    """
    Analyzes a list of article dictionaries and returns a DataFrame with sentiment.
    """
    start_time = time.time()
    
    # Create the DataFrame from the articles
    df = pd.DataFrame(articles)
    
    # Create a single text column for analysis
    df['full_text'] = df['title'].fillna('') + " " + df['description'].fillna('')
    
    # Apply the sentiment analysis function
    df['sentiment_data'] = df['full_text'].apply(get_sentiment)
    
    # Expand the sentiment dictionary into separate columns
    df['VADER Score'] = df['sentiment_data'].apply(lambda x: x['VADER Score'])
    df['Predicted Sentiment'] = df['sentiment_data'].apply(lambda x: x['Sentiment'])
    
    # Calculate overall average VADER score
    overall_vader_score = df['VADER Score'].mean()

    end_time = time.time()
    st.info(f"Analysis of {len(df)} articles complete in {end_time - start_time:.2f} seconds.")

    return df[['pubDate', 'source_name', 'Predicted Sentiment', 'VADER Score', 'title', 'link']], overall_vader_score


# --- To demonstrate modularity, you can test this function locally ---
if __name__ == '__main__':
    test_articles = [
        {'title': 'Stocks rocket up after strong earnings report.', 'description': 'The S&P 500 hit a new high today.'},
        {'title': 'Company X misses estimates, shares tumble.', 'description': 'Analysts predict a weak quarter ahead.'}
    ]
    st.write(analyze_articles(test_articles))