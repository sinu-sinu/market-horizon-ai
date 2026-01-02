from fastapi import APIRouter, Depends, HTTPException
from api.schemas.requests import ClearCacheRequest
from api.schemas.responses import CacheStatsResponse, CacheTypeStats
from api.dependencies import get_orchestrator
from core.orchestrator import AgentOrchestrator
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/cache", tags=["cache"])


@router.get("/stats", response_model=CacheStatsResponse)
async def get_cache_stats(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
):
    """
    Get cache statistics.

    Returns detailed statistics about the cache including hit rate,
    size, and breakdown by cache type.
    """
    try:
        stats = orchestrator.get_cache_stats()
        return CacheStatsResponse(
            stats=stats.get("stats", {}),
            hit_rate=stats.get("hit_rate", "0%"),
            total_entries_valid=stats.get("total_entries_valid", 0),
            total_entries_all=stats.get("total_entries_all", 0),
            total_size_bytes=stats.get("total_size_bytes", 0),
            total_size_mb=stats.get("total_size_mb", 0.0),
            by_type=[
                CacheTypeStats(
                    type=t.get("type", "unknown"),
                    count=t.get("count", 0),
                    hits=t.get("hits", 0),
                )
                for t in stats.get("by_type", [])
            ],
        )
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.post("/clear")
async def clear_cache(
    request: ClearCacheRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
):
    """
    Clear cache entries.

    Can clear by:
    - cache_type: Clear all entries of a specific type
    - query: Clear all entries for a specific query
    - Neither: Clear all cache entries
    """
    try:
        if request.cache_type:
            deleted = orchestrator.clear_cache_by_type(request.cache_type)
            return {
                "deleted": deleted,
                "message": f"Cleared {deleted} entries of type '{request.cache_type}'"
            }
        elif request.query:
            deleted = orchestrator.clear_cache_by_query(request.query)
            return {
                "deleted": deleted,
                "message": f"Cleared {deleted} entries for query '{request.query[:50]}...'"
            }
        else:
            deleted = orchestrator.clear_cache_all()
            return {
                "deleted": deleted,
                "message": f"Cleared all {deleted} cache entries"
            }
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")


@router.post("/cleanup")
async def cleanup_expired(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
):
    """
    Remove expired cache entries.

    This is a maintenance operation that removes entries that have
    exceeded their TTL (time-to-live).
    """
    try:
        deleted = orchestrator.cleanup_cache()
        return {
            "deleted": deleted,
            "message": f"Cleaned up {deleted} expired entries"
        }
    except Exception as e:
        logger.error(f"Failed to cleanup cache: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to cleanup: {str(e)}")
