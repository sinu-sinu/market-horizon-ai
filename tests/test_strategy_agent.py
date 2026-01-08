"""
Tests for Strategy Agent
"""
import pytest
from agents.strategy_agent import StrategyAgent
from tests.fixtures.sample_data import SAMPLE_ANALYSIS_INSIGHTS, SAMPLE_STRATEGY_RECOMMENDATIONS


class TestStrategyAgent:
    """Test suite for Strategy Agent"""
    
    @pytest.fixture
    def agent(self):
        """Create Strategy Agent instance"""
        return StrategyAgent()
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly"""
        assert agent is not None
        assert agent.llm is not None
    
    def test_strategy_output_structure(self, agent):
        """Test that strategy output has correct structure"""
        result = agent.run(SAMPLE_ANALYSIS_INSIGHTS)
        
        # Verify structure
        assert "positioning_map" in result
        assert "opportunity_zones" in result
        assert "content_recommendations" in result
        assert "strategic_moves" in result
        
        # Verify positioning map structure
        assert "dimensions" in result["positioning_map"]
        assert "companies" in result["positioning_map"]
        
        # Verify types
        assert isinstance(result["opportunity_zones"], list)
        assert isinstance(result["content_recommendations"], list)
        assert isinstance(result["strategic_moves"], list)
    
    def test_positioning_map_generation(self, agent):
        """Test positioning map generation"""
        result = agent.run(SAMPLE_ANALYSIS_INSIGHTS)
        
        positioning_map = result["positioning_map"]
        
        # Should have dimensions
        assert "x_axis" in positioning_map["dimensions"]
        assert "y_axis" in positioning_map["dimensions"]
        
        # Should have positioned companies
        companies = positioning_map["companies"]
        assert len(companies) > 0, "Should position at least one company"
        
        # Check coordinate validity
        for company, coords in companies.items():
            assert "x" in coords
            assert "y" in coords
            assert 1 <= coords["x"] <= 10, f"X coordinate for {company} out of range"
            assert 1 <= coords["y"] <= 10, f"Y coordinate for {company} out of range"
    
    def test_opportunity_zones_detection(self, agent):
        """Test opportunity zone detection"""
        result = agent.run(SAMPLE_ANALYSIS_INSIGHTS)
        
        zones = result["opportunity_zones"]
        
        # Each zone should have required fields
        for zone in zones:
            assert "coordinates" in zone
            assert "description" in zone
            assert "rationale" in zone
            assert "opportunity_score" in zone
            
            # Verify coordinate structure
            coords = zone["coordinates"]
            assert "x" in coords
            assert "y" in coords
            assert 1 <= coords["x"] <= 10
            assert 1 <= coords["y"] <= 10
            
            # Verify score is positive
            assert zone["opportunity_score"] > 0
    
    def test_content_recommendations(self, agent):
        """Test content recommendation generation"""
        result = agent.run(SAMPLE_ANALYSIS_INSIGHTS)
        
        recommendations = result["content_recommendations"]
        
        # Should generate some recommendations
        assert len(recommendations) > 0, "Should generate at least one recommendation"
        
        # Check recommendation structure
        for rec in recommendations:
            assert "topic" in rec
            assert "priority" in rec
            assert "opportunity_score" in rec
            assert "recommended_format" in rec
            
            # Verify priority values
            assert rec["priority"] in ["high", "medium", "low"]
            
            # Verify score range
            assert 0 <= rec["opportunity_score"] <= 10
    
    def test_strategic_moves(self, agent):
        """Test strategic move generation"""
        result = agent.run(SAMPLE_ANALYSIS_INSIGHTS)
        
        moves = result["strategic_moves"]
        
        # Should generate some strategic moves
        assert len(moves) > 0, "Should generate at least one strategic move"
        
        # Each move should be a non-empty string
        for move in moves:
            assert isinstance(move, str)
            assert len(move) > 0
            assert len(move) < 500  # Reasonable length
    
    def test_empty_input_handling(self, agent):
        """Test handling of empty analysis insights"""
        empty_insights = {
            "competitors": [],
            "content_themes": [],
            "competitor_attributes": {},
            "vectorstore_path": None
        }
        
        result = agent.run(empty_insights)
        
        # Should return valid empty structure
        assert isinstance(result, dict)
        assert len(result["positioning_map"]["companies"]) == 0
        assert len(result["opportunity_zones"]) == 0
    
    def test_coordinate_validation(self, agent):
        """Test coordinate validation function"""
        # Test valid coordinates
        valid_data = {
            "Company A": {"x": 5.0, "y": 7.0, "rationale": "test"}
        }
        
        cleaned = agent._validate_coordinates(valid_data)
       
        assert "Company A" in cleaned
        assert cleaned["Company A"]["x"] == 5.0
        assert cleaned["Company A"]["y"] == 7.0
        
        # Test out-of-range coordinates (should be clamped)
        invalid_data = {
            "Company B": {"x": 15.0, "y": -2.0, "rationale": "test"}
        }
        
        cleaned = agent._validate_coordinates(invalid_data)
        
        assert cleaned["Company B"]["x"] == 10.0  # Clamped to max
        assert cleaned["Company B"]["y"] == 1.0   # Clamped to min


class TestStrategyAgentMethods:
    """Test individual agent methods"""
    
    @pytest.fixture
    def agent(self):
        """Create Strategy Agent instance"""
        return StrategyAgent()
    
    def test_content_format_suggestion(self, agent):
        """Test content format suggestion"""
        # Test different theme types
        tutorial_theme = "How to use CRM"
        comparison_theme = "Salesforce vs HubSpot"
        review_theme = "Best CRM tools"
        case_theme = "Case study examples"
        general_theme = "CRM features"
        
        tutorial_format = agent._suggest_content_format(tutorial_theme)
        comparison_format = agent._suggest_content_format(comparison_theme)
        review_format = agent._suggest_content_format(review_theme)
        case_format = agent._suggest_content_format(case_theme)
        general_format = agent._suggest_content_format(general_theme)
        
        # Verify appropriate formats suggested
        assert "tutorial" in tutorial_format.lower() or "video" in tutorial_format.lower()
        assert "comparison" in comparison_format.lower() or "infographic" in comparison_format.lower()
        assert "review" in review_format.lower() or "checklist" in review_format.lower()
        assert "case" in case_format.lower() or "webinar" in case_format.lower()
        assert isinstance(general_format, str)
    
    def test_fallback_positioning(self, agent):
        """Test fallback positioning logic"""
        competitors = ["Company A", "Company B", "Company C"]
        
        positioning = agent._fallback_positioning(competitors)
        
        # Should position all competitors
        assert len(positioning) == 3
        
        # Each should have valid coordinates
        for comp in competitors:
            assert comp in positioning
            assert "x" in positioning[comp]
            assert "y" in positioning[comp]
            assert 1 <= positioning[comp]["x"] <= 10
            assert 1 <= positioning[comp]["y"] <= 10


class TestSampleData:
    """Validate sample data structure"""
    
    def test_sample_strategy_recommendations_structure(self):
        """Test that sample strategy recommendations have correct structure"""
        strategy = SAMPLE_STRATEGY_RECOMMENDATIONS
        
        assert "positioning_map" in strategy
        assert "opportunity_zones" in strategy
        assert "content_recommendations" in strategy
        assert "strategic_moves" in strategy
        
        # Verify positioning map
        assert "dimensions" in strategy["positioning_map"]
        assert "companies" in strategy["positioning_map"]
        
        # Verify companies have coordinates
        for company, coords in strategy["positioning_map"]["companies"].items():
            assert "x" in coords
            assert "y" in coords
            assert 1 <= coords["x"] <= 10
            assert 1 <= coords["y"] <= 10
        
        # Verify opportunity zones
        for zone in strategy["opportunity_zones"]:
            assert "coordinates" in zone
            assert "description" in zone
            assert "opportunity_score" in zone
        
        # Verify content recommendations
        for rec in strategy["content_recommendations"]:
            assert "topic" in rec
            assert "priority" in rec
            assert "opportunity_score" in rec


# Integration test (requires OpenAI API key)
@pytest.mark.integration
def test_strategy_agent_with_llm():
    """
    Integration test with actual LLM calls
    
    Mark: @pytest.mark.integration
    Run with: pytest tests/test_strategy_agent.py -m integration
    """
    agent = StrategyAgent()
    
    result = agent.run(SAMPLE_ANALYSIS_INSIGHTS)
    
    # Should generate complete output
    assert len(result["positioning_map"]["companies"]) > 0
    assert len(result["strategic_moves"]) > 0
    
    # Positioning should be based on LLM analysis
    companies = result["positioning_map"]["companies"]
    for coords in companies.values():
        assert 1 <= coords["x"] <= 10
        assert 1 <= coords["y"] <= 10


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])