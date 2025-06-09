import mysql.connector
from typing import Dict, Any
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
            values = (
                data.get('user_id'),
                data.get('session_id'),
                data.get('url'),
                data.get('title'),
                data.get('text'),
                data.get('scroll_depth'),
                data.get('visit_start'),
                data.get('visit_end'),
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
