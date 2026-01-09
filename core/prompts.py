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
# THEME EXTRACTION PROMPT (Phase 1 Fix)
# ============================================================================

THEME_EXTRACTION_PROMPT = """
You are analyzing search results to identify meaningful business concepts that users care about.

Query context: {query}

Source content to analyze:
{source_content}

Your task: Identify 5 distinct BUSINESS CONCEPTS discussed across these sources.

RULES FOR GOOD THEMES:
1. Each theme MUST be a multi-word phrase (2-5 words) representing a specific topic
2. Themes must be DISTINCT from each other (no overlapping concepts)
3. Themes must NOT simply restate the query terms
4. Themes must represent something users would want to learn about or solve

GOOD THEME EXAMPLES:
- "Lead scoring automation" (specific capability)
- "CRM onboarding complexity" (specific pain point)
- "Email deliverability rates" (specific metric users care about)
- "Integration with marketing tools" (specific use case)
- "Pricing transparency concerns" (specific user sentiment)

BAD THEME EXAMPLES (DO NOT OUTPUT THESE):
- "CRM" (single word, too generic)
- "Software" (single word, obvious from context)
- "Best tools" (restates query pattern)
- "Features" (too vague, no specificity)
- "Management" (single word, no context)

For each theme, you MUST provide:
1. The theme name (multi-word phrase)
2. Source evidence: For each source that mentions this concept, extract the EXACT quote (10-30 words) that supports it
3. A brief reason why users care about this topic

Output ONLY valid JSON in this exact format:
{{
  "themes": [
    {{
      "theme": "Lead scoring automation",
      "source_evidence": [
        {{"source_idx": 0, "quote": "automated lead scoring helps prioritize high-value prospects"}},
        {{"source_idx": 2, "quote": "scoring leads automatically saves hours of manual work"}}
      ],
      "user_interest": "Users want to prioritize leads without manual effort"
    }},
    {{
      "theme": "CRM data migration challenges",
      "source_evidence": [
        {{"source_idx": 1, "quote": "migrating data between CRMs can take weeks"}},
        {{"source_idx": 3, "quote": "data loss during migration is a major concern"}}
      ],
      "user_interest": "Switching CRMs is risky and users fear data loss"
    }}
  ]
}}

IMPORTANT: Each quote must be an ACTUAL substring from the source text, not a paraphrase.

Analyze the sources and extract exactly 5 themes.
"""

# ============================================================================
# CONTENT GAP ANALYSIS PROMPT (Phase 3 Fix)
# ============================================================================

CONTENT_GAP_ANALYSIS_PROMPT = """
You are a content strategist analyzing market research to identify specific content opportunities.

Query context: {query}

Themes identified (with source evidence):
{themes_with_evidence}

Competitors in market:
{competitors}

Your task: For each theme, identify a SPECIFIC content gap and generate an actionable recommendation.

A CONTENT GAP is something users want to know that existing content doesn't adequately address.

For each recommendation, provide:
1. topic: A specific, actionable article title (NOT generic like "Deep dive into X")
2. gap_reasoning: What question do users have that competitors don't answer?
3. target_audience: Who specifically would benefit from this content?
4. format_rationale: Why this format is best (Tutorial, Comparison, Case Study, Checklist, Guide)
5. why_now: What signals indicate this content is needed now?

GOOD RECOMMENDATION EXAMPLES:
- topic: "Step-by-step CRM data migration checklist: What to prepare before switching"
  gap_reasoning: "Sources discuss migration difficulty but none provide actionable preparation steps"

- topic: "HubSpot vs Salesforce for real estate teams under 10 agents: A cost analysis"
  gap_reasoning: "Comparisons exist but none focus on small real estate team economics"

BAD RECOMMENDATION EXAMPLES (DO NOT OUTPUT):
- "Deep dive into CRM" (too generic)
- "Everything about lead management" (not specific)
- "CRM best practices" (doesn't address a gap)

Output ONLY valid JSON in this exact format:
{{
  "recommendations": [
    {{
      "topic": "Specific, actionable article title",
      "gap_reasoning": "What's missing from existing content that users need",
      "target_audience": "Specific audience segment",
      "recommended_format": "Tutorial|Comparison|Case Study|Checklist|Guide",
      "format_rationale": "Why this format serves the audience best",
      "why_now": "What signals indicate this content is timely"
    }}
  ]
}}

Generate exactly 5 recommendations, one per theme.
"""

# ============================================================================
# OPPORTUNITY SCORING PROMPT (Phase 4 Fix)
# ============================================================================

OPPORTUNITY_SCORING_PROMPT = """
You are evaluating content opportunities based on market evidence.

For each content recommendation, provide an evidence-based opportunity score.

Recommendations to score:
{recommendations}

Source evidence context:
{source_evidence}

Competitors in market:
{competitors}

For each recommendation, evaluate these dimensions (1-10 scale):

1. **demand_signal** (1-10): How strongly do sources indicate user interest?
   - 8-10: Multiple sources explicitly mention this as a pain point or frequent question
   - 5-7: Some sources discuss this topic with engagement signals
   - 1-4: Weak or no evidence of user demand

2. **competitive_gap** (1-10): How underserved is this topic?
   - 8-10: No competitors adequately address this; clear whitespace
   - 5-7: Competitors touch on this but leave gaps
   - 1-4: Well-covered by multiple competitors

3. **actionability** (1-10): How easily can this content be created?
   - 8-10: Clear format, well-defined scope, executable immediately
   - 5-7: Moderate complexity, may need some research
   - 1-4: Requires deep expertise or extensive research

Calculate opportunity_score as weighted average:
opportunity_score = (demand_signal * 0.4) + (competitive_gap * 0.4) + (actionability * 0.2)

Output ONLY valid JSON:
{{
  "scored_recommendations": [
    {{
      "topic": "Original topic title",
      "opportunity_score": 7.8,
      "score_reasoning": {{
        "demand_signal": 8,
        "demand_evidence": "3 sources mention lead scoring as top pain point",
        "competitive_gap": 7,
        "gap_evidence": "Competitors discuss leads but not scoring mechanics",
        "actionability": 9,
        "actionability_reasoning": "Tutorial format, clear step-by-step structure possible"
      }}
    }}
  ]
}}

Score all provided recommendations.
"""

# ============================================================================
# COMBINED CONTENT GAP + SCORING PROMPT (Performance Optimization)
# ============================================================================

CONTENT_GAP_WITH_SCORING_PROMPT = """
You are a content strategist analyzing market research to identify AND score content opportunities.

Query context: {query}

Themes identified (with source evidence):
{themes_with_evidence}

Source evidence context:
{source_evidence}

Competitors in market:
{competitors}

Your task: For each theme, identify a SPECIFIC content gap, generate an actionable recommendation, AND provide an evidence-based opportunity score.

A CONTENT GAP is something users want to know that existing content doesn't adequately address.

For each recommendation, provide:
1. topic: A specific, actionable article title (NOT generic like "Deep dive into X")
2. gap_reasoning: What question do users have that competitors don't answer?
3. target_audience: Who specifically would benefit from this content?
4. recommended_format: Tutorial|Comparison|Case Study|Checklist|Guide
5. format_rationale: Why this format serves the audience best
6. why_now: What signals indicate this content is needed now?
7. opportunity_score: Weighted average of demand_signal (40%), competitive_gap (40%), actionability (20%)
8. score_reasoning: Evidence for each dimension

GOOD RECOMMENDATION EXAMPLES:
- topic: "Step-by-step CRM data migration checklist: What to prepare before switching"
  gap_reasoning: "Sources discuss migration difficulty but none provide actionable preparation steps"
  opportunity_score: 8.4 (high demand, clear gap, easy to create)

- topic: "HubSpot vs Salesforce for real estate teams under 10 agents: A cost analysis"
  gap_reasoning: "Comparisons exist but none focus on small real estate team economics"
  opportunity_score: 7.6 (moderate demand, good gap, moderate complexity)

BAD RECOMMENDATION EXAMPLES (DO NOT OUTPUT):
- "Deep dive into CRM" (too generic)
- "Everything about lead management" (not specific)
- "CRM best practices" (doesn't address a gap)

Scoring dimensions (1-10 scale):

1. **demand_signal** (1-10): How strongly do sources indicate user interest?
   - 8-10: Multiple sources explicitly mention this as a pain point or frequent question
   - 5-7: Some sources discuss this topic with engagement signals
   - 1-4: Weak or no evidence of user demand

2. **competitive_gap** (1-10): How underserved is this topic?
   - 8-10: No competitors adequately address this; clear whitespace
   - 5-7: Competitors touch on this but leave gaps
   - 1-4: Well-covered by multiple competitors

3. **actionability** (1-10): How easily can this content be created?
   - 8-10: Clear format, well-defined scope, executable immediately
   - 5-7: Moderate complexity, may need some research
   - 1-4: Requires deep expertise or extensive research

Calculate: opportunity_score = (demand_signal * 0.4) + (competitive_gap * 0.4) + (actionability * 0.2)

Output ONLY valid JSON in this exact format:
{{
  "recommendations": [
    {{
      "topic": "Specific, actionable article title",
      "gap_reasoning": "What's missing from existing content that users need",
      "target_audience": "Specific audience segment",
      "recommended_format": "Tutorial|Comparison|Case Study|Checklist|Guide",
      "format_rationale": "Why this format serves the audience best",
      "why_now": "What signals indicate this content is timely",
      "opportunity_score": 7.8,
      "score_reasoning": {{
        "demand_signal": 8,
        "demand_evidence": "3 sources mention lead scoring as top pain point",
        "competitive_gap": 7,
        "gap_evidence": "Competitors discuss leads but not scoring mechanics",
        "actionability": 9,
        "actionability_reasoning": "Tutorial format, clear step-by-step structure possible"
      }}
    }}
  ]
}}

Generate exactly 5 recommendations, one per theme.
"""

# ============================================================================
# CONTEXTUAL SENTIMENT PROMPT (Phase 5 Fix)
# ============================================================================

CONTEXTUAL_SENTIMENT_PROMPT = """
You are analyzing sentiment in market research sources to provide contextual attribution.

Theme to analyze: {theme}

Source quotes mentioning this theme:
{quotes}

Your task: Analyze sentiment WITH context. Don't just say "positive" or "negative" - explain WHAT the sentiment is about and WHY.

For each theme, provide:
1. sentiment_summary: A readable sentence describing the overall sentiment (e.g., "Users praise the ease of use but criticize the pricing")
2. sentiment_signals: List of specific sentiment observations with:
   - subject: What specifically is the sentiment about?
   - polarity: "positive", "negative", or "mixed"
   - reason: Why do users feel this way? (quote or paraphrase from sources)

GOOD SENTIMENT EXAMPLES:
- subject: "HubSpot onboarding process"
  polarity: "positive"
  reason: "described as 'quick and intuitive' by multiple users"

- subject: "Salesforce pricing"
  polarity: "negative"
  reason: "users mention it's 'expensive for small teams'"

BAD SENTIMENT EXAMPLES (DO NOT OUTPUT):
- subject: "CRM" (too vague)
  polarity: "positive"
  reason: "sources are positive" (no specific reason)

Output ONLY valid JSON:
{{
  "sentiment_summary": "Users appreciate X but express concerns about Y",
  "sentiment_signals": [
    {{
      "subject": "Specific feature or aspect",
      "polarity": "positive|negative|mixed",
      "reason": "Specific reason from sources"
    }}
  ]
}}

Provide 2-4 sentiment signals based on the source quotes.
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
    'THEME_EXTRACTION_PROMPT',
    'CONTENT_GAP_ANALYSIS_PROMPT',
    'OPPORTUNITY_SCORING_PROMPT',
    'CONTENT_GAP_WITH_SCORING_PROMPT',
    'CONTEXTUAL_SENTIMENT_PROMPT',
    'format_prompt'
]