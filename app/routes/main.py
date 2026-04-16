from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    網站的入口首頁。
    輸入：無
    邏輯：直接返回首頁。首頁可顯示功能簡介或引導抽籤的行動呼籲。
    輸出：渲染 templates/index.html
    """
    pass
