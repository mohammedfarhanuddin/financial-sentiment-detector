import requests
import streamlit as st

SEARCH_ENDPOINT = "https://newsdata.io/api/1/news"

# --- Main Fetching Function ---

@st.cache_data(ttl=60*60)
def fetch_news(api_key, query, max_results=10):
    """
    Fetches news articles related to the query.
    Uses caching to limit repeated API calls.
    """
    if not api_key:
        st.warning("⚠️ API Key is missing.")
        return []

    params = {
        'apikey': api_key,
        'q': query,
        'language': 'en',
        'category': 'business,finance',
        'country': 'us',
        'max_results': max_results
    }

    try:
        response = requests.get(SEARCH_ENDPOINT, params=params)
        response.raise_for_status() # Raise HTTPError for bad status codes
        data = response.json()

        if data.get('results'):
            # Return list of articles, taking only necessary fields
            return [
                {
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'content': article.get('content', article.get('description')),
                    'source_name': article.get('source_name'),
                    'pubDate': article.get('pubDate'),
                    'link': article.get('link')
                } for article in data['results']
            ]
        elif data.get('status') == 'error':
            st.error(f"API Error: {data.get('message')}")
            return []
        else:
            return []

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return []

# --- To demonstrate modularity, you can test this function locally ---
if __name__ == '__main__':
    print("Run via app.py")