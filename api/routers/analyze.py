from fastapi import APIRouter, Depends, HTTPException
from api.schemas.requests import AnalyzeRequest
from api.schemas.responses import AnalysisResponse
from api.dependencies import get_orchestrator, get_history
from api.config import get_settings
from core.orchestrator import AgentOrchestrator
from utils.query_history import QueryHistory
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    request: AnalyzeRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
    history: QueryHistory = Depends(get_history),
    settings=Depends(get_settings),
):
    """
    Run full market analysis pipeline.

    This endpoint executes the 4-agent workflow:
    1. Research Agent - Gathers data from web, trends, and Reddit
    2. Analysis Agent - Extracts competitors and themes
    3. Strategy Agent - Generates positioning map and recommendations
    4. Quality Agent - Validates and synthesizes final report
    """
    query = request.query.strip()

    if len(query) < settings.min_query_length:
        raise HTTPException(
            status_code=400,
            detail=f"Query must be at least {settings.min_query_length} characters"
        )

    if len(query) > settings.max_query_length:
        raise HTTPException(
            status_code=400,
            detail=f"Query must be at most {settings.max_query_length} characters"
        )

    logger.info(f"Starting analysis for query: '{query[:50]}...'")

    try:
        result = orchestrator.run(query, request.parameters)
        result["query_text"] = query
        history.save_query(query, result)
        logger.info(f"Analysis completed for query: '{query[:50]}...'")
        return result

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
