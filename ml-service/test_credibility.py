from credibility import get_credibility, is_known_satire

# Test URLs
test_urls = [
    "https://www.reuters.com/world/us/some-article",
    "https://www.theonion.com/funny-fake-article",
    "https://infowars.com/conspiracy-article",
    "https://www.bbc.com/news/some-article",
    "https://randomsite123.com/article",
    "https://www.snopes.com/fact-check/something",
    "https://babylonbee.com/news/satire-article",
    "https://www.cnn.com/2024/some-article",
]

print("DOMAIN CREDIBILITY SCORER TEST")
print("=" * 50)

for url in test_urls:
    result = get_credibility(url)
    satire_tag = " [SATIRE]" if result["is_satire"] else ""
    print(f"\nURL: {url}")
    print(f"  Domain:   {result['domain']}")
    print(f"  Score:    {result['score']}")
    print(f"  Category: {result['category']}{satire_tag}")

print("\n" + "=" * 50)
print("Satire checks:")
print("theonion.com is satire:", is_known_satire("https://theonion.com/article"))
print("reuters.com is satire:", is_known_satire("https://reuters.com/article"))