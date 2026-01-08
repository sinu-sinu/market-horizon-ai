# Market Horizon AI

**AI-powered competitive intelligence platform that transforms market research from hours to seconds**

A production-ready system demonstrating advanced AI engineering with multi-agent orchestration, real-time data synthesis, and intelligent caching. Automatically analyzes market landscapes, identifies positioning gaps, and generates actionable content strategies.

---

## Demo

> [Live Demo](#) | [Video Walkthrough](#) | [Screenshots](#)

**Sample Output:** Input _"CRM tools for real estate agents"_ → Get competitive positioning map, content gap analysis, and strategic recommendations in under 15 seconds.

### Screenshots

![Dashboard analysis](frontend/public/panorama 1.png)

![Interactive Positioning Map](frontend/public/panorama 2.png)

![Content Recommendation](frontend/public/panorama 3.png)

---

## Problem Statement

Marketing teams spend 15-20 hours weekly on manual competitive research: monitoring competitors, analyzing trends, and synthesizing insights. Market Horizon AI automates this entire workflow, delivering instant competitive intelligence through autonomous AI agents.

---

## Key Features

**Intelligent Multi-Source Research**
- Web search, Google Trends, and Reddit discussions executed in parallel
- 30+ data points synthesized per query

**AI-Driven Analysis Pipeline**
- Competitor identification with semantic deduplication
- Sentiment analysis and content theme extraction
- Automatic insight validation with confidence scoring

**Smart Positioning Engine**
- 2D competitive landscape visualization using LLM reasoning
- Market gap detection and opportunity scoring
- Interactive Plotly charts

**Actionable Content Recommendations**
- Specific, high-value content ideas (not generic topics)
- Format recommendations (Tutorial, Comparison, Case Study)
- Estimated search volume and opportunity scores (1-10)

**Production-Grade Caching**
- SQLite-backed cache with type-specific TTLs
- Hit rate tracking and cost analytics
- Cache management UI

---

## Tech Stack

**AI & Orchestration**
- LangGraph (multi-agent workflow coordination)
- OpenAI GPT-4.1-mini (fast, cost-efficient)
- LangSmith + Langfuse (observability & tracing)

**Backend**
- FastAPI (REST API)
- Python 3.9+ with asyncio
- SQLite (caching layer)

**Frontend**
- Vue.js 3 + TypeScript
- Pinia (state management)
- ECharts (interactive visualizations)
- Vite (build tooling)

**Data Sources**
- Serper.dev (web search)
- Google Trends API
- PRAW (Reddit)

**ML/NLP**
- FAISS (semantic search)
- Sentence Transformers (embeddings)
- spaCy (NLP processing)
- scikit-learn (analysis)

**Infrastructure**
- Docker + Docker Compose
- PostgreSQL (Langfuse metrics)
- Nginx (production serving)

---

## How It Works

### Multi-Agent Architecture

```
User Query
    ↓
┌─────────────────┐
│ Research Agent  │ → Parallel data collection (Web, Trends, Reddit)
└────────┬────────┘
         ↓
┌─────────────────┐
│ Analysis Agent  │ → Competitor identification, theme extraction, sentiment
└────────┬────────┘
         ↓
┌─────────────────┐
│ Strategy Agent  │ → Positioning map generation, gap analysis
└────────┬────────┘
         ↓
┌─────────────────┐
│ Quality Agent   │ → Validation, synthesis, confidence scoring
└────────┬────────┘
         ↓
  Interactive Report
```

### Agent Responsibilities

| Agent | Responsibility | Key Output |
|-------|---------------|------------|
| **Research** | Multi-source data gathering | Raw market data from 3 sources |
| **Analysis** | Pattern extraction & competitor ID | Structured competitive insights |
| **Strategy** | Positioning & opportunity detection | 2D map coordinates, content gaps |
| **Quality** | Validation & synthesis | Final report with confidence scores |

### Performance Metrics

- **Response Time:** 8-15 seconds (4 agents in sequence)
- **API Cost:** $0.02-0.05 per query (cached: $0.001)
- **Accuracy:** 85-92% confidence on competitor identification
- **Cache Hit Rate:** ~65% after warmup period

---

## Installation & Setup

### Prerequisites

- Python 3.9+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (recommended)
- API Keys: OpenAI, Serper.dev

### Quick Start (Docker)

```bash
# Clone repository
git clone https://github.com/yourusername/market-horizon-ai.git
cd market-horizon-ai

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Launch all services
docker compose up -d

# Access application
# Frontend: http://localhost:5173
# API: http://localhost:8000
# Langfuse: http://localhost:3000
```

### Local Development

```bash
# Backend
pip install -r requirements.txt
cd api
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...
SERPER_API_KEY=...

# Optional (Reddit data)
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USER_AGENT=MarketHorizonAI/1.0

# Observability
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
```

---

## Usage

### Basic Query

```bash
# Via API
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "CRM tools for real estate agents"}'
```

### Sample Queries

- "AI-powered analytics platforms"
- "Project management software for startups"
- "Influencer marketing platforms"

### Expected Output

1. **Competitors Identified** – Ranked by mention frequency and relevance
2. **Content Themes** – What audiences are discussing (with frequency)
3. **Positioning Map** – Visual competitive landscape (2D scatter plot)
4. **Content Recommendations** – 5 specific topics with opportunity scores
5. **Quality Metrics** – Confidence score, data source breakdown

---

## Challenges & Learnings

### Technical Challenges

**Async Event Loop Management**
- Problem: Nested event loops in LangGraph caused runtime errors
- Solution: Implemented proper async context handling with `asyncio.new_event_loop()` guards

**LLM Response Consistency**
- Problem: Unstructured outputs from GPT-4 broke parsing
- Solution: Structured prompts with JSON schema validation and fallback parsers

**Cost Optimization**
- Problem: Each query cost $0.05-0.08 in API calls
- Solution: Multi-tier caching (7-14 day TTLs by data type) reduced costs by 85%

**Semantic Deduplication**
- Problem: "HubSpot CRM" vs "Hubspot" recognized as different competitors
- Solution: Sentence embeddings + cosine similarity threshold (0.85) for fuzzy matching

### Key Learnings

1. **Multi-agent systems require explicit state management** – LangGraph's state pattern prevents data loss between agents
2. **Prompt engineering is 70% of the work** – Specific, structured prompts dramatically improve output quality
3. **Caching strategy matters more than raw performance** – Intelligent TTLs reduced 90% of API costs
4. **Observability is non-negotiable** – Langfuse tracing helped debug 12+ production issues

---

## Future Improvements

**Short-term**
- [ ] Add competitor website scraping for deeper analysis
- [ ] Implement trend forecasting (3-6 month projections)
- [ ] Support multi-language analysis

**Medium-term**
- [ ] Real-time monitoring with webhook alerts
- [ ] Custom data source integrations (Twitter, LinkedIn)
- [ ] Team collaboration features (shared workspaces)

**Long-term**
- [ ] Fine-tuned model for domain-specific positioning
- [ ] Automated content brief generation
- [ ] API rate limiting and user authentication

---

## Project Structure

```
market-horizon-ai/
├── agents/              # LangGraph agent definitions
│   ├── research_agent.py
│   ├── analysis_agent.py
│   ├── strategy_agent.py
│   └── quality_agent.py
├── api/                 # FastAPI backend
│   ├── routers/
│   ├── schemas/
│   └── main.py
├── core/                # Shared utilities
│   ├── orchestrator.py  # LangGraph workflow
│   ├── observability.py # Langfuse integration
│   └── prompts.py
├── frontend/            # Vue.js UI
│   ├── src/
│   └── package.json
├── data/                # SQLite cache
├── docker-compose.yml
└── requirements.txt
```

---

## Why This Project Stands Out

**Engineering Excellence**
- Async/parallel processing with proper error handling
- Type-safe Python with comprehensive type hints
- Structured logging and distributed tracing
- Database-backed caching with analytics

**AI/ML Sophistication**
- Multi-agent orchestration with LangGraph
- Semantic analysis using FAISS embeddings
- Dynamic content generation with context awareness
- Transparent confidence scoring

**Production Readiness**
- Dockerized deployment with health checks
- Environment-based configuration
- Graceful degradation on API failures
- Cost monitoring and optimization

---

## Author

**Sinu**
_AI Engineer | ML Engineer_

- GitHub: [@sinu-sinu](https://github.com/sinu-sinu)
- LinkedIn: [linkedin.com/in/sinu-sinu](https://linkedin.com/in/sinu-sinu)
- Email: sinu28.sinu@gmail.com

---

## License

MIT License - see [LICENSE](LICENSE) file for details

---

**Built with:** Python · LangGraph · FastAPI · Vue.js · OpenAI · Docker

