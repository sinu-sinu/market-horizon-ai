from typing import Dict, List, Optional, TypedDict
from datetime import datetime


class AgentError(TypedDict):
    """Error information from agent execution"""
    agent: str
    error: str
    timestamp: str
    fallback_used: bool


class AgentState(TypedDict):
    """Shared state passed between agents in the workflow"""

    # User Input
    query: str
    parameters: Dict

    # Agent Outputs
    research_data: Optional[Dict]
    analysis_insights: Optional[Dict]
    strategy_recommendations: Optional[Dict]
    quality_report: Optional[Dict]

    # Metadata
    errors: List[AgentError]
    retry_count: int
    start_time: datetime
    current_agent: str

    # Cost Tracking
    total_tokens: int
    api_calls: int

    # Observability
    trace_id: Optional[str]