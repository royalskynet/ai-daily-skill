"""
Brave Search API 獲取模塊
負責調用 Brave Search News API 獲取全球最新的熱門新聞
"""
import requests
from typing import Optional, Dict, Any

from src.config import BRAVE_API_KEY, BRAVE_SEARCH_QUERY


class BraveFetcher:
    """Brave Search API 獲取器"""

    def __init__(self, api_key: str = None, query: str = None):
        self.api_key = api_key or BRAVE_API_KEY
        self.query = query or BRAVE_SEARCH_QUERY
        self.base_url = "https://api.search.brave.com/res/v1/news/search"
        self._feed_data = None

    def fetch(self) -> Dict[str, Any]:
        """調用 API 獲取最新新聞"""
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY 未配置，無法使用 Brave Search，請檢查 .env 文件。")
            
        print(f"📥 正在透過 Brave Search 獲取新聞，關鍵字: '{self.query}'")

        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        
        params = {
            "q": self.query,
            "count": 50,           # 提升抓取數量以供後續嚴格時間過濾
            "freshness": "pd",     # 過去 24 小時內 (past day)
            "search_lang": "en",   # 確保抓取英文原版全球新聞
            "extra_snippets": 1    # 獲取更多摘要內容
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            print(f"✅ Brave Search 成功，共獲取 {len(results)} 條新聞")
            
            self._feed_data = data
            return data

        except requests.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                print(f"❌ Brave Search API 錯誤: HTTP {e.response.status_code} - {e.response.text}")
            raise Exception(f"Brave Search 獲取失敗: {e}")
        except Exception as e:
            raise Exception(f"Brave Search 解析失敗: {e}")

    def get_all_entries(self) -> list:
        """獲取所有條目"""
        if not self._feed_data:
            self.fetch()
        return self._feed_data.get("results", [])

    def get_content_by_date(self, target_date: str, feed_data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        將 Brave 返還的搜尋結果組合成單一共用的內容，供後續 Claude 分析使用
        因為 Brave 是動態搜尋所以不強制根據 target_date 嚴格過濾發佈日，而是回傳所有拿到的"過去24小時"新聞
        """
        if feed_data is None:
            feed_data = self.fetch()

        all_results = feed_data.get("results", [])
        if not all_results:
            print("❌ 未從 Brave Search 獲取到任何新聞結果")
            return None

        # 嚴格過濾 24 小時內的新聞
        recent_results = []
        for item in all_results:
            age = str(item.get("age", "")).lower()
            if not age:
                continue
                
            # 判斷是否為「24小時內」:
            # - 包含 mins, min, secs, sec, hours, hour
            # - 或是 1 day (排除 2 days, 3 days 等)
            is_recent = False
            if any(x in age for x in ["min", "sec", "hour"]):
                is_recent = True
            elif "1 day" in age and "days" not in age:
                is_recent = True
                
            if is_recent:
                recent_results.append(item)
                
        # 提取過濾後的前 15 條，若都被過濾掉則至少回傳原本拿到的最前面結果作為保底
        results = recent_results[:15] if recent_results else all_results[:15]
        
        print(f"🔍 經過嚴格 24 小時時間過濾，最終提取 {len(results)} 條新聞送交分析。")

        # 組合所有的 snippets 成為一整大段文字
        combined_content = ""
        for i, item in enumerate(results, 1):
            title = item.get("title", "")
            url = item.get("url", "")
            desc = item.get("description", "")
            source = item.get("meta_url", {}).get("hostname", "Unknown Source")
            
            # 加入 extra snippets 讓內文更豐富
            extra = " ".join(item.get("extra_snippets", []))
            
            combined_content += f"Article {i}:\n"
            combined_content += f"Title: {title}\n"
            combined_content += f"Source: {source}\n"
            combined_content += f"Link: {url}\n"
            combined_content += f"Content: {desc} {extra}\n"
            combined_content += "-" * 40 + "\n\n"

        return {
            "title": f"Brave Search Daily Global News ({target_date})",
            "link": "https://search.brave.com/",
            "guid": f"brave-search-{target_date}",
            "description": f"Daily global news aggregated from Brave Search for {target_date}",
            "content": combined_content,
            "pubDate": target_date
        }

    def get_latest_date(self, feed_data: Dict[str, Any] = None) -> Optional[str]:
        return "Today (Fresh)"

    def get_date_range(self, feed_data: Dict[str, Any] = None) -> tuple:
        """回傳近期的範圍，因為 freshness='pd'，直接回傳即可"""
        return ("Past 24 Hours", "Now")
