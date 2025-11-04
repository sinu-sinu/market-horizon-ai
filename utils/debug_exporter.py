"""
Debug Report Exporter - Exports detailed debugging information
"""
import json
import os
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class DebugExporter:
    """Exports detailed debug information for analysis"""

    def __init__(self, output_dir: str = "outputs/debug"):
        """Initialize debug exporter

        Args:
            output_dir: Directory to save debug reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export_analysis_debug(
        self,
        query: str,
        sources: list,
        llm_competitors: list,
        ner_competitors: list,
        final_competitors: list,
        validation_results: Dict[str, Any] = None
    ) -> str:
        """Export comprehensive analysis debug report

        Args:
            query: Search query
            sources: Research sources
            llm_competitors: Competitors from LLM
            ner_competitors: Competitors from NER
            final_competitors: Final merged competitors
            validation_results: Validation scores and results

        Returns:
            Path to saved debug report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debug_{query.replace(' ', '_')}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        # Build comprehensive debug report
        debug_report = {
            "metadata": {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "total_sources": len(sources)
            },
            "sources_analysis": {
                "count": len(sources),
                "sample_titles": [s.get("title", "")[:100] for s in sources[:5]],
                "sample_snippets": [s.get("snippet", "")[:200] for s in sources[:5]]
            },
            "competitor_extraction": {
                "llm_extracted": {
                    "count": len(llm_competitors),
                    "competitors": llm_competitors
                },
                "ner_extracted": {
                    "count": len(ner_competitors),
                    "competitors": ner_competitors
                },
                "final_merged": {
                    "count": len(final_competitors),
                    "competitors": final_competitors
                }
            },
            "validation": validation_results or {},
            "sources_full": sources  # Full source data for deep analysis
        }

        # Save to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(debug_report, f, indent=2, ensure_ascii=False)

        logger.info(f"Debug report saved to: {filepath}")
        return filepath


# Global debug exporter instance
debug_exporter = DebugExporter()
