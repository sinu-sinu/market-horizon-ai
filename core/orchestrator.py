from langgraph.graph import StateGraph, END
from core.state import AgentState
from core.observability import Tracer, Span, flush as flush_traces, log_score
from utils.cache_manager import get_cache_manager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orchestrates the multi-agent workflow using LangGraph.
    
    Workflow: Research → Analysis → Strategy → Quality → END
    """
    
    def __init__(self):
        """Initialize orchestrator and build workflow"""
        # Import agents here to avoid circular imports
        from agents.research_agent import ResearchAgent
        from agents.analysis_agent import AnalysisAgent
        from agents.strategy_agent import StrategyAgent
        from agents.quality_agent import QualityAgent

        # Initialize cache manager
        self.cache = get_cache_manager()

        # Initialize all agents
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.strategy_agent = StrategyAgent()
        self.quality_agent = QualityAgent()

        self.workflow = self._build_workflow()

        logger.info("AgentOrchestrator initialized with all 4 agents")
        logger.info(f"Cache manager initialized with database at data/cache.db")
    
    def _build_workflow(self) -> StateGraph:
        """Build LangGraph workflow with StateGraph API (LangGraph 1.0.2)"""
        # Create workflow with AgentState
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("research", self._run_research)
        workflow.add_node("analysis", self._run_analysis)
        workflow.add_node("strategy", self._run_strategy)
        workflow.add_node("quality", self._run_quality)
        
        # Define workflow edges (sequential execution)
        workflow.set_entry_point("research")
        workflow.add_edge("research", "analysis")
        workflow.add_edge("analysis", "strategy")
        workflow.add_edge("strategy", "quality")
        workflow.add_edge("quality", END)
        
        # Compile and return the workflow
        return workflow.compile()
    
    def _run_research(self, state: AgentState) -> AgentState:
        """Execute Research Agent"""
        state["current_agent"] = "research"
        logger.info(f"Research Agent: Processing query '{state['query']}'")

        trace_id = state.get("trace_id")
        with Span(trace_id, "research_agent", input_data={"query": state["query"]}) as span:
            try:
                result = self.research_agent.run(state["query"], trace_id=trace_id)
                state["research_data"] = result
                state["api_calls"] += 1
                logger.info("Research Agent: Completed successfully")

                # Update span with output summary
                span.update(output={
                    "sources_count": len(result.get("sources", [])) if result else 0,
                    "success": True,
                })

            except Exception as e:
                logger.error(f"Research agent failed: {e}", exc_info=True)
                state["errors"].append({
                    "agent": "research",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                    "fallback_used": False
                })
                span.update(output={"success": False, "error": str(e)})

        return state
    
    def _run_analysis(self, state: AgentState) -> AgentState:
        """Execute Analysis Agent"""
        state["current_agent"] = "analysis"
        logger.info("Analysis Agent: Processing research data")

        trace_id = state.get("trace_id")
        with Span(trace_id, "analysis_agent", input_data={"has_research_data": bool(state.get("research_data"))}) as span:
            try:
                result = self.analysis_agent.run(state["research_data"], trace_id=trace_id)
                state["analysis_insights"] = result
                state["api_calls"] += 1
                logger.info("Analysis Agent: Completed successfully")

                span.update(output={
                    "competitors_count": len(result.get("competitors", [])) if result else 0,
                    "themes_count": len(result.get("content_themes", [])) if result else 0,
                    "success": True,
                })

            except Exception as e:
                logger.error(f"Analysis agent failed: {e}", exc_info=True)
                state["errors"].append({
                    "agent": "analysis",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                    "fallback_used": False
                })
                span.update(output={"success": False, "error": str(e)})

        return state
    
    def _run_strategy(self, state: AgentState) -> AgentState:
        """Execute Strategy Agent"""
        state["current_agent"] = "strategy"
        logger.info("Strategy Agent: Generating recommendations")

        trace_id = state.get("trace_id")
        query = state.get("query", "")  # Pass query for content gap analysis
        with Span(trace_id, "strategy_agent", input_data={"has_analysis_insights": bool(state.get("analysis_insights"))}) as span:
            try:
                result = self.strategy_agent.run(state["analysis_insights"], trace_id=trace_id, query=query)
                state["strategy_recommendations"] = result
                state["api_calls"] += 1
                logger.info("Strategy Agent: Completed successfully")

                span.update(output={
                    "opportunity_zones": len(result.get("opportunity_zones", [])) if result else 0,
                    "content_recommendations": len(result.get("content_recommendations", [])) if result else 0,
                    "success": True,
                })

            except Exception as e:
                logger.error(f"Strategy agent failed: {e}", exc_info=True)
                state["errors"].append({
                    "agent": "strategy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                    "fallback_used": False
                })
                span.update(output={"success": False, "error": str(e)})

        return state
    
    def _run_quality(self, state: AgentState) -> AgentState:
        """Execute Quality Agent"""
        state["current_agent"] = "quality"
        logger.info("Quality Agent: Validating outputs")

        trace_id = state.get("trace_id")
        with Span(trace_id, "quality_agent", input_data={"has_strategy_recommendations": bool(state.get("strategy_recommendations"))}) as span:
            try:
                result = self.quality_agent.run(state, trace_id=trace_id)
                state["quality_report"] = result
                logger.info("Quality Agent: Completed successfully")

                span.update(output={
                    "confidence_score": result.get("report_metadata", {}).get("confidence_score", 0) if result else 0,
                    "quality_flags_count": len(result.get("quality_flags", [])) if result else 0,
                    "success": True,
                })

            except Exception as e:
                logger.error(f"Quality agent failed: {e}", exc_info=True)
                state["errors"].append({
                    "agent": "quality",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                    "fallback_used": False
                })
                span.update(output={"success": False, "error": str(e)})

        return state
    
    def run(self, query: str, parameters: dict = None) -> dict:
        """
        Execute full pipeline

        Args:
            query: User's market research query
            parameters: Optional parameters for customization

        Returns:
            Final quality report with all insights
        """
        logger.info(f"Orchestrator: Starting pipeline for query: '{query}'")

        # Create Langfuse trace for the entire pipeline
        with Tracer(
            name="market_horizon_pipeline",
            user_id="streamlit-user",  # Default user for Streamlit app
            metadata={
                "query": query,
                "parameters": parameters or {},
            }
        ) as trace:
            # Initialize state with trace_id for child spans
            initial_state: AgentState = {
                "query": query,
                "parameters": parameters or {},
                "research_data": None,
                "analysis_insights": None,
                "strategy_recommendations": None,
                "quality_report": None,
                "errors": [],
                "retry_count": 0,
                "start_time": datetime.now(),
                "current_agent": "",
                "total_tokens": 0,
                "api_calls": 0,
                "trace_id": trace.id,  # Pass trace ID to agents
            }

            # Execute workflow
            final_state = self.workflow.invoke(initial_state)

            # Compile the output
            output = self._compile_output(final_state)

            # Log quality score to Langfuse
            confidence_score = output.get("report_metadata", {}).get("confidence_score", 0)
            if trace.id and confidence_score:
                log_score(
                    trace_id=trace.id,
                    name="confidence_score",
                    value=confidence_score,
                    comment=f"Pipeline confidence score based on data quality and completeness"
                )

            # Flush traces before returning
            flush_traces()

            return output
    
    def _compile_output(self, state: AgentState) -> dict:
        """Compile final output from state"""
        # If quality report exists, return it
        if state.get("quality_report"):
            return state["quality_report"]

        # Fallback: construct basic report
        processing_time = (datetime.now() - state["start_time"]).total_seconds()

        return {
            "report_metadata": {
                "query": state["query"],
                "timestamp": datetime.now().isoformat(),
                "total_sources": 0,
                "processing_time_seconds": int(processing_time),
                "confidence_score": 0.0,
                "errors": state["errors"]
            },
            "validated_insights": {
                "competitors": [],
                "content_themes": [],
                "positioning_map": {},
                "content_recommendations": [],
                "strategic_recommendations": []
            },
            "quality_flags": [
                {
                    "type": "error",
                    "message": "Pipeline incomplete - agents not fully initialized",
                    "agent": "orchestrator"
                }
            ],
            "source_attribution": {}
        }

    # ==================== CACHE MANAGEMENT ====================

    def get_cache_stats(self) -> dict:
        """
        Get cache statistics

        Returns:
            Dictionary with cache statistics
        """
        return self.cache.get_stats()

    def print_cache_stats(self):
        """Print formatted cache statistics"""
        self.cache.print_stats()

    def clear_cache_all(self, force: bool = False) -> int:
        """
        Clear entire cache

        Args:
            force: Skip confirmation

        Returns:
            Number of entries deleted
        """
        logger.warning("Clearing entire cache...")
        deleted = self.cache.clear_all()
        logger.info(f"Cleared {deleted} cache entries")
        return deleted

    def clear_cache_by_type(self, cache_type: str) -> int:
        """
        Clear cache by type

        Args:
            cache_type: Type of cache to clear

        Returns:
            Number of entries deleted
        """
        deleted = self.cache.delete_by_type(cache_type)
        logger.info(f"Cleared {deleted} cache entries of type '{cache_type}'")
        return deleted

    def clear_cache_by_query(self, query: str) -> int:
        """
        Clear cache for specific query

        Args:
            query: Query to clear

        Returns:
            Number of entries deleted
        """
        deleted = self.cache.delete_by_query(query)
        logger.info(f"Cleared {deleted} cache entries for query '{query}'")
        return deleted

    def cleanup_cache(self) -> int:
        """
        Remove expired cache entries

        Returns:
            Number of entries deleted
        """
        deleted = self.cache.cleanup_expired()
        logger.info(f"Cache cleanup removed {deleted} expired entries")
        return deleted


# CLI entry point for testing
if __name__ == "__main__":
    import sys
    
    # Set up basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get query from command line or use default
    query = sys.argv[1] if len(sys.argv) > 1 else "CRM tools for real estate agents"
    
    # Run orchestrator
    orchestrator = AgentOrchestrator()
    result = orchestrator.run(query)
    
    # Print result
    import json
    print("\n" + "="*60)
    print("ORCHESTRATOR TEST RESULT")
    print("="*60)
    print(json.dumps(result, indent=2))