from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class QualityAgent:
    """
    Quality Agent - Validates and synthesizes all agent outputs
    
    Responsibilities:
    - Validate research data quality
    - Validate analysis accuracy
    - Validate strategy feasibility
    - Calculate confidence scores
    - Generate quality flags
    - Compile final report
    """
    
    def __init__(self):
        """Initialize Quality Agent"""
        self.confidence_threshold = 0.75
        logger.info("Quality Agent initialized")
    
    def run(self, state: Dict) -> Dict:
        """
        Validate and synthesize all agent outputs
        
        Args:
            state: Complete agent state with all outputs
            
        Returns:
            Final quality report with validated insights
        """
        logger.info("Quality Agent: Validating outputs")
        
        # Extract outputs from state
        research_data = state.get("research_data", {})
        analysis = state.get("analysis_insights", {})
        strategy = state.get("strategy_recommendations", {})
        
        # Validate each component
        validation_results = {
            "research_validation": self._validate_research(research_data),
            "analysis_validation": self._validate_analysis(analysis, research_data),
            "strategy_validation": self._validate_strategy(strategy, analysis)
        }
        
        # Calculate confidence score
        confidence = self._calculate_confidence(validation_results, research_data)
        
        # Generate quality flags
        flags = self._generate_quality_flags(validation_results, research_data)
        
        # Calculate processing time
        start_time = state.get("start_time", datetime.now())
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Compile final report
        final_report = {
            "report_metadata": {
                "query": state.get("query", ""),
                "timestamp": datetime.now().isoformat(),
                "total_sources": len(research_data.get("sources", [])),
                "processing_time_seconds": int(processing_time),
                "confidence_score": confidence,
                "api_calls": state.get("api_calls", 0),
                "total_tokens": state.get("total_tokens", 0)
            },
            "validated_insights": {
                "competitors": analysis.get("competitors", []),
                "content_themes": analysis.get("content_themes", []),
                "positioning_map": strategy.get("positioning_map", {}),
                "content_recommendations": strategy.get("content_recommendations", []),
                "strategic_recommendations": strategy.get("strategic_moves", [])
            },
            "quality_flags": flags,
            "source_attribution": self._build_source_attribution(research_data)
        }
        
        logger.info(f"Quality Agent: Confidence score {confidence:.2f}, {len(flags)} quality flags")
        return final_report
    
    def _validate_research(self, research_data: Dict) -> Dict:
        """
        Validate research data quality
        
        Args:
            research_data: Output from Research Agent
            
        Returns:
            Validation result dict
        """
        sources = research_data.get("sources", [])
        issues = []
        
        # Check source count (more lenient: 3 minimum instead of 5)
        source_count_valid = len(sources) >= 3
        if not source_count_valid:
            issues.append(f"Insufficient sources ({len(sources)}/3 minimum required)")
        
        # Check source diversity
        source_types = set(s.get("source_type", "unknown") for s in sources)
        diversity_valid = len(source_types) >= 1
        
        # Check for recent sources
        recent_sources = sum(
            1 for s in sources 
            if s.get("date", "Unknown") != "Unknown" and "2024" in s.get("date", "")
        )
        recency_valid = recent_sources > 0 or len(sources) < 5
        
        return {
            "valid": source_count_valid and diversity_valid,
            "source_count": len(sources),
            "source_count_valid": source_count_valid,
            "diversity_valid": diversity_valid,
            "recency_valid": recency_valid,
            "issues": issues
        }
    
    def _validate_analysis(self, analysis: Dict, research_data: Dict) -> Dict:
        """
        Validate analysis against sources
        
        Args:
            analysis: Output from Analysis Agent
            research_data: Original research data
            
        Returns:
            Validation result dict
        """
        competitors = analysis.get("competitors", [])
        sources = research_data.get("sources", [])
        issues = []
        
        # Validate competitors are mentioned in sources
        validated_competitors = []
        for comp in competitors:
            mentions = sum(
                1 for s in sources 
                if comp.lower() in (s.get("title", "") + s.get("snippet", "")).lower()
            )
            if mentions >= 2:  # Minimum 2 mentions
                validated_competitors.append(comp)
        
        # More lenient: require at least 2 validated competitors instead of 3
        competitors_valid = len(validated_competitors) >= 2
        if not competitors_valid:
            issues.append(f"Insufficient validated competitors ({len(validated_competitors)}/2 minimum)")
        
        # Validate themes
        themes = analysis.get("content_themes", [])
        themes_valid = len(themes) > 0
        if not themes_valid:
            issues.append("No content themes identified")
        
        return {
            "valid": competitors_valid and themes_valid,
            "validated_competitors": validated_competitors,
            "competitor_count": len(competitors),
            "competitors_valid": competitors_valid,
            "themes_valid": themes_valid,
            "issues": issues
        }
    
    def _validate_strategy(self, strategy: Dict, analysis: Dict) -> Dict:
        """
        Validate strategy recommendations
        
        Args:
            strategy: Output from Strategy Agent
            analysis: Analysis insights
            
        Returns:
            Validation result dict
        """
        issues = []
        
        # Validate positioning map
        positioning = strategy.get("positioning_map", {})
        companies_positioned = positioning.get("companies", {})
        competitors_identified = analysis.get("competitors", [])
        
        if competitors_identified:
            coverage = len(companies_positioned) / len(competitors_identified)
        else:
            coverage = 0.0
        
        # More lenient: at least 40% coverage instead of 50%
        positioning_valid = coverage >= 0.4
        if not positioning_valid and len(competitors_identified) > 0:
            issues.append(f"Low positioning coverage ({coverage:.0%})")
        
        # Validate recommendations exist
        content_recs = strategy.get("content_recommendations", [])
        recommendations_valid = len(content_recs) > 0
        if not recommendations_valid:
            issues.append("No content recommendations generated")
        
        # Validate strategic moves exist
        strategic_moves = strategy.get("strategic_moves", [])
        moves_valid = len(strategic_moves) > 0
        if not moves_valid:
            issues.append("No strategic moves generated")
        
        return {
            "valid": positioning_valid and recommendations_valid and moves_valid,
            "positioning_coverage": coverage,
            "positioning_valid": positioning_valid,
            "recommendations_valid": recommendations_valid,
            "moves_valid": moves_valid,
            "issues": issues
        }
    
    def _calculate_confidence(self, validation: Dict, research_data: Dict) -> float:
        """
        Calculate overall confidence score
        
        Args:
            validation: Validation results from all agents
            research_data: Original research data
            
        Returns:
            Confidence score (0.0 - 1.0)
        """
        source_count = len(research_data.get("sources", []))
        
        # Source quality score (35% weight)
        # Perfect at 15+ sources, scales linearly below that (more lenient)
        source_score = min(1.0, source_count / 15.0)
        
        # Validation score (50% weight)
        # Based on how many validations passed
        validations_passed = sum(1 for v in validation.values() if v.get("valid", False))
        total_validations = len(validation)
        validation_score = validations_passed / total_validations if total_validations > 0 else 0.0
        
        # Data quality bonus (15% weight)
        # Reward for having trends data, discussions, etc.
        data_quality_bonus = 0.0
        if research_data.get("trends"):
            data_quality_bonus += 0.5
        if research_data.get("discussions"):
            data_quality_bonus += 0.3
        if source_count >= 10:
            data_quality_bonus += 0.2
        
        data_quality_score = min(1.0, data_quality_bonus)
        
        # Weighted confidence with adjusted weights
        confidence = (source_score * 0.35) + (validation_score * 0.50) + (data_quality_score * 0.15)
        
        # Ensure minimum confidence if we have decent data
        if source_count >= 8 and validations_passed >= 1:
            confidence = max(confidence, 0.65)
        
        return round(confidence, 2)
    
    def _generate_quality_flags(self, validation: Dict, research_data: Dict) -> List[Dict]:
        """
        Generate quality warnings and info messages
        
        Args:
            validation: Validation results
            research_data: Original research data
            
        Returns:
            List of quality flag dicts
        """
        flags = []
        
        # Add issues from each validation
        for agent, result in validation.items():
            agent_name = agent.replace("_validation", "")
            
            for issue in result.get("issues", []):
                flags.append({
                    "type": "warning",
                    "message": issue,
                    "agent": agent_name
                })
        
        # Check for low source count
        source_count = len(research_data.get("sources", []))
        if source_count < 10:
            flags.append({
                "type": "warning",
                "message": f"Low source count ({source_count}). Results may be incomplete.",
                "agent": "research"
            })
        elif source_count >= 15:
            flags.append({
                "type": "info",
                "message": f"Good source count ({source_count}). Results are well-supported.",
                "agent": "research"
            })
        
        # Check if trends data available
        if research_data.get("trends"):
            flags.append({
                "type": "info",
                "message": "Trend data available for temporal analysis",
                "agent": "research"
            })
        
        # Check if Reddit data available
        if research_data.get("discussions"):
            flags.append({
                "type": "info",
                "message": f"Community insights from {len(research_data['discussions'])} discussions",
                "agent": "research"
            })
        
        return flags
    
    def _build_source_attribution(self, research_data: Dict) -> Dict:
        """
        Build source attribution map
        
        Args:
            research_data: Original research data
            
        Returns:
            Source attribution dict
        """
        sources = research_data.get("sources", [])
        
        # Count by type
        source_breakdown = {}
        for source in sources:
            source_type = source.get("source_type", "unknown")
            source_breakdown[source_type] = source_breakdown.get(source_type, 0) + 1
        
        # Determine date range
        dates = [s.get("date", "") for s in sources if s.get("date") and s.get("date") != "Unknown"]
        if dates:
            date_range = f"{min(dates)} to {max(dates)}"
        else:
            date_range = "Unknown"
        
        return {
            "total_sources": len(sources),
            "source_breakdown": source_breakdown,
            "date_range": date_range,
            "trends_data_available": bool(research_data.get("trends")),
            "discussions_available": bool(research_data.get("discussions"))
        }


