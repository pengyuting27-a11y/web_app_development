from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# 假設之後有 login_required 防護功能
# from app.utils.auth import login_required

bp = Blueprint('fortune', __name__, url_prefix='/fortune')

@bp.route('/')
# @login_required
def index():
    """
    算命與抽籤頁面的準備入口。
    輸入：無
    邏輯：直接進入即可看見求神問卜的視覺特效與頁面。需為登入狀態。
    輸出：渲染 templates/fortune/index.html。
    """
    pass

@bp.route('/draw', methods=['POST'])
# @login_required
def draw():
    """
    執行抽隨機籤的邏輯。
    輸入：無 (只需 POST 請求即可觸發)
    邏輯：
        使用 Fortune.get_random() 取出一筆籤詩。
        讀取使用者的 session id。
        使用 History.create() 紀錄該筆抽籤過程。
    輸出：重導向至 /fortune/result/<id> 以顯示詳細的籤詩及占卜建議。
    """
    pass

@bp.route('/result/<int:id>')
# @login_required
def result(id):
    """
    顯示由 draw 求得的籤詩詳細解說。
    輸入：URL路徑變數 id (可以為 History id 或 Fortune id)
    邏輯：依據 ID 到資料庫抓取所對應的整首籤詩、吉凶類別及解文內容。
    輸出：渲染 templates/fortune/result.html。
    """
    pass
