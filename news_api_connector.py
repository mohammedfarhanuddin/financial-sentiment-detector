import streamlit as st
import requests

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
