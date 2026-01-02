from pydantic import BaseModel, Field
from typing import Optional, Any


class ContentTheme(BaseModel):
    """Content theme with sentiment"""
    theme: str
    frequency: int
    sentiment: float


class CompanyPosition(BaseModel):
    """Company position on the positioning map"""
    x: float
    y: float
    rationale: Optional[str] = None


class OpportunityZone(BaseModel):
    """Opportunity zone on positioning map"""
    coordinates: dict[str, float]
    description: Optional[str] = None
    rationale: Optional[str] = None
    opportunity_score: Optional[float] = None


class PositioningMap(BaseModel):
    """Competitive positioning map"""
    dimensions: Optional[dict[str, str]] = None
    companies: Optional[dict[str, CompanyPosition]] = None
    opportunity_zones: Optional[list[OpportunityZone]] = None


class ContentRecommendation(BaseModel):
    """Content recommendation"""
    topic: str
    priority: str
    opportunity_score: float
    recommended_format: Optional[str] = None
    effort_level: Optional[str] = None


class QualityFlag(BaseModel):
    """Quality flag from validation"""
    type: str
    message: str
    agent: str


class AgentError(BaseModel):
    """Error from an agent"""
    agent: str
    error: str
    timestamp: str
    fallback_used: bool


class ReportMetadata(BaseModel):
    """Report metadata"""
    query: str
    timestamp: str
    total_sources: int
    processing_time_seconds: int
    confidence_score: float
    api_calls: Optional[int] = None
    total_tokens: Optional[int] = None
    errors: Optional[list[AgentError]] = None


class ValidatedInsights(BaseModel):
    """Validated insights from analysis"""
    competitors: list[str] = Field(default_factory=list)
    content_themes: list[ContentTheme] = Field(default_factory=list)
    positioning_map: Optional[dict[str, Any]] = None
    content_recommendations: list[ContentRecommendation] = Field(default_factory=list)
    strategic_recommendations: list[str] = Field(default_factory=list)


class SourceAttribution(BaseModel):
    """Source attribution data"""
    total_sources: Optional[int] = None
    source_breakdown: Optional[dict[str, int]] = None
    date_range: Optional[str] = None
    trends_data_available: Optional[bool] = None
    discussions_available: Optional[bool] = None


class AnalysisResponse(BaseModel):
    """Full analysis response"""
    report_metadata: ReportMetadata
    validated_insights: ValidatedInsights
    quality_flags: list[QualityFlag] = Field(default_factory=list)
    source_attribution: Optional[dict[str, Any]] = None
    query_text: Optional[str] = None


class QueryHistoryItem(BaseModel):
    """Query history item for listing"""
    id: int
    query: str
    timestamp: str
    confidence_score: Optional[float] = None
    num_competitors: Optional[int] = None


class CacheTypeStats(BaseModel):
    """Statistics for a cache type"""
    type: str
    count: int
    hits: int


class CacheStatsResponse(BaseModel):
    """Cache statistics response"""
    stats: dict[str, int]
    hit_rate: str
    total_entries_valid: int
    total_entries_all: int
    total_size_bytes: int
    total_size_mb: float
    by_type: list[CacheTypeStats]
