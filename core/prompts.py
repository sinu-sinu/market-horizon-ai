"""
LLM Prompts for Market Horizon AI Agents
"""

# ============================================================================
# RESEARCH AGENT PROMPTS
# ============================================================================

RESEARCH_PROMPT = """
You are a data gathering specialist for market research. Your task is to search for and retrieve 
information about: {query}

Your objectives:
1. Identify the top competitors in this space
2. Find recent content (last 3 months) from these competitors
3. Identify trending topics related to {query}

Search Strategy:
- Look for company names, product names, and service providers
- Focus on blog posts, case studies, product pages, and news articles
- Identify thought leaders and key players in the market

Output Requirements:
- List all competitor names you find
- Provide URLs for all sources
- Include publication dates where available
- Summarize key points from each source (1-2 sentences)

Format your findings as structured JSON:
{{
  "competitors": ["Company A", "Company B", "Company C"],
  "sources": [
    {{
      "url": "https://example.com/article",
      "title": "Article Title",
      "date": "2024-10-15",
      "summary": "Brief summary of key points"
    }}
  ],
  "key_topics": ["Topic 1", "Topic 2", "Topic 3"]
}}
"""

# ============================================================================
# ANALYSIS AGENT PROMPTS
# ============================================================================

ANALYSIS_PROMPT = """
You are a pattern detection specialist analyzing market research data about {topic}.

Your task is to analyze the following data corpus and extract meaningful insights:

Data to analyze:
{data_corpus}

Analysis objectives:
1. Identify 3-5 major content themes across all sources
2. Determine competitor positioning attributes for each company:
   - Price tier (estimate on 1-10 scale based on language used)
   - Target market size (1=freelancers/SMB, 10=enterprise)
   - Feature emphasis (technical vs. user-friendly)
3. Analyze sentiment trends toward competitors and topics

Output Requirements:
- For each theme, provide:
  * Theme name
  * Frequency of mentions
  * Key phrases that represent it
  * Sentiment score (-1 to +1)
  
- For each competitor, provide:
  * Price positioning (1-10 score with rationale)
  * Target company size (1-10 score with rationale)
  * Competitive advantages mentioned
  * Weaknesses or gaps mentioned

- Include confidence levels (low/medium/high) based on:
  * Number of sources
  * Consistency of information
  * Recency of data

Format as structured JSON with clear rationale for each insight.
"""

COMPETITOR_ANALYSIS_PROMPT = """
Analyze the following competitors and their market positioning:

Competitors: {competitors}
Source data: {source_data}

For each competitor, determine:
1. **Price Positioning** (1-10 scale):
   - 1-3: Budget/entry-level
   - 4-6: Mid-market
   - 7-10: Premium/enterprise
   
   Base your assessment on:
   - Explicit pricing mentions
   - Target customer language
   - Feature complexity
   - Case study company sizes

2. **Target Company Size** (1-10 scale):
   - 1-3: Freelancers, solopreneurs, micro-businesses
   - 4-6: Small to medium businesses (10-100 employees)
   - 7-10: Enterprises (100+ employees)
   
   Base your assessment on:
   - Customer testimonials and case studies
   - Feature set complexity
   - Integration capabilities
   - Self-described target audience

3. **Key Differentiators**:
   - What makes this competitor unique?
   - What features do they emphasize?
   - What problems do they solve?

Provide your analysis in JSON format with scores and detailed rationale.
"""

# ============================================================================
# STRATEGY AGENT PROMPTS
# ============================================================================

POSITIONING_PROMPT = """
Analyze the following competitors and assign positioning coordinates on a 2D map:

Competitor data:
{competitor_data}

Task: Assign X,Y coordinates for each competitor on a 1-10 scale:
- **X-axis**: Price Positioning (1=budget, 10=premium)
- **Y-axis**: Target Company Size (1=freelancer/SMB, 10=enterprise)

Consider these factors:
1. **Pricing indicators**:
   - Mentions of "affordable", "budget-friendly" → lower X
   - Mentions of "enterprise", "custom pricing" → higher X
   - Free tiers → lower X
   - "Contact sales" pricing → higher X

2. **Target market indicators**:
   - "For freelancers", "solo entrepreneurs" → lower Y
   - "For small businesses", "teams" → mid Y
   - "For enterprises", "large organizations" → higher Y
   - Integration complexity → higher Y
   - Scalability mentions → higher Y

3. **Feature complexity**:
   - Simple, easy-to-use tools → lower scores
   - Advanced features, customization → higher scores

Output **ONLY** valid JSON with company names as keys and x,y coordinates:

{{
  "Company A": {{"x": 7.5, "y": 8.0, "rationale": "Enterprise focus, premium pricing"}},
  "Company B": {{"x": 3.0, "y": 4.5, "rationale": "SMB focus, affordable pricing"}}
}}

Ensure all coordinates are between 1.0 and 10.0.
"""

