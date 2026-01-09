import streamlit as st
import pandas as pd
from news_api_connector import fetch_news
from sentiment_analyser import analyze_articles

# --- Streamlit UI ---

st.set_page_config(page_title="Financial News Sentiment Analyzer", layout="centered")

st.title("📈 Financial News Sentiment Analyzer")
st.markdown("Fetch the latest business news and analyze the overall market sentiment.")

# User Input
search_term = st.text_input("Enter a company or keyword (e.g., Apple, Bitcoin, S&P 500):", "Financial Markets")

# API Key Handling
if 'news_api_key' in st.secrets:
    api_key = st.secrets['news_api_key']
else:
    api_key = st.sidebar.text_input("Enter NewsData.io API Key", type="password")
    if not api_key:
        st.sidebar.warning("Please enter your API key to proceed.")

# Run Analysis Button
if st.button("Analyze Sentiment"):
    
    if not api_key:
        st.error("API Key is required. Please enter it in the sidebar or configure secrets.")
    else:
        with st.spinner(f"Fetching and analyzing news for '{search_term}'..."):
            # 1. Fetch News (from news_api_connector.py)
            articles = fetch_news(api_key, search_term, max_results=20)

            if not articles:
                st.warning(f"No recent articles found for '{search_term}' or API key is missing/invalid.")
            else:
                # 2. Analyze Sentiment (from sentiment_analyser.py)
                df_results, overall_vader_score = analyze_articles(articles)

                # --- Results and Visualization ---
                st.subheader(f"Results for '{search_term}' ({len(articles)} Articles)")
                
                # 3. Calculate Overall Sentiment Summary
                
                if overall_vader_score >= 0.1:
                    final_sentiment = "Strongly Positive 🚀"
                    color = "green"
                elif overall_vader_score >= 0.01:
                    final_sentiment = "Positive 😊"
                    color = "green"
                elif overall_vader_score <= -0.1:
                    final_sentiment = "Strongly Negative 📉"
                    color = "red"
                elif overall_vader_score <= -0.01:
                    final_sentiment = "Negative 😔"
                    color = "red"
                else:
                    final_sentiment = "Neutral 😐"
                    color = "blue"

                st.markdown(f"**Overall Market Sentiment:** <span style='font-size: 24px; color:{color}'>{final_sentiment}</span>", unsafe_allow_html=True)

                st.metric(
                    label="Average VADER Polarity Score (Range: -1 to +1)",
                    value=f"{overall_vader_score:.4f}"
                )
                
                st.markdown("---")
                
                # 4. Display Details in an Interactive Table
                st.subheader("Article Breakdown")
                st.dataframe(
                    df_results,
                    column_config={
                        "link": st.column_config.LinkColumn("Link"),
                        "title": st.column_config.Column("Headline"),
                        "source_name": st.column_config.Column("Source"),
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Optional: Display a simple bar chart of VADER scores
                sentiment_counts = df_results['Predicted Sentiment'].value_counts().reset_index()
                sentiment_counts.columns = ['Sentiment', 'Count']
                
                st.markdown("### Sentiment Distribution")
                st.bar_chart(sentiment_counts, x='Sentiment', y='Count')