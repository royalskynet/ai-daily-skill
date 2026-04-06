#!/usr/bin/env python3
"""
Global Daily News Fetcher (Brave Search Version)
Fetches trending global news using Brave Search API.
"""
import sys
import json
import argparse
import os
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Add project root to path to import config
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.config import BRAVE_API_KEY, BRAVE_SEARCH_QUERY

class BraveFetcher:
    def __init__(self, api_key=None, query=None):
        self.api_key = api_key or BRAVE_API_KEY
        self.query = query or BRAVE_SEARCH_QUERY
        self.base_url = "https://api.search.brave.com/res/v1/news/search"

    def fetch(self):
        if not self.api_key:
            return {"error": "BRAVE_API_KEY_NOT_SET"}
            
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        
        params = {
            "q": self.query,
            "count": 50,
            "freshness": "pd",
            "search_lang": "en",
            "extra_snippets": 1
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def format_for_claude(self, data, target_date):
        results = data.get("results", [])
        if not results:
            return None

        recent_results = []
        for item in results:
            age = str(item.get("age", "")).lower()
            if not age: continue
            is_recent = False
            if any(x in age for x in ["min", "sec", "hour"]):
                is_recent = True
            elif "1 day" in age and "days" not in age:
                is_recent = True
            if is_recent:
                recent_results.append(item)
                
        final_results = recent_results[:15] if recent_results else results[:15]
        
        combined_content = ""
        for i, item in enumerate(final_results, 1):
            title = item.get("title", "")
            url = item.get("url", "")
            desc = item.get("description", "")
            source = item.get("meta_url", {}).get("hostname", "Unknown")
            extra = " ".join(item.get("extra_snippets", []))
            
            combined_content += f"Article {i}:\nTitle: {title}\nSource: {source}\nLink: {url}\nContent: {desc} {extra}\n" + "-"*40 + "\n\n"

        return {
            "title": f"Brave Search Daily Global News ({target_date})",
            "link": "https://search.brave.com/",
            "content": combined_content,
            "pubDate": target_date
        }

def main():
    parser = argparse.ArgumentParser(description='Fetch Global News via Brave Search')
    parser.add_argument('--date', type=str, help='Target date (YYYY-MM-DD)')
    parser.add_argument('--relative', type=str, choices=['yesterday', 'today'], default='today')

    args = parser.parse_args()

    fetcher = BraveFetcher()
    raw_data = fetcher.fetch()
    
    if "error" in raw_data:
        print(json.dumps(raw_data))
        sys.exit(1)

    target_date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    content = fetcher.format_for_claude(raw_data, target_date)

    if content:
        print(json.dumps(content, indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": "no_results", "message": "No news found in the last 24h"}))

if __name__ == "__main__":
    main()
