from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List
from core.config import config
from utils.debug_exporter import debug_exporter
import logging
import os
import json
import re

logger = logging.getLogger(__name__)


class AnalysisAgent:
    """
    Analysis Agent - Processes research data and extracts patterns
    
    Features:
    - Text chunking and embedding with LangChain
    - FAISS vector store for semantic search
    - NER-based competitor identification using spaCy
    - Sentiment analysis with VADER
    - Theme extraction
    """
    
    def __init__(self):
        """Initialize analysis tools"""
        # OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            dimensions=1536,
            api_key=config.OPENAI_API_KEY
        )

        # OpenAI LLM for competitor extraction
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",  # Fast and cheap for extraction
            temperature=0,
            api_key=config.OPENAI_API_KEY
        )

        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        # spaCy for NER
        try:
            self.nlp = spacy.load("en_core_web_lg")
            logger.info("spaCy large model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load spaCy model: {e}")
            logger.info("Run: python -m spacy download en_core_web_lg")
            self.nlp = None

        # VADER for sentiment
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

        logger.info("Analysis Agent initialized")
    
    def run(self, research_data: Dict) -> Dict:
        """
        Analyze research data and extract insights
        
        Args:
            research_data: Output from Research Agent
            
        Returns:
            Dict with competitors, themes, attributes, vectorstore path
        """
        logger.info("Analysis Agent: Processing research data")
        
        if not research_data or not research_data.get("sources"):
            logger.warning("No research data to analyze")
            return self._empty_output()
        
        # Extract text from sources
        documents = self._extract_documents(research_data["sources"])
        
        if not documents:
            logger.warning("No documents extracted from sources")
            return self._empty_output()
        
        # Chunk and embed
        chunks = self.text_splitter.create_documents(documents)
        logger.info(f"Created {len(chunks)} document chunks")
        
        # Create vectorstore
        try:
            vectorstore = FAISS.from_documents(chunks, self.embeddings)
            vectorstore_path = self._save_vectorstore(vectorstore)
            logger.info(f"Vectorstore created and saved to {vectorstore_path}")
        except Exception as e:
            logger.error(f"Failed to create vectorstore: {e}")
            vectorstore = None
            vectorstore_path = None
        
        # Extract insights
        competitors = self._identify_competitors(research_data["sources"])
        themes = self._extract_themes(research_data["sources"])
        competitor_attributes = self._analyze_competitors(
            competitors,
            vectorstore,
            research_data["sources"]
        )

        # DEBUG: Export debug report (if debug mode enabled)
        try:
            if logger.level <= logging.DEBUG:
                query = research_data.get("query", "unknown")
                debug_exporter.export_analysis_debug(
                    query=query,
                    sources=research_data["sources"],
                    llm_competitors=getattr(self, '_last_llm_competitors', []),
                    ner_competitors=getattr(self, '_last_ner_competitors', []),
                    final_competitors=competitors,
                    validation_results=None  # Will be filled by quality agent
                )
        except Exception as e:
            logger.warning(f"Failed to export debug report: {e}")
        
        output = {
            "competitors": competitors,
            "content_themes": themes,
            "competitor_attributes": competitor_attributes,
            "vectorstore_path": vectorstore_path
        }
        
        logger.info(f"Analysis Agent: Identified {len(competitors)} competitors, {len(themes)} themes")
        return output
    
    def _extract_documents(self, sources: List[Dict]) -> List[str]:
        """
        Extract text from sources for analysis
        
        Args:
            sources: List of source dictionaries
            
        Returns:
            List of text strings
        """
        documents = []
        
        for source in sources:
            # Combine title and snippet for rich context
            text = f"{source.get('title', '')}. {source.get('snippet', '')}"
            if text.strip():
                documents.append(text)
        
        logger.debug(f"Extracted {len(documents)} documents from {len(sources)} sources")
        return documents
    
    def _identify_competitors(self, sources: List[Dict]) -> List[str]:
        """
        Use hybrid approach (LLM + NER) to identify company names from sources

        Args:
            sources: List of source dictionaries

        Returns:
            List of competitor names
        """
        # Step 1: Use LLM extraction (primary method)
        llm_competitors = self._llm_competitor_extraction(sources)

        # Step 2: Use spaCy NER as backup/enhancement (DISABLED - causes noise)
        # NER was extracting title fragments like "Best Influencer Marketing Software"
        # LLM extraction is much more accurate, so we disable NER
        ner_competitors = []
        # if self.nlp:
        #     ner_competitors = self._ner_competitor_extraction(sources)
        # else:
        #     logger.warning("spaCy not available, skipping NER extraction")
        #     ner_competitors = []

        # Save for debug export
        self._last_llm_competitors = llm_competitors
        self._last_ner_competitors = ner_competitors

        # Step 3: Use LLM results directly (NER disabled)
        all_competitors = {}

        # Use LLM results only
        for comp in llm_competitors:
            all_competitors[comp] = all_competitors.get(comp, 0) + 1

        # NER disabled due to noise
        # for comp in ner_competitors:
        #     all_competitors[comp] = all_competitors.get(comp, 0) + 1

        # Sort by combined score and return top 15
        sorted_competitors = sorted(
            all_competitors.items(),
            key=lambda x: x[1],
            reverse=True
        )

        result = [name for name, score in sorted_competitors[:15]]
        logger.info(f"Identified {len(result)} competitors (LLM only - NER disabled due to noise)")
        return result

    def _llm_competitor_extraction(self, sources: List[Dict]) -> List[str]:
        """
        Use LLM to extract competitor names from sources

        Args:
            sources: List of source dictionaries

        Returns:
            List of competitor company/product names
        """
        # Combine source texts for analysis
        texts = []
        for source in sources[:15]:  # Limit to 15 sources to avoid token limits
            text = f"{source.get('title', '')}. {source.get('snippet', '')}"
            if text.strip():
                texts.append(text)

        combined_text = "\n\n".join(texts)

        # DEBUG: Log the input text being sent to LLM
        logger.debug("=" * 80)
        logger.debug("LLM INPUT TEXT (first 1000 chars):")
        logger.debug(combined_text[:1000])
        logger.debug("=" * 80)

        # Create extraction prompt with better context
        prompt = f"""You are analyzing search results to find competitor companies and products.

        Extract ALL company names, product names, and software tool names mentioned in the text below.

        DO EXTRACT (examples of what TO extract):
        - Software companies: "HubSpot", "Salesforce", "Zoho"
        - Influencer platforms: "Aspire", "Grin", "Upfluence", "Creator.co", "Traackr"
        - SaaS products: "ActiveCampaign", "Pipedrive", "Monday.com"
        - Any proper noun that is a brand/company/product name

        DO NOT EXTRACT (examples of what NOT to extract):
        - Generic categories: "CRM", "Software", "Tools", "Platform", "App"
        - Adjectives: "Best", "Top", "Free", "Simple", "Easy", "Popular"
        - Common words: "Business", "Small", "Marketing", "Management"
        - Sentence fragments or phrases
        - Acronyms without context (unless they're well-known brands like "IBM")

        Text to analyze:
        {combined_text}

        IMPORTANT: Be comprehensive - extract ALL company/product names you can find, even if mentioned only once.

        Return ONLY a JSON array of company/product names: ["Company1", "Company2", "Company3", ...]
        No explanations, just the JSON array."""

        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()

            # DEBUG: Log raw LLM response
            logger.debug("LLM RAW RESPONSE:")
            logger.debug(content)
            logger.debug("=" * 80)

            # Parse JSON response
            # Handle cases where LLM might wrap in markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            competitors = json.loads(content)

            # DEBUG: Log parsed competitors before filtering
            logger.debug(f"LLM PARSED COMPETITORS (before filtering): {competitors}")

            # Additional filtering: remove common stop words
            stop_words = {
                "best", "top", "free", "simple", "easy", "software", "tool", "tools",
                "platform", "solution", "solutions", "service", "services", "app", "apps",
                "business", "small", "crm", "management", "system", "contact", "marketing"
            }

            filtered = []
            filtered_out = []

            for comp in competitors:
                if isinstance(comp, str) and len(comp) > 2:
                    # Check each filter condition
                    is_stop_word = comp.lower() in stop_words
                    is_all_caps = bool(re.match(r'^[A-Z\s]+$', comp))

                    if is_stop_word or is_all_caps:
                        filtered_out.append((comp, "stop_word" if is_stop_word else "all_caps"))
                    else:
                        filtered.append(comp)

            # DEBUG: Log filtering results
            logger.debug(f"LLM FILTERED COMPETITORS ({len(filtered)}): {filtered}")
            if filtered_out:
                logger.debug(f"LLM FILTERED OUT ({len(filtered_out)}): {filtered_out}")

            logger.info(f"LLM extracted {len(filtered)} competitors from {len(sources)} sources")
            return filtered[:15]  # Increased from 10 to 15

        except Exception as e:
            logger.error(f"LLM competitor extraction failed: {e}")
            logger.error(f"Raw response: {content if 'content' in locals() else 'N/A'}")
            return []

    def _ner_competitor_extraction(self, sources: List[Dict]) -> List[str]:
        """
        Use spaCy NER to extract organization names

        Args:
            sources: List of source dictionaries

        Returns:
            List of organization names
        """
        competitors = {}  # Use dict to track frequency

        for source in sources:
            # Combine title and snippet
            text = f"{source.get('title', '')} {source.get('snippet', '')}"

            # Run NER
            doc = self.nlp(text)

            # Extract ORG entities
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    name = ent.text.strip()
                    # Filter out common non-company words
                    stop_words = {"The", "Inc", "LLC", "Ltd", "Best", "Top", "Free"}
                    if len(name) > 2 and name not in stop_words:
                        competitors[name] = competitors.get(name, 0) + 1

        # Sort by frequency and return top 10
        sorted_competitors = sorted(
            competitors.items(),
            key=lambda x: x[1],
            reverse=True
        )

        result = [name for name, count in sorted_competitors[:15]]
        logger.info(f"NER extracted {len(result)} competitors")
        return result
    
    def _fallback_competitor_detection(self, sources: List[Dict]) -> List[str]:
        """
        Improved fallback method for competitor detection without spaCy/LLM

        Args:
            sources: List of source dictionaries

        Returns:
            List of potential competitor names
        """
        # Stop words to filter out
        stop_words = {
            # Common adjectives
            "best", "top", "free", "simple", "easy", "popular", "leading",
            "powerful", "essential", "ultimate", "complete", "perfect",
            # Generic business terms
            "software", "tool", "tools", "platform", "solution", "solutions",
            "service", "services", "app", "apps", "system", "systems",
            "business", "small", "contact", "management", "customer",
            # CRM-specific terms
            "crm", "marketing", "sales", "email", "campaign",
            # Common words
            "the", "and", "for", "with", "your", "more", "about",
            "this", "that", "from", "their", "they", "what", "when"
        }

        competitors_count = {}

        for source in sources:
            text = f"{source.get('title', '')} {source.get('snippet', '')}"

            # Find potential company names (capitalized words, including multi-word names)
            # Match patterns like "HubSpot", "Zoho CRM", "ActiveCampaign"
            potential_names = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', text)

            for name in potential_names:
                name = name.strip()
                name_lower = name.lower()

                # Filter by length and stop words
                if (
                    len(name) > 3
                    and name_lower not in stop_words
                    and not name.isupper()  # Skip all-caps words (likely acronyms)
                    and not re.match(r'^\d+', name)  # Skip numbers
                ):
                    competitors_count[name] = competitors_count.get(name, 0) + 1

        # Sort by frequency and take top 10
        sorted_competitors = sorted(
            competitors_count.items(),
            key=lambda x: x[1],
            reverse=True
        )

        result = [name for name, count in sorted_competitors[:10]]
        logger.info(f"Fallback extracted {len(result)} potential competitors")
        return result
    
    def _extract_themes(self, sources: List[Dict]) -> List[Dict]:
        """
        Identify content themes using keyword frequency
        
        Args:
            sources: List of source dictionaries
            
        Returns:
            List of theme dictionaries
        """
        # For MVP, use simple keyword counting
        # In production, this would use clustering or topic modeling
        
        from collections import Counter
        import re
        
        # Extended stop words to filter garbage themes
        stop_words = set([
            # Common articles and prepositions
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but',
            'in', 'with', 'to', 'for', 'of', 'as', 'by', 'that', 'this',
            'from', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had',
            # Generic business terms that shouldn't be themes
            'best', 'top', 'free', 'simple', 'easy', 'software', 'tool', 'tools',
            'platform', 'solution', 'service', 'app', 'system', 'business',
            'company', 'product', 'features', 'pricing', 'review', 'reviews',
            # Common query words
            'what', 'when', 'where', 'which', 'who', 'how', 'why',
            'can', 'will', 'should', 'would', 'could', 'may', 'might',
            'more', 'most', 'some', 'any', 'all', 'each', 'every',
            'their', 'they', 'them', 'your', 'you', 'our', 'we', 'us'
        ])
        
        # Extract all words
        all_text = " ".join([
            f"{s.get('title', '')} {s.get('snippet', '')}" 
            for s in sources
        ])
        
        # Clean and tokenize (lowercase, min 4 chars)
        words = re.findall(r'\b[a-z]{4,}\b', all_text.lower())

        # Filter stop words and count
        word_counts = Counter([
            word for word in words
            if word not in stop_words
        ])

        # DEBUG: Log theme extraction
        logger.debug(f"Theme extraction: {len(word_counts)} unique words after filtering")
        logger.debug(f"Top 10 themes: {word_counts.most_common(10)}")
        
        # Get top themes
        themes = []
        for word, count in word_counts.most_common(5):
            # Calculate sentiment for this theme
            theme_texts = [
                s.get('snippet', '') 
                for s in sources 
                if word in s.get('snippet', '').lower()
            ]
            
            sentiments = [
                self.sentiment_analyzer.polarity_scores(text)['compound']
                for text in theme_texts if text
            ]
            
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
            
            themes.append({
                "theme": word.capitalize(),
                "frequency": count,
                "sentiment": round(avg_sentiment, 2),
                "key_phrases": [word]  # Simplified for MVP
            })
        
        logger.info(f"Extracted {len(themes)} content themes")
        return themes
    
    def _analyze_competitors(
        self, 
        competitors: List[str], 
        vectorstore, 
        sources: List[Dict]
    ) -> Dict:
        """
        Analyze competitor attributes
        
        Args:
            competitors: List of competitor names
            vectorstore: FAISS vectorstore (or None)
            sources: Original sources for fallback
            
        Returns:
            Dict mapping competitor names to attributes
        """
        attributes = {}
        
        for competitor in competitors:
            if vectorstore:
                try:
                    # Query vectorstore for competitor mentions
                    docs = vectorstore.similarity_search(competitor, k=5)
                    texts = [doc.page_content for doc in docs]
                except Exception as e:
                    logger.warning(f"Vectorstore query failed for {competitor}: {e}")
                    texts = self._fallback_text_search(competitor, sources)
            else:
                texts = self._fallback_text_search(competitor, sources)
            
            # Analyze sentiment
            sentiment_scores = [
                self.sentiment_analyzer.polarity_scores(t)["compound"]
                for t in texts if t
            ]
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
            
            # Placeholder for positioning (will be determined by Strategy Agent)
            attributes[competitor] = {
                "price_positioning": 5.0,  # Neutral default
                "target_market_size": 5.0,  # Neutral default
                "sentiment": round(avg_sentiment, 2),
                "mention_count": len(texts)
            }
        
        logger.info(f"Analyzed attributes for {len(attributes)} competitors")
        return attributes
    
    def _fallback_text_search(self, competitor: str, sources: List[Dict]) -> List[str]:
        """
        Fallback text search when vectorstore is not available
        
        Args:
            competitor: Competitor name to search for
            sources: List of sources
            
        Returns:
            List of text snippets mentioning the competitor
        """
        texts = []
        competitor_lower = competitor.lower()
        
        for source in sources:
            text = f"{source.get('title', '')} {source.get('snippet', '')}"
            if competitor_lower in text.lower():
                texts.append(text)
        
        return texts
    
    def _save_vectorstore(self, vectorstore) -> str:
        """
        Save FAISS vectorstore to disk
        
        Args:
            vectorstore: FAISS vectorstore
            
        Returns:
            Path where vectorstore was saved
        """
        path = "data/faiss_index"
        
        # Create directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        
        # Save vectorstore
        vectorstore.save_local(path)
        
        logger.info(f"Vectorstore saved to {path}")
        return path
    
    def _empty_output(self) -> Dict:
        """Return empty output structure"""
        return {
            "competitors": [],
            "content_themes": [],
            "competitor_attributes": {},
            "vectorstore_path": None
        }


# CLI testing
if __name__ == "__main__":
    import json
    import sys
    from tests.fixtures.sample_data import SAMPLE_RESEARCH_DATA
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test the agent
    agent = AnalysisAgent()
    
    # Use sample data for testing
    print("\n" + "="*60)
    print("ANALYSIS AGENT TEST")
    print("="*60)
    print("Using sample research data...")
    
    result = agent.run(SAMPLE_RESEARCH_DATA)
    
    # Print results
    print(f"\nCompetitors identified: {len(result['competitors'])}")
    for comp in result['competitors'][:5]:
        print(f"  - {comp}")
    
    print(f"\nContent themes: {len(result['content_themes'])}")
    for theme in result['content_themes']:
        print(f"  - {theme['theme']}: {theme['frequency']} mentions, sentiment {theme['sentiment']}")
    
    print(f"\nCompetitor attributes: {len(result['competitor_attributes'])}")
    for comp, attrs in list(result['competitor_attributes'].items())[:3]:
        print(f"  - {comp}: sentiment {attrs['sentiment']}, {attrs['mention_count']} mentions")
    
    print(f"\nVectorstore: {result['vectorstore_path']}")
    
    # Save full output
    output_path = "outputs/reports/analysis_agent_test.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print("\n" + "="*60)
    print(f"Full output saved to: {output_path}")