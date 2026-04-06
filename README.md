# Global Daily Skill

> 全球熱門資訊日報 Claude Code Skill - 每天自動獲取、分析、歸類全量國際熱點。

---

## 簡介

**Global Daily** 是一個強大的自動化資訊聚合與分析系統。它透過 **Brave Search API** 深入網際網路，抓取過去 24 小時內全球最受關注的新聞。隨後，系統調用 **Claude AI** 的深度理解能力，將生硬的各國報導翻譯、分析並歸納為精簡的中文日報。

### 核心功能

- **全量新聞獲取**：自動抓取全球政治、經濟、科技、生活、體育與娛樂熱點。
- **Claude 智能摘要**：不再只是翻譯，而是將碎片化資訊精煉成具備洞察力的核心摘要。
- **動態主題網頁**：生成精美的響應式 HTML 頁面（支援蘋果風、深海藍等主題）。
- **社交分享卡片**：一鍵生成 4:5 比例（1080x1350）的極簡社交媒體分享圖片。
- **多渠道通知**：支援 Telegram Bot 與 Email 自動推播日報連結。

---

## 安裝與設定

### 1. 獲取 API 金鑰
- **Brave Search API**: 前往 [Brave API Dashboard](https://api.search.brave.com/) 申請金鑰。
- **Claude API**: 確保環境中已配置 `CLAUDE_API_KEY`。

### 2. 環境變量配置
複製 `.env.example` 為 `.env` 並填入：
```bash
# Brave API 配置
BRAVE_API_KEY=your_brave_api_key

# 搜尋內容 (預設為全球熱門新聞)
BRAVE_SEARCH_QUERY="top trending global news"

# 其它選填配置 (如 Telegram, Email)
# ...
```

---

## 使用方法

### 基礎查詢
在 Claude Code 中直接輸入：
```bash
# 獲取今天全球重要新聞
今天全球資訊

# 獲取特定日期動態
2026-04-06的熱門新聞
```

### 進階操作
```bash
# 生成精美網頁主題
今天資訊，生成網頁

# 產出 IG 風格分享卡片
生成分享圖片
```

---

## 項目結構

```
global-daily-skill/
├── src/
│   ├── brave_fetcher.py        # Brave Search API 新聞獲取模組
│   ├── claude_analyzer.py      # Claude AI 智能分析與翻譯模組
│   ├── html_generator.py       # HTML 網頁生成引擎
│   ├── image_generator.py      # 4:5 分享圖片生成
│   └── main.py                 # 系統主入口
├── docs/                       # 生成的網頁與圖片存放處
└── plugins/                    # Claude Code Skill 擴充定義
```

---

## 開源協議
MIT License
