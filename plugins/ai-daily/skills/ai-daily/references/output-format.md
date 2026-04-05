# Markdown Output Format

This document defines the standard markdown output format for AI Daily news.

---

## Template

```markdown
# AI Daily · {年}年{月}月{日}日

> {一句話核心摘要}

## 核心摘要

{3-5條核心要點，每條一句話}

## {分類名稱}

### [{標題}](連結)

{詳細摘要}

**關鍵信息**: {相關標籤}

---

數據來源: smol.ai
生成時間: {YYYY-MM-DD HH:MM}
```

---

## Complete Example

```markdown
# AI Daily · 2026年1月13日

> Anthropic 整合 Agent 產品線，Google 發布醫療 AI 模型，LangChain 推出 Agent 構建工具

## 核心摘要

- Anthropic 發布 Cowork 統一 Agent 平臺，整合 Claude Code 和 MCP
- Google 開源 MedGemma 1.5 醫療多模態模型，支持 3D 影像分析
- LangChain Agent Builder 正式發布，支持內存和人工審核循環
- 社區討論"Vibe Coding"定義，強調工程師驗證的重要性
- 開源項目快速複製 Cowork 功能，Agent 技術商品化加速

## 模型發布

### [MedGemma 1.5](https://news.smol.ai/issues/26-01-13-not-much/)

Google 發布 4B 參數醫療多模態模型 MedGemma 1.5，專為離線醫療場景設計。支持 3D 體積（CT/MRI）處理、縱向對比和解剖定位。聲稱在 EHR 理解上達到 89.6% 準確率（+22%），X 光定位達到 38% IoU。

**關鍵信息**: Google, MedGemma, 醫療AI, 多模態, 3D影像

### [Open 復現 Cowork](https://news.smol.ai/issues/26-01-13-not-much/)

開發者使用 QEMU + bubblewrap + seccomp 構建了跨平臺類 Cowork VM 環境。這表明 Agent shell 技術正在快速商品化，成為基礎設施而非產品護城河。

**關鍵信息**: 開源, QEMU, Agent, 虛擬化

## 產品動態

### [Cowork 品牌整合](https://news.smol.ai/issues/26-01-13-not-much/)

Anthropic 將其 AI agent 產品統一到 Cowork 品牌，整合了之前的 Claude Code、Claude for Chrome 等工具。使用 Apple 的虛擬化技術和 bubblewrap 實現安全沙箱。

**關鍵信息**: Anthropic, Cowork, Claude Code, MCP

### [LangChain Agent Builder GA](https://news.smol.ai/issues/26-01-13-not-much/)

LangChain 宣布 Agent Builder 正式發布（GA），提供無代碼但強大的 agent 編排功能：內存、觸發器、人工審核循環和 agent 收件箱。

**關鍵信息**: LangChain, Agent Builder, 編排, 工具鏈

## 研究方向

### [MemRL: 記憶即強化學習](https://news.smol.ai/issues/26-01-13-not-much/)

DAIR AI 強調 MemRL 方法，將記憶檢索視為強化學習問題。保持基礎模型凍結，學習情節記憶的 Q 值（意圖-經驗-效用），兩階段檢索：語義過濾 + 效用排序。

**關鍵信息**: MemRL, 強化學習, 記憶檢索, DAIR AI

### [遞歸語言模型 (RLMs)](/root/ai-daily-skill/docs/2026-01-12.html)

Omar Khattab 等人指出大多數"子 agent"實現錯過了核心思想：需要類似指針的符號訪問提示詞來遞歸遍歷。這可以實現超過 1000 萬 tokens 的上下文而無需重新訓練。

**關鍵信息**: RLMs, 遞歸模型, 長上下文, 符號訪問

## 工具框架

### [Diffusers 統一注意力後端](https://news.smol.ai/issues/26-01-13-not-much/)

Hugging Face Diffusers 發布統一注意力後端，結合了 Ring 和 Ulysses 的屬性。這是持續推動注意力內核/後端可互換和性能可移植化的一部分。

**關鍵信息**: Hugging Face, Diffusers, 注意力機制

### [量化的注意事項](https://news.smol.ai/issues/26-01-13-not-much/)

TensorPro 報告稱 MXFP4 量化的注意力可能破壞因果建模，發布了診斷和修復"洩漏量化"行為的方法。對於從業者："以 FP8/4 位訓練"日益可行，但數值邊緣情況仍是活躍的研究/運維問題。

**關鍵信息**: 量化, FP8, MXFP4, 數值穩定性

## 關鍵詞

#Anthropic #Google #MedGemma #LangChain #Agent #MemRL #RLMs #Diffusers #量化

---

數據來源: smol.ai
生成時間: 2026-01-15 10:30
```

---

## Category Names

Use these Chinese category names:

| Category | Chinese Name | Icon |
|----------|--------------|------|
| Model Releases | 模型發布 | 🤖 |
| Product Updates | 產品動態 | 💼 |
| Research | 研究論文 | 📚 |
| Tools & Frameworks | 工具框架 | 🛠️ |
| Funding & M&A | 融資併購 | 💰 |
| Industry Events | 行業事件 | 🏆 |

---

## Output Guidelines

1. **Title format**: `# AI Daily · {年}年{月}月{日}日`
2. **Summary**: 3-5 bullet points, one sentence each
3. **Categories**: Use category sections above
4. **Links**: Include original smol.ai links
5. **Keywords**: 5-10 hashtags, comma separated
6. **Footer**: Source and generation time
