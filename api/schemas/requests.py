from pydantic import BaseModel, Field
from typing import Optional


class AnalyzeRequest(BaseModel):
    """Request model for analysis endpoint"""

    query: str = Field(
        ...,
        min_length=3,
        max_length=5000,
        description="The market research query to analyze"
    )
    parameters: Optional[dict] = Field(
        default=None,
        description="Optional parameters for customization"
    )


class ClearCacheRequest(BaseModel):
    """Request model for clearing cache"""

    cache_type: Optional[str] = Field(
        default=None,
        description="Specific cache type to clear (web_search, google_trends, etc.)"
    )
    query: Optional[str] = Field(
        default=None,
        description="Specific query to clear cache for"
    )
