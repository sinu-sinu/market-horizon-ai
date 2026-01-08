"""Test script to run full pipeline with Langfuse tracing"""
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import logging
from core.orchestrator import AgentOrchestrator

# Set logging to WARNING to reduce noise
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s - %(message)s'
)

# Enable INFO for core modules
logging.getLogger('core.orchestrator').setLevel(logging.INFO)
logging.getLogger('core.observability').setLevel(logging.INFO)

print('='*80)
print('Market Horizon AI - Full Pipeline Test with Langfuse Tracing')
print('='*80)

# Run pipeline
query = 'Best CRM tools for real estate agents'
print(f'\nQuery: {query}')
print('Starting pipeline...\n')

orchestrator = AgentOrchestrator()
result = orchestrator.run(query)

print('\n' + '='*80)
print('Pipeline Complete!')
print('='*80)
print(f'Confidence Score: {result.get("confidence_score", 0):.2f}')
print(f'Competitors Found: {len(result.get("competitors", []))}')
print(f'Content Recommendations: {len(result.get("content_recommendations", []))}')

print('\n' + '='*80)
print('Langfuse Trace Available')
print('='*80)
print('URL: http://localhost:3000')
print('Trace Name: "market-horizon-pipeline"')
print('\nExpected to see:')
print('  - research-agent span (API calls)')
print('  - analysis-agent span + LLM generation (competitor-extraction)')
print('  - strategy-agent span + LLM generation (positioning-map)')
print('  - quality-agent span')
print('  - Total tokens and cost')
print('='*80)
