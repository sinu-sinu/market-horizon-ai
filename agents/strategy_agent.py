from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from core.prompts import POSITIONING_PROMPT, CONTENT_GAP_PROMPT, STRATEGIC_MOVES_PROMPT, CONTENT_GAP_ANALYSIS_PROMPT, OPPORTUNITY_SCORING_PROMPT
from core.config import config
from core.observability import log_llm_call
from typing import Dict, List, Optional
from datetime import datetime
import json
import logging
import re

logger = logging.getLogger(__name__)


class StrategyAgent:
    """
    Strategy Agent - Generates positioning strategies and recommendations
    
    Capabilities:
    - Generate competitive positioning maps
    - Identify market opportunity zones
    - Recommend content strategies
    - Provide strategic moves
    """
    
    def __init__(self):
        """Initialize Strategy Agent with LLM"""
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",  # Using gpt-4.1-mini for cost efficiency
            temperature=0.3,  # Lower temperature for more consistent outputs
            max_tokens=2000,
            api_key=config.OPENAI_API_KEY
        )
        
        logger.info("Strategy Agent initialized with gpt-4.1-mini")
    
    def run(self, analysis_insights: Dict, trace_id: Optional[str] = None, query: str = "") -> Dict:
        """
        Generate positioning strategies and recommendations

        Args:
            analysis_insights: Output from Analysis Agent
            trace_id: Optional Langfuse trace ID for observability
            query: Original search query for context

        Returns:
            Dict with positioning map, opportunity zones, and recommendations
        """
        self._current_trace_id = trace_id
        self._query = query
        logger.info("Strategy Agent: Generating recommendations")

        if not analysis_insights or not analysis_insights.get("competitors"):
            logger.warning("No analysis insights available")
            return self._empty_output()

        # Generate positioning map
        positioning_map = self._generate_positioning_map(
            analysis_insights.get("competitor_attributes", {}),
            analysis_insights.get("competitors", [])
        )

        # Identify opportunity zones
        opportunity_zones = self._detect_opportunity_zones(
            positioning_map,
            analysis_insights
        )

        # Generate content recommendations (Phase 3: LLM-based gap analysis)
        content_recs = self._generate_content_recommendations(
            analysis_insights.get("content_themes", []),
            analysis_insights.get("competitors", []),
            query=query
        )

        # Score recommendations with evidence-based reasoning (Phase 4)
        if content_recs:
            content_recs = self._score_recommendations(
                content_recs,
                analysis_insights.get("content_themes", []),
                analysis_insights.get("competitors", [])
            )

        # Strategic moves
        strategic_moves = self._generate_strategic_moves(
            positioning_map,
            opportunity_zones
        )

        output = {
            "positioning_map": positioning_map,
            "opportunity_zones": opportunity_zones,
            "content_recommendations": content_recs,
            "strategic_moves": strategic_moves
        }
        
        logger.info(f"Strategy Agent: Generated {len(opportunity_zones)} opportunity zones, {len(content_recs)} content recommendations")
        return output
    
    def _generate_positioning_map(self, competitor_attrs: Dict, competitors: List[str]) -> Dict:
        """
        Use LLM to assign positioning coordinates
        
        Args:
            competitor_attrs: Competitor attributes from Analysis Agent
            competitors: List of competitor names
            
        Returns:
            Dict with positioning data
        """
        if not competitors:
            logger.warning("No competitors to position")
            return self._empty_positioning_map()
        
        try:
            # Prepare data for LLM
            competitor_data = {}
            for comp in competitors:
                attrs = competitor_attrs.get(comp, {})
                competitor_data[comp] = {
                    "sentiment": attrs.get("sentiment", 0.0),
                    "mention_count": attrs.get("mention_count", 0)
                }
            
            # Format prompt
            prompt = PromptTemplate.from_template(POSITIONING_PROMPT)
            formatted_prompt = prompt.format(
                competitor_data=json.dumps(competitor_data, indent=2)
            )

            # Get LLM response with timing
            llm_start = datetime.now()
            response = self.llm.invoke(formatted_prompt)
            llm_end = datetime.now()

            # Log LLM call to Langfuse with token usage and timing
            trace_id = getattr(self, "_current_trace_id", None)
            if trace_id and hasattr(response, 'usage_metadata'):
                usage = response.usage_metadata
                model_name = response.response_metadata.get('model_name', 'gpt-4.1-mini')
                log_llm_call(
                    trace_id=trace_id,
                    name="positioning-map",
                    model=model_name,
                    input_text=formatted_prompt,
                    output_text=response.content,
                    input_tokens=usage.get('input_tokens', 0),
                    output_tokens=usage.get('output_tokens', 0),
                    start_time=llm_start,
                    end_time=llm_end,
                )

            # Parse JSON response - handle markdown code blocks
            response_text = response.content.strip()
            
            # Try to extract JSON from markdown code blocks if present
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            
            # Also try extracting JSON object directly (if not already extracted)
            if not json_match:
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    response_text = json_match.group(0)
            
            try:
                positioning_data = json.loads(response_text)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM positioning response as JSON: {e}")
                logger.debug(f"Response content: {response.content[:200]}...")
                # Fallback to simple positioning
                positioning_data = self._fallback_positioning(competitors)
            
            # Validate and clean coordinates
            positioning_data = self._validate_coordinates(positioning_data)
            
            # Add dimensions metadata
            result = {
                "dimensions": {
                    "x_axis": "Price Positioning (1-10)",
                    "y_axis": "Target Company Size (1-10)"
                },
                "companies": positioning_data
            }
            
            logger.info(f"Positioned {len(positioning_data)} competitors")
            return result
            
        except Exception as e:
            logger.error(f"Error generating positioning map: {e}", exc_info=True)
            return self._fallback_positioning_map(competitors)
    
    def _fallback_positioning(self, competitors: List[str]) -> Dict:
        """
        Fallback positioning when LLM fails
        
        Args:
            competitors: List of competitor names
            
        Returns:
            Simple positioning dict
        """
        positioning = {}
        
        # Distribute competitors evenly across grid
        import math
        n = len(competitors)
        cols = math.ceil(math.sqrt(n))
        
        for i, comp in enumerate(competitors):
            row = i // cols
            col = i % cols
            
            x = 2.0 + (col * 6.0 / max(cols - 1, 1))
            y = 2.0 + (row * 6.0 / max((n // cols), 1))
            
            positioning[comp] = {
                "x": round(x, 1),
                "y": round(y, 1),
                "rationale": "Estimated positioning"
            }
        
        return positioning
    
    def _validate_coordinates(self, positioning_data: Dict) -> Dict:
        """
        Validate and clean positioning coordinates
        
        Args:
            positioning_data: Raw positioning data
            
        Returns:
            Cleaned positioning data
        """
        cleaned = {}
        
        for company, data in positioning_data.items():
            if isinstance(data, dict) and "x" in data and "y" in data:
                x = float(data["x"])
                y = float(data["y"])
                
                # Clamp to valid range
                x = max(1.0, min(10.0, x))
                y = max(1.0, min(10.0, y))
                
                cleaned[company] = {
                    "x": round(x, 1),
                    "y": round(y, 1),
                    "rationale": data.get("rationale", "Positioning based on market analysis")
                }
        
        return cleaned
    
    def _detect_opportunity_zones(self, positioning_map: Dict, insights: Dict) -> List[Dict]:
        """
        Identify empty market spaces (opportunity zones)
        
        Args:
            positioning_map: Generated positioning map
            insights: Analysis insights
            
        Returns:
            List of opportunity zone dicts
        """
        zones = []
        
        companies = positioning_map.get("companies", {})
        if not companies:
            return zones
        
        # Get all occupied positions
        occupied_positions = [
            (data["x"], data["y"]) 
            for data in companies.values()
        ]
        
        # Check grid for empty spaces (simplified algorithm)
        # In production, this would use more sophisticated gap analysis
        
        # Define grid points to check
        grid_points = [
            (x, y) 
            for x in range(2, 10, 2)  # Check every 2 units
            for y in range(2, 10, 2)
        ]
        
        for x, y in grid_points:
            # Check if this point is far from all occupied positions
            min_distance = min([
                ((x - ox)**2 + (y - oy)**2)**0.5
                for ox, oy in occupied_positions
            ] or [float('inf')])
            
            # If minimum distance > 2.5, it's an opportunity zone
            if min_distance > 2.5:
                # Determine zone description
                if x < 5 and y > 7:
                    desc = "Budget enterprise gap"
                elif x > 6 and y < 4:
                    desc = "Premium SMB gap"
                elif 4 <= x <= 6 and y > 7:
                    desc = "Mid-price enterprise gap"
                else:
                    desc = "Market gap"
                
                zones.append({
                    "coordinates": {"x": float(x), "y": float(y)},
                    "description": desc,
                    "rationale": f"No major competitors in this segment",
                    "opportunity_score": round(min_distance * 2, 1)  # Simple scoring
                })
        
        # Sort by opportunity score and limit to top 3
        zones.sort(key=lambda z: z["opportunity_score"], reverse=True)
        zones = zones[:3]
        
        logger.info(f"Identified {len(zones)} opportunity zones")
        return zones
    
    def _generate_content_recommendations(self, themes: List[Dict], competitors: List[str], query: str = "") -> List[Dict]:
        """
        Generate content gap recommendations using LLM-based gap analysis (Phase 3)

        Args:
            themes: Content themes from Analysis Agent (with source_evidence)
            competitors: List of competitors
            query: Original search query for context

        Returns:
            List of content recommendation dicts with gap_reasoning
        """
        if not themes:
            logger.warning("No themes available for content recommendations")
            return []

        # Build themes with evidence for LLM prompt
        themes_with_evidence = []
        for theme in themes[:5]:
            theme_info = {
                "theme": theme.get("theme", ""),
                "user_interest": theme.get("user_interest", ""),
                "source_evidence": theme.get("source_evidence", [])
            }
            themes_with_evidence.append(theme_info)

        # Format prompt
        prompt = CONTENT_GAP_ANALYSIS_PROMPT.format(
            query=query or "market research",
            themes_with_evidence=json.dumps(themes_with_evidence, indent=2),
            competitors=", ".join(competitors[:10])  # Limit to 10 competitors
        )

        try:
            # Call LLM for gap analysis
            llm_start = datetime.now()
            response = self.llm.invoke(prompt)
            llm_end = datetime.now()
            content = response.content.strip()

            # Log LLM call to Langfuse
            trace_id = getattr(self, "_current_trace_id", None)
            if trace_id and hasattr(response, 'usage_metadata'):
                usage = response.usage_metadata
                model_name = response.response_metadata.get('model_name', 'gpt-4.1-mini')
                log_llm_call(
                    trace_id=trace_id,
                    name="content-gap-analysis",
                    model=model_name,
                    input_text=prompt,
                    output_text=content,
                    input_tokens=usage.get('input_tokens', 0),
                    output_tokens=usage.get('output_tokens', 0),
                    start_time=llm_start,
                    end_time=llm_end,
                )

            # Parse JSON response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            result = json.loads(content)
            llm_recommendations = result.get("recommendations", [])

            # Transform to output format
            recommendations = []
            for i, rec in enumerate(llm_recommendations[:5]):
                topic = rec.get("topic", "")

                # Validate: topic should not be generic template
                if self._is_generic_topic(topic):
                    logger.warning(f"Skipping generic topic: {topic}")
                    continue

                recommendations.append({
                    "topic": topic,
                    "gap_reasoning": rec.get("gap_reasoning", ""),
                    "target_audience": rec.get("target_audience", ""),
                    "recommended_format": rec.get("recommended_format", "Article"),
                    "format_rationale": rec.get("format_rationale", ""),
                    "why_now": rec.get("why_now", ""),
                    "priority": "high" if i < 2 else "medium" if i < 4 else "low",
                    "estimated_effort": "medium"
                })

            logger.info(f"LLM generated {len(recommendations)} content recommendations")
            return recommendations

        except Exception as e:
            logger.error(f"LLM content gap analysis failed: {e}")
            return []

    def _is_generic_topic(self, topic: str) -> bool:
        """
        Check if a topic is too generic (matches template patterns)

        Args:
            topic: Topic title to check

        Returns:
            True if topic is generic, False otherwise
        """
        topic_lower = topic.lower()

        generic_patterns = [
            "deep dive into",
            "everything about",
            "best practices for",
            "complete guide to",
            "all you need to know",
            "introduction to",
            "getting started with"
        ]

        # Check if topic matches generic patterns AND is short (under 8 words)
        word_count = len(topic.split())
        if word_count < 6:
            for pattern in generic_patterns:
                if pattern in topic_lower:
                    return True

        return False

    def _score_recommendations(
        self,
        recommendations: List[Dict],
        themes: List[Dict],
        competitors: List[str]
    ) -> List[Dict]:
        """
        Score recommendations using LLM-based evidence analysis (Phase 4)

        Args:
            recommendations: Content recommendations from gap analysis
            themes: Content themes with source evidence
            competitors: List of competitors

        Returns:
            Recommendations with evidence-based opportunity scores
        """
        if not recommendations:
            return recommendations

        # Build source evidence summary from themes
        source_evidence = []
        for theme in themes[:5]:
            evidence = theme.get("source_evidence", [])
            for e in evidence:
                source_evidence.append({
                    "theme": theme.get("theme", ""),
                    "quote": e.get("quote", ""),
                    "source_idx": e.get("source_idx")
                })

        # Format prompt
        prompt = OPPORTUNITY_SCORING_PROMPT.format(
            recommendations=json.dumps([
                {"topic": r.get("topic", ""), "gap_reasoning": r.get("gap_reasoning", "")}
                for r in recommendations
            ], indent=2),
            source_evidence=json.dumps(source_evidence[:20], indent=2),  # Limit evidence
            competitors=", ".join(competitors[:10])
        )

        try:
            # Call LLM for scoring
            llm_start = datetime.now()
            response = self.llm.invoke(prompt)
            llm_end = datetime.now()
            content = response.content.strip()

            # Log LLM call to Langfuse
            trace_id = getattr(self, "_current_trace_id", None)
            if trace_id and hasattr(response, 'usage_metadata'):
                usage = response.usage_metadata
                model_name = response.response_metadata.get('model_name', 'gpt-4.1-mini')
                log_llm_call(
                    trace_id=trace_id,
                    name="opportunity-scoring",
                    model=model_name,
                    input_text=prompt,
                    output_text=content,
                    input_tokens=usage.get('input_tokens', 0),
                    output_tokens=usage.get('output_tokens', 0),
                    start_time=llm_start,
                    end_time=llm_end,
                )

            # Parse JSON response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            result = json.loads(content)
            scored_recs = result.get("scored_recommendations", [])

            # Match scores back to original recommendations
            score_map = {r.get("topic", "").lower(): r for r in scored_recs}

            for rec in recommendations:
                topic_lower = rec.get("topic", "").lower()
                if topic_lower in score_map:
                    scored = score_map[topic_lower]
                    rec["opportunity_score"] = scored.get("opportunity_score", 5.0)
                    rec["score_reasoning"] = scored.get("score_reasoning", {})
                else:
                    # Fallback if no match found
                    rec["opportunity_score"] = 5.0
                    rec["score_reasoning"] = {"note": "Score not computed"}

            # Sort by opportunity score
            recommendations.sort(key=lambda x: x.get("opportunity_score", 0), reverse=True)

            logger.info(f"Scored {len(recommendations)} recommendations with evidence-based reasoning")
            return recommendations

        except Exception as e:
            logger.error(f"LLM opportunity scoring failed: {e}")
            # Return recommendations without scores
            for rec in recommendations:
                rec["opportunity_score"] = 5.0
                rec["score_reasoning"] = {"error": str(e)}
            return recommendations

    def _generate_strategic_moves(self, positioning_map: Dict, zones: List[Dict]) -> List[str]:
        """
        Generate strategic recommendations
        
        Args:
            positioning_map: Positioning map
            zones: Opportunity zones
            
        Returns:
            List of strategic move strings
        """
        moves = []
        
        # Analyze positioning map for insights
        companies = positioning_map.get("companies", {})
        
        if not companies:
            return ["Conduct additional market research to identify competitors"]
        
        # Calculate average positioning
        avg_x = sum(c["x"] for c in companies.values()) / len(companies)
        avg_y = sum(c["y"] for c in companies.values()) / len(companies)
        
        # Generate moves based on opportunity zones
        if zones:
            top_zone = zones[0]
            coords = top_zone["coordinates"]
            
            if coords["x"] < 5 and coords["y"] > 7:
                moves.append("Position as 'enterprise features at SMB pricing'")
            elif coords["x"] > 6 and coords["y"] < 4:
                moves.append("Target premium small business segment with high-touch service")
            elif 4 <= coords["x"] <= 6:
                moves.append("Position in mid-market sweet spot with balanced offering")
        
        # Generate moves based on market density
        if avg_x > 6:
            moves.append("Consider value-based positioning to differentiate from premium competitors")
        elif avg_x < 4:
            moves.append("Opportunity to establish premium positioning in budget-dominated market")
        
        if avg_y > 6:
            moves.append("Most competitors target enterprises - consider focusing on underserved SMB segment")
        elif avg_y < 4:
            moves.append("SMB market is crowded - explore enterprise opportunity")
        
        # Add default strategic moves
        moves.append("Emphasize unique value propositions not covered by competitors")
        moves.append("Develop content addressing underserved topics identified in gap analysis")
        
        # Limit to top 5 moves
        moves = moves[:5]
        
        logger.info(f"Generated {len(moves)} strategic moves")
        return moves
    
    def _empty_output(self) -> Dict:
        """Return empty output structure"""
        return {
            "positioning_map": self._empty_positioning_map(),
            "opportunity_zones": [],
            "content_recommendations": [],
            "strategic_moves": []
        }
    
    def _empty_positioning_map(self) -> Dict:
        """Return empty positioning map structure"""
        return {
            "dimensions": {
                "x_axis": "Price Positioning (1-10)",
                "y_axis": "Target Company Size (1-10)"
            },
            "companies": {}
        }
    
    def _fallback_positioning_map(self, competitors: List[str]) -> Dict:
        """Return fallback positioning map"""
        return {
            "dimensions": {
                "x_axis": "Price Positioning (1-10)",
                "y_axis": "Target Company Size (1-10)"
            },
            "companies": self._fallback_positioning(competitors)
        }


# CLI testing
if __name__ == "__main__":
    import sys
    from tests.fixtures.sample_data import SAMPLE_ANALYSIS_INSIGHTS
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*60)
    print("STRATEGY AGENT TEST")
    print("="*60)
    print("Using sample analysis insights...")
    
    # Test the agent
    agent = StrategyAgent()
    result = agent.run(SAMPLE_ANALYSIS_INSIGHTS)
    
    # Print results
    print(f"\nPositioning Map:")
    companies = result["positioning_map"]["companies"]
    for comp, coords in list(companies.items())[:5]:
        print(f"  {comp}: ({coords['x']}, {coords['y']})")
    
    print(f"\nOpportunity Zones: {len(result['opportunity_zones'])}")
    for zone in result["opportunity_zones"]:
        print(f"  - {zone['description']}: score {zone['opportunity_score']}")
    
    print(f"\nContent Recommendations: {len(result['content_recommendations'])}")
    for rec in result["content_recommendations"][:3]:
        print(f"  - {rec['topic']}: {rec['priority']} priority, score {rec['opportunity_score']}")
    
    print(f"\nStrategic Moves:")
    for i, move in enumerate(result["strategic_moves"], 1):
        print(f"  {i}. {move}")
    
    # Save output
    import os
    output_path = "outputs/reports/strategy_agent_test.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print("\n" + "="*60)
    print(f"Full output saved to: {output_path}")