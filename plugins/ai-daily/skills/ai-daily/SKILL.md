---
name: ai-daily-news
description: Fetches AI news from smol.ai RSS and generates structured markdown with intelligent summarization and categorization. Optionally creates beautiful HTML webpages with Apple-style themes and shareable card images. Use when user asks about AI news, daily tech updates, or wants news organized by date or category.
---

# AI Daily News

Fetches AI industry news from smol.ai, intelligently summarizes and categorizes using built-in Claude AI capabilities, outputs structured markdown, and optionally generates themed webpages and shareable card images.

## Quick Start

```bash
# Yesterday's news
昨天AI資訊

# Specific date
2026-01-13的AI新聞

# By category
昨天的模型發布相關資訊

# Generate webpage
昨天AI資訊，生成網頁

# Generate shareable card image
昨天AI資訊，生成分享圖片
生成日報卡片圖片
```

## Supported Query Types

| Type | Examples | Description |
|------|----------|-------------|
| **相對日期** | "昨天AI資訊" "前天的新聞" "今天的AI動態" | Yesterday, day before, today |
| **絕對日期** | "2026-01-13的新聞" | YYYY-MM-DD format |
| **分類篩選** | "模型相關資訊" "產品動態" | Filter by category |
| **網頁生成** | "生成網頁" "製作HTML頁面" | Optional webpage generation |
| **圖片生成** | "生成圖片" "生成分享卡片" "製作日報卡片" | Generate shareable card image |

---

## Workflow

Copy this checklist to track progress:

```
Progress:
- [ ] Step 1: Parse date from user request
- [ ] Step 2: Fetch RSS from smol.ai
- [ ] Step 3: Check if content exists for target date
- [ ] Step 4: Extract and analyze content
- [ ] Step 5: Generate structured markdown
- [ ] Step 6: Ask about webpage generation (if requested)
- [ ] Step 7: Generate shareable card image (if requested)
```

---

## Step 1: Parse Date

Extract the target date from user request.

| User Input | Target Date | Calculation |
|------------|-------------|-------------|
| "昨天AI資訊" | Yesterday | today - 1 day |
| "前天AI資訊" | Day before yesterday | today - 2 days |
| "2026-01-13的新聞" | 2026-01-13 | Direct parse |
| "今天的AI動態" | Today | Current date |

**Date format**: Always use `YYYY-MM-DD` format (e.g., `2026-01-13`)

---

## Step 2: Fetch RSS

Run the fetch script to get RSS data:

```bash
python plugins/ai-daily/skills/ai-daily/scripts/fetch_news.py
```

This downloads and parses `https://news.smol.ai/rss.xml`, returning structured JSON.

**Available dates** can be checked with:

```bash
python plugins/ai-daily/skills/ai-daily/scripts/fetch_news.py --date-range
```

---

## Step 3: Check Content

Verify if content exists for the target date.

### When Content Exists

Continue to Step 4.

### When Content NOT Found

Display a friendly message with available dates:

```markdown
抱歉，2026-01-14 暫無資訊

可用日期範圍: 2026-01-10 ~ 2026-01-13

建議:
- 查看 [2026-01-13](command:查看2026-01-13的資訊) 的資訊
- 查看 [2026-01-12](command:查看2026-01-12的資訊) 的資訊
```

**User experience principles**:
1. Clear problem statement
2. Show available alternatives
3. Provide clickable commands for quick access
4. Never leave user stuck with no options

---

## Step 4: Extract and Analyze Content

Use built-in Claude AI capabilities to:

1. **Extract full content** from the RSS entry
2. **Generate summary** - 3-5 key takeaways
3. **Categorize** items by topic:
   - Model Releases (模型發布)
   - Product Updates (產品動態)
   - Research Papers (研究論文)
   - Tools & Frameworks (工具框架)
   - Funding & M&A (融資併購)
   - Industry Events (行業事件)
4. **Extract keywords** - Companies, products, technologies

**Prompt Template**:

```
Analyze this AI news content and organize it:

1. Generate 3-5 key takeaways (one sentence each)
2. Categorize items into: Model Releases, Product Updates, Research, Tools, Funding, Events
3. Extract 5-10 keywords

Original content:
{content}
```

---

## Step 5: Generate Markdown

Output structured markdown following the format in [output-format.md](references/output-format.md).

**Key sections**:
- Title with date
- Core summary
- Categorized news items
- Keywords
- Footer with source info

**Example output**:

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

## 產品動態

...

## 關鍵詞

#Anthropic #Google #MedGemma #LangChain

---
數據來源: smol.ai
```

---

## Step 6: Webpage Generation (Optional)

**Only trigger when user explicitly says**:

- "生成網頁"
- "製作HTML頁面"
- "生成靜態網站"

### Ask User Preferences

```
是否需要生成精美的網頁？

可選主題:
- [蘋果風](command:使用蘋果風主題) - 簡潔專業，適合技術內容
- [深海藍](command:使用深海藍主題) - 商務風格，適合產品發布
- [秋日暖陽](command:使用秋日暖陽主題) - 溫暖活力，適合社區動態
```

### Theme Prompt Templates

See [html-themes.md](references/html-themes.md) for detailed prompt templates for each theme.

**Apple Style Theme** (Key Points):

```markdown
Generate a clean, minimalist HTML page inspired by Apple's design:

