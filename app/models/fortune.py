import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')


def get_db_connection():
    """建立並回傳資料庫連線，使用 Row 工廠讓結果可以用欄位名稱取值"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class Fortune:
    def __init__(self, id, title, category, poem, description, created_at):
        self.id = id
        self.title = title
        self.category = category
        self.poem = poem
        self.description = description
        self.created_at = created_at

    @classmethod
    def create(cls, title, category, poem, description):
        """
        新增一筆籤詩到題庫中。
        :param title: 籤詩標題，例如「第三十二籤」
        :param category: 吉凶類別，例如「大吉」、「下下籤」
        :param poem: 籤詩原文
        :param description: 白話解析內容
        :return: 新建立的籤詩 id，若失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO fortunes (title, category, poem, description) VALUES (?, ?, ?, ?)",
                (title, category, poem, description)
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"[Fortune.create] 發生錯誤：{e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有籤詩清單。
        :return: Fortune 物件的 list，若失敗回傳空 list
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortunes ORDER BY id ASC")
            rows = cursor.fetchall()
            conn.close()
            return [cls(row['id'], row['title'], row['category'], row['poem'], row['description'], row['created_at']) for row in rows]
        except Exception as e:
            print(f"[Fortune.get_all] 發生錯誤：{e}")
            return []

    @classmethod
    def get_by_id(cls, fortune_id):
        """
        依照 id 取得單一籤詩。
        :param fortune_id: 籤詩 id
        :return: Fortune 物件，若找不到回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortunes WHERE id = ?", (fortune_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return cls(row['id'], row['title'], row['category'], row['poem'], row['description'], row['created_at'])
            return None
        except Exception as e:
            print(f"[Fortune.get_by_id] 發生錯誤：{e}")
            return None

    @classmethod
    def get_random(cls):
        """
        從題庫中隨機取出一筆籤詩，用於抽籤功能。
        :return: Fortune 物件，若題庫為空回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fortunes ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            conn.close()
            if row:
                return cls(row['id'], row['title'], row['category'], row['poem'], row['description'], row['created_at'])
            return None
        except Exception as e:
            print(f"[Fortune.get_random] 發生錯誤：{e}")
            return None

    @classmethod
    def update(cls, fortune_id, title, category, poem, description):
        """
        更新一筆籤詩的內容。
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE fortunes SET title = ?, category = ?, poem = ?, description = ? WHERE id = ?",
                (title, category, poem, description, fortune_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[Fortune.update] 發生錯誤：{e}")
            return False

    @classmethod
    def delete(cls, fortune_id):
        """
        刪除一筆籤詩。
        :param fortune_id: 要刪除的籤詩 id
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fortunes WHERE id = ?", (fortune_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[Fortune.delete] 發生錯誤：{e}")
            return False
