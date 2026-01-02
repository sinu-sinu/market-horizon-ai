from functools import lru_cache
from core.orchestrator import AgentOrchestrator
from utils.query_history import QueryHistory
from api.config import get_settings


@lru_cache()
def get_orchestrator() -> AgentOrchestrator:
    """Get cached orchestrator instance"""
    return AgentOrchestrator()


@lru_cache()
def get_history() -> QueryHistory:
    """Get cached query history instance"""
    settings = get_settings()
    return QueryHistory(db_path=settings.history_db_path)
