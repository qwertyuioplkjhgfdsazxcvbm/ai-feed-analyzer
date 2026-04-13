# 🚀 AI-Powered Content Intelligence Tool

An automated blog aggregator and analyzer built to solve content categorization challenges at scale.

## 🛠️ Tech Stack
- **Backend:** Python / Flask
- **Extraction:** BeautifulSoup4 (Web Scraping)
- **Data:** Feedparser (RSS Ingestion)
- **Analysis:** Local NLP Heuristics (Modular for LLM integration)

## 🌟 Key Features
- **Smart Scraper:** Falls back to RSS metadata if web scraping is blocked.
- **Heuristic Engine:** Categorizes and tags articles instantly without API latency.
- **Content Ranking:** Automatically ranks articles based on content density.

## 🚀 Future Roadmap
1. Integration with OpenAI/Llama-3 for deeper sentiment analysis.
2. Asynchronous task queues (Celery) for high-volume feed processing.
3. Vector database integration for semantic search.
