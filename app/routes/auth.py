from flask import Blueprint, render_template, request, redirect, url_for, session, flash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    使用者註冊路由。
    輸入：使用者名稱(username)、密碼(password)
    邏輯：
        GET：顯示註冊表單。
        POST：檢查使用者是否存在，若無則進行密碼加密後寫入資料庫 User 表。
    輸出：成功後重導向登入頁面；失敗則重新渲染 templates/auth/register.html 帶有錯誤訊息。
    """
    pass

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    使用者登入路由。
    輸入：使用者名稱(username)、密碼(password)
    邏輯：
        GET：顯示登入表單。
        POST：驗證密碼雜湊，通過後建立 session 登入狀態。
    輸出：成功後重導向首頁；失敗則重新渲染 templates/auth/login.html。
    """
    pass

@bp.route('/logout')
def logout():
    """
    使用者登出路由。
    輸入：無
    邏輯：清除 session 中的所有登入資訊。
    輸出：重導向至首頁大廳。
    """
    pass