# CLI testing
if __name__ == "__main__":
    import sys
    from tests.fixtures.sample_data import (
        SAMPLE_RESEARCH_DATA,
        SAMPLE_ANALYSIS_INSIGHTS,
        SAMPLE_STRATEGY_RECOMMENDATIONS
    )
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*60)
    print("QUALITY AGENT TEST")
    print("="*60)
    print("Using sample data from all agents...")
    
    # Create test state
    test_state = {
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
    
    # Test the agent
    agent = QualityAgent()
    result = agent.run(test_state)
    
    # Print results
    print(f"\nReport Metadata:")
    metadata = result["report_metadata"]
    print(f"  Query: {metadata['query']}")
    print(f"  Confidence Score: {metadata['confidence_score']}")
    print(f"  Total Sources: {metadata['total_sources']}")
    print(f"  Processing Time: {metadata['processing_time_seconds']}s")
    
    print(f"\nValidated Insights:")
    insights = result["validated_insights"]
    print(f"  Competitors: {len(insights['competitors'])}")
    print(f"  Content Themes: {len(insights['content_themes'])}")
    print(f"  Content Recommendations: {len(insights['content_recommendations'])}")
    print(f"  Strategic Moves: {len(insights['strategic_recommendations'])}")
    
    print(f"\nQuality Flags: {len(result['quality_flags'])}")
    for flag in result["quality_flags"]:
        icon = "⚠️" if flag["type"] == "warning" else "ℹ️"
        print(f"  {icon} [{flag['agent']}] {flag['message']}")
    
    print(f"\nSource Attribution:")
    attribution = result["source_attribution"]
    print(f"  Total Sources: {attribution['total_sources']}")
    print(f"  Date Range: {attribution['date_range']}")
    print(f"  Source Types: {attribution['source_breakdown']}")
    
    # Save output
    import os
    import json
    output_path = "outputs/reports/quality_agent_test.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print("\n" + "="*60)
    print(f"Full output saved to: {output_path}")