import streamlit as st
import requests

SEARCH_ENDPOINT = "https://newsdata.io/api/1/news"
API_KEY = st.secrets["NEWS_API_KEY"]

@st.cache_data(ttl=60*60)
def fetch_news(query, max_results=10):
    if not API_KEY:
        st.warning("⚠️ API Key is missing.")
        return []

    params = {
        "apikey": API_KEY,
        "q": query,
        "language": "en",
        "category": "business",   # MUST be one category
        "country": "us",
        "max_results": max_results
    }

    try:
        response = requests.get(SEARCH_ENDPOINT, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            return [
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "content": article.get("content", article.get("description")),
                    "source_name": article.get("source_name"),
                    "pubDate": article.get("pubDate"),
                    "link": article.get("link")
                }
                for article in data["results"]
            ]

        if data.get("status") == "error":
            st.error(f"API Error: {data.get('message')}")

        return []

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return []


# --- To demonstrate modularity, you can test this function locally ---
if __name__ == '__main__':
    print("Run via app.py")
