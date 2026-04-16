import sqlite3

DB_PATH = "instance/database.db"

class History:
    def __init__(self, id, user_id, fortune_id, created_at):
        self.id = id
        self.user_id = user_id
        self.fortune_id = fortune_id
        self.created_at = created_at

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, user_id, fortune_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO histories (user_id, fortune_id) VALUES (?, ?)",
                (user_id, fortune_id)
            )
            return cursor.lastrowid

    @classmethod
    def get_all(cls):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM histories")
            return [cls(*row) for row in cursor.fetchall()]

    @classmethod
    def get_by_id(cls, history_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM histories WHERE id = ?", (history_id,))
            row = cursor.fetchone()
            if row:
                return cls(*row)
            return None

    @classmethod
    def get_by_user_id(cls, user_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM histories WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
            return [cls(*row) for row in cursor.fetchall()]

    @classmethod
    def delete(cls, history_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM histories WHERE id = ?", (history_id,))
            return True
