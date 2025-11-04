"""
SQLite-based Cache Manager for Market Horizon AI

Features:
- Persistent SQLite caching
- TTL (Time-To-Live) support
- Cache statistics and monitoring
- Multiple cache types (web, trends, reddit, analysis, etc.)
- Automatic cache cleanup
- Thread-safe operations
- Detailed logging and metrics
"""

import sqlite3
import json
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional, Dict, List
from contextlib import contextmanager
import threading

logger = logging.getLogger(__name__)


class CacheManager:
    """SQLite-based cache manager with TTL support"""

    # Cache types
    CACHE_TYPE_WEB = "web_search"
    CACHE_TYPE_TRENDS = "google_trends"
    CACHE_TYPE_REDDIT = "reddit_discussions"
    CACHE_TYPE_ANALYSIS = "analysis_results"
    CACHE_TYPE_STRATEGY = "strategy_results"
    CACHE_TYPE_QUALITY = "quality_results"

    # Default TTL (in hours)
    DEFAULT_TTLS = {
        CACHE_TYPE_WEB: 7 * 24,      # 7 days for web search
        CACHE_TYPE_TRENDS: 24,        # 1 day for trends
        CACHE_TYPE_REDDIT: 14 * 24,   # 14 days for reddit
        CACHE_TYPE_ANALYSIS: 7 * 24,  # 7 days for analysis
        CACHE_TYPE_STRATEGY: 7 * 24,  # 7 days for strategy
        CACHE_TYPE_QUALITY: 7 * 24,   # 7 days for quality
    }

    def __init__(self, db_path: str = "data/cache.db", auto_cleanup: bool = True):
        """
        Initialize cache manager

        Args:
            db_path: Path to SQLite database
            auto_cleanup: Automatically clean expired entries
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

        # Initialize database
        self._init_db()

        # Statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "writes": 0,
            "deletes": 0,
            "errors": 0
        }

        if auto_cleanup:
            self.cleanup_expired()

        logger.info(f"Cache Manager initialized with database at {self.db_path}")

    def _init_db(self):
        """Initialize SQLite database and create tables"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Create cache table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cache (
                        key TEXT PRIMARY KEY,
                        cache_type TEXT NOT NULL,
                        value TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP NOT NULL,
                        hits INTEGER DEFAULT 0,
                        metadata TEXT,
                        query TEXT
                    )
                """)

                # Create index on expires_at for efficient cleanup
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_expires_at
                    ON cache(expires_at)
                """)

                # Create index on cache_type for type-based queries
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_cache_type
                    ON cache(cache_type)
                """)

                # Create index on query for search
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_query
                    ON cache(query)
                """)

                # Create statistics table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cache_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        operation TEXT NOT NULL,
                        cache_type TEXT,
                        status TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        details TEXT
                    )
                """)

                conn.commit()
                logger.debug("Cache database initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize cache database: {e}")
            self.stats["errors"] += 1
            raise

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    @staticmethod
    def _make_key(*args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_parts = [str(arg) for arg in args] + [f"{k}={v}" for k, v in sorted(kwargs.items())]
        key_str = "|".join(key_parts)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, key: str, cache_type: str = None) -> Optional[Any]:
        """
        Retrieve value from cache

        Args:
            key: Cache key
            cache_type: Optional cache type for validation

        Returns:
            Cached value or None if not found/expired
        """
        try:
            with self._lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()

                    # Get value if not expired
                    query = "SELECT value, hits FROM cache WHERE key = ? AND expires_at > ?"
                    params = [key, datetime.now()]

                    if cache_type:
                        query += " AND cache_type = ?"
                        params.append(cache_type)

                    cursor.execute(query, params)
                    row = cursor.fetchone()

                    if row:
                        # Update hit count
                        cursor.execute(
                            "UPDATE cache SET hits = hits + 1 WHERE key = ?",
                            [key]
                        )
                        conn.commit()

                        self.stats["hits"] += 1
                        logger.debug(f"Cache HIT for key: {key}")

                        try:
                            return json.loads(row[0])
                        except (json.JSONDecodeError, TypeError):
                            logger.warning(f"Failed to decode cache value for key: {key}")
                            return None
                    else:
                        self.stats["misses"] += 1
                        logger.debug(f"Cache MISS for key: {key}")
                        return None

        except Exception as e:
            logger.error(f"Error retrieving cache for key {key}: {e}")
            self.stats["errors"] += 1
            return None

    def set(
        self,
        key: str,
        value: Any,
        cache_type: str,
        ttl_hours: int = None,
        query: str = None,
        metadata: Dict = None
    ) -> bool:
        """
        Store value in cache

        Args:
            key: Cache key
            value: Value to cache
            cache_type: Type of cache (web, trends, etc.)
            ttl_hours: Time-to-live in hours (uses default if not specified)
            query: Optional query string for tracking
            metadata: Optional metadata dict

        Returns:
            True if successful, False otherwise
        """
        try:
            # Use default TTL if not specified
            if ttl_hours is None:
                ttl_hours = self.DEFAULT_TTLS.get(cache_type, 24)

            expires_at = datetime.now() + timedelta(hours=ttl_hours)
            json_value = json.dumps(value)

            metadata_json = json.dumps(metadata) if metadata else None

            with self._lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO cache
                        (key, cache_type, value, expires_at, query, metadata)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        [key, cache_type, json_value, expires_at, query, metadata_json]
                    )
                    conn.commit()

            self.stats["writes"] += 1
            logger.debug(
                f"Cache SET for key: {key} (type: {cache_type}, TTL: {ttl_hours}h)"
            )
            return True

        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {e}")
            self.stats["errors"] += 1
            return False

    def delete(self, key: str) -> bool:
        """
        Delete specific cache entry

        Args:
            key: Cache key to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            with self._lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM cache WHERE key = ?", [key])
                    conn.commit()

            self.stats["deletes"] += 1
            logger.debug(f"Cache DELETED for key: {key}")
            return True

        except Exception as e:
            logger.error(f"Error deleting cache for key {key}: {e}")
            self.stats["errors"] += 1
            return False

    def delete_by_type(self, cache_type: str) -> int:
        """
        Delete all cache entries of specific type

        Args:
            cache_type: Type of cache to delete

        Returns:
            Number of entries deleted
        """
        try:
            with self._lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM cache WHERE cache_type = ?", [cache_type])
                    conn.commit()
                    deleted = cursor.rowcount

            self.stats["deletes"] += deleted
            logger.info(f"Deleted {deleted} cache entries of type: {cache_type}")
            return deleted

        except Exception as e:
            logger.error(f"Error deleting cache by type {cache_type}: {e}")
            self.stats["errors"] += 1
            return 0

    def delete_by_query(self, query: str) -> int:
        """
        Delete all cache entries for specific query

        Args:
            query: Query string to delete

        Returns:
            Number of entries deleted
        """
        try:
            with self._lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM cache WHERE query = ?", [query])
                    conn.commit()
                    deleted = cursor.rowcount

            self.stats["deletes"] += deleted
            logger.info(f"Deleted {deleted} cache entries for query: {query}")
            return deleted

        except Exception as e:
            logger.error(f"Error deleting cache by query {query}: {e}")
            self.stats["errors"] += 1
            return 0

    def clear_all(self) -> int:
        """
        Clear entire cache

        Returns:
            Number of entries deleted
        """
        try:
            with self._lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM cache")
                    conn.commit()
                    deleted = cursor.rowcount

            self.stats["deletes"] += deleted
            logger.warning(f"Cleared entire cache: {deleted} entries deleted")
            return deleted

        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            self.stats["errors"] += 1
            return 0

    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries

        Returns:
            Number of entries deleted
        """
        try:
            with self._lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM cache WHERE expires_at < ?",
                        [datetime.now()]
                    )
                    conn.commit()
                    deleted = cursor.rowcount

            if deleted > 0:
                logger.info(f"Cleanup removed {deleted} expired cache entries")
            return deleted

        except Exception as e:
            logger.error(f"Error during cache cleanup: {e}")
            self.stats["errors"] += 1
            return 0

    def get_stats(self) -> Dict:
        """
        Get cache statistics

        Returns:
            Dictionary with cache statistics
        """
        try:
            with self._lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()

                    # Count total entries
                    cursor.execute("SELECT COUNT(*) FROM cache WHERE expires_at > ?", [datetime.now()])
                    total_valid = cursor.fetchone()[0]

                    # Count all entries
                    cursor.execute("SELECT COUNT(*) FROM cache")
                    total_all = cursor.fetchone()[0]

                    # Get size
                    cursor.execute("SELECT SUM(LENGTH(value)) FROM cache")
                    total_size = cursor.fetchone()[0] or 0

                    # Get by type
                    cursor.execute("""
                        SELECT cache_type, COUNT(*), SUM(hits)
                        FROM cache
                        WHERE expires_at > ?
                        GROUP BY cache_type
                    """, [datetime.now()])
                    by_type = cursor.fetchall()

            hit_rate = (
                (self.stats["hits"] / (self.stats["hits"] + self.stats["misses"]) * 100)
                if (self.stats["hits"] + self.stats["misses"]) > 0
                else 0
            )

            return {
                "stats": self.stats,
                "hit_rate": f"{hit_rate:.2f}%",
                "total_entries_valid": total_valid,
                "total_entries_all": total_all,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "by_type": [
                    {
                        "type": row[0],
                        "count": row[1],
                        "hits": row[2] or 0
                    }
                    for row in by_type
                ]
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"error": str(e)}

    def print_stats(self):
        """Print formatted cache statistics"""
        stats = self.get_stats()

        if "error" in stats:
            print(f"Error retrieving stats: {stats['error']}")
            return

        print("\n" + "=" * 60)
        print("CACHE STATISTICS")
        print("=" * 60)

        s = stats["stats"]
        print(f"\nOperations:")
        print(f"  Hits:       {s['hits']:,}")
        print(f"  Misses:     {s['misses']:,}")
        print(f"  Hit Rate:   {stats['hit_rate']}")
        print(f"  Writes:     {s['writes']:,}")
        print(f"  Deletes:    {s['deletes']:,}")
        print(f"  Errors:     {s['errors']:,}")

        print(f"\nStorage:")
        print(f"  Valid Entries:  {stats['total_entries_valid']:,}")
        print(f"  Total Entries:  {stats['total_entries_all']:,}")
        print(f"  Size:           {stats['total_size_mb']} MB ({stats['total_size_bytes']:,} bytes)")

        if stats["by_type"]:
            print(f"\nBy Type:")
            for item in stats["by_type"]:
                print(f"  {item['type']:20s} - {item['count']:4d} entries, {item['hits']:,} hits")

        print("=" * 60 + "\n")


# Global cache manager instance
_cache_manager = None


def get_cache_manager(db_path: str = "data/cache.db") -> CacheManager:
    """Get or create global cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager(db_path=db_path)
    return _cache_manager