CONTENT_GAP_PROMPT = """
Identify content opportunities and gaps based on the following analysis:

Content themes identified: {themes}
Competitors analyzed: {competitors}
Trend data: {trends}

Your task:
1. Identify underserved topics (themes with <30% competitor coverage)
2. Find high-opportunity content areas where:
   - Search interest is growing
   - Competition is low
   - Topic relevance is high

3. Prioritize content recommendations by:
   - Search volume (higher is better)
   - Competitor coverage (lower is better)
   - Trend direction (increasing is better)
   - Recency (newer trends score higher)

For each content recommendation, provide:
- Topic/keyword
- Priority level (high/medium/low)
- Opportunity score (0-10)
- Estimated monthly search volume
- Number of competitors covering this topic
- Recommended content format (blog, video, case study, etc.)
- Estimated effort (low/medium/high)

Output as structured JSON with recommendations sorted by opportunity score.
"""

STRATEGIC_MOVES_PROMPT = """
Based on the competitive positioning map and opportunity analysis, generate strategic recommendations:

Positioning data: {positioning_map}
Opportunity zones: {opportunity_zones}
Market trends: {trends}

Generate 3-5 strategic recommendations in these categories:

1. **Positioning Strategy**:
   - Where should we position in the market?
   - What white space opportunities exist?
   - How to differentiate from competitors?

2. **Content Strategy**:
   - What topics to prioritize?
   - What content formats to use?
   - What narratives to develop?

3. **Messaging Strategy**:
   - What key messages resonate with target audience?
   - What pain points to address?
   - What value propositions to emphasize?

Each recommendation should include:
- Clear actionable statement
- Rationale based on data
- Expected impact
- Implementation difficulty

Output as structured list of strategic moves.
"""

# ============================================================================
# QUALITY AGENT PROMPTS
# ============================================================================

VALIDATION_PROMPT = """
Validate the quality and accuracy of the following market intelligence report:

Report data: {report_data}

Validation checklist:
1. **Source Quality**:
   - Are sources credible and recent?
   - Is there sufficient source diversity?
   - Minimum 5 sources required

2. **Competitor Validation**:
   - Are competitors verified across multiple sources?
   - Minimum 2 mentions per competitor
   - At least 3 competitors identified

3. **Positioning Accuracy**:
   - Do positioning scores align with source evidence?
   - Are coordinates within valid ranges (1-10)?
   - Coverage of at least 70% of identified competitors

4. **Recommendation Quality**:
   - Are recommendations actionable?
   - Are they backed by data?
   - Do they address clear opportunities?

5. **Consistency**:
   - Do insights contradict each other?
   - Is the narrative coherent?
   - Are confidence levels appropriate?

For each validation item, mark as PASS/FAIL and provide:
- Issue description (if failed)
- Severity (low/medium/high)
- Suggested correction

Calculate overall confidence score (0-1.0) based on:
- Source count and quality: 40%
- Validation pass rate: 30%
- Data consistency: 20%
- Completeness: 10%

Output validation report with confidence score and quality flags.
"""

SOURCE_ATTRIBUTION_PROMPT = """
Build complete source attribution for all insights in the report:

Insights: {insights}
Sources: {sources}

For each insight or claim, identify:
1. Which source(s) support it
2. Strength of evidence (strong/moderate/weak)
3. Any contradicting sources
4. Gaps in evidence

Output source attribution map linking each insight to its supporting sources.
Highlight any unsupported claims that need additional research.
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_prompt(template: str, **kwargs) -> str:
    """
    Format a prompt template with provided arguments
    
    Args:
        template: Prompt template string
        **kwargs: Values to insert into template
        
    Returns:
        Formatted prompt string
    """
    return template.format(**kwargs)


# Export all prompts
__all__ = [
    'RESEARCH_PROMPT',
    'ANALYSIS_PROMPT',
    'COMPETITOR_ANALYSIS_PROMPT',
    'POSITIONING_PROMPT',
    'CONTENT_GAP_PROMPT',
    'STRATEGIC_MOVES_PROMPT',
    'VALIDATION_PROMPT',
    'SOURCE_ATTRIBUTION_PROMPT',
    'format_prompt'
]