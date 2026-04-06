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
            "freshness": "pw",     # 抓取過去一週以滿足 72 小時需求
            "search_lang": "en",   # 確保抓取英文原版全球新聞
            "extra_snippets": 1    # 仍抓取但後續過濾時精簡使用
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

        # 嚴格過濾 72 小時 (3 天) 內的新聞並排序
        recent_results = []
        for item in all_results:
            age = str(item.get("age", "")).lower()
            if not age:
                continue
                
            # 判斷是否為「72小時 (3天) 內」:
            # - 包含 mins, min, secs, sec, hours, hour
            # - 或是 1 day, 2 days, 3 days
            is_recent = False
            if any(x in age for x in ["min", "sec", "hour"]):
                is_recent = True
            elif any(x in age for x in ["1 day", "2 days", "3 days"]):
                is_recent = True
                
            if is_recent:
                recent_results.append(item)
        
        # 排序：解析 age 字串，越新的在最前面
        def parse_age_to_minutes(age_str):
            age_str = age_str.lower()
            import re
            match = re.search(r"(\d+)\s*(min|hour|day|sec)", age_str)
            if not match: return 999999
            val = int(match.group(1))
            unit = match.group(2)
            if "sec" in unit: return val / 60
            if "min" in unit: return val
            if "hour" in unit: return val * 60
            if "day" in unit: return val * 1440
            return 999999

        recent_results.sort(key=lambda x: parse_age_to_minutes(str(x.get("age", ""))))
                
        # 提取前 20 則 (減少內容體積)
        results = recent_results[:20] if recent_results else all_results[:20]
        
        print(f"🔍 經過 72 小時過濾與排序，最終提取 {len(results)} 則精簡資料送交分析。")

        # 組合極簡內容以節省 Token
        combined_content = ""
        for i, item in enumerate(results, 1):
            title = item.get("title", "")
            url = item.get("url", "")
            # 僅保留極簡摘要以節省 Token
            desc = item.get("description", "")[:250]
            age = item.get("age", "N/A")
            source = item.get("meta_url", {}).get("hostname", "Unknown")
            
            combined_content += f"No.{i}: {title}\n"
            combined_content += f"S:{source} | T:{age} | U:{url}\n"
            combined_content += f"C: {desc}...\n"
            combined_content += "-" * 10 + "\n"

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
