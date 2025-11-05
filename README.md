# Market Horizon AI

> **AI-powered competitive intelligence platform** that automatically analyzes market landscapes, identifies positioning gaps, and generates actionable content strategies using multi-agent AI orchestration.

A production-ready portfolio project demonstrating **advanced AI engineering** with autonomous agent coordination, intelligent caching, and real-time data synthesis.

---

## 🎯 What It Does

Market Horizon AI transforms raw market data into strategic insights in seconds:

- **Competitive Positioning Maps** – Interactive 2D visualizations showing where competitors stand (price vs. company size)
- **Content Gap Analysis** – AI-identified opportunities where competitors have weak coverage
- **Strategic Recommendations** – Data-driven positioning strategies and market angles
- **Smart Caching** – Intelligent result caching with type-specific TTLs to minimize API costs

Simply ask: *"What are the top CRM tools for real estate?"* and get a complete competitive analysis with actionable insights.

---

## 🏗️ Architecture

A **multi-agent system** using LangGraph for orchestration:

```
User Query
    ↓
[Research Agent] → Gathers data from 3 sources in parallel
    ↓
[Analysis Agent] → Extracts competitors, themes, sentiment
    ↓
[Strategy Agent] → Generates positioning map & content gaps
    ↓
[Quality Agent] → Validates, structures, and synthesizes final report
    ↓
Interactive UI Report
```

### Core Agents

| Agent | Responsibility | Key Features |
|-------|---|---|
| **Research** | Web search, trends, Reddit discussions | Async parallel calls, multi-source integration |
| **Analysis** | Pattern extraction, competitor identification | Semantic clustering, sentiment analysis |
| **Strategy** | Positioning math, opportunity detection | Gap analysis algorithm, content scoring |
| **Quality** | Report validation and synthesis | Confidence scoring, quality flags |

---

## 💡 Key Features

### 1. **Intelligent Multi-Source Research**
- Web search via Serper.dev (20 results)
- Google Trends analysis (3-month history)
- Reddit discussions (10 threads)
- All executed in parallel for speed

### 2. **Advanced Analysis Pipeline**
- Competitor identification and deduplication
- Sentiment analysis on mentions
- Content theme extraction with frequency tracking
- Automatic insight validation

### 3. **Smart Positioning Engine**
- 2D coordinate assignment using LLM reasoning
- Market gap detection (empty spaces in competitive landscape)
- Opportunity scoring based on underserved segments
- Interactive Plotly visualizations

### 4. **Content Gap Generator**
Instead of generic "X best practices," generates **specific, actionable content ideas**:
- "How to integrate X with your workflow" (integration themes)
- "X: ROI analysis and cost comparison" (pricing themes)
- "Complete X setup guide for beginners" (setup themes)
- Recommends format (Tutorial, Comparison, Case Study, etc.)
- Scores by opportunity (1-10) and estimated monthly search volume

### 5. **Production-Grade Caching**
- Database-backed cache with SQLite
- Type-specific TTLs (7 days for analysis, 14 days for Reddit, etc.)
- Hit rate tracking and analytics
- Manual cache management UI

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Orchestration** | LangGraph (multi-agent workflow) |
| **LLM** | GPT-4.1-mini (fast + cost-efficient) |
| **Data Sources** | Serper.dev, Google Trends, PRAW (Reddit) |
| **Vectorization** | FAISS (semantic search) |
| **Visualization** | Plotly (interactive charts) |
| **UI** | Streamlit (production-grade dashboard) |
| **Caching** | SQLite + Python |
| **Logging** | Python logging with structured format |

---

## 📊 Performance

- **Response Time:** 8-15 seconds (4 agents in sequence)
- **API Cost:** ~$0.02-0.05 per query (cached reduces to $0.001)
- **Accuracy:** Typically 85-92% confidence on competitive identification
- **Data Sources:** 30+ web results, 1 trends dataset, 10 Reddit threads per query

---

## 🛠️ Setup

