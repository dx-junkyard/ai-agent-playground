import mysql.connector

class MessageRepository:
    def __init__(self):
        self.config = {
            'host': 'db',
            'user': 'me',
            'password': 'me',
            'database': 'mydb',
            'port': 3306,
            'charset': 'utf8mb4'
        }

    def insert_message(self, user_id, message):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()

            query = """
                INSERT INTO user_messages (user_id, message)
                VALUES (%s, %s)
            """
            values = (user_id, message)
            cursor.execute(query, values)
            conn.commit()

            print(f"[✓] Inserted user_messages for user_id={user_id}")

        except mysql.connector.Error as err:
            print(f"[✗] MySQL Error: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_user_messages(self, limit=10):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
    
    
            # 結果格納用
            user_messages = {}
    
            cursor.execute("""
                SELECT message, msg_cate, msg_type
                FROM user_messages
                WHERE user_id = %s
                ORDER BY id DESC
                LIMIT 100
            """, (user_id,))
            user_messages[user_id] = cursor.fetchall()
    
            return user_messages
    
        except mysql.connector.Error as err:
            print(f"[✗] MySQL Error: {err}")
            return {}
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

