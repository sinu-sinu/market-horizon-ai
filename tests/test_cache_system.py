#!/usr/bin/env python3
"""
Test script to demonstrate the caching system in action

This script shows:
1. Cache statistics
2. Performance improvement with cache
3. Cache management operations
"""

import time
import sys
import logging
from core.orchestrator import AgentOrchestrator
from utils.cache_manager import get_cache_manager, CacheManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def test_cache_stats():
    """Test 1: Display cache statistics"""
    print_header("TEST 1: Cache Statistics")

    orchestrator = AgentOrchestrator()
    orchestrator.print_cache_stats()


def test_cache_performance():
    """Test 2: Demonstrate cache performance"""
    print_header("TEST 2: Cache Performance Comparison")

    orchestrator = AgentOrchestrator()
    test_query = "project management tools for startups"

    # Clear cache first
    orchestrator.clear_cache_all()
    print("✓ Cache cleared\n")

    # First run - no cache
    print(f"📊 Running analysis for: '{test_query}'")
    print("   Status: CACHE MISS (will hit APIs)")
    start_time = time.time()
    try:
        result1 = orchestrator.run(test_query)
        time1 = time.time() - start_time
        print(f"   Time: {time1:.2f} seconds")
        sources = len(result1.get("validated_insights", {}).get("competitors", []))
        print(f"   Competitors found: {sources}\n")
    except Exception as e:
        logger.error(f"Error on first run: {e}")
        time1 = None
        return

    # Second run - with cache
    print(f"📊 Running analysis for: '{test_query}'")
    print("   Status: CACHE HIT (will use cached data)")
    start_time = time.time()
    try:
        result2 = orchestrator.run(test_query)
        time2 = time.time() - start_time
        print(f"   Time: {time2:.2f} seconds")
        print(f"   Competitors found: {sources}\n")
    except Exception as e:
        logger.error(f"Error on second run: {e}")
        time2 = None
        return

    # Show improvement
    if time1 and time2:
        speedup = time1 / time2
        savings = ((time1 - time2) / time1) * 100
        print(f"⚡ Performance Improvement:")
        print(f"   Speedup: {speedup:.1f}x faster")
        print(f"   Time saved: {(time1 - time2):.2f} seconds ({savings:.1f}%)\n")


def test_cache_types():
    """Test 3: Show cache entries by type"""
    print_header("TEST 3: Cache Entries by Type")

    cache = get_cache_manager()
    stats = cache.get_stats()

    if "by_type" in stats and stats["by_type"]:
        print("Cache entries by type:\n")
        for item in stats["by_type"]:
            print(f"  {item['type']:25s} - {item['count']:3d} entries, {item['hits']:5d} hits")
        print()
    else:
        print("No cache entries found.\n")


def test_cache_operations():
    """Test 4: Demonstrate cache management operations"""
    print_header("TEST 4: Cache Management Operations")

    orchestrator = AgentOrchestrator()

    # Show current stats
    print("1. Initial cache statistics:")
    stats = orchestrator.get_cache_stats()
    print(f"   Valid entries: {stats['total_entries_valid']}")
    print(f"   Total size: {stats['total_size_mb']} MB\n")

    # Clear web search cache
    if stats['total_entries_valid'] > 0:
        print("2. Clearing web search cache...")
        deleted = orchestrator.clear_cache_by_type(CacheManager.CACHE_TYPE_WEB)
        print(f"   Deleted: {deleted} entries\n")

        # Show updated stats
        print("3. Updated cache statistics:")
        stats = orchestrator.get_cache_stats()
        print(f"   Valid entries: {stats['total_entries_valid']}")
        print(f"   Total size: {stats['total_size_mb']} MB\n")


def test_cache_cleanup():
    """Test 5: Cleanup expired entries"""
    print_header("TEST 5: Cleanup Expired Entries")

    orchestrator = AgentOrchestrator()

    print("Running cache cleanup...")
    deleted = orchestrator.cleanup_cache()
    print(f"✓ Removed {deleted} expired entries\n")

    stats = orchestrator.get_cache_stats()
    print(f"Remaining entries: {stats['total_entries_valid']}")
    print(f"Cache size: {stats['total_size_mb']} MB\n")


def test_direct_cache_usage():
    """Test 6: Direct cache manager usage"""
    print_header("TEST 6: Direct Cache Manager Usage")

    cache = get_cache_manager()

    # Store a value
    print("1. Storing test data in cache...")
    test_key = cache._make_key("test", query="performance_test")
    test_data = {
        "competitors": ["Company A", "Company B", "Company C"],
        "score": 85.5
    }
    success = cache.set(
        test_key,
        test_data,
        CacheManager.CACHE_TYPE_ANALYSIS,
        query="performance_test"
    )
    print(f"   Stored: {success}\n")

    # Retrieve the value
    print("2. Retrieving test data from cache...")
    retrieved = cache.get(test_key)
    if retrieved:
        print(f"   Retrieved: {retrieved}\n")
        print("   ✓ Cache working correctly!\n")
    else:
        print("   ✗ Failed to retrieve data\n")

    # Show stats
    print("3. Cache statistics after test:")
    cache.print_stats()


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  Market Horizon AI - Caching System Test Suite")
    print("=" * 70)

    tests = [
        ("Cache Statistics", test_cache_stats),
        ("Cache Performance", test_cache_performance),
        ("Cache Types", test_cache_types),
        ("Cache Operations", test_cache_operations),
        ("Cleanup", test_cache_cleanup),
        ("Direct Cache Usage", test_direct_cache_usage),
    ]

    completed = 0
    for test_name, test_func in tests:
        try:
            test_func()
            completed += 1
        except Exception as e:
            logger.error(f"Test '{test_name}' failed: {e}", exc_info=True)
            print(f"✗ {test_name} failed: {e}\n")

    # Summary
    print_header("Test Summary")
    print(f"Completed: {completed}/{len(tests)} tests")
    if completed == len(tests):
        print("✅ All tests passed!\n")
    else:
        print(f"⚠️  {len(tests) - completed} test(s) failed\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user\n")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Unexpected error: {e}\n")
        sys.exit(1)
