import requests
import aiohttp
import asyncio
from pytrends.request import TrendReq
import praw
from typing import Dict, List
from core.config import config
from utils.error_handler import retry_on_failure
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    Research Agent - Gathers data from multiple sources
    
    Data sources:
    - Serper.dev (web search API)
    - Google Trends (via pytrends)
    - Reddit API (optional)
    """
    
    def __init__(self):
        """Initialize API clients"""
        # Serper.dev API
        self.serper_api_key = config.SERPER_API_KEY

        # Google Trends
        self.trends_client = TrendReq(hl='en-US', tz=360)

        # Reddit API - Store credentials as attributes for testing/debugging
        self.reddit_client_id = config.REDDIT_CLIENT_ID
        self.reddit_client_secret = config.REDDIT_CLIENT_SECRET
        self.reddit_user_agent = config.REDDIT_USER_AGENT

        if config.REDDIT_CLIENT_ID:
            try:
                self.reddit_client = praw.Reddit(
                    client_id=config.REDDIT_CLIENT_ID,
                    client_secret=config.REDDIT_CLIENT_SECRET,
                    user_agent=config.REDDIT_USER_AGENT
                )
                logger.info("Reddit API initialized successfully")
            except Exception as e:
                logger.warning(f"Reddit API initialization failed: {e}")
                self.reddit_client = None
        else:
            self.reddit_client = None
            logger.info("Reddit API credentials not configured")

        # Thread pool executor for running non-async libraries (pytrends, praw)
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    @retry_on_failure
    def run(self, query: str) -> Dict:
        """
        Execute research pipeline with parallel API calls

        Args:
            query: User's search query

        Returns:
            Dict containing sources, trends, discussions, and metadata
        """
        logger.info(f"Research Agent: Processing query '{query}'")

        # Run async operations
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            web_results, trends_data, reddit_data = loop.run_until_complete(
                self._run_parallel(query)
            )
        finally:
            loop.close()

        # Structure output
        output = {
            "sources": web_results,
            "trends": trends_data,
            "discussions": reddit_data,
            "metadata": {
                "total_sources": len(web_results),
                "source_types": {
                    "web": len(web_results),
                    "trends": 1 if trends_data else 0,
                    "reddit": len(reddit_data)
                }
            }
        }

        logger.info(f"Research Agent: Found {len(web_results)} web sources, {len(reddit_data)} discussions")
        return output

    async def _run_parallel(self, query: str) -> tuple:
        """
        Run all three API calls in parallel

        Args:
            query: User's search query

        Returns:
            Tuple of (web_results, trends_data, reddit_data)
        """
        # Execute all three API calls concurrently
        web_results, trends_data, reddit_data = await asyncio.gather(
            self._search_web(query),
            self._get_trends(query),
            self._search_reddit(query),
            return_exceptions=True
        )

        # Handle any exceptions in results
        if isinstance(web_results, Exception):
            logger.error(f"Web search error: {web_results}")
            web_results = []
        if isinstance(trends_data, Exception):
            logger.error(f"Trends error: {trends_data}")
            trends_data = {}
        if isinstance(reddit_data, Exception):
            logger.error(f"Reddit error: {reddit_data}")
            reddit_data = []

        return web_results, trends_data, reddit_data
    
    async def _search_web(self, query: str) -> List[Dict]:
        """
        Search web via Serper.dev API (async)

        Args:
            query: Search query

        Returns:
            List of web sources with title, snippet, URL, date
        """
        try:
            # Serper.dev API endpoint
            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": self.serper_api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "q": query,
                "num": 20,  # Request 20 results
                "gl": "us",  # Country: US
                "hl": "en"   # Language: English
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    response.raise_for_status()
                    results = await response.json()

            sources = []

            # Parse organic results (Serper.dev uses "organic" not "organic_results")
            for item in results.get("organic", []):
                sources.append({
                    "url": item.get("link", ""),
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "date": item.get("date", "Unknown"),
                    "source_type": "web"
                })

            logger.info(f"Serper.dev API: Retrieved {len(sources)} web results")
            return sources

        except Exception as e:
            logger.error(f"Serper.dev API error: {e}", exc_info=True)
            return []
    
    async def _get_trends(self, query: str) -> Dict:
        """
        Get Google Trends data (async via thread pool)

        Args:
            query: Search term

        Returns:
            Dict with trend data and average interest
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._get_trends_sync, query)

    def _get_trends_sync(self, query: str) -> Dict:
        """
        Synchronous Google Trends data fetching (runs in thread pool)

        Args:
            query: Search term

        Returns:
            Dict with trend data and average interest
        """
        try:
            # Build payload for last 3 months
            self.trends_client.build_payload([query], timeframe='today 3-m')
            interest_over_time = self.trends_client.interest_over_time()

            if not interest_over_time.empty:
                # Calculate average interest
                avg_interest = float(interest_over_time[query].mean())

                # Convert to dict for JSON serialization
                trend_dict = {}
                for date, value in interest_over_time[query].items():
                    trend_dict[date.strftime('%Y-%m-%d')] = int(value)

                result = {
                    "query": query,
                    "trend_data": trend_dict,
                    "average_interest": avg_interest
                }

                logger.info(f"Google Trends: Average interest {avg_interest:.1f}/100")
                return result
            else:
                logger.warning("Google Trends: No data available")
                return {}

        except Exception as e:
            error_str = str(e)
            # Handle rate limiting (429 errors) gracefully
            if "429" in error_str or "rate limit" in error_str.lower():
                logger.warning(f"Google Trends API rate limit exceeded, skipping trends data")
            else:
                logger.warning(f"Trends API error: {e}")
            return {}
    
    async def _search_reddit(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search Reddit discussions (async via thread pool)

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of Reddit posts with metadata
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._search_reddit_sync, query, limit)

    def _search_reddit_sync(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Synchronous Reddit search (runs in thread pool)

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of Reddit posts with metadata
        """
        if not self.reddit_client:
            logger.debug("Reddit API not configured, skipping")
            return []

        discussions = []
        try:
            # Search across all subreddits
            for submission in self.reddit_client.subreddit("all").search(query, limit=limit, time_filter='month'):
                discussions.append({
                    "title": submission.title,
                    "url": f"https://reddit.com{submission.permalink}",
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    "created": submission.created_utc,
                    "subreddit": str(submission.subreddit),
                    "source_type": "reddit"
                })

            logger.info(f"Reddit API: Retrieved {len(discussions)} discussions")

        except Exception as e:
            logger.warning(f"Reddit API error: {e}")

        return discussions


# CLI testing
if __name__ == "__main__":
    import json
    import sys
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get query from command line or use default
    query = sys.argv[1] if len(sys.argv) > 1 else "CRM tools for real estate"
    
    # Test the agent
    agent = ResearchAgent()
    result = agent.run(query)
    
    # Print results
    print("\n" + "="*60)
    print("RESEARCH AGENT TEST")
    print("="*60)
    print(f"Query: {query}")
    print(f"Total sources: {result['metadata']['total_sources']}")
    print(f"Web results: {len(result['sources'])}")
    print(f"Reddit discussions: {len(result['discussions'])}")
    print(f"Trends data available: {'Yes' if result['trends'] else 'No'}")
    
    print("\n" + "-"*60)
    print("Sample web sources:")
    for i, source in enumerate(result['sources'][:3], 1):
        print(f"\n{i}. {source['title']}")
        print(f"   {source['url']}")
        print(f"   {source['snippet'][:100]}...")
    
    # Save full output
    with open("outputs/reports/research_agent_test.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print("\n" + "="*60)
    print("Full output saved to: outputs/reports/research_agent_test.json")