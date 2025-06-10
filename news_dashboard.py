from flask import Flask, render_template_string
import feedparser
import datetime
import html
import requests
from dateutil import parser  # pip install python-dateutil

app = Flask(__name__)

INDIA_FEEDS = {
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "Times of India": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    "Indian Express": "https://indianexpress.com/section/india/feed/",
}

WORLD_FEEDS = {
    "BBC World News": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Reuters World News": "https://feeds.reuters.com/reuters/worldNews",
    "The Guardian World": "https://www.theguardian.com/world/rss",
}

INDIAN_FINANCE_FEEDS = {
    "Moneycontrol": "https://www.moneycontrol.com/rss/MCtopnews.xml",
    "Economic Times Markets": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "Business Standard": "https://www.business-standard.com/rss/latest-news-economy-finance.rss",
}

TECH_FEEDS = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "Wired": "https://www.wired.com/feed/rss",
    "The Verge": "https://www.theverge.com/rss/index.xml",
}

def fetch_articles(feed_url):
    """Fetch and parse articles from an RSS feed with timeout using requests."""
    try:
        response = requests.get(feed_url, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        if feed.bozo:
            print(f"Warning: Malformed feed from {feed_url}: {feed.bozo_exception}")
        return feed.entries
    except Exception as e:
        print(f"Error fetching feed from {feed_url}: {e}")
        return []

def parse_article_date(article):
    """Extract a datetime from article, with fallback parsing."""
    published_time = None

    if hasattr(article, 'published_parsed') and article.published_parsed:
        published_time = datetime.datetime(*article.published_parsed[:6], tzinfo=datetime.timezone.utc)
    elif hasattr(article, 'updated_parsed') and article.updated_parsed:
        published_time = datetime.datetime(*article.updated_parsed[:6], tzinfo=datetime.timezone.utc)
    else:
        date_str = getattr(article, 'published', None) or getattr(article, 'updated', None)
        if date_str:
            try:
                parsed = parser.parse(date_str)
                if not parsed.tzinfo:
                    parsed = parsed.replace(tzinfo=datetime.timezone.utc)
                published_time = parsed
            except Exception as e:
                print(f"Date parsing error for '{article.title}': {e}")
    return published_time

def filter_and_sort_articles(feeds):
    all_articles = []
    seen_identifiers = set()
    twenty_four_hours_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24)

    for source_name, feed_url in feeds.items():
        print(f"Fetching articles from {source_name}...")
        articles = fetch_articles(feed_url)
        for article in articles:
            published_time = parse_article_date(article)
            if not published_time:
                # Skip articles without a valid date
                continue

            title_words = article.title.lower().split()
            article_identifier = (" ".join(title_words[:10]), article.link)

            if published_time > twenty_four_hours_ago and article_identifier not in seen_identifiers:
                all_articles.append({
                    'title': article.title,
                    'link': article.link,
                    'published': published_time,
                    'source': source_name
                })
                seen_identifiers.add(article_identifier)
            else:
                # Uncomment for debug info on skipped articles
                # print(f"Skipping article: '{article.title}' Published: {published_time}")
                pass

    all_articles.sort(key=lambda x: x['published'], reverse=True)
    return all_articles[:5]

def generate_html_section(title, articles):
    section_html = f"<h2>{title}</h2>"
    if not articles:
        section_html += "<p>No recent articles.</p>"
        return section_html

    section_html += "<ul>"
    for article in articles:
        published_date = article['published'].strftime("%a, %d %b %Y %H:%M:%S GMT")
        escaped_title = html.escape(article['title'])
        section_html += f"""
            <li>
                <h3><a href="{article['link']}" target="_blank" rel="noopener noreferrer">{escaped_title}</a></h3>
                <p class="source">Source: {article['source']}</p>
                <p class="date">Published: {published_date}</p>
            </li>
        """
    section_html += "</ul>"
    return section_html

@app.route('/')
def index():
    india_articles = filter_and_sort_articles(INDIA_FEEDS)
    world_articles = filter_and_sort_articles(WORLD_FEEDS)
    indian_finance_articles = filter_and_sort_articles(INDIAN_FINANCE_FEEDS)
    tech_articles = filter_and_sort_articles(TECH_FEEDS)
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    india_section = generate_html_section("🇮🇳 India News (Last 24 Hours)", india_articles)
    world_section = generate_html_section("🌍 World News (Last 24 Hours)", world_articles)
    indian_finance_section = generate_html_section("📈 Indian Stock Market & Finance (Last 24 Hours)", indian_finance_articles)
    tech_section = generate_html_section("💻 Global Tech News (Last 24 Hours)", tech_articles)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Latest News Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            margin: 0 auto;
            padding: 2em;
            background-color: #121212;
            color: #e0e0e0;
        }}
        h1 {{
            text-align: center;
            color: #ffffff;
            margin-bottom: 1em;
        }}
        h2 {{
            color: #ffffff;
            border-bottom: 1px solid #333;
            padding-bottom: 0.5em;
            margin-top: 0;
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2em;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .news-section {{
            background-color: #1e1e1e;
            padding: 1.5em;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        li {{
            margin-bottom: 1em;
            padding-bottom: 0.5em;
            border-bottom: 1px solid #333;
        }}
        li:last-child {{
            border-bottom: none;
        }}
        a {{
            text-decoration: none;
            color: #bb86fc;
        }}
        a:hover {{
            text-decoration: underline;
            color: #ffffff;
        }}
        .source {{
            font-style: italic;
            color: #b0b0b0;
            font-size: 0.9em;
        }}
        .date {{
            font-size: 0.8em;
            color: #b0b0b0;
        }}
        .timestamp {{
            text-align: center;
            margin-bottom: 2em;
            font-size: 0.9em;
            color: #b0b0b0;
        }}
        @media (max-width: 768px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        @media (max-width: 600px) {{
            body {{
                padding: 1em;
            }}
        }}
    </style>
</head>
<body>
    <h1>Latest News Dashboard</h1>
    <p class="timestamp">🕒 Updated: {now}</p>
    <div class="dashboard-grid">
        <div class="news-section">{india_section}</div>
        <div class="news-section">{world_section}</div>
        <div class="news-section">{indian_finance_section}</div>
        <div class="news-section">{tech_section}</div>
    </div>
</body>
</html>"""
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)