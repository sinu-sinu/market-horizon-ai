"""
Tests for Research Agent
"""
import pytest
from agents.research_agent import ResearchAgent
from tests.fixtures.sample_data import SAMPLE_RESEARCH_DATA


class TestResearchAgent:
    """Test suite for Research Agent"""
    
    @pytest.fixture
    def agent(self):
        """Create Research Agent instance"""
        return ResearchAgent()
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly"""
        assert agent is not None
        assert agent.serper_api_key is not None
        assert agent.trends_client is not None
    
    def test_research_output_structure(self, agent):
        """Test that research output has correct structure"""
        # Use a simple query that should return results
        query = "test query"
        
        # Mock the _search_web, _get_trends, and _search_reddit methods
        # to avoid actual API calls during testing
        agent._search_web = lambda q: []
        agent._get_trends = lambda q: {}
        agent._search_reddit = lambda q, limit=10: []
        
        result = agent.run(query)
        
        # Verify structure
        assert "sources" in result
        assert "trends" in result
        assert "discussions" in result
        assert "metadata" in result
        
        # Verify metadata structure
        assert "total_sources" in result["metadata"]
        assert "source_types" in result["metadata"]
        assert isinstance(result["sources"], list)
        assert isinstance(result["discussions"], list)
        assert isinstance(result["trends"], dict)
    
    def test_web_source_structure(self):
        """Test web source data structure"""
        # Verify sample data has correct structure
        for source in SAMPLE_RESEARCH_DATA["sources"]:
            assert "url" in source
            assert "title" in source
            assert "snippet" in source
            assert "date" in source
            assert "source_type" in source
            assert source["source_type"] == "web"
    
    def test_metadata_calculation(self, agent):
        """Test metadata is calculated correctly"""
        # Mock methods
        test_sources = [{"url": "test1"}, {"url": "test2"}]
        test_discussions = [{"title": "disc1"}]
        
        agent._search_web = lambda q: test_sources
        agent._get_trends = lambda q: {"query": q}
        agent._search_reddit = lambda q, limit=10: test_discussions
        
        result = agent.run("test query")
        
        assert result["metadata"]["total_sources"] == 2
        assert result["metadata"]["source_types"]["web"] == 2
        assert result["metadata"]["source_types"]["reddit"] == 1
        assert result["metadata"]["source_types"]["trends"] == 1
    
    def test_empty_results_handling(self, agent):
        """Test that agent handles empty results gracefully"""
        # Mock methods to return empty results
        agent._search_web = lambda q: []
        agent._get_trends = lambda q: {}
        agent._search_reddit = lambda q, limit=10: []
        
        result = agent.run("nonexistent query 123456789")
        
        # Should still return valid structure
        assert isinstance(result, dict)
        assert result["metadata"]["total_sources"] == 0
        assert len(result["sources"]) == 0


class TestResearchAgentMethods:
    """Test individual agent methods"""
    
    @pytest.fixture
    def agent(self):
        """Create Research Agent instance"""
        return ResearchAgent()
    
    def test_trends_data_structure(self):
        """Test trends data structure from sample"""
        trends = SAMPLE_RESEARCH_DATA["trends"]
        
        assert "query" in trends
        assert "trend_data" in trends
        assert "average_interest" in trends
        assert isinstance(trends["trend_data"], dict)
        assert isinstance(trends["average_interest"], (int, float))
    
    def test_reddit_discussion_structure(self):
        """Test Reddit discussion structure from sample"""
        for discussion in SAMPLE_RESEARCH_DATA["discussions"]:
            assert "title" in discussion
            assert "url" in discussion
            assert "score" in discussion
            assert "num_comments" in discussion
            assert "created" in discussion
            assert "subreddit" in discussion
            assert "source_type" in discussion
            assert discussion["source_type"] == "reddit"


# Integration test (only runs if API keys are configured)
@pytest.mark.integration
def test_research_agent_with_real_api():
    """
    Integration test with real API calls
    
    Mark: @pytest.mark.integration
    Run with: pytest tests/test_research_agent.py -m integration
    """
    agent = ResearchAgent()
    
    # Use a simple, reliable query
    query = "CRM software"
    
    result = agent.run(query)
    
    # Verify we got some results
    assert result["metadata"]["total_sources"] > 0, "Should find at least some sources"
    
    # Verify structure
    if result["sources"]:
        source = result["sources"][0]
        assert "url" in source
        assert "title" in source
        assert len(source["title"]) > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])