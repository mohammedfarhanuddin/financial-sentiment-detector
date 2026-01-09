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

3.  **Configure Secrets**:
    - Create a file `.streamlit/secrets.toml` with the content:
      ```toml
      NEWS_API_KEY = "YOUR_API_KEY_HERE"
      ```

4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## Deployment

### Streamlit Community Cloud
1. Push your code to GitHub.
2. Deploy on Streamlit Cloud.
3. In the app settings, go to **Secrets** and add:
   ```toml
   NEWS_API_KEY = "your_actual_api_key"
   ```
