import sqlite3

DB_PATH = "instance/database.db"

class Fortune:
    def __init__(self, id, title, category, poem, description, created_at):
        self.id = id
        self.title = title
        self.category = category
        self.poem = poem
        self.description = description
        self.created_at = created_at

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, title, category, poem, description):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO fortunes (title, category, poem, description) VALUES (?, ?, ?, ?)",
                (title, category, poem, description)
            )
            return cursor.lastrowid

    @classmethod
    def get_all(cls):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortunes")
            return [cls(*row) for row in cursor.fetchall()]

    @classmethod
    def get_by_id(cls, fortune_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortunes WHERE id = ?", (fortune_id,))
            row = cursor.fetchone()
            if row:
                return cls(*row)
            return None

    @classmethod
    def get_random(cls):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortunes ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            if row:
                return cls(*row)
            return None

    @classmethod
    def update(cls, fortune_id, title, category, poem, description):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE fortunes SET title = ?, category = ?, poem = ?, description = ? WHERE id = ?",
                (title, category, poem, description, fortune_id)
            )
            return True

    @classmethod
    def delete(cls, fortune_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fortunes WHERE id = ?", (fortune_id,))
            return True
