from urllib.parse import urlparse

# Credibility database
CREDIBILITY_DB = {
    # Tier 1 — Highly credible (0.95-0.99)
    "reuters.com": 0.99,
    "apnews.com": 0.99,
    "bbc.com": 0.98,
    "bbc.co.uk": 0.98,
    "npr.org": 0.97,
    "pbs.org": 0.97,
    "theguardian.com": 0.95,
    "nytimes.com": 0.95,
    "washingtonpost.com": 0.95,
    "wsj.com": 0.95,
    "economist.com": 0.95,
    "ft.com": 0.95,
    "bloomberg.com": 0.94,
    "politico.com": 0.93,
    "theatlantic.com": 0.93,
    "time.com": 0.92,
    "who.int": 0.99,
    "cdc.gov": 0.99,
    "nih.gov": 0.99,
    "nasa.gov": 0.99,

    # Tier 2 — Generally reliable (0.75-0.89)
    "cnn.com": 0.82,
    "msnbc.com": 0.80,
    "foxnews.com": 0.78,
    "nypost.com": 0.75,
    "dailymail.co.uk": 0.75,
    "usatoday.com": 0.85,
    "newsweek.com": 0.80,
    "forbes.com": 0.83,
    "businessinsider.com": 0.78,
    "vice.com": 0.76,
    "vox.com": 0.80,
    "thehill.com": 0.80,
    "axios.com": 0.88,

    # Fact checkers (0.97-0.99)
    "snopes.com": 0.98,
    "factcheck.org": 0.98,
    "politifact.com": 0.97,
    "fullfact.org": 0.97,

    # Satire sites (0.05)
    "theonion.com": 0.05,
    "babylonbee.com": 0.05,
    "clickhole.com": 0.05,
    "thebeaverton.com": 0.05,
    "waterfordwhispersnews.com": 0.05,

    # Known fake news / conspiracy (0.01)
    "infowars.com": 0.01,
    "naturalnews.com": 0.01,
    "beforeitsnews.com": 0.01,
    "worldnewsdailyreport.com": 0.01,
    "empirenews.net": 0.01,
    "nationalreport.net": 0.01,
}

def get_credibility(url: str) -> dict:
    """
    Returns credibility score and category for a given URL.

    Args:
        url (str): Full article URL

    Returns:
        dict: {
            domain (str): extracted domain,
            score (float): credibility score 0.0-1.0,
            category (str): human readable category,
            is_satire (bool): True if satire site
        }
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Remove www. prefix
        if domain.startswith("www."):
            domain = domain[4:]

        score = CREDIBILITY_DB.get(domain, 0.40)

        # Determine category
        if score >= 0.95:
            category = "Highly Credible"
        elif score >= 0.75:
            category = "Generally Reliable"
        elif score >= 0.50:
            category = "Mixed Reliability"
        elif score <= 0.05:
            category = "Satire" if domain in [
                "theonion.com", "babylonbee.com",
                "clickhole.com", "thebeaverton.com",
                "waterfordwhispersnews.com"
            ] else "Known Misinformation"
        else:
            category = "Unknown Source"

        return {
            "domain": domain,
            "score": score,
            "category": category,
            "is_satire": score == 0.05
        }

    except Exception as e:
        return {
            "domain": "unknown",
            "score": 0.40,
            "category": "Unknown Source",
            "is_satire": False
        }


def is_known_satire(url: str) -> bool:
    """Quick check if URL is from a known satire site."""
    result = get_credibility(url)
    return result["is_satire"]