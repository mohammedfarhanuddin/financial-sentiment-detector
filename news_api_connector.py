import streamlit as st
import requests

SEARCH_ENDPOINT = "https://newsdata.io/api/1/news"

# Financial keywords used to filter out non-business news
FINANCE_KEYWORDS = [
    "stock", "stocks", "share", "shares", "market", "earnings", "revenue",
    "profit", "loss", "ipo", "nasdaq", "dow", "s&p", "trading",
    "crypto", "bitcoin", "forex", "investment", "economy",
    "bank", "hedge", "fund", "dividend", "quarter", "q1", "q2", "q3", "q4"
]

def is_financial(article):
    text = f"{article.get('title','')} {article.get('description','')}".lower()
    return any(word in text for word in FINANCE_KEYWORDS)

@st.cache_data(ttl=60 * 60)
def fetch_news(query, max_results=10):
    """
    Fetches financial news related to a company, stock, or keyword.
    Uses keyword search + intelligent financial filtering.
    """

    # Load API Key from Streamlit secrets
    if "NEWS_API_KEY" not in st.secrets:
        st.error("⚠️ NEWS_API_KEY is missing in Streamlit secrets.")
        return []

    api_key = st.secrets["NEWS_API_KEY"]

    params = {
        "apikey": api_key,
        "category": "business",
        "language": "en",
        "size": max_results * 3
    }

    try:
        response = requests.get(SEARCH_ENDPOINT, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return []

        # Filter to financial news only
        raw_articles = data["results"]
        financial_articles = [a for a in raw_articles if is_financial(a)]

        # Return clean structured data
        return [
            {
                "title": article.get("title"),
                "description": article.get("description"),
                "content": article.get("content", article.get("description")),
                "source_name": article.get("source_name"),
                "pubDate": article.get("pubDate"),
                "link": article.get("link")
            }
            for article in financial_articles[:max_results]
        ]

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return []


# Local test guard
if __name__ == "__main__":
    print("Run via app.py")
