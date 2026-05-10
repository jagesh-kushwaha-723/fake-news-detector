import feedparser
import httpx
from datetime import datetime
from readability import Document
import re

# RSS feeds from credible sources
RSS_FEEDS = [
    # News agencies
    "https://feeds.reuters.com/reuters/topNews",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://feeds.npr.org/1001/rss.xml",
    "https://www.theguardian.com/world/rss",

    # Health
    "https://www.who.int/rss-feeds/news-english.xml",
    "https://tools.cdc.gov/api/v2/resources/media/316422.rss",

    # Science
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://feeds.sciencedaily.com/sciencedaily/top_news",

    # Fact checkers
    "https://www.snopes.com/feed/",
    "https://www.politifact.com/rss/all/",
]

def clean_text(text: str) -> str:
    """Remove HTML tags and extra whitespace from text."""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def fetch_articles_from_feed(feed_url: str) -> list:
    """
    Fetches articles from a single RSS feed.

    Args:
        feed_url (str): URL of the RSS feed

    Returns:
        list: List of article dicts with title, text, url, source, published
    """
    articles = []

    try:
        feed = feedparser.parse(feed_url)
        source = feed.feed.get('title', 'Unknown')

        for entry in feed.entries[:10]:  # Max 10 per feed
            title = clean_text(entry.get('title', ''))
            summary = clean_text(entry.get('summary', ''))
            url = entry.get('link', '')

            # Skip if missing key fields
            if not title or not url:
                continue

            # Get published date
            published = entry.get('published', '')
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6]).isoformat()

            articles.append({
                'title': title,
                'text': summary,
                'url': url,
                'source': source,
                'published': published
            })

    except Exception as e:
        print(f"Error fetching feed {feed_url}: {e}")

    return articles


def fetch_all_articles() -> list:
    """
    Fetches articles from all RSS feeds.

    Returns:
        list: Combined list of all articles from all feeds
    """
    all_articles = []

    for feed_url in RSS_FEEDS:
        print(f"Fetching: {feed_url}")
        articles = fetch_articles_from_feed(feed_url)
        all_articles.extend(articles)
        print(f"  Got {len(articles)} articles")

    print(f"\nTotal articles fetched: {len(all_articles)}")
    return all_articles