from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Import our fetchers
from rss_parser import fetch_all_articles
from wikipedia_ingest import fetch_all_wikipedia_articles

load_dotenv('../.env')

# Configuration
QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY', None)
COLLECTION_NAME = 'verified_news'
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
VECTOR_SIZE = 384

def get_qdrant_client() -> QdrantClient:
    """Initialize and return Qdrant client."""
    if QDRANT_API_KEY:
        return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    return QdrantClient(url=QDRANT_URL)


def create_collection_if_not_exists(client: QdrantClient):
    """Create Qdrant collection if it doesn't already exist."""
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
        print(f"Created collection: {COLLECTION_NAME}")
    else:
        print(f"Collection already exists: {COLLECTION_NAME}")


def embed_and_store(client: QdrantClient, articles: list, model: SentenceTransformer):
    """
    Converts articles to vectors and stores them in Qdrant.

    Args:
        client: Qdrant client
        articles: List of article dicts
        model: SentenceTransformer model for embeddings
    """
    if not articles:
        print("No articles to store!")
        return

    points = []

    for article in articles:
        # Combine title and text for embedding
        content = f"{article['title']} {article['text']}"

        # Generate vector embedding
        vector = model.encode(content).tolist()

        # Create Qdrant point
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                'title': article['title'],
                'text': article['text'][:1000],  # Store first 1000 chars
                'url': article['url'],
                'source': article['source'],
                'published': article['published'],
                'ingested_at': datetime.now().isoformat()
            }
        )
        points.append(point)

    # Store in batches of 100
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch
        )
        print(f"Stored batch {i // batch_size + 1} ({len(batch)} articles)")

    print(f"\nTotal stored in Qdrant: {len(points)} articles")


def run_ingestion():
    """Main ingestion function — fetches all sources and stores in Qdrant."""
    print("=" * 50)
    print("STARTING INGESTION PIPELINE")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 50)

    # Connect to Qdrant
    print("\nConnecting to Qdrant...")
    client = get_qdrant_client()
    print("Connected!")

    # Create collection
    create_collection_if_not_exists(client)

    # Load embedding model
    print(f"\nLoading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("Model loaded!")

    # Fetch articles from all sources
    print("\nFetching RSS articles...")
    rss_articles = fetch_all_articles()

    print("\nFetching Wikipedia articles...")
    wiki_articles = fetch_all_wikipedia_articles()

    # Combine all articles
    all_articles = rss_articles + wiki_articles
    print(f"\nTotal articles to store: {len(all_articles)}")

    # Store in Qdrant
    print("\nStoring in Qdrant...")
    embed_and_store(client, all_articles, model)

    # Final stats
    collection_info = client.get_collection(COLLECTION_NAME)
    print("\n" + "=" * 50)
    print("INGESTION COMPLETE!")
    print(f"Total vectors in Qdrant: {collection_info.points_count}")
    print("=" * 50)


if __name__ == "__main__":
    run_ingestion()