import wikipedia
from datetime import datetime

# Topics to fetch from Wikipedia for the knowledge base
TOPICS = [
    # Health
    "COVID-19 pandemic",
    "vaccine safety",
    "climate change",
    "global warming",

    # Science
    "moon landing",
    "evolution",
    "flat earth theory",
    "germ theory of disease",

    # Politics
    "2024 United States presidential election",
    "European Union",
    "United Nations",

    # Common misinformation topics
    "5G conspiracy theories",
    "QAnon",
    "anti-vaccination movement",
    "chemtrail conspiracy theory",

    # General knowledge
    "World Health Organization",
    "Centers for Disease Control and Prevention",
    "NASA",
    "Reuters",
]

def fetch_wikipedia_article(topic: str) -> dict | None:
    """
    Fetches a Wikipedia article summary for a given topic.

    Args:
        topic (str): Topic to search for

    Returns:
        dict: Article dict with title, text, url, source, published
        None: If article not found
    """
    try:
        page = wikipedia.page(topic, auto_suggest=False)

        # Get first 500 words of the article
        text = ' '.join(page.content.split()[:500])

        return {
            'title': page.title,
            'text': text,
            'url': page.url,
            'source': 'Wikipedia',
            'published': datetime.now().isoformat()
        }

    except wikipedia.exceptions.DisambiguationError as e:
        # Take the first option if ambiguous
        try:
            page = wikipedia.page(e.options[0], auto_suggest=False)
            text = ' '.join(page.content.split()[:500])
            return {
                'title': page.title,
                'text': text,
                'url': page.url,
                'source': 'Wikipedia',
                'published': datetime.now().isoformat()
            }
        except:
            return None

    except Exception as e:
        print(f"Error fetching Wikipedia article for '{topic}': {e}")
        return None


def fetch_all_wikipedia_articles() -> list:
    """
    Fetches Wikipedia articles for all predefined topics.

    Returns:
        list: List of article dicts
    """
    articles = []

    for topic in TOPICS:
        print(f"Fetching Wikipedia: {topic}")
        article = fetch_wikipedia_article(topic)
        if article:
            articles.append(article)
            print(f"  Got: {article['title']}")
        else:
            print(f"  Skipped: {topic}")

    print(f"\nTotal Wikipedia articles fetched: {len(articles)}")
    return articles