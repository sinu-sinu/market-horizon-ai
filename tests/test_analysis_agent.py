"""
Tests for Analysis Agent
"""
import pytest
from agents.analysis_agent import AnalysisAgent
from tests.fixtures.sample_data import SAMPLE_RESEARCH_DATA, SAMPLE_ANALYSIS_INSIGHTS


class TestAnalysisAgent:
    """Test suite for Analysis Agent"""
    
    @pytest.fixture
    def agent(self):
        """Create Analysis Agent instance"""
        return AnalysisAgent()
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly"""
        assert agent is not None
        assert agent.embeddings is not None
        assert agent.text_splitter is not None
        assert agent.sentiment_analyzer is not None
    
    def test_analysis_output_structure(self, agent):
        """Test that analysis output has correct structure"""
        result = agent.run(SAMPLE_RESEARCH_DATA)
        
        # Verify structure
        assert "competitors" in result
        assert "content_themes" in result
        assert "competitor_attributes" in result
        assert "vectorstore_path" in result
        
        # Verify types
        assert isinstance(result["competitors"], list)
        assert isinstance(result["content_themes"], list)
        assert isinstance(result["competitor_attributes"], dict)
    
    def test_competitor_identification(self, agent):
        """Test competitor identification from sources"""
        result = agent.run(SAMPLE_RESEARCH_DATA)
        
        # Should identify some competitors
        assert len(result["competitors"]) > 0, "Should identify at least one competitor"
        
        # Competitors should be strings
        for comp in result["competitors"]:
            assert isinstance(comp, str)
            assert len(comp) > 0
    
    def test_theme_extraction(self, agent):
        """Test content theme extraction"""
        result = agent.run(SAMPLE_RESEARCH_DATA)
        
        themes = result["content_themes"]
       
        # Should extract some themes
        assert len(themes) > 0, "Should extract at least one theme"
        
        # Each theme should have required fields
        for theme in themes:
            assert "theme" in theme
            assert "frequency" in theme
            assert "sentiment" in theme
            assert isinstance(theme["frequency"], int)
            assert isinstance(theme["sentiment"], (int, float))
            assert -1 <= theme["sentiment"] <= 1  # VADER sentiment range
    
    def test_competitor_attributes(self, agent):
        """Test competitor attribute analysis"""
        result = agent.run(SAMPLE_RESEARCH_DATA)
        
        attributes = result["competitor_attributes"]
        
        # Should have attributes for identified competitors
        if result["competitors"]:
            assert len(attributes) > 0
            
            # Check first competitor's attributes
            first_comp = list(attributes.keys())[0]
            attrs = attributes[first_comp]
            
            assert "price_positioning" in attrs
            assert "target_market_size" in attrs
            assert "sentiment" in attrs
            assert "mention_count" in attrs
            
            # Verify value ranges
            assert 1 <= attrs["price_positioning"] <= 10
            assert 1 <= attrs["target_market_size"] <= 10
            assert -1 <= attrs["sentiment"] <= 1
            assert attrs["mention_count"] >= 0
    
    def test_empty_input_handling(self, agent):
        """Test handling of empty research data"""
        empty_data = {
            "sources": [],
            "trends": {},
            "discussions": [],
            "metadata": {"total_sources": 0}
        }
        
        result = agent.run(empty_data)
        
        # Should return valid empty structure
        assert isinstance(result, dict)
        assert len(result["competitors"]) == 0
        assert len(result["content_themes"]) == 0
        assert len(result["competitor_attributes"]) == 0
    
    def test_document_extraction(self, agent):
        """Test document text extraction"""
        documents = agent._extract_documents(SAMPLE_RESEARCH_DATA["sources"])
        
        # Should extract documents
        assert len(documents) > 0
        
        # Each document should be a string
        for doc in documents:
            assert isinstance(doc, str)
            assert len(doc) > 0


class TestAnalysisAgentMethods:
    """Test individual agent methods"""
    
    @pytest.fixture
    def agent(self):
        """Create Analysis Agent instance"""
        return AnalysisAgent()
    
    def test_sentiment_analysis(self, agent):
        """Test sentiment analysis functionality"""
        positive_text = "This is an excellent and amazing product!"
        negative_text = "This is terrible and awful software."
        neutral_text = "The software has features."
        
        positive_score = agent.sentiment_analyzer.polarity_scores(positive_text)["compound"]
        negative_score = agent.sentiment_analyzer.polarity_scores(negative_text)["compound"]
        neutral_score = agent.sentiment_analyzer.polarity_scores(neutral_text)["compound"]
        
        # Verify sentiment direction
        assert positive_score > 0, "Positive text should have positive sentiment"
        assert negative_score < 0, "Negative text should have negative sentiment"
        assert abs(neutral_score) < 0.5, "Neutral text should have neutral sentiment"
    
    def test_text_chunking(self, agent):
        """Test text splitter creates appropriate chunks"""
        long_text = "This is a test sentence. " * 100  # Create long text
        
        chunks = agent.text_splitter.create_documents([long_text])
        
        # Should create multiple chunks for long text
        assert len(chunks) > 1
        
        # Each chunk should be within size limits
        for chunk in chunks:
            assert len(chunk.page_content) <= 512 + 50  # chunk_size + overlap
    
    def test_fallback_competitor_detection(self, agent):
        """Test fallback competitor detection without spaCy"""
        sources = SAMPLE_RESEARCH_DATA["sources"]
        
        competitors = agent._fallback_competitor_detection(sources)
        
        # Should identify some potential competitors
        assert isinstance(competitors, list)
        
        # Each competitor should be a string
        for comp in competitors:
            assert isinstance(comp, str)
            assert len(comp) > 3  # Minimum length filter


class TestSampleData:
    """Validate sample data structure"""
    
    def test_sample_analysis_insights_structure(self):
        """Test that sample analysis insights have correct structure"""
        insights = SAMPLE_ANALYSIS_INSIGHTS
        
        assert "competitors" in insights
        assert "content_themes" in insights
        assert "competitor_attributes" in insights
        assert "vectorstore_path" in insights
        
        # Verify competitors
        assert isinstance(insights["competitors"], list)
        assert len(insights["competitors"]) > 0
        
        # Verify themes
        for theme in insights["content_themes"]:
            assert "theme" in theme
            assert "frequency" in theme
            assert "sentiment" in theme
        
        # Verify competitor attributes
        for comp, attrs in insights["competitor_attributes"].items():
            assert "price_positioning" in attrs
            assert "target_market_size" in attrs
            assert "sentiment" in attrs
            assert "mention_count" in attrs


# Integration test (requires OpenAI API key)
@pytest.mark.integration
def test_analysis_agent_with_vectorstore():
    """
    Integration test with actual vectorstore creation
    
    Mark: @pytest.mark.integration
    Run with: pytest tests/test_analysis_agent.py -m integration
    """
    agent = AnalysisAgent()
    
    result = agent.run(SAMPLE_RESEARCH_DATA)
    
    # Should create vectorstore
    assert result["vectorstore_path"] is not None
    assert "faiss_index" in result["vectorstore_path"]
    
    # Should have identified content
    assert len(result["competitors"]) > 0
    assert len(result["content_themes"]) > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])