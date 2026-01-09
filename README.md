# Financial News Sentiment Analyzer

A Streamlit application that fetches financial news articles and analyzes their sentiment using NLTK's VADER.

## Features
- Fetches real-time news from NewsData.io.
- Analyzes sentiment (Positive, Negative, Neutral) of headlines and descriptions.
- Visualizes sentiment distribution and overall market score.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Get API Key**:
    - Sign up at [NewsData.io](https://newsdata.io/) to get a free API key.

3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

4.  **Enter API Key**:
    - When the app runs, enter your API key in the sidebar.
    - OR create a file `.streamlit/secrets.toml` with the content:
      ```toml
      news_api_key = "YOUR_API_KEY_HERE"
      ```

## Deployment
See `DEPLOYMENT.md` (if available) or use Streamlit Community Cloud for easy hosting.
