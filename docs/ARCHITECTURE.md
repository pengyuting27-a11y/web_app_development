# 系統架構設計文件：線上算命系統

## 1. 技術架構說明
- **選用技術與原因**：
  - **後端 (Python + Flask)**：Flask 是一個輕量且靈活的 Web 框架，學習曲線平緩且容易上手。它擁有豐富的生態系可以滿足會員系統、各種自訂路由等需求，適合快速打造產品 MVP。
  - **模板引擎 (Jinja2)**：Jinja2 是與 Flask 深度整合的模板引擎。本專案不選擇前後端分離，而是透過 Jinja2 將後端計算好的運勢結果、登入狀態等，直接渲染成最終的 HTML 傳遞給瀏覽器，大幅降低架構複雜度。
  - **資料庫 (SQLite)**：作為輕量級的關聯式資料庫，SQLite 儲存為單一檔案，無須額外的伺服器建置與設定，適合用來儲存本專案的「籤詩題庫」、「會員資料」以及「測算紀錄」。

- **Flask MVC 模式說明**：
  - **Model (模型)**：負責與資料庫溝通，定義資料表結構並處理資料的增刪改查（CRUD）。例如定出 `User`（帳號密碼） 與 `History`（算命紀錄）。
  - **View (視圖)**：負責將資料呈現給使用者看的手機或電腦螢幕，對應到系統裡的 Jinja2 HTML 模板，負責組合畫面的樣式與資料。
  - **Controller (控制器)**：系統的大腦，接收使用者的請求後進行對應處理。對應到 Flask 的 Routes（路由），如：收到使用者註冊、點擊抽籤等動作後，指示 Model 動作，然後將結果交給 View 來生成畫面。

## 2. 專案資料夾結構

為了讓程式碼好維護並確保各元件各司其職，我們規劃以下資料夾與檔案結構：

```text
web_app_development/
├── app/
│   ├── __init__.py      ← 應用程式的初始化工廠 (Application Factory)，設定 db 等
│   ├── models/          ← 資料庫模型 (Model)
│   │   ├── user.py      ← 定義會員資料結構
│   │   ├── fortune.py   ← 定義所有的算命/籤詩結果庫
│   │   └── history.py   ← 定義用戶的歷史抽籤紀錄
│   ├── routes/          ← Flask 路由 (Controller)
│   │   ├── auth.py      ← 處理註冊、登入、登出等驗證邏輯
│   │   ├── main.py      ← 負責系統首頁等靜態導覽頁面
│   │   └── fortune.py   ← 處理抽籤過程、隨機邏輯、儲存結果等
│   ├── templates/       ← Jinja2 HTML 模板 (View)
│   │   ├── base.html    ← 網站外觀基礎模板（Header / Footer）
│   │   ├── index.html   ← 首頁入口
│   │   ├── auth/        ← 包含註冊、登入的表單畫面
│   │   └── fortune/     ← 包含進行抽籤的動畫頁面與最終結果展示頁面
│   └── static/          ← 靜態資源 (不需經過後端算算的檔案)
│       ├── css/         ← 排版與畫面美化樣式表
│       ├── js/          ← 負責前端互動如抽籤點擊動畫的腳本
│       └── images/      ← 各種神像、塔羅牌、Icon 等圖檔
├── instance/
│   └── database.db      ← SQLite 實際存入硬碟的資料庫檔案
├── docs/                ← 專案規劃相關文件 (PRD, 架構設計等)
├── requirements.txt     ← 紀錄需安裝哪些 Python 套件
└── app.py               ← 開發時的專案啟動入口程式
```

## 3. 元件關係圖

透過 Mermaid 語法繪製系統處理「抽籤動作」時的資料流向關係圖。

```mermaid
graph TD
    Browser[瀏覽器 / 使用者] --> |1. 送出請求 (點擊抽籤)| Routes[Flask Route<br>(Controller)]
    Routes --> |2. 運算邏輯與呼叫| Model[Database Model<br>(Model)]
    Model --> |3. 從資料庫讀取籤詩/寫入紀錄| SQLite[(SQLite 資料庫)]
    SQLite --> |4. 回傳抽中結果語句| Model
    Model --> |5. 封裝資料後反饋| Routes
    Routes --> |6. 傳遞籤詩資料與圖文| Jinja2[Jinja2 Template<br>(View)]
    Jinja2 --> |7. 產生最終美觀的 HTML| Routes
    Routes --> |8. HTTP 回應送回| Browser
```

## 4. 關鍵設計決策

1. **採用伺服器端渲染 (SSR)**
   - **決定**：使用 Flask 配合 Jinja2 渲染 HTML，而非建造獨立的 SPA (如 React 或 Vue) 搭配 API。
   - **原因**：為了最快實現產品上線 (MVP)，這能減少處理 CORS 問題、Token 通訊等 API 串接的複雜性，並有利於對各占卜專頁的 SEO。
   
2. **利用 Flask Blueprint (藍圖) 切分路由**
   - **決定**：將網站的不同重點路徑如 `/auth` (驗證) 和 `/fortune` (算命) 作為獨立區塊分開開發。
   - **原因**：避免全部代碼塞在同一個檔案內。透過模組化有助於前後端成員協作與日後的網站功能擴展。

3. **系統題庫與個人紀錄分離**
   - **決定**：在資料庫層級中，將系統預設的「籤詩題庫 (Fortune)」與「個人算命紀錄 (History)」分為兩張不同的資料表。
   - **原因**：當系統未來需要修改某些算命題庫的錯字或文案時，不影響用戶過去個人歷史抽籤的純淨性，同時也可以大幅減小資料庫的存儲重複性。
