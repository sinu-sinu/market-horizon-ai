from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Configuration for Market Horizon AI"""
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Serper
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

    # Reddit
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "MarketHorizonAI/1.0")

    # YouTube
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

    # Langfuse Observability
    LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
    LANGFUSE_ENABLED = os.getenv("LANGFUSE_ENABLED", "true").lower() == "true"

    # App Settings
    APP_ENV = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    CACHE_TTL_DAYS = int(os.getenv("CACHE_TTL_DAYS", 7))
    MAX_TOKENS_PER_QUERY = int(os.getenv("MAX_TOKENS_PER_QUERY", 15000))
    BUDGET_LIMIT_TOKENS = int(os.getenv("BUDGET_LIMIT_TOKENS", 100000))
    
    # Performance Optimization Settings
    ENABLE_PARALLEL_SENTIMENT = os.getenv("ENABLE_PARALLEL_SENTIMENT", "true").lower() == "true"
    SENTIMENT_MAX_WORKERS = int(os.getenv("SENTIMENT_MAX_WORKERS", "4"))

config = Config()
