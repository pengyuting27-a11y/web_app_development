from flask import Blueprint, render_template, request, redirect, url_for, session

# 假設之後會有一個登入防護
# from app.utils.auth import login_required

bp = Blueprint('history', __name__, url_prefix='/history')

@bp.route('/')
# @login_required
def index():
    """
    使用者查閱過往自身的所有測算紀錄。
    輸入：無
    邏輯：依據 session 中之 user_id 呼叫 History.get_by_user_id 取得所有清單。並組合關連之籤詩標題顯示。
    輸出：渲染 templates/history/index.html。
    """
    pass
