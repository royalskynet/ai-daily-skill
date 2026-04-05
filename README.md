# AI Daily Skill

> AI 資訊日報 Claude Code Skill - 每天自動獲取、分析、歸類 AI 前沿資訊

> [!CAUTION]
$\color{#FF0000}{想每天咖啡時間就幫你找到好的選題，自動發給你嗎？ 有需要定製的朋友拉到底部通過公眾號聯繫到我。}$

---

## 簡介

AI Daily 是一個 Claude Code Skill，幫助你在 Claude Code 中快速獲取 AI 行業資訊。它從 [smol.ai](https://news.smol.ai/) 獲取資訊，使用內置的 Claude AI 能力進行智能分析和分類，生成結構化的 Markdown 文檔，並可按需生成精美的網頁。

### 核心功能

- 每天自動獲取 AI 行業資訊
- Claude AI 智能摘要和分類
- 支持相對日期查詢（昨天、前天等）
- 可選生成精美網頁（蘋果風/深海藍/秋日暖陽主題）
- 可選生成分享卡片圖片（智能尺寸，適合社交媒體分享）
- 可選生成INSTAGRAM風格封面（3:4 比例，極簡格柵設計）
- 友好的用戶體驗，無數據時提供建議

---

## 安裝

### 方式一：Plugin Marketplace（推薦）

在 Claude Code 中運行：

```bash
/plugin marketplace add geekjourneyx/ai-daily-skill
/plugin install ai-daily@geekjourneyx-ai-daily-skill
```

### 方式二：項目內使用

克隆項目後，Skill 自動可用：

```bash
git clone https://github.com/geekjourneyx/ai-daily-skill.git
cd ai-daily-skill
```

在 Claude Code 中直接使用即可。

### 方式三：全局安裝

```bash
cp -r plugins/ai-daily ~/.claude/skills/
```

---

## 使用方法

### 基礎查詢

```bash
# 昨天的 AI 資訊
昨天AI資訊

# 前天的 AI 新聞
前天AI資訊

# 具體日期
2026-01-13的AI新聞

# 按分類篩選
昨天的模型發布相關資訊
```

### 生成網頁

```bash
# 查詢並詢問是否生成網頁
昨天AI資訊，生成網頁

# 直接選擇主題
昨天AI資訊，生成蘋果風網頁
```

### 生成分享圖片

```bash
# 生成社交媒體分享卡片
昨天AI資訊，生成分享圖片
生成日報卡片圖片
```

### 生成INSTAGRAM封面

自動生成INSTAGRAM風格封面，包含：
- 3:4 比例（750x1000px）
- 極簡格柵主義設計
- 黑白主色調 + 綠色點綴
- 一鍵保存為 PNG 圖片

封面保存在 `docs/instagram/` 目錄，在瀏覽器中打開 HTML 文件後點擊"保存封面"按鈕即可下載。

### 完整對話示例

```
用戶: 昨天AI資訊

Claude: [展示 Markdown 格式的資訊摘要，包含核心摘要和分類資訊]

用戶: 生成網頁

Claude: 可選主題:
- 蘋果風 - 簡潔專業，適合技術內容
- 深海藍 - 商務風格，適合產品發布
- 秋日暖陽 - 溫暖活力，適合社區動態

用戶: 蘋果風

Claude: [生成 HTML 網頁並保存到 docs/ 目錄]
```

---

## 項目結構

```
ai-daily-skill/
├── .claude-plugin/
│   └── plugin.json                 # 插件清單
├── plugins/ai-daily/skills/ai-daily/
│   ├── SKILL.md                     # 主技能定義
│   ├── scripts/
│   │   └── fetch_news.py            # RSS 獲取腳本
│   └── references/
│       ├── output-format.md         # Markdown 輸出格式
│       └── html-themes.md            # 網頁主題提示詞
├── docs/                            # 生成的網頁和文檔
│   ├── images/                      # 分享卡片圖片
│   ├── instagram/                 # INSTAGRAM封面
│   ├── css/                         # 樣式文件
│   └── *.html                       # 生成的 HTML 頁面
├── src/                             # GitHub Actions 自動化腳本
│   ├── main.py                      # 主入口
│   ├── config.py                    # 配置管理
│   ├── rss_fetcher.py               # RSS 獲取
│   ├── claude_analyzer.py           # AI 分析
│   ├── html_generator.py            # HTML 生成
│   ├── image_generator.py           # 圖片生成
│   ├── instagram_generator.py     # INSTAGRAM封面生成
│   └── notifier.py                  # 郵件通知
└── README.md
```

---

## 輸出格式

### Markdown 格式

```markdown
# AI Daily · 2026年1月13日

## 核心摘要

- Anthropic 發布 Cowork 統一 Agent 平臺
- Google 開源 MedGemma 1.5 醫療多模態模型
- LangChain Agent Builder 正式發布

## 模型發布

### MedGemma 1.5
Google 發布 4B 參數醫療多模態模型...
[原文連結](https://news.smol.ai/issues/26-01-13-not-much/)

## 關鍵詞

#Anthropic #Google #MedGemma #LangChain
```

### 網頁格式

- 純黑背景 + 漸變光暈
- 響應式設計，支持移動端
- 平滑動畫和懸停效果
- 單文件 HTML，無外部依賴

---

## 網頁主題

| 主題 | 風格 | 適用場景 |
|------|------|----------|
| 蘋果風 | 簡潔專業 | 技術內容、產品評測 |
| 深海藍 | 商務風格 | 產品發布、企業動態 |
| 秋日暖陽 | 溫暖活力 | 社區新聞、討論 |

---

## 常見問題

### Q: 支持哪些日期查詢方式？

A: 支持相對日期（昨天、前天、今天）和絕對日期（YYYY-MM-DD 格式）。

### Q: 如果某天沒有資訊會怎樣？

A: 系統會友好提示，並列出可用的日期範圍供選擇。

### Q: 網頁保存在哪裡？

A: 網頁保存在 `docs/` 目錄，文件名為 `{日期}.html` 格式。

### Q: 圖片保存在哪裡？

A: 分享卡片圖片保存在 `docs/images/` 目錄，文件名為 `{日期}.png` 格式。

### Q: 需要配置 API Key 嗎？

A: 不需要。Skill 使用 Claude Code 內置的 AI 能力，無需額外配置。

### Q: 如何啟用圖片生成功能？

A: 需要設置環境變量 `ENABLE_IMAGE_GENERATION=true`，並配置 Firefly API。

### Q: 可以自定義主題嗎？

A: 可以。主題提示詞在 `references/html-themes.md` 中，可以修改或添加新主題。

---

## 開發

### 環境要求

- Python 3.11+
- feedparser
- requests

### 環境變量

```bash
# Claude API 配置（必需）
ZHIPU_API_KEY=your_api_key
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic

# 圖片生成配置（可選）
ENABLE_IMAGE_GENERATION=true
FIREFLY_API_URL=https://fireflycard-api.302ai.cn/api/saveImg
FIREFLY_API_KEY=your_firefly_key

# 郵件通知配置（可選）
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASSWORD=your_password
NOTIFICATION_TO=recipient@example.com
```

### 安裝依賴

```bash
pip install feedparser requests
```

### 測試腳本

```bash
# 獲取可用日期範圍
python plugins/ai-daily/skills/ai-daily/scripts/fetch_news.py --date-range

# 獲取特定日期內容
python plugins/ai-daily/skills/ai-daily/scripts/fetch_news.py --date 2026-01-13

# 獲取昨天的內容
python plugins/ai-daily/skills/ai-daily/scripts/fetch_news.py --relative yesterday
```

---

## 貢獻

歡迎提交 Issue 和 Pull Request！

---

## 開源協議

MIT License

---

## 💰 打賞 Buy Me A Coffee

如果該項目幫助了您，請作者喝杯咖啡吧 ☕️

### WeChat

<img src="https://raw.githubusercontent.com/geekjourneyx/awesome-developer-go-sail/main/docs/assets/wechat-reward-code.jpg" alt="微信打賞碼" width="200" />

## 🧑‍💻 作者
- 作者：`geekjourneyx`
- X（Twitter）：https://x.com/seekjourney
- 公眾號：極客傑尼

關注公眾號，獲取更多 AI 編程、AI 工具與 AI 出海建站的實戰分享：

<p>
<img src="https://raw.githubusercontent.com/geekjourneyx/awesome-developer-go-sail/main/docs/assets/qrcode.jpg" alt="公眾號：極客傑尼" width="180" />
</p>

