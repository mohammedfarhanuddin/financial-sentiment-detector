import React, { useState, useEffect, useMemo } from 'react';

// --- Configuration ---
// IMPORTANT: Replace "YOUR_API_KEY" with your free API key from https://gnews.io/
const API_KEY = "YOUR_API_KEY"; 
const API_URL = "https://gnews.io/api/v4/search";

// --- Helper Components & Functions ---

/**
 * A simple loading spinner component.
 */
const Spinner = () => (
  <div className="flex justify-center items-center p-8">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-sky-400"></div>
  </div>
);

/**
 * A component to display error messages.
 * @param {{ message: string }} props - The error message to display.
 */
const ErrorDisplay = ({ message }) => (
  <div className="bg-red-900/50 border border-red-700 text-red-200 px-4 py-3 rounded-lg relative my-4" role="alert">
    <strong className="font-bold">Error: </strong>
    <span className="block sm:inline">{message}</span>
  </div>
);

/**
 * A component to represent a single news article card.
 * @param {{ article: object }} props - The article object to display.
 */
const ArticleCard = ({ article }) => {
  /**
   * Determines the color classes for the sentiment badge.
   * @param {string} sentiment - The sentiment string ('Positive', 'Negative', 'Neutral').
   * @returns {string} Tailwind CSS classes for the badge.
   */
  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'Positive':
        return 'bg-green-500/20 text-green-300 border-green-500/50';
      case 'Negative':
        return 'bg-red-500/20 text-red-300 border-red-500/50';
      default:
        return 'bg-gray-500/20 text-gray-300 border-gray-500/50';
    }
  };

  const formattedDate = new Date(article.publishedAt).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div className="bg-gray-800/50 rounded-xl shadow-lg hover:shadow-sky-400/20 hover:ring-1 hover:ring-gray-700 transition-all duration-300 p-6 flex flex-col justify-between">
      <div>
        <h3 className="text-xl font-bold text-gray-100 mb-2">
          <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:text-sky-400 transition-colors">
            {article.title}
          </a>
        </h3>
        <p className="text-gray-400 text-sm mb-4">{article.description}</p>
      </div>
      <div className="flex justify-between items-center mt-4">
        <span className="text-xs font-medium text-gray-500">{article.source.name} &bull; {formattedDate}</span>
        <span className={`text-xs font-semibold px-3 py-1 rounded-full border ${getSentimentColor(article.sentiment.label)}`}>
          {article.sentiment.label}
        </span>
      </div>
    </div>
  );
};

// --- Main Application Component ---

export default function App() {
  // --- State Management ---
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('Apple'); // Default search term
  const [sentimentFilter, setSentimentFilter] = useState('All'); // 'All', 'Positive', 'Negative', 'Neutral'

  // --- Data Fetching and Processing ---
  useEffect(() => {
    // Immediately set loading state to true when a new fetch is initiated.
    setLoading(true);
    setError(null); // Clear previous errors

    if (API_KEY === "YOUR_API_KEY") {
      setError("Please replace 'YOUR_API_KEY' with your actual key from gnews.io.");
      setLoading(false);
      return;
    }

    const fetchNews = async () => {
      try {
        const query = `${searchTerm} AND (finance OR stock OR market)`;
        const url = `${API_URL}?q=${encodeURIComponent(query)}&lang=en&token=${API_KEY}`;
        
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`API request failed with status ${response.status}. Check your API key or network.`);
        }
        
        const data = await response.json();

        // --- MOCK SENTIMENT ANALYSIS ---
        // In a real-world app, this logic would be on a backend server.
        // The backend would use an NLP library (like NLTK in Python) to analyze the text.
        // Here, we simulate it by assigning a random sentiment to each article.
        const articlesWithSentiment = data.articles.map(article => {
          const rand = Math.random();
          let label = 'Neutral';
          let score = 0;

          if (rand < 0.35) {
            label = 'Positive';
            score = Math.random() * 0.5 + 0.5; // Score between 0.5 and 1.0
          } else if (rand < 0.7) {
            label = 'Negative';
            score = -(Math.random() * 0.5 + 0.5); // Score between -0.5 and -1.0
          } else {
            score = Math.random() * 0.4 - 0.2; // Score between -0.2 and 0.2
          }

          return {
            ...article,
            sentiment: { label, score },
          };
        });

        setArticles(articlesWithSentiment);
      } catch (err) {
        setError(err.message);
        setArticles([]); // Clear articles on error
      } finally {
        // Ensure loading is set to false after the fetch attempt is complete.
        setLoading(false);
      }
    };

    fetchNews();
  }, [searchTerm]); // This effect re-runs whenever the `searchTerm` state changes.

  // --- Filtering Logic ---
  const filteredArticles = useMemo(() => {
    if (sentimentFilter === 'All') {
      return articles;
    }
    return articles.filter(article => article.sentiment.label === sentimentFilter);
  }, [articles, sentimentFilter]); // This recalculates only when articles or filter change.


  // --- Event Handlers ---
  const handleSearch = (e) => {
    e.preventDefault();
    const newSearchTerm = e.target.elements.search.value;
    if (newSearchTerm && newSearchTerm !== searchTerm) {
      setSearchTerm(newSearchTerm);
    }
  };
  
  const filterButtons = ['All', 'Positive', 'Negative', 'Neutral'];

  // --- Render ---
  return (
    <div className="bg-gray-900 min-h-screen font-sans text-gray-300">
      <div className="container mx-auto px-4 py-8">
        
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-extrabold text-white">
            Financial News <span className="text-sky-400">Sentiment Analyzer</span>
          </h1>
          <p className="text-gray-400 mt-2">
            Real-time market sentiment analysis powered by GNews API.
          </p>
        </header>

        {/* Search and Filter Controls */}
        <div className="bg-gray-800/60 p-4 rounded-lg mb-8 sticky top-4 z-10 backdrop-blur-sm">
          <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-4 mb-4">
            <input
              type="text"
              name="search"
              defaultValue={searchTerm}
              placeholder="Enter a stock, company, or keyword (e.g., Tesla, inflation)"
              className="flex-grow bg-gray-700 border border-gray-600 rounded-md px-4 py-2 text-white placeholder-gray-500 focus:ring-2 focus:ring-sky-500 focus:outline-none transition"
            />
            <button type="submit" className="bg-sky-600 hover:bg-sky-500 text-white font-bold py-2 px-6 rounded-md transition-colors">
              Analyze
            </button>
          </form>
          
          <div className="flex flex-wrap justify-center gap-2">
             {filterButtons.map(filter => (
                <button
                  key={filter}
                  onClick={() => setSentimentFilter(filter)}
                  className={`px-4 py-1.5 text-sm font-medium rounded-full transition-all duration-200 ${
                    sentimentFilter === filter
                      ? 'bg-sky-500 text-white shadow-md'
                      : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                  }`}
                >
                  {filter}
                </button>
             ))}
          </div>
        </div>

        {/* Content Area */}
        <main>
          {loading && <Spinner />}
          {error && <ErrorDisplay message={error} />}
          {!loading && !error && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredArticles.length > 0 ? (
                filteredArticles.map((article, index) => (
                  <ArticleCard key={`${article.url}-${index}`} article={article} />
                ))
              ) : (
                <div className="col-span-full text-center text-gray-500 py-8">
                  No articles found. Try a different search term.
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
