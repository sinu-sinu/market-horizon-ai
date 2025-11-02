# Market Horizon AI

> AI-powered market intelligence system that helps marketers understand their competitive landscape through autonomous multi-agent analysis.

##  What It Does

Market Horizon AI automatically gathers and analyzes competitive intelligence to provide:

- **Competitive Positioning Maps** - Visual 2D maps showing where competitors stand in the market
- **Content Gap Analysis** - Discover high-opportunity topics your competitors aren't covering
- **Strategic Recommendations** - Data-driven insights for positioning and content strategy

##  Current Status

**Early Development Stage** - Building the core multi-agent system

This is a portfolio project demonstrating advanced AI engineering concepts including multi-agent orchestration, RAG implementation, and real-time data integration.

##  Architecture

The system uses four specialized AI agents:

1. **Research Agent** - Gathers data from web searches, trends, and discussions
2. **Analysis Agent** - Extracts patterns and insights using RAG and semantic analysis
3. **Strategy Agent** - Generates positioning coordinates and content recommendations
4. **Quality Agent** - Validates accuracy and synthesizes the final report

##  Tech Stack

- **Framework:** LangChain + LangGraph for agent orchestration
- **LLM:** GPT-4.1-mini for strategic reasoning
- **Data Sources:** Serper.dev API, Google Trends, Reddit API
- **Vector Store:** FAISS for semantic search
- **Visualization:** Plotly for interactive positioning maps
- **UI:** Streamlit

##  Prerequisites

- Python 3.9+
- OpenAI API key
- Serper.dev API key (free tier available)

##  Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/market-horizon-ai.git
cd market-horizon-ai

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

##  Configuration

Create a `.env` file with:

```bash
OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
```

## 📖 Usage

Coming soon - The system is currently under development.

## 🗺️ Roadmap

- [x] Project planning and architecture design
- [x] phase 1: Research & Analysis Agents
- [x] phase 2: Strategy Agent + Positioning Map
- [ ] phase 3: Quality Agent + Streamlit UI
- [ ] phase 4: Caching + Testing
- [ ] phase 5: Content Gap Analysis
- [ ] phase 6: Deployment

## 💡 Example Use Cases

- **Marketing Strategists** - Identify positioning opportunities and competitive gaps
- **Content Managers** - Discover high-performing content topics
- **Product Marketers** - Monitor competitor messaging
- **Growth Marketers** - Understand audience behavior patterns

##  License

MIT License - See LICENSE file for details

##  Contributing

This is a portfolio project, but feedback and suggestions are welcome! Feel free to open an issue or reach out.

##  Contact

For questions or collaboration: sinu28.sinu@gmail.com / linkedin/in/sinu-sinu

---

**Note:** This project is for educational and portfolio purposes. All data is gathered from public sources with proper attribution.