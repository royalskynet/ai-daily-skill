"""
Claude 分析模塊
使用 Claude API 對資訊內容進行智能分析、分類和摘要
"""
import os
import json
from typing import Dict, Any, Optional
from anthropic import Anthropic

from src.config import (
    ANTHROPIC_BASE_URL,
    CLAUDE_API_KEY,
    CLAUDE_MODEL,
    CLAUDE_MAX_TOKENS,
    CATEGORIES,
    THEMES,
    DEFAULT_THEME
)


class ClaudeAnalyzer:
    """Claude AI 分析器"""

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        初始化 Claude 客戶端

        Args:
            api_key: API 密鑰，默認從環境變量讀取
            base_url: API 基礎 URL，默認從環境變量讀取
        """
        self.api_key = api_key or CLAUDE_API_KEY
        self.base_url = base_url or ANTHROPIC_BASE_URL
        self.model = CLAUDE_MODEL
        self.max_tokens = CLAUDE_MAX_TOKENS

        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY 環境變量未設置")

        try:
            self.client = Anthropic(
                base_url=self.base_url,
                api_key=self.api_key
            )
            print(f"✅ Claude 客戶端初始化成功")
            print(f"   Base URL: {self.base_url}")
            print(f"   Model: {self.model}")
        except Exception as e:
            raise Exception(f"Claude 客戶端初始化失敗: {e}")

    def analyze(self, content: Dict[str, Any], target_date: str) -> Dict[str, Any]:
        """
        分析資訊內容

        Args:
            content: RSS 內容字典
            target_date: 目標日期

        Returns:
            分析結果字典，包含：
            - status: success/empty/error
            - date: 日期
            - theme: 主題名稱
            - summary: 核心摘要列表
            - keywords: 關鍵詞列表
            - categories: 分類資訊列表
        """
        if not content or not content.get("content"):
            return self._empty_result(target_date, "內容為空")

        print(f"🤖 正在調用 Claude 分析內容...")

        # 構建提示詞
        prompt = self._build_prompt(content, target_date)

        try:
            # 調用 Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0.3,  # 較低溫度保證穩定性
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # 解析響應
            result_text = response.content[0].text
            print(f"✅ Claude 響應成功，響應長度: {len(result_text)} 字符")

            # 解析 JSON 結果
            result = self._parse_result(result_text, target_date)

            return result

        except Exception as e:
            print(f"❌ Claude API 調用失敗: {e}")
            # 返回帶有原始內容的結果，讓生成器可以繼續工作
            return {
                "status": "success",
                "date": target_date,
                "theme": DEFAULT_THEME,
                "summary": [
                    "AI 資訊分析遇到技術問題，以下是原始內容摘要",
                    f"標題: {content.get('title', '')[:100]}..."
                ],
                "keywords": ["AI", "資訊"],
                "categories": self._fallback_categories(content),
                "raw_content": content
            }

    def _build_prompt(self, content: Dict[str, Any], target_date: str) -> str:
        """構建 Claude 提示詞"""
        # 構建分類說明
        category_desc = "\n".join([
            f"- {cat['icon']} {cat['name']}: {cat['description']}"
            for cat in CATEGORIES.values()
        ])

        # 構建主題說明
        theme_desc = "\n".join([
            f"- {key}: {theme['name']} - {theme['description']}"
            for key, theme in THEMES.items()
        ])

        prompt = f"""你是一個專業的 AI 資訊分析師，請對以下 AI 日報內容進行深度分析。

【目標日期】
{target_date}

【原始資訊內容】
標題: {content.get('title', '')}
連結: {content.get('link', '')}

完整內容:
{content.get('content', '')[:15000]}

---

【任務要求】

0. **內容過濾**
   - 請嚴格排除任何來自中國大陸及臺灣媒體的新聞來源或相關報導，若判斷為相關內容請直接丟棄該條資訊。

1. **狀態檢查**
   - 如果內容確實存在且有效，返回狀態為 "success"
   - 如果內容為空或無效，返回狀態為 "empty"

2. **核心摘要** (summary)
   - 生成 3-5 條今日最重要的 AI 資訊要點
   - 每條摘要不超過 50 字，簡潔明了
   - 按重要性排序

3. **智能分類** (categories)
   將資訊按以下維度分類（可空）:
{category_desc}

   每個分類包含:
   - key: 分類標識 (model/product/research/tools/funding/events)
   - name: 分類名稱
   - icon: 分類圖標
   - items: 該分類下的資訊列表

   每條資訊包含:
   - title: 簡化版標題（適合快速瀏覽，不超過40字）
   - summary: 一句話核心要點（不超過80字）
   - url: 相關連結（如果有的話）
   - tags: 相關標籤（如公司名、產品名）

