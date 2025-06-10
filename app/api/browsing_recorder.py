import mysql.connector
from typing import Dict, Any, Optional
from datetime import datetime
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, ROOT_CATEGORIES

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
        """Create tables if they don't exist."""
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
                    summary TEXT,
                    scroll_depth FLOAT,
                    visit_start DATETIME,
                    visit_end DATETIME,
                    keywords TEXT,
                    search_query TEXT,
                    PRIMARY KEY (id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS root_categories (
                    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                    name VARCHAR(255) UNIQUE,
                    PRIMARY KEY (id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sub_categories (
                    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                    root_id BIGINT UNSIGNED NOT NULL,
                    name VARCHAR(255),
                    PRIMARY KEY (id),
                    FOREIGN KEY (root_id) REFERENCES root_categories(id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS log_sub_categories (
                    log_id BIGINT UNSIGNED NOT NULL,
                    sub_id BIGINT UNSIGNED NOT NULL,
                    PRIMARY KEY (log_id, sub_id),
                    FOREIGN KEY (log_id) REFERENCES browsing_logs(id),
                    FOREIGN KEY (sub_id) REFERENCES sub_categories(id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            # insert root categories if table empty
            cursor.execute("SELECT COUNT(*) FROM root_categories")
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.executemany(
                    "INSERT INTO root_categories(name) VALUES (%s)",
                    [(name,) for name in ROOT_CATEGORIES]
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
                    summary,
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
                data.get('summary'),
                scroll_depth,
                self._parse_datetime(data.get('visit_start')),
                self._parse_datetime(data.get('visit_end')),
                keywords,
                data.get('search_query')
            )
            cursor.execute(query, values)
            log_id = cursor.lastrowid
            labels = data.get('labels', [])
            for label in labels:
                root_name = label.get('root')
                sub_name = label.get('sub')
                if not root_name or not sub_name:
                    continue
                cursor.execute(
                    "SELECT id FROM root_categories WHERE name=%s", (root_name,)
                )
                root_row = cursor.fetchone()
                if not root_row:
                    continue
                root_id = root_row[0]
                cursor.execute(
                    "SELECT id FROM sub_categories WHERE root_id=%s AND name=%s",
                    (root_id, sub_name),
                )
                row = cursor.fetchone()
                if row:
                    sub_id = row[0]
                else:
                    cursor.execute(
                        "INSERT INTO sub_categories(root_id, name) VALUES (%s,%s)",
                        (root_id, sub_name),
                    )
                    sub_id = cursor.lastrowid
                cursor.execute(
                    "INSERT IGNORE INTO log_sub_categories(log_id, sub_id) VALUES (%s,%s)",
                    (log_id, sub_id),
                )
            conn.commit()
            print("[✓] Inserted browsing log")
        except mysql.connector.Error as err:
            print(f"[✗] MySQL Error: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
