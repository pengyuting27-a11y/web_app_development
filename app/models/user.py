import sqlite3
import os

DB_PATH = os.path.join('instance', 'database.db')


def get_db_connection():
    """建立並回傳資料庫連線，使用 Row 工廠讓結果可以用欄位名稱取值"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class User:
    def __init__(self, id, username, password_hash, created_at):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at

    @classmethod
    def create(cls, username, password_hash):
        """
        新增一位使用者。
        :param username: 使用者帳號 (必須唯一)
        :param password_hash: 已雜湊的密碼
        :return: 新建立的使用者 id，若失敗回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except sqlite3.IntegrityError:
            # 使用者名稱重複
            return None
        except Exception as e:
            print(f"[User.create] 發生錯誤：{e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有使用者清單。
        :return: User 物件的 list，若失敗回傳空 list
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            return [cls(row['id'], row['username'], row['password_hash'], row['created_at']) for row in rows]
        except Exception as e:
            print(f"[User.get_all] 發生錯誤：{e}")
            return []

    @classmethod
    def get_by_id(cls, user_id):
        """
        依照 id 取得單一使用者。
        :param user_id: 使用者的 id
        :return: User 物件，若找不到回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return cls(row['id'], row['username'], row['password_hash'], row['created_at'])
            return None
        except Exception as e:
            print(f"[User.get_by_id] 發生錯誤：{e}")
            return None

    @classmethod
    def get_by_username(cls, username):
        """
        依照使用者名稱查詢使用者，用於登入驗證。
        :param username: 使用者帳號
        :return: User 物件，若找不到回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return cls(row['id'], row['username'], row['password_hash'], row['created_at'])
            return None
        except Exception as e:
            print(f"[User.get_by_username] 發生錯誤：{e}")
            return None

    @classmethod
    def update(cls, user_id, username=None, password_hash=None):
        """
        更新使用者資料。
        :param user_id: 要更新的使用者 id
        :param username: 新的使用者名稱 (可選)
        :param password_hash: 新的雜湊密碼 (可選)
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if username:
                cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
            if password_hash:
                cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[User.update] 發生錯誤：{e}")
            return False

    @classmethod
    def delete(cls, user_id):
        """
        刪除一位使用者（連帶刪除相關的歷史紀錄）。
        :param user_id: 要刪除的使用者 id
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[User.delete] 發生錯誤：{e}")
            return False
