import json
import os
import sqlite3
from datetime import datetime


class QueryHistory:
    def __init__(self, db_path: str = "data/history.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                confidence_score FLOAT,
                num_competitors INT,
                processing_time INT,
                result_json TEXT
            )
            """
        )
        self.conn.commit()

    def save_query(self, query: str, result: dict):
        metadata = result.get("report_metadata", {})
        self.conn.execute(
            """
            INSERT INTO queries 
            (query, timestamp, confidence_score, num_competitors, processing_time, result_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                query,
                datetime.now(),
                metadata.get("confidence_score"),
                len(result.get("validated_insights", {}).get("competitors", [])),
                metadata.get("processing_time_seconds"),
                json.dumps(result),
            ),
        )
        self.conn.commit()

    def get_recent_queries(self, limit: int = 10):
        cursor = self.conn.execute(
            """
            SELECT id, query, timestamp, confidence_score, num_competitors
            FROM queries
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()

    def get_query_by_id(self, query_id: int) -> dict | None:
        cursor = self.conn.execute(
            """
            SELECT query, result_json FROM queries WHERE id = ?
            """,
            (query_id,),
        )
        row = cursor.fetchone()
        if row:
            result = json.loads(row[1])
            # Add the original query text to the result
            result["query_text"] = row[0]
            return result
        return None
    
    def get_latest_result(self) -> dict | None:
        """Get the most recent query result"""
        cursor = self.conn.execute(
            """
            SELECT query, result_json FROM queries 
            ORDER BY timestamp DESC 
            LIMIT 1
            """
        )
        row = cursor.fetchone()
        if row:
            result = json.loads(row[1])
            result["query_text"] = row[0]
            return result
        return None


