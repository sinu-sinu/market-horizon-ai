from langgraph.graph import StateGraph, END
from core.state import AgentState
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
        
        # Initialize all agents
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.strategy_agent = StrategyAgent()
        self.quality_agent = QualityAgent()
        
        self.workflow = self._build_workflow()
        
        logger.info("AgentOrchestrator initialized with all 4 agents")
    
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
        
        try:
            result = self.research_agent.run(state["query"])
            state["research_data"] = result
            state["api_calls"] += 1
            logger.info("Research Agent: Completed successfully")
            
        except Exception as e:
            logger.error(f"Research agent failed: {e}", exc_info=True)
            state["errors"].append({
                "agent": "research",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "fallback_used": False
            })
        
        return state
    
    def _run_analysis(self, state: AgentState) -> AgentState:
        """Execute Analysis Agent"""
        state["current_agent"] = "analysis"
        logger.info("Analysis Agent: Processing research data")
        
        try:
            result = self.analysis_agent.run(state["research_data"])
            state["analysis_insights"] = result
            state["api_calls"] += 1
            logger.info("Analysis Agent: Completed successfully")
            
        except Exception as e:
            logger.error(f"Analysis agent failed: {e}", exc_info=True)
            state["errors"].append({
                "agent": "analysis",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "fallback_used": False
            })
        
        return state
    
    def _run_strategy(self, state: AgentState) -> AgentState:
        """Execute Strategy Agent"""
        state["current_agent"] = "strategy"
        logger.info("Strategy Agent: Generating recommendations")
        
        try:
            result = self.strategy_agent.run(state["analysis_insights"])
            state["strategy_recommendations"] = result
            state["api_calls"] += 1
            logger.info("Strategy Agent: Completed successfully")
            
        except Exception as e:
            logger.error(f"Strategy agent failed: {e}", exc_info=True)
            state["errors"].append({
                "agent": "strategy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "fallback_used": False
            })
        
        return state
    
    def _run_quality(self, state: AgentState) -> AgentState:
        """Execute Quality Agent"""
        state["current_agent"] = "quality"
        logger.info("Quality Agent: Validating outputs")
        
        try:
            result = self.quality_agent.run(state)
            state["quality_report"] = result
            logger.info("Quality Agent: Completed successfully")
            
        except Exception as e:
            logger.error(f"Quality agent failed: {e}", exc_info=True)
            state["errors"].append({
                "agent": "quality",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "fallback_used": False
            })
        
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
        
        # Initialize state
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
            "api_calls": 0
        }
        
        # Execute workflow
        final_state = self.workflow.invoke(initial_state)
        
        # Return compiled output
        return self._compile_output(final_state)
    
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