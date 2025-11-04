"""
Cache Management CLI - Command-line interface for managing the cache

Commands:
    python -m utils.cache_cli stats          - Show cache statistics
    python -m utils.cache_cli clear          - Clear entire cache
    python -m utils.cache_cli clear-type     - Clear cache by type
    python -m utils.cache_cli clear-query    - Clear cache by query
    python -m utils.cache_cli cleanup        - Remove expired entries
    python -m utils.cache_cli help           - Show help
"""

import sys
import argparse
import logging
from utils.cache_manager import get_cache_manager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def cmd_stats(args):
    """Show cache statistics"""
    cache = get_cache_manager()
    cache.print_stats()


def cmd_clear(args):
    """Clear entire cache"""
    cache = get_cache_manager()

    if not args.force:
        response = input(
            "⚠️  WARNING: This will clear all cached data!\n"
            "Type 'yes' to confirm: "
        )
        if response.lower() != 'yes':
            print("❌ Cache clear cancelled")
            return

    deleted = cache.clear_all()
    print(f"✅ Cleared {deleted} cache entries")


def cmd_clear_type(args):
    """Clear cache by type"""
    cache = get_cache_manager()

    if not args.cache_type:
        print("Available cache types:")
        types = [
            cache.CACHE_TYPE_WEB,
            cache.CACHE_TYPE_TRENDS,
            cache.CACHE_TYPE_REDDIT,
            cache.CACHE_TYPE_ANALYSIS,
            cache.CACHE_TYPE_STRATEGY,
            cache.CACHE_TYPE_QUALITY,
        ]
        for ct in types:
            print(f"  - {ct}")
        print("\nUsage: python -m utils.cache_cli clear-type --type <cache_type>")
        return

    deleted = cache.delete_by_type(args.cache_type)
    print(f"✅ Deleted {deleted} cache entries of type '{args.cache_type}'")


def cmd_clear_query(args):
    """Clear cache by query"""
    if not args.query:
        print("Usage: python -m utils.cache_cli clear-query --query '<your_query>'")
        return

    cache = get_cache_manager()
    deleted = cache.delete_by_query(args.query)
    print(f"✅ Deleted {deleted} cache entries for query '{args.query}'")


def cmd_cleanup(args):
    """Remove expired cache entries"""
    cache = get_cache_manager()
    deleted = cache.cleanup_expired()
    print(f"✅ Cleanup removed {deleted} expired cache entries")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Cache Management CLI for Market Horizon AI',
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show cache statistics')
    stats_parser.set_defaults(func=cmd_stats)

    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear entire cache')
    clear_parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Skip confirmation prompt'
    )
    clear_parser.set_defaults(func=cmd_clear)

    # Clear by type command
    clear_type_parser = subparsers.add_parser(
        'clear-type',
        help='Clear cache by type'
    )
    clear_type_parser.add_argument(
        '--type',
        dest='cache_type',
        help='Cache type to clear'
    )
    clear_type_parser.set_defaults(func=cmd_clear_type)

    # Clear by query command
    clear_query_parser = subparsers.add_parser(
        'clear-query',
        help='Clear cache by query'
    )
    clear_query_parser.add_argument(
        '--query', '-q',
        dest='query',
        help='Query to clear from cache'
    )
    clear_query_parser.set_defaults(func=cmd_clear_query)

    # Cleanup command
    cleanup_parser = subparsers.add_parser(
        'cleanup',
        help='Remove expired cache entries'
    )
    cleanup_parser.set_defaults(func=cmd_cleanup)

    # Help command
    help_parser = subparsers.add_parser('help', help='Show this help message')

    # Parse arguments
    args = parser.parse_args()

    if args.command is None or args.command == 'help':
        parser.print_help()
        sys.exit(0)

    # Execute command
    try:
        args.func(args)
    except Exception as e:
        logger.error(f"Error executing command: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
