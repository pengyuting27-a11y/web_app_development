import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')


def get_db_connection():
    """建立並回傳資料庫連線，使用 Row 工廠讓結果可以用欄位名稱取值"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class History:
    def __init__(self, id, user_id, fortune_id, created_at):
        self.id = id
        self.user_id = user_id
        self.fortune_id = fortune_id
        self.created_at = created_at

    @classmethod
    def create(cls, user_id, fortune_id):
        """
        新增一筆算命歷史紀錄。
        :param user_id: 使用者 id
        :param fortune_id: 抽中的籤詩 id
        :return: 新建立的紀錄 id，若失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO histories (user_id, fortune_id) VALUES (?, ?)",
                (user_id, fortune_id)
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"[History.create] 發生錯誤：{e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有使用者的算命紀錄清單。
        :return: History 物件的 list，若失敗回傳空 list
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM histories ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            return [cls(row['id'], row['user_id'], row['fortune_id'], row['created_at']) for row in rows]
        except Exception as e:
            print(f"[History.get_all] 發生錯誤：{e}")
            return []

    @classmethod
    def get_by_id(cls, history_id):
        """
        依照 id 取得單一筆算命紀錄。
        :param history_id: 紀錄 id
        :return: History 物件，若找不到回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM histories WHERE id = ?", (history_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return cls(row['id'], row['user_id'], row['fortune_id'], row['created_at'])
            return None
        except Exception as e:
            print(f"[History.get_by_id] 發生錯誤：{e}")
            return None

    @classmethod
    def get_by_user_id(cls, user_id):
        """
        取得特定使用者的所有算命紀錄，並 JOIN 籤詩資料表以取得標題與吉凶。
        :param user_id: 使用者 id
        :return: sqlite3.Row 物件的 list（含籤詩欄位），若失敗回傳空 list
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT h.id, h.user_id, h.fortune_id, h.created_at,
                       f.title AS fortune_title, f.category AS fortune_category
                FROM histories h
                JOIN fortunes f ON h.fortune_id = f.id
                WHERE h.user_id = ?
                ORDER BY h.created_at DESC
                """,
                (user_id,)
            )
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            print(f"[History.get_by_user_id] 發生錯誤：{e}")
            return []

    @classmethod
    def delete(cls, history_id):
        """
        刪除一筆算命紀錄。
        :param history_id: 要刪除的紀錄 id
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM histories WHERE id = ?", (history_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[History.delete] 發生錯誤：{e}")
            return False
