"""
Telegram 發送模塊
"""
import requests
from typing import Dict, Any

from src.config import TG_BOT_TOKEN, TG_CHAT_ID

class TelegramNotifier:
    def __init__(self):
        self.bot_token = TG_BOT_TOKEN
        self.chat_id = TG_CHAT_ID
        self.is_enabled = bool(self.bot_token and self.chat_id)

    def send_daily_summary(self, result: Dict[str, Any], date: str, url: str = None):
        if not self.is_enabled:
            return

        summaries = result.get("summary", [])
        
        lines = [f"🤖 *AI Daily 重點摘要 ({date})*"]
        for s in summaries:
            lines.append(f"• {s}")
            
        if url:
            lines.append("")
            lines.append(f"🔗 [閱讀完整網頁版]({url})")
            
        text = "\n".join(lines)
        
        try:
            print(f"   正在發送 Telegram 通知...")
            api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
            resp = requests.post(api_url, json=payload, timeout=10)
            resp.raise_for_status()
            print("   ✅ Telegram 摘要推送成功")
        except Exception as e:
            print(f"   ❌ Telegram 推送失敗: {e}")
