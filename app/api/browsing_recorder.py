import mysql.connector
from typing import Dict, Any, Optional
from datetime import datetime
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

class BrowsingRecorder:
    """Receive browsing data from Chrome extension and store it in MySQL."""

    def __init__(self):
        self.config = {
            'host': DB_HOST,
            'user': DB_USER,
            'password': DB_PASSWORD,
            'database': DB_NAME,
            'port': DB_PORT,
            'charset': 'utf8mb4'
        }
        self._ensure_table()

    def _ensure_table(self) -> None:
        """Create browsing_logs table if it doesn't exist."""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS browsing_logs (
                    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                    user_id VARCHAR(255),
                    session_id VARCHAR(255),
                    url TEXT,
                    title TEXT,
                    body_text LONGTEXT,
                    scroll_depth FLOAT,
                    visit_start DATETIME,
                    visit_end DATETIME,
                    keywords TEXT,
                    search_query TEXT,
                    PRIMARY KEY (id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            conn.commit()
        except mysql.connector.Error as err:
            print(f"[✗] MySQL Error: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _parse_datetime(self, value: Optional[str]) -> Optional[datetime]:
        """Convert ISO8601 string to naive datetime for MySQL."""
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00')).replace(tzinfo=None)
        except ValueError:
            return None

    def insert_action(self, data: Dict[str, Any]) -> None:
        """Insert browsing action data into browsing_logs table."""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            query = """
                INSERT INTO browsing_logs (
                    user_id,
                    session_id,
                    url,
                    title,
                    body_text,
                    scroll_depth,
                    visit_start,
                    visit_end,
                    keywords,
                    search_query
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            keywords = data.get('keywords')
            if isinstance(keywords, list):
                keywords = ','.join(keywords)

            scroll_depth = data.get('scroll_depth')
            if scroll_depth is None:
                scroll_depth = data.get('scrollDepth')
            try:
                scroll_depth = float(scroll_depth) if scroll_depth is not None else None
            except (ValueError, TypeError):
                scroll_depth = None

            values = (
                data.get('user_id'),
                data.get('session_id'),
                data.get('url'),
                data.get('title'),
                data.get('text'),
                scroll_depth,
                self._parse_datetime(data.get('visit_start')),
                self._parse_datetime(data.get('visit_end')),
                keywords,
                data.get('search_query')
            )
            cursor.execute(query, values)
            conn.commit()
            print("[✓] Inserted browsing log")
        except mysql.connector.Error as err:
            print(f"[✗] MySQL Error: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
