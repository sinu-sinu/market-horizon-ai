from fastapi import APIRouter, Depends, HTTPException, Query
from api.schemas.responses import QueryHistoryItem, AnalysisResponse
from api.dependencies import get_history
from utils.query_history import QueryHistory
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("/recent", response_model=list[QueryHistoryItem])
async def get_recent_queries(
    limit: int = Query(default=5, ge=1, le=50, description="Number of queries to return"),
    history: QueryHistory = Depends(get_history),
):
    """
    Get recent query history.

    Returns the most recent queries with their basic metadata.
    """
    try:
        queries = history.get_recent_queries(limit=limit)
        return [
            QueryHistoryItem(
                id=q[0],
                query=q[1],
                timestamp=str(q[2]),
                confidence_score=q[3],
                num_competitors=q[4],
            )
            for q in queries
        ]
    except Exception as e:
        logger.error(f"Failed to get recent queries: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@router.get("/{query_id}", response_model=AnalysisResponse)
async def get_query_by_id(
    query_id: int,
    history: QueryHistory = Depends(get_history),
):
    """
    Get a specific query result by ID.

    Returns the full analysis result for a previously executed query.
    """
    try:
        result = history.get_query_by_id(query_id)
        if not result:
            raise HTTPException(status_code=404, detail="Query not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get query {query_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get query: {str(e)}")


@router.get("/latest", response_model=AnalysisResponse)
async def get_latest_result(
    history: QueryHistory = Depends(get_history),
):
    """
    Get the most recent query result.
    """
    try:
        result = history.get_latest_result()
        if not result:
            raise HTTPException(status_code=404, detail="No queries found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get latest result: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get latest: {str(e)}")
