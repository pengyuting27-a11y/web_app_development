# 流程圖：線上算命系統

## 1. 使用者流程圖（User Flow）

這張圖描述了使用者進入網站後的主要操作路徑與體驗流程。

```mermaid
flowchart TD
    Start([使用者開啟網站]) --> Home[首頁]
    
    Home --> CheckLogin{是否已登入?}
    
    CheckLogin -- 否 --> AuthSelect{選擇登入或註冊}
    AuthSelect --> Login[登入頁面]
    AuthSelect --> Register[註冊頁面]
    Login --> Home
    Register --> Login
    
    CheckLogin -- 是 --> ActionSelect{想要做什麼?}
    
    ActionSelect --> |查看紀錄| HistoryList[歷史算命紀錄]
    ActionSelect --> |求神問卜| DrawLotMain[抽籤首頁]
    
    DrawLotMain --> ClickDraw[點擊抽籤/擲筊]
    ClickDraw --> Animation[播放抽籤動畫]
    Animation --> Result[展示詳細籤詩與解析]
    
    Result --> OptionalAction{後續操作}
    OptionalAction --> |分享| ShareResult[複製分享連結/文字]
    OptionalAction --> |回顧| HistoryList
    OptionalAction --> |繼續算命| DrawLotMain
```

## 2. 系統序列圖（Sequence Diagram）

以下是一次完整的**線上抽籤**運作機制。描述從使用者點擊抽籤按鈕，到系統返回最終結果畫面的整個資料流動。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route (fortune.py)
    participant Model as Database Model
    participant DB as SQLite 資料庫

    User->>Browser: 點擊「開始抽籤」
    Browser->>Route: POST /fortune/draw
    Route->>Route: 確認使用者為登入狀態 (檢查 Session)
    
    Route->>Model: 呼叫 Fortune Model 隨機抽取一支籤
    Model->>DB: SELECT * FROM fortune ORDER BY RANDOM() LIMIT 1
    DB-->>Model: 回傳抽中籤詩 (例如：第三十二籤)
    Model-->>Route: 籤詩資料
    
    Route->>Model: 將結果存入使用者紀錄 (History)
    Model->>DB: INSERT INTO history (user_id, fortune_id, date)
    DB-->>Model: 儲存成功
    Model-->>Route: 紀錄成功
    
    Route->>Browser: 重新導向 (Redirect) 至詳細結果頁面
    Browser->>Route: GET /fortune/result/32
    Route->>Route: 載入 Jinja2 模板，帶入籤詩變數
    Route-->>Browser: 回傳渲染好的頁面 HTML
    Browser-->>User: 顯示美觀的籤詩內容與解析
```

## 3. 功能清單對照表

整理目前架構與流程對應的 HTTP 路由表，此表可直接作為後續「API 與路由設計」的藍圖參考。

| 功能模組 | 功能名稱 | URL 路徑 | HTTP 方法 | 備註說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | 網站首頁入口 | `/` | GET | 展示網站形象與功能入口 |
| **會員(auth)** | 註冊帳號 | `/auth/register` | GET, POST | 呈現表單(GET)，與送出寫入資料表(POST) |
| **會員(auth)** | 登入 | `/auth/login` | GET, POST | 驗證帳密並發放 Session |
| **會員(auth)** | 登出 | `/auth/logout` | GET | 清除使用者的登入 Session |
| **算命(fortune)** | 抽籤入口 | `/fortune/` | GET | 準備準備抽籤的頁面（例如點擊靈籤筒） |
| **算命(fortune)** | 執行抽籤 | `/fortune/draw` | POST | 系統隨機挑選籤詩並儲存抽籤紀錄 |
| **算命(fortune)** | 結果展示 | `/fortune/result/<id>` | GET | 渲染 Jinja2 模板呈現抽中的詳細解說 |
| **與歷史(history)**| 個人紀錄 | `/history/` | GET | 從歷史資料表撈出過往曾擁有的算命與抽籤清單 |
