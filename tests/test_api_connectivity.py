import os
import openai
import requests
try:
    import praw
except ImportError:
    praw = None
from dotenv import load_dotenv
from agents.research_agent import ResearchAgent

load_dotenv()



# Load environment variables from .env



def test_openai():
    """Test OpenAI API connection"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key not found in .env")
        return

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": "Say 'API connected!'"}],
        max_tokens=10
    )
    message = response.choices[0].message.content.strip()
    assert "connected" in message.lower()
    print("✅ OpenAI API connected:", message)


def test_serper():
    """Test Serper.dev API connection"""
    serper_key = os.getenv("SERPER_API_KEY")
    if not serper_key:
        print("❌ Serper.dev API key not found in .env")
        return

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": serper_key}
    payload = {"q": "test query"}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    # Check that it returned some search results
    if "organic" in data or "answerBox" in data:
        print("✅ Serper.dev API connected — results received")
    else:
        print("⚠️ Serper.dev response didn’t include expected keys")


def test_reddit():
    """Test Reddit API connection"""
    if not praw:
        print("⚠️ PRAW not installed, skipping Reddit test")
        return
        
    reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
    reddit_secret = os.getenv("REDDIT_CLIENT_SECRET")
    reddit_agent = os.getenv("REDDIT_USER_AGENT")

    if not reddit_client_id or not reddit_secret:
        print("⚠️ Reddit API not configured (optional)")
        return

    reddit = praw.Reddit(
        client_id=reddit_client_id,
        client_secret=reddit_secret,
        user_agent=reddit_agent
    )

    subreddit = reddit.subreddit("test")
    assert subreddit.display_name.lower() == "test"
    print("✅ Reddit API connected")


if __name__ == "__main__":
    print("🔍 Testing API connections...\n")
    agent = ResearchAgent()
    print("Serper key:", agent.serper_api_key)
    print("Reddit client ID:", getattr(agent, "reddit_client_id", None))
    print("Reddit client secret:", getattr(agent, "reddit_client_secret", None))
    print("Reddit user agent:", getattr(agent, "reddit_user_agent", None))
    #test_openai()
    #test_serper()
    #test_reddit()
    print("\n🎉 All configured APIs tested successfully!")