### Requirements
- Python 3.9+
- API Keys: OpenAI, Serper.dev (free tier works)
- Optional: Reddit API (for discussions)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/market-horizon-ai.git
cd market-horizon-ai

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your API keys to .env
```

### Environment Variables

```bash
OPENAI_API_KEY=sk-...
SERPER_API_KEY=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USER_AGENT=...
```

---

## 💻 Usage

### Launch the UI

```bash
streamlit run streamlit/app.py
```

Then navigate to `http://localhost:8501`

### Example Queries

- "CRM tools for real estate agents"
- "AI-powered analytics platforms"
- "Project management software for startups"
- "Influencer marketing platforms"

The system returns:
1. **Competitors Identified** – Ranked by mention frequency
2. **Content Themes** – What people are discussing
3. **Positioning Map** – Visual competitive landscape
4. **Content Recommendations** – 5 specific topics to create content on
5. **Quality Metrics** – Confidence score and data sources

### Cache Management

Access the **Cache Management** panel in the sidebar to:
- View cache statistics (hit rate, size, entries)
- Clear all cache or by type
- Inspect expired entries
- Manage costs

---

## 🎨 UI Highlights

- **Clean, minimal design** – Focus on data, not visual noise
- **Real-time feedback** – See processing status as agents run
- **Query history** – Load previous reports instantly
- **Export functionality** – Download analysis as Markdown
- **Responsive layout** – Works on desktop and tablet

---

## 📈 What Makes This Stand Out

### Engineering Excellence
✅ **Async/Parallel Processing** – 3 API calls executed simultaneously
✅ **Intelligent Caching** – Reduces repeated queries to ~10ms
✅ **Error Handling** – Graceful fallbacks if APIs fail
✅ **Structured Logging** – Debug issues efficiently
✅ **Type Safety** – Full type hints throughout

### AI/ML Sophistication
✅ **Multi-Agent Orchestration** – Each agent has specialized prompts
✅ **Semantic Analysis** – FAISS for intelligent pattern matching
✅ **Dynamic Topic Generation** – Context-aware content recommendations
✅ **Confidence Scoring** – Transparent about data quality

### Production Readiness
✅ **Database Caching** – SQLite-backed persistence
✅ **Rate Limiting Handling** – Graceful degradation
✅ **Query Validation** – Input sanitization
✅ **Comprehensive Logging** – Monitor system health

---

## 📚 Learning Outcomes

This project demonstrates:

1. **Multi-Agent Architecture** – Coordinating 4+ AI agents with LangGraph
2. **LLM Integration** – Prompt engineering, response parsing, fallback handling
3. **Data Processing** – Web scraping, API integration, sentiment analysis
4. **Performance Optimization** – Async I/O, caching strategies, cost management
5. **Full-Stack Development** – Backend agents + Streamlit frontend
6. **DevOps** – Environment management, logging, error tracking

---

## 🗺️ Implementation Status

- [x] Multi-agent orchestration (Research, Analysis, Strategy, Quality)
- [x] Web/Trends/Reddit data integration
- [x] Competitive positioning engine
- [x] Content gap analysis with specific topic generation
- [x] SQLite-based caching with analytics
- [x] Streamlit UI with history + cache management
- [x] Production logging and error handling
- [x] Performance optimization (async, parallel, caching)

**Status:** ✅ Production Ready

---

## 🎓 Use Cases

This system is useful for:

- **Marketing Strategists** – Find white space in competitive markets
- **Content Teams** – Discover high-value content topics with proven demand
- **Product Marketers** – Monitor competitor messaging and positioning
- **Growth Teams** – Identify underserved audience segments
- **Entrepreneurs** – Validate market opportunities before launch

---

## 📝 License

MIT License – See [LICENSE](LICENSE) file

---

## 💬 Feedback

Questions or suggestions? Feel free to reach out!

- **Email:** sinu28.sinu@gmail.com
- **LinkedIn:** [linkedin.com/in/sinu-sinu](https://linkedin.com/in/sinu-sinu)

---

**Built with:** Python · LangChain · LangGraph · Streamlit · OpenAI · Plotly

**Status:** Ready for production use and portfolio showcase
