import os
import re
import requests
import feedparser
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from collections import Counter

app = Flask(__name__)

# 🔍 Fetch full article content
def get_full_text(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')
        text = " ".join([p.get_text() for p in paragraphs])

        return text[:2000]
    except:
        return ""


# 🧠 Mock AI analysis (rule-based NLP)
def mock_ai_analysis(text):
    if len(text) < 150:
        return {
            "category": "General",
            "summary": "Content too short for deep analysis.",
            "tags": "#news"
        }

    text_lower = text.lower()

    # 📌 Category detection
    categories = {
        "Technology": ["ai", "software", "tech", "google", "apple", "data", "cloud"],
        "Finance": ["money", "stock", "market", "bitcoin", "bank", "investment"],
        "Health": ["health", "fitness", "doctor", "medical"],
        "Business": ["startup", "company", "ceo", "industry", "marketing"]
    }

    category = "General"
    for cat, keywords in categories.items():
        if any(word in text_lower for word in keywords):
            category = cat
            break

    # 📌 Tag extraction
    words = re.findall(r'\w+', text_lower)
    meaningful_words = [w for w in words if len(w) > 5]
    top_keywords = [item[0] for item in Counter(meaningful_words).most_common(3)]
    tags = ", ".join([f"#{w}" for w in top_keywords])

    # 📌 Summary
    sentences = text.split('.')
    summary = ". ".join(sentences[:2]).strip()
    if summary:
        summary += "."
    else:
        summary = "No summary available."

    return {
        "category": category,
        "summary": summary,
        "tags": tags
    }


@app.route('/', methods=['GET', 'POST'])
def home():
    articles_data = []

    if request.method == 'POST':
        rss_url = request.form.get('rss_url')
        feed = feedparser.parse(rss_url)

        for entry in feed.entries[:5]:
            raw_text = get_full_text(entry.link)

            if not raw_text or len(raw_text) < 100:
                raw_text = entry.get("summary", "") + " " + entry.get("title", "")

            analysis = mock_ai_analysis(raw_text)

            articles_data.append({
                'title': entry.title,
                'link': entry.link,
                'category': analysis['category'],
                'summary': analysis['summary'],
                'tags': analysis['tags']
            })

        # 🔥 Basic ranking (longer summary = more content)
        articles_data = sorted(
            articles_data,
            key=lambda x: len(x['summary']),
            reverse=True
        )

    return render_template('index.html', articles=articles_data)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)