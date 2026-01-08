"""
Sample test data for Market Horizon AI agents
"""

# Sample research data output
SAMPLE_RESEARCH_DATA = {
    "query": "CRM tools for real estate agents",
    "sources": [
        {
            "url": "https://example.com/article1",
            "title": "Top 10 CRM Tools for Real Estate Agents in 2024",
            "snippet": "Review of the best CRM tools including Salesforce, HubSpot, and Zoho for real estate professionals.",
            "date": "2024-10-15",
            "source_type": "web"
        },
        {
            "url": "https://example.com/article2",
            "title": "How Real Estate Agents Use CRM Software",
            "snippet": "Case studies showcasing how top agents use CRM tools to manage leads and close more deals.",
            "date": "2024-09-28",
            "source_type": "web"
        },
        {
            "url": "https://example.com/article3",
            "title": "Salesforce vs HubSpot: Which CRM is Better?",
            "snippet": "Detailed comparison of Salesforce and HubSpot CRM features, pricing, and use cases.",
            "date": "2024-10-01",
            "source_type": "web"
        },
        {
            "url": "https://example.com/article4",
            "title": "Zoho CRM Review: Affordable Option for Small Teams",
            "snippet": "In-depth review of Zoho CRM features and why it's popular among small businesses.",
            "date": "2024-09-15",
            "source_type": "web"
        },
        {
            "url": "https://example.com/article5",
            "title": "Real Estate CRM Features You Need",
            "snippet": "Essential features every real estate CRM should have: lead management, automation, integrations.",
            "date": "2024-10-10",
            "source_type": "web"
        }
    ],
    "trends": {
        "query": "CRM tools real estate",
        "trend_data": {
            "2024-08-01": 65,
            "2024-08-15": 70,
            "2024-09-01": 75,
            "2024-09-15": 72,
            "2024-10-01": 80,
            "2024-10-15": 85
        },
        "average_interest": 74.5
    },
    "discussions": [
        {
            "title": "What CRM do you use for your real estate business?",
            "url": "https://reddit.com/r/realestate/comments/abc123",
            "score": 125,
            "num_comments": 47,
            "created": 1696204800,
            "subreddit": "realestate",
            "source_type": "reddit"
        },
        {
            "title": "Switching from Salesforce to HubSpot - worth it?",
            "url": "https://reddit.com/r/sales/comments/def456",
            "score": 89,
            "num_comments": 32,
            "created": 1697414400,
            "subreddit": "sales",
            "source_type": "reddit"
        }
    ],
    "metadata": {
        "total_sources": 5,
        "source_types": {
            "web": 5,
            "trends": 1,
            "reddit": 2
        }
    }
}

# Sample analysis insights output
SAMPLE_ANALYSIS_INSIGHTS = {
    "competitors": ["Salesforce", "HubSpot", "Zoho", "Pipedrive", "Monday.com"],
    "content_themes": [
        {
            "theme": "Lead management automation",
            "frequency": 15,
            "sentiment": 0.8,
            "key_phrases": ["lead scoring", "automated follow-ups", "pipeline tracking"]
        },
        {
            "theme": "Integration capabilities",
            "frequency": 12,
            "sentiment": 0.7,
            "key_phrases": ["API integrations", "third-party apps", "data sync"]
        },
        {
            "theme": "Mobile accessibility",
            "frequency": 10,
            "sentiment": 0.75,
            "key_phrases": ["mobile app", "on-the-go access", "field updates"]
        }
    ],
    "competitor_attributes": {
        "Salesforce": {
            "price_positioning": 8.5,
            "target_market_size": 9.0,
            "sentiment": 0.75,
            "mention_count": 8
        },
        "HubSpot": {
            "price_positioning": 6.0,
            "target_market_size": 6.5,
            "sentiment": 0.85,
            "mention_count": 7
        },
        "Zoho": {
            "price_positioning": 3.5,
            "target_market_size": 4.0,
            "sentiment": 0.80,
            "mention_count": 6
        }
    },
    "vectorstore_path": "data/faiss_index"
}

# Sample strategy recommendations output
SAMPLE_STRATEGY_RECOMMENDATIONS = {
    "positioning_map": {
        "dimensions": {
            "x_axis": "Price Positioning (1-10)",
            "y_axis": "Target Company Size (1-10)"
        },
        "companies": {
            "Salesforce": {"x": 8.5, "y": 9.0, "rationale": "Enterprise focus, premium pricing"},
            "HubSpot": {"x": 6.0, "y": 6.5, "rationale": "Mid-market focus, flexible pricing"},
            "Zoho": {"x": 3.5, "y": 4.0, "rationale": "SMB focus, affordable pricing"}
        }
    },
    "opportunity_zones": [
        {
            "coordinates": {"x": 4.5, "y": 8.5},
            "description": "Mid-price enterprise gap",
            "rationale": "No major competitors targeting this segment",
            "opportunity_score": 8.5
        }
    ],
    "content_recommendations": [
        {
            "topic": "CRM implementation best practices for real estate",
            "priority": "high",
            "opportunity_score": 8.7,
            "search_volume_monthly": 5400,
            "competitor_coverage": "2 of 5 companies",
            "recommended_format": "Blog post + video tutorial",
            "estimated_effort": "medium"
        },
        {
            "topic": "Lead scoring strategies for realtors",
            "priority": "high",
            "opportunity_score": 8.2,
            "search_volume_monthly": 3200,
            "competitor_coverage": "1 of 5 companies",
            "recommended_format": "Case study + webinar",
            "estimated_effort": "high"
        }
    ],
    "strategic_moves": [
        "Position as 'enterprise-ready at mid-market prices'",
        "Emphasize implementation speed vs competitors",
        "Focus on mobile-first approach for field agents"
    ]
}

# Sample quality report output
SAMPLE_QUALITY_REPORT = {
    "report_metadata": {
        "query": "CRM tools for real estate agents",
        "timestamp": "2024-11-02T10:00:00",
        "total_sources": 5,
        "processing_time_seconds": 45,
        "confidence_score": 0.85
    },
    "validated_insights": {
        "competitors": ["Salesforce", "HubSpot", "Zoho"],
        "content_themes": [
            {
                "theme": "Lead management automation",
                "frequency": 15,
                "sentiment": 0.8
            }
        ],
        "positioning_map": {
            "dimensions": {
                "x_axis": "Price Positioning (1-10)",
                "y_axis": "Target Company Size (1-10)"
            },
            "companies": {
                "Salesforce": {"x": 8.5, "y": 9.0},
                "HubSpot": {"x": 6.0, "y": 6.5},
                "Zoho": {"x": 3.5, "y": 4.0}
            }
        },
        "content_recommendations": [
            {
                "topic": "CRM implementation best practices",
                "priority": "high",
                "opportunity_score": 8.7
            }
        ],
        "strategic_recommendations": [
            "Position as 'enterprise-ready at mid-market prices'"
        ]
    },
    "quality_flags": [
        {
            "type": "info",
            "message": "Source count is adequate (5 sources)",
            "agent": "research"
        }
    ],
    "source_attribution": {
        "total_sources": 5,
        "source_breakdown": {
            "web_articles": 5,
            "reddit_discussions": 2
        },
        "date_range": "Last 3 months"
    }
}

# Test queries for different scenarios
TEST_QUERIES = {
    "b2b_saas": [
        "CRM tools for real estate agents",
        "Project management software for construction",
        "Email marketing platforms for B2B"
    ],
    "ecommerce": [
        "Shopify vs WooCommerce",
        "Subscription box platforms",
        "Returns management software"
    ],
    "developer_tools": [
        "API documentation tools",
        "CI/CD platforms for small teams",
        "Code review tools"
    ]
}