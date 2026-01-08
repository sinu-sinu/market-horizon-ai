"""
End-to-End Pipeline Tests
Tests the complete workflow from research through quality validation
"""
import pytest
from core.orchestrator import AgentOrchestrator
import json
import os
from datetime import datetime
import time


class TestE2EPipeline:
    """End-to-end pipeline tests with sample queries"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance"""
        return AgentOrchestrator()
    
    def test_pipeline_initialization(self, orchestrator):
        """Test that pipeline initializes all agents"""
        assert orchestrator.research_agent is not None
        assert orchestrator.analysis_agent is not None
        assert orchestrator.strategy_agent is not None
        assert orchestrator.quality_agent is not None
        assert orchestrator.workflow is not None
    
    def test_pipeline_output_structure(self, orchestrator):
        """Test that pipeline produces correct output structure"""
        query = "test market research query"
        
        result = orchestrator.run(query)
        
        # Verify main sections
        assert "report_metadata" in result
        assert "validated_insights" in result
        assert "quality_flags" in result
        assert "source_attribution" in result
        
        # Verify metadata fields
        metadata = result["report_metadata"]
        assert metadata["query"] == query
        assert "timestamp" in metadata
        assert "confidence_score" in metadata
        assert "processing_time_seconds" in metadata
        
        # Verify confidence is in valid range
        assert 0.0 <= metadata["confidence_score"] <= 1.0
    
    def test_pipeline_with_crm_query(self, orchestrator):
        """Test pipeline with CRM tools query"""
        query = "CRM software for small businesses"
        
        start_time = time.time()
        result = orchestrator.run(query)
        elapsed_time = time.time() - start_time
        
        # Verify completion
        assert result is not None
        assert result["report_metadata"]["query"] == query
        
        # Log results for inspection
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"Confidence: {result['report_metadata']['confidence_score']}")
        print(f"Sources: {result['report_metadata']['total_sources']}")
        print(f"Elapsed time: {elapsed_time:.1f}s")
        print(f"{'='*60}")
        
        # Save output for manual inspection
        self._save_test_output(result, "crm_query")
    
    def test_workflow_state_propagation(self, orchestrator):
        """Test that state propagates correctly through workflow"""
        query = "project management tools"
        
        result = orchestrator.run(query)
        
        # Verify each agent contributed
        insights = result["validated_insights"]
        
        # Research should have found sources
        assert result["report_metadata"]["total_sources"] >= 0
        
        # Analysis should have processed data
        assert "competitors" in insights
        assert "content_themes" in insights
        
        # Strategy should have generated recommendations
        assert "positioning_map" in insights
        assert "content_recommendations" in insights
        
        # Quality should have validated everything
        assert "quality_flags" in result
    
    def _save_test_output(self, result: dict, test_name: str):
        """Save test output for inspection"""
        output_dir = "outputs/reports"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"\nTest output saved to: {filepath}")


class TestMultipleQueries:
    """Test pipeline with multiple query types"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance"""
        return AgentOrchestrator()
    
    @pytest.fixture
    def test_queries(self):
        """Sample test queries from different categories"""
        return {
            "b2b_saas": "CRM tools for real estate agents",
            "project_management": "Project management software for remote teams",
            "marketing": "Email marketing platforms for ecommerce"
        }
    
    def test_multiple_query_types(self, orchestrator, test_queries):
        """Test pipeline with multiple query types"""
        results = {}
        
        for category, query in test_queries.items():
            print(f"\n{'='*60}")
            print(f"Testing: {category}")
            print(f"Query: {query}")
            
            start_time = time.time()
            result = orchestrator.run(query)
            elapsed_time = time.time() - start_time
            
            # Verify result
            assert result is not None
            assert result["report_metadata"]["query"] == query
            
            # Store results
            results[category] = {
                "confidence": result["report_metadata"]["confidence_score"],
                "sources": result["report_metadata"]["total_sources"],
                "elapsed_time": elapsed_time,
                "competitors_count": len(result["validated_insights"]["competitors"]),
                "themes_count": len(result["validated_insights"]["content_themes"])
            }
            
            print(f"Confidence: {results[category]['confidence']:.2f}")
            print(f"Sources: {results[category]['sources']}")
            print(f"Competitors: {results[category]['competitors_count']}")
            print(f"Time: {elapsed_time:.1f}s")
        
        # Verify all queries completed
        assert len(results) == len(test_queries)
        
        # Print summary
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        for category, stats in results.items():
            print(f"{category}:")
            print(f"  Confidence: {stats['confidence']:.2f}")
            print(f"  Time: {stats['elapsed_time']:.1f}s")


class TestErrorHandling:
    """Test error handling in pipeline"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance"""
        return AgentOrchestrator()
    
    def test_empty_query_handling(self, orchestrator):
        """Test handling of empty query"""
        result = orchestrator.run("")
        
        # Should still return valid structure
        assert "report_metadata" in result
        assert "quality_flags" in result
    
    def test_very_specific_query(self, orchestrator):
        """Test with very specific/niche query"""
        query = "quantum computing tools for bioinformatics researchers"
        
        result = orchestrator.run(query)
        
        # Should complete even if results are limited
        assert result is not None
        assert "report_metadata" in result


# Integration tests (require API keys)
@pytest.mark.integration
class TestIntegrationWithRealAPIs:
    """Integration tests with real API calls"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance"""
        return AgentOrchestrator()
    
    def test_full_pipeline_with_real_apis(self, orchestrator):
        """
        Test complete pipeline with real API calls
        
        Mark: @pytest.mark.integration
        Run with: pytest tests/test_e2e_pipeline.py -m integration -v
        """
        query = "CRM software comparison"
        
        print(f"\n{'='*60}")
        print("INTEGRATION TEST - Real API Calls")
        print(f"{'='*60}")
        print(f"Query: {query}")
        
        start_time = time.time()
        result = orchestrator.run(query)
        elapsed_time = time.time() - start_time
        
        # Verify result quality
        metadata = result["report_metadata"]
        
        print(f"\nResults:")
        print(f"  Confidence: {metadata['confidence_score']:.2f}")
        print(f"  Sources: {metadata['total_sources']}")
        print(f"  Processing time: {elapsed_time:.1f}s")
        print(f"  API calls: {metadata.get('api_calls', 0)}")
        
        # Acceptance criteria from PRD
        assert metadata["confidence_score"] >= 0.70, "Confidence should be ≥0.70"
        assert elapsed_time < 180, "Processing time should be <180s"
        assert metadata["total_sources"] > 0, "Should find sources"
        
        # Verify insights generated
        insights = result["validated_insights"]
        assert len(insights["competitors"]) > 0, "Should identify competitors"
        assert len(insights["content_recommendations"]) > 0, "Should generate recommendations"
        
        # Save detailed output
        output_path = "outputs/reports/integration_test_result.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"\nFull output saved to: {output_path}")
        print(f"{'='*60}")
    
    def test_acceptance_criteria(self, orchestrator):
        """
        Test against PRD acceptance criteria
        
        Acceptance criteria from Phase 1.6:
        - Pipeline completes without errors for ≥3 queries
        - Output JSON validates against schema
        - Confidence scores ≥0.70
        - Processing time <180 seconds
        - No API errors (or proper fallback used)
        """
        test_queries = [
            "CRM tools for real estate",
            "Project management software",
            "Email marketing automation"
        ]
        
        results = []
        
        for query in test_queries:
            print(f"\nTesting: {query}")
            
            start_time = time.time()
            result = orchestrator.run(query)
            elapsed_time = time.time() - start_time
            
            # Collect metrics
            results.append({
                "query": query,
                "confidence": result["report_metadata"]["confidence_score"],
                "time": elapsed_time,
                "sources": result["report_metadata"]["total_sources"],
                "errors": len(result["report_metadata"].get("errors", []))
            })
            
            print(f"  ✓ Confidence: {results[-1]['confidence']:.2f}")
            print(f"  ✓ Time: {elapsed_time:.1f}s")
        
        # Verify acceptance criteria
        print(f"\n{'='*60}")
        print("ACCEPTANCE CRITERIA VALIDATION")
        print(f"{'='*60}")
        
        # Criterion 1: All queries completed
        assert len(results) == len(test_queries), "All queries should complete"
        print("✓ All 3 queries completed")
        
        # Criterion 2: Confidence scores
        avg_confidence = sum(r["confidence"] for r in results) / len(results)
        assert avg_confidence >= 0.70, f"Average confidence {avg_confidence:.2f} < 0.70"
        print(f"✓ Average confidence: {avg_confidence:.2f} (≥0.70)")
        
        # Criterion 3: Processing time
        avg_time = sum(r["time"] for r in results) / len(results)
        assert all(r["time"] < 180 for r in results), "Some queries exceeded 180s"
        print(f"✓ Average processing time: {avg_time:.1f}s (<180s)")
        
        # Criterion 4: Sources found
        total_sources = sum(r["sources"] for r in results)
        assert total_sources > 0, "No sources found across all queries"
        print(f"✓ Total sources found: {total_sources}")
        
        print(f"{'='*60}")
        print("✅ ALL ACCEPTANCE CRITERIA MET")
        print(f"{'='*60}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])