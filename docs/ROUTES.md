# 路由設計 — ROUTES

根據產品需求、系統架構與流程圖，本文件定義了線上算命系統所有的路由規則、詳細的輸入輸出邏輯，以及渲染用之 Jinja2 模板清單。

## 1. 路由總覽表格

| 功能模組 | 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **首頁 (main)** | 網站首頁 | GET | `/` | `templates/index.html` | 網站首頁入口，包含功能導覽 |
| **會員 (auth)** | 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 呈現註冊表單 |
| **會員 (auth)** | 執行註冊 | POST | `/auth/register` | — | 寫入資料表，成功後重導向登入頁 |
| **會員 (auth)** | 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 呈現登入表單 |
| **會員 (auth)** | 執行登入 | POST | `/auth/login` | — | 驗證使用者的帳號密碼並發放 Session |
| **會員 (auth)** | 取消登入 | GET | `/auth/logout` | — | 刪除登入 Session 並重導回首頁 |
| **算命 (fortune)**| 抽籤入口 | GET | `/fortune/` | `templates/fortune/index.html` | 呈現準備抽籤的準備畫面、互動元件 |
| **算命 (fortune)**| 執行抽籤 | POST | `/fortune/draw` | — | 處理抽籤邏輯、寫入紀錄，並重導向詳細結果頁 |
| **算命 (fortune)**| 籤詩結果 | GET | `/fortune/result/<id>`| `templates/fortune/result.html`| 根據傳入的 id，顯示求得的籤詩解說 |
| **歷史 (history)**| 個人紀錄 | GET | `/history/` | `templates/history/index.html`| 從 DB 撈出過往紀錄並條列呈現 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁 (main)
- **URL**: `/`
- **輸入**: 無
- **處理邏輯**: 單純返回首頁畫面。若已登入可於 UI 顯示使用者名稱。
- **輸出**: 渲染 `index.html`

### 2.2 會員模組 (auth)
#### /auth/register
- **輸入**: 
  - `GET`: 無
  - `POST`: 表單的 `username` 與 `password` (與 `confirm_password`)
- **處理邏輯**: 
  - 驗證密碼是否一致。檢查使用者是否已存在。密碼進行雜湊後呼叫 `User.create` 寫入。
- **輸出**: 
  - 成功：重導向至 `/auth/login`，跳出「註冊成功」通知。
  - 失敗/尚未提交：渲染 `auth/register.html`。
- **錯誤處理**: 遇到使用者已存在時，回傳相應錯誤訊息至畫面上。

#### /auth/login
- **輸入**: 
  - `GET`: 無
  - `POST`: `username` 和 `password`
- **處理邏輯**: 呼叫 `User.get_by_username`，驗證密碼是否符合雜湊值。建立登入 session。
- **輸出**: 
  - 成功：重導向 `/` 或 `/fortune/`
  - 失敗：重新渲染 `auth/login.html` 並顯示錯誤訊息
- **錯誤處理**: 若帳戶不存在或密碼錯誤顯示「登入失敗」。

#### /auth/logout
- **輸入**: 無
- **處理邏輯**: 清除 `session.clear()` 內的所有登入狀態。
- **輸出**: 重導回首頁 `/`

### 2.3 算命模組 (fortune)
#### /fortune/
- **輸入**: 無
- **處理邏輯**: 檢查是否登入 (使用修飾器 `@login_required`)，若已登入則可進入抽籤系統介面。
- **輸出**: 渲染 `fortune/index.html`。

#### /fortune/draw
- **輸入**: 通常為表單提交的隱藏參數或按鈕 POST。
- **處理邏輯**: 
  1. 呼叫 `Fortune.get_random()` 從題庫中隨機拿取一筆紀錄。
  2. 提取當前使用者的 `user_id`。
  3. 呼叫 `History.create(user_id, fortune.id)` 留存紀錄。
- **輸出**: 重導向至 `/fortune/result/<紀錄的id 或 籤詩id>`。

#### /fortune/result/<id>
- **輸入**: URL 參數 `id`
- **處理邏輯**: 呼叫 `History.get_by_id(id)` 確保資料存在，並提取關聯的籤詩內容，組合出該籤的 `title`, `poem`, 與 `description` 等。
- **輸出**: 渲染 `fortune/result.html` 給予神明解答。
- **錯誤處理**: 若 `id` 不存在或是別人帳號的紀錄，則返回 404 及對應錯誤提示。

### 2.4 歷史模組 (history)
#### /history/
- **輸入**: 無
- **處理邏輯**: 檢查登入。依照 `session['user_id']` 呼叫 `History.get_by_user_id` 抓出清單，並順道 JOIN 回相關的名稱與日期。
- **輸出**: 渲染 `history/index.html`。

---

## 3. Jinja2 模板清單

所有的 HTML 模板檔案都會繼承從 `base.html` 基礎框架：

- `templates/base.html`: 共同框架，包含 `<header>`, `<nav>`, `<footer>`，以及警示訊息列。
- `templates/index.html`: 首頁大廳內容介紹。
- `templates/auth/login.html`: 會員登入畫面。
- `templates/auth/register.html`: 會員註冊畫面。
- `templates/fortune/index.html`: 裝載可互動求籤按鈕、籤筒動畫的入口。
- `templates/fortune/result.html`: 細緻排版後的解籤詩頁並帶有分享按鈕。
- `templates/history/index.html`: 條列顯示個人抽籤時間、抽中吉凶籤的表格。