4. **關鍵詞提取** (keywords)
   - 提取 5-10 個今日熱門關鍵詞
   - 包括: 公司名稱、人物、技術名詞、產品名
   - 去重並按重要性排序

5. **主題選擇** (theme)
   根據內容主類別選擇最佳主題:
{theme_desc}

   選擇規則:
   - 模型/框架/開發工具 → blue (柔和藍色)
   - 企業動態/產品發布 → indigo (深靛藍)
   - 融資/併購/金融 → teal (冷色青綠)
   - 創意/AIGC/設計 → purple (優雅紫色)
   - 醫療/健康AI → green (清新綠色)
   - 熱點/爭議話題 → orange (溫暖橙色)
   - 研究/論文/數據 → gray (中性灰色)
   - 應用/生活/消費 → pink (玫瑰粉色)

【輸出格式】

請嚴格按照以下 JSON 格式輸出，不要包含任何其他文字說明：

```json
{{
  "status": "success",
  "date": "{target_date}",
  "theme": "blue",
  "summary": [
    "第一條核心摘要",
    "第二條核心摘要",
    "第三條核心摘要"
  ],
  "keywords": ["Anthropic", "Google", "Claude", "MedGemma", "LangChain"],
  "categories": [
    {{
      "key": "model",
      "name": "模型發布",
      "icon": "🤖",
      "items": [
        {{
          "title": "MedGemma 1.5 發布",
          "summary": "Google 發布 4B 參數醫療多模態模型，支持 3D 影像分析",
          "url": "https://news.smol.ai/issues/26-01-13-not-much/",
          "tags": ["Google", "MedGemma", "醫療AI"]
        }}
      ]
    }},
    {{
      "key": "product",
      "name": "產品動態",
      "icon": "💼",
      "items": []
    }}
  ]
}}
```

重要：只輸出 JSON，不要有任何其他說明文字。確保 JSON 格式正確有效。
"""
        return prompt

    def _parse_result(self, result_text: str, target_date: str) -> Dict[str, Any]:
        """解析 Claude 的響應結果"""
        # 清理可能的 markdown 代碼塊標記
        result_text = result_text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()

        try:
            result = json.loads(result_text)

            # 驗證必要欄位
            if "status" not in result:
                result["status"] = "success"
            if "date" not in result:
                result["date"] = target_date
            if "theme" not in result:
                result["theme"] = DEFAULT_THEME
            if "summary" not in result:
                result["summary"] = []
            if "keywords" not in result:
                result["keywords"] = []
            if "categories" not in result:
                result["categories"] = []

            print(f"✅ 結果解析成功")
            print(f"   主題: {result.get('theme')}")
            print(f"   摘要數: {len(result.get('summary', []))}")
            print(f"   關鍵詞數: {len(result.get('keywords', []))}")
            print(f"   分類數: {len(result.get('categories', []))}")

            return result

        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失敗: {e}")
            print(f"   原始響應: {result_text[:500]}...")

            # 返回一個基本的成功結果，使用原始內容
            return {
                "status": "success",
                "date": target_date,
                "theme": DEFAULT_THEME,
                "summary": ["AI 資訊已獲取"],
                "keywords": ["AI"],
                "categories": [],
                "parse_error": str(e)
            }

    def _empty_result(self, target_date: str, reason: str) -> Dict[str, Any]:
        """返回空結果"""
        return {
            "status": "empty",
            "date": target_date,
            "theme": DEFAULT_THEME,
            "summary": [],
            "keywords": [],
            "categories": [],
            "reason": reason
        }

    def _fallback_categories(self, content: Dict[str, Any]) -> list:
        """當 Claude 解析失敗時的備用分類"""
        # 簡單地將原始內容作為一個通用資訊
        title = content.get('title', '')[:100]
        description = content.get('description', '')[:200]
        url = content.get('link', '')

        return [
            {
                "key": "model",
                "name": "模型發布",
                "icon": "🤖",
                "items": [
                    {
                        "title": title,
                        "summary": description,
                        "url": url,
                        "tags": ["AI"]
                    }
                ]
            }
        ]


def analyze_content(content: Dict[str, Any], target_date: str) -> Dict[str, Any]:
    """便捷函數：分析資訊內容"""
    analyzer = ClaudeAnalyzer()
    return analyzer.analyze(content, target_date)