**Design**:
- Pure black background (#000000)
- Subtle blue glow from bottom-right (#0A1929 → #1A3A52)
- Generous white space, content density ≤ 40%
- SF Pro Display for headings, SF Pro Text for body
- Smooth animations and hover effects

**Structure**:
- Header: Logo icon + Date badge
- Main: Summary card + Category sections
- Footer: Keywords + Copyright

**Colors**:
- Title: #FFFFFF
- Body: #E3F2FD
- Accent: #42A5F5
- Secondary: #B0BEC5
```

### Save Webpage

Save to `docs/{date}.html`:

```bash
# Save webpage
cat > docs/2026-01-13.html << 'EOF'
{generated_html}
EOF
```

---

## Step 7: Shareable Card Image Generation (Optional)

**Trigger when user explicitly requests**:

- "生成圖片"
- "生成分享卡片"
- "製作日報卡片"
- "生成卡片圖片"
- "生成分享圖"

### Image Generation Process

1. **Build condensed Markdown** for card display:
   - Title and date
   - Core summary (3-5 items)
   - Top items per category (3 items each)
   - Keywords

2. **Call Firefly Card API**:
   - API: `POST https://fireflycard-api.302ai.cn/api/saveImg`
   - Body contains `content` field with Markdown
   - Returns binary image stream (`Content-Type: image/png`)

3. **Save and display result**:
   - Save to `docs/images/{date}.png`
   - Display preview or download link

### API Request Format

```json
{
  "content": "# AI Daily\\n## 2026年1月13日\\n...",
  "font": "SourceHanSerifCN_Bold",
  "align": "left",
  "width": 400,
  "height": 533,
  "fontScale": 1.2,
  "ratio": "3:4",
  "padding": 30,
  "switchConfig": {
    "showIcon": false,
    "showTitle": false,
    "showContent": true,
    "showTranslation": false,
    "showAuthor": false,
    "showQRCode": false,
    "showSignature": false,
    "showQuotes": false,
    "showWatermark": false
  },
  "temp": "tempBlackSun",
  "textColor": "rgba(0,0,0,0.8)",
  "borderRadius": 15,
  "color": "pure-ray-1"
}
```

### Output Example

```markdown
📸 分享卡片已生成

圖片已保存到: docs/images/2026-01-13.png

[預覽圖片](docs/images/2026-01-13.png)

你可以將此圖片分享到社交媒體！
```

---

## Configuration

No configuration required. Uses built-in RSS fetching and Claude AI capabilities.

**RSS Source**: `https://news.smol.ai/rss.xml`

**Date Calculation**: Uses current UTC date, subtracts days for relative queries.

---

## Complete Examples

### Example 1: Yesterday's News (Basic)

**User Input**: "昨天AI資訊"

**Process**:
1. Calculate yesterday's date: `2026-01-14`
2. Fetch RSS
3. Check content exists
4. Analyze and categorize
5. Output markdown

**Output**: Structured markdown with all categories

### Example 2: Specific Date

**User Input**: "2026-01-13的AI新聞"

**Process**:
1. Parse date: `2026-01-13`
2. Fetch RSS
3. Check content exists
4. Analyze and categorize
5. Output markdown

### Example 3: By Category

**User Input**: "昨天的模型發布相關資訊"

**Process**:
1. Calculate yesterday's date
2. Fetch RSS
3. Analyze and filter for "Model Releases" category
4. Output filtered markdown

### Example 4: With Webpage Generation

**User Input**: "昨天AI資訊，生成網頁"

**Process**:
1-5. Same as Example 1
6. Ask: "Which theme?"
7. User selects: "蘋果風"
8. Generate HTML with Apple-style theme
9. Save to `docs/2026-01-14.html`

### Example 5: Content Not Found

**User Input**: "2026-01-15的資訊"

**Output**:
```markdown
抱歉，2026-01-15 暫無資訊

可用日期範圍: 2026-01-10 ~ 2026-01-13

建議:
- 查看 [2026-01-13](command:查看2026-01-13的資訊) 的資訊
- 查看 [2026-01-12](command:查看2026-01-12的資訊) 的資訊
```

---

## References

- [Output Format](references/output-format.md) - Markdown output structure
- [HTML Themes](references/html-themes.md) - Webpage theme prompts

---

## Troubleshooting

### RSS Fetch Fails

**Error**: "Failed to fetch RSS"

**Solution**: Check network connectivity to `news.smol.ai`

### Date Parsing Fails

**Error**: "Invalid date format"

**Solution**: Use `YYYY-MM-DD` format or relative terms like "昨天"

### No Content for Date

**Output**: Friendly message with available dates (see Step 3)

### Webpage Save Fails

**Error**: "Cannot save to docs/"

**Solution**: Ensure `docs/` directory exists:
```bash
mkdir -p docs
```

---

## CLI Reference

```bash
# Fetch RSS (returns JSON)
python plugins/ai-daily/skills/ai-daily/scripts/fetch_news.py

# Get available date range
python plugins/ai-daily/skills/ai-daily/scripts/fetch_news.py --date-range

# Get specific date content
python plugins/ai-daily/skills/ai-daily/scripts/fetch_news.py --date 2026-01-13
```
