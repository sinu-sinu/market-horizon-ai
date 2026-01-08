"""
Tests for Quality Agent
"""
import pytest
from agents.quality_agent import QualityAgent
from tests.fixtures.sample_data import (
    SAMPLE_RESEARCH_DATA,
    SAMPLE_ANALYSIS_INSIGHTS,
    SAMPLE_STRATEGY_RECOMMENDATIONS,
    SAMPLE_QUALITY_REPORT
)
from datetime import datetime


class TestQualityAgent:
    """Test suite for Quality Agent"""
    
    @pytest.fixture
    def agent(self):
        """Create Quality Agent instance"""
        return QualityAgent()
    
    @pytest.fixture
    def complete_state(self):
        """Create complete agent state for testing"""
        return {
            "query": "CRM tools for real estate agents",
            "parameters": {},
            "research_data": SAMPLE_RESEARCH_DATA,
            "analysis_insights": SAMPLE_ANALYSIS_INSIGHTS,
            "strategy_recommendations": SAMPLE_STRATEGY_RECOMMENDATIONS,
            "errors": [],
            "retry_count": 0,
            "start_time": datetime.now(),
            "current_agent": "quality",
            "total_tokens": 0,
            "api_calls": 3
        }
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly"""
        assert agent is not None
        assert agent.confidence_threshold == 0.75
    
    def test_quality_report_structure(self, agent, complete_state):
        """Test that quality report has correct structure"""
        result = agent.run(complete_state)
        
        # Verify main sections
        assert "report_metadata" in result
        assert "validated_insights" in result
        assert "quality_flags" in result
        assert "source_attribution" in result
        
        # Verify metadata fields
        metadata = result["report_metadata"]
        assert "query" in metadata
        assert "timestamp" in metadata
        assert "total_sources" in metadata
        assert "processing_time_seconds" in metadata
        assert "confidence_score" in metadata
        
        # Verify validated insights
        insights = result["validated_insights"]
        assert "competitors" in insights
        assert "content_themes" in insights
        assert "positioning_map" in insights
        assert "content_recommendations" in insights
        assert "strategic_recommendations" in insights
    
    def test_confidence_score_calculation(self, agent, complete_state):
        """Test confidence score calculation"""
        result = agent.run(complete_state)
        
        confidence = result["report_metadata"]["confidence_score"]
        
        # Confidence should be between 0 and 1
        assert 0.0 <= confidence <= 1.0
        
        # With good sample data, should have reasonable confidence
        assert confidence >= 0.5, "Sample data should yield reasonable confidence"
    
    def test_research_validation(self, agent):
        """Test research data validation"""
        # Test with sufficient sources
        good_research = SAMPLE_RESEARCH_DATA
        validation = agent._validate_research(good_research)
        
        assert validation["source_count"] >= 5
        assert validation["source_count_valid"] == True
        
        # Test with insufficient sources
        bad_research = {"sources": [{"title": "test"}]}
        validation = agent._validate_research(bad_research)
        
        assert validation["source_count_valid"] == False
        assert len(validation["issues"]) > 0
    
    def test_analysis_validation(self, agent):
        """Test analysis validation"""
        validation = agent._validate_analysis(
            SAMPLE_ANALYSIS_INSIGHTS,
            SAMPLE_RESEARCH_DATA
        )
        
        # Should validate competitors
        assert "validated_competitors" in validation
        assert "competitors_valid" in validation
        assert "themes_valid" in validation
    
    def test_strategy_validation(self, agent):
        """Test strategy validation"""
        validation = agent._validate_strategy(
            SAMPLE_STRATEGY_RECOMMENDATIONS,
            SAMPLE_ANALYSIS_INSIGHTS
        )
        
        assert "positioning_coverage" in validation
        assert "positioning_valid" in validation
        assert "recommendations_valid" in validation
        assert "moves_valid" in validation
        
        # Coverage should be between 0 and 1
        assert 0.0 <= validation["positioning_coverage"] <= 1.0
    
    def test_quality_flags_generation(self, agent, complete_state):
        """Test quality flag generation"""
        result = agent.run(complete_state)
        
        flags = result["quality_flags"]
        
        # Should generate some flags
        assert isinstance(flags, list)
        
        # Each flag should have required fields
        for flag in flags:
            assert "type" in flag
            assert "message" in flag
            assert "agent" in flag
            assert flag["type"] in ["info", "warning", "error"]
    
    def test_source_attribution(self, agent):
        """Test source attribution building"""
        attribution = agent._build_source_attribution(SAMPLE_RESEARCH_DATA)
        
        assert "total_sources" in attribution
        assert "source_breakdown" in attribution
        assert "date_range" in attribution
        
        # Total sources should match
        assert attribution["total_sources"] == len(SAMPLE_RESEARCH_DATA["sources"])
    
    def test_empty_state_handling(self, agent):
        """Test handling of empty state"""
        empty_state = {
            "query": "test",
            "parameters": {},
            "research_data": {},
            "analysis_insights": {},
            "strategy_recommendations": {},
            "errors": [],
            "retry_count": 0,
            "start_time": datetime.now(),
            "current_agent": "quality",
            "total_tokens": 0,
            "api_calls": 0
        }
        
        result = agent.run(empty_state)
        
        # Should still return valid structure
        assert isinstance(result, dict)
        assert "report_metadata" in result
        assert "quality_flags" in result
        
        # Confidence should be low
        assert result["report_metadata"]["confidence_score"] < 0.5


class TestQualityAgentValidation:
    """Test validation logic"""
    
    @pytest.fixture
    def agent(self):
        """Create Quality Agent instance"""
        return QualityAgent()
    
    def test_confidence_with_many_sources(self, agent):
        """Test confidence increases with more sources"""
        # Create research data with different source counts
        few_sources = {
            "sources": [{"title": f"Source {i}"} for i in range(5)],
            "trends": {},
            "discussions": []
        }
        
        many_sources = {
            "sources": [{"title": f"Source {i}"} for i in range(20)],
            "trends": {},
            "discussions": []
        }
        
        # Create minimal validation (all pass)
        validation_all_pass = {
            "research_validation": {"valid": True},
            "analysis_validation": {"valid": True},
            "strategy_validation": {"valid": True}
        }
        
        confidence_few = agent._calculate_confidence(validation_all_pass, few_sources)
        confidence_many = agent._calculate_confidence(validation_all_pass, many_sources)
        
        # More sources should give higher confidence
        assert confidence_many > confidence_few
    
    def test_confidence_with_failed_validations(self, agent):
        """Test confidence decreases with failed validations"""
        research = SAMPLE_RESEARCH_DATA
        
        validation_all_pass = {
            "research_validation": {"valid": True},
            "analysis_validation": {"valid": True},
            "strategy_validation": {"valid": True}
        }
        
        validation_some_fail = {
            "research_validation": {"valid": False},
            "analysis_validation": {"valid": True},
            "strategy_validation": {"valid": False}
        }
        
        confidence_pass = agent._calculate_confidence(validation_all_pass, research)
        confidence_fail = agent._calculate_confidence(validation_some_fail, research)
        
        # Failed validations should lower confidence
        assert confidence_fail < confidence_pass


class TestSampleData:
    """Validate sample data structure"""
    
    def test_sample_quality_report_structure(self):
        """Test that sample quality report has correct structure"""
        report = SAMPLE_QUALITY_REPORT
        
        assert "report_metadata" in report
        assert "validated_insights" in report
        assert "quality_flags" in report
        assert "source_attribution" in report
        
        # Verify metadata
        metadata = report["report_metadata"]
        assert "query" in metadata
        assert "confidence_score" in metadata
        assert 0.0 <= metadata["confidence_score"] <= 1.0
        
        # Verify insights
        insights = report["validated_insights"]
        assert isinstance(insights["competitors"], list)
        assert isinstance(insights["content_themes"], list)
        assert isinstance(insights["positioning_map"], dict)
        
        # Verify quality flags
        for flag in report["quality_flags"]:
            assert "type" in flag
            assert "message" in flag
            assert flag["type"] in ["info", "warning", "error"]


# Integration test
@pytest.mark.integration
def test_quality_agent_full_pipeline():
    """
    Integration test with complete pipeline data
    
    Mark: @pytest.mark.integration
    Run with: pytest tests/test_quality_agent.py -m integration
    """
    agent = QualityAgent()
    
    complete_state = {
        "query": "CRM tools for real estate agents",
        "parameters": {},
        "research_data": SAMPLE_RESEARCH_DATA,
        "analysis_insights": SAMPLE_ANALYSIS_INSIGHTS,
        "strategy_recommendations": SAMPLE_STRATEGY_RECOMMENDATIONS,
        "errors": [],
        "retry_count": 0,
        "start_time": datetime.now(),
        "current_agent": "quality",
        "total_tokens": 1000,
        "api_calls": 3
    }
    
    result = agent.run(complete_state)
    
    # Should produce complete report
    assert result["report_metadata"]["confidence_score"] >= 0.7
    assert len(result["validated_insights"]["competitors"]) > 0
    assert result["report_metadata"]["total_sources"] > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])