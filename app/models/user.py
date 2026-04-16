import sqlite3

DB_PATH = "instance/database.db"

class User:
    def __init__(self, id, username, password_hash, created_at):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, username, password_hash):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            return cursor.lastrowid

    @classmethod
    def get_by_id(cls, user_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return cls(*row)
            return None

    @classmethod
    def get_by_username(cls, username):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return cls(*row)
            return None

    @classmethod
    def update(cls, user_id, username=None, password_hash=None):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            if username:
                cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
            if password_hash:
                cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
            return True

    @classmethod
    def delete(cls, user_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return True
