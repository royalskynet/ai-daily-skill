"""
配置模塊 - 包含所有配置信息和主題定義
"""
import os
from dotenv import load_dotenv

# 自動加載 .env 檔案
load_dotenv()

# ============================================================================
# API 配置
# ============================================================================
ANTHROPIC_BASE_URL = os.getenv(
    "ANTHROPIC_BASE_URL",
    "https://api.anthropic.com"
)
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", os.getenv("ZHIPU_API_KEY"))

# Claude 模型配置
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
CLAUDE_MAX_TOKENS = 8192

# ============================================================================
# Brave Search API 配置
# ============================================================================
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")
BRAVE_SEARCH_QUERY = os.getenv("BRAVE_SEARCH_QUERY", "top trending global news, Taiwan latest news, cryptocurrency blockchain regulation")

# ============================================================================
# 輸出配置
# ============================================================================
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "docs")
GITHUB_PAGES_URL = os.getenv("GITHUB_PAGES_URL", "")

# ============================================================================
# 郵件通知配置
# ============================================================================
def _get_env_int(key: str, default: int) -> int:
    """獲取整數環境變量，處理空字符串情況"""
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return int(value)


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = _get_env_int("SMTP_PORT", 587)
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
NOTIFICATION_TO = os.getenv("NOTIFICATION_TO")

# ============================================================================
# Telegram 通知配置
# ============================================================================
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

# ============================================================================
# 8種主題配色方案
# ============================================================================
THEMES = {
    "blue": {
        "name": "柔和藍色",
        "description": "適用於科技/商務/數據類內容",
        "glow_start": "#0A1929",
        "glow_end": "#1A3A52",
        "title": "#FFFFFF",
        "text": "#E3F2FD",
        "accent": "#42A5F5",
        "secondary": "#B0BEC5",
        "gradient": "linear-gradient(135deg, #0A1929 0%, #1A3A52 100%)"
    },
    "indigo": {
        "name": "深靛藍",
        "description": "適用於高端/企業/權威類內容",
        "glow_start": "#0F1C3F",
        "glow_end": "#1A2F5A",
        "title": "#FFFFFF",
        "text": "#E3F2FD",
        "accent": "#5C9FE5",
        "secondary": "#BBDEFB",
        "gradient": "linear-gradient(135deg, #0F1C3F 0%, #1A2F5A 100%)"
    },
    "purple": {
        "name": "優雅紫色",
        "description": "適用於創意/奢華/創新類內容",
        "glow_start": "#1A0A28",
        "glow_end": "#2D1B3D",
        "title": "#FFFFFF",
        "text": "#F3E5F5",
        "accent": "#B39DDB",
        "secondary": "#D1C4E9",
        "gradient": "linear-gradient(135deg, #1A0A28 0%, #2D1B3D 100%)"
    },
    "green": {
        "name": "清新綠色",
        "description": "適用於健康/可持續/成長類內容",
        "glow_start": "#0D1F12",
        "glow_end": "#1B3A26",
        "title": "#FFFFFF",
        "text": "#E8F5E9",
        "accent": "#66BB6A",
        "secondary": "#C8E6C9",
        "gradient": "linear-gradient(135deg, #0D1F12 0%, #1B3A26 100%)"
    },
    "orange": {
        "name": "溫暖橙色",
        "description": "適用於活力/熱情/社交類內容",
        "glow_start": "#1F1410",
        "glow_end": "#3D2415",
        "title": "#FFFFFF",
        "text": "#FFF3E0",
        "accent": "#FFA726",
        "secondary": "#FFCCBC",
        "gradient": "linear-gradient(135deg, #1F1410 0%, #3D2415 100%)"
    },
    "pink": {
        "name": "玫瑰粉色",
        "description": "適用於生活/美妝/健康類內容",
        "glow_start": "#1F0A14",
        "glow_end": "#3D1528",
        "title": "#FFFFFF",
        "text": "#FCE4EC",
        "accent": "#F06292",
        "secondary": "#F8BBD0",
        "gradient": "linear-gradient(135deg, #1F0A14 0%, #3D1528 100%)"
    },
    "teal": {
        "name": "冷色青綠",
        "description": "適用於金融/信任/穩定類內容",
        "glow_start": "#0A1F1F",
        "glow_end": "#164E4D",
        "title": "#FFFFFF",
        "text": "#E0F2F1",
        "accent": "#26A69A",
        "secondary": "#B2DFDB",
        "gradient": "linear-gradient(135deg, #0A1F1F 0%, #164E4D 100%)"
    },
    "gray": {
        "name": "中性灰色",
        "description": "適用於極簡/專業/通用類內容",
        "glow_start": "#1A1A1D",
        "glow_end": "#2D2D30",
        "title": "#FFFFFF",
        "text": "#F5F5F5",
        "accent": "#9E9E9E",
        "secondary": "#E0E0E0",
        "gradient": "linear-gradient(135deg, #1A1A1D 0%, #2D2D30 100%)"
    }
}

# ============================================================================
# 資訊分類定義
# ============================================================================
CATEGORIES = {
    "world": {
        "name": "國際要聞",
        "icon": "🌎",
        "description": "全球政治/外事/重大事件"
    },
    "finance": {
        "name": "經濟財經",
        "icon": "📈",
        "description": "股市/匯市/宏觀經濟/商業動態"
    },
    "tech": {
        "name": "科技創新",
        "icon": "🚀",
        "description": "科技新品/AI/互聯網/未來技術"
    },
    "lifestyle": {
        "name": "社會生活",
        "icon": "🏠",
        "description": "社會新聞/生活方式/健康/環境"
    },
    "sports": {
        "name": "體育競技",
        "icon": "⚽",
        "description": "全球賽事/體壇明星/體制變動"
    },
    "entertainment": {
        "name": "娛樂影視",
        "icon": "🎬",
        "description": "電影/音樂/名人/文化"
    }
}

# ============================================================================
# 內容類型到主題的映射
# ============================================================================
CATEGORY_THEME_MAP = {
    "world": "indigo",      # 國際要聞
    "finance": "teal",      # 經濟財經
    "tech": "blue",         # 科技創新
    "lifestyle": "green",   # 社會生活
    "sports": "orange",     # 體育競技
    "entertainment": "purple", # 娛樂影視
}

# ============================================================================
# 默認主題（當無法判斷內容類型時使用）
# ============================================================================
DEFAULT_THEME = "blue"

# ============================================================================
# 網站元信息
# ============================================================================
SITE_META = {
    "title": "Global Daily",
    "subtitle": "全球熱門資訊日報",
    "description": "每日全球前沿熱點，智能分類，快速掌握核心動態",
    "author": "Global Daily",
    "keywords": ["Global News", "全球資訊", "熱點日報", "每日新聞", "動態摘要"]
}

# ============================================================================
# HTML 模板配置
# ============================================================================
HTML_TEMPLATE_CONFIG = {
    "lang": "zh-CN",
    "charset": "UTF-8",
    "viewport": "width=device-width, initial-scale=1.0"
}

# ============================================================================
# 圖片生成 API 配置 (Firefly Card API)
# ============================================================================
FIREFLY_API_URL = os.getenv("FIREFLY_API_URL", "https://fireflycard-api.302ai.cn/api/saveImg")
FIREFLY_API_KEY = os.getenv("FIREFLY_API_KEY", "")  # 如果需要 API Key

# Firefly Card API 默認配置
FIREFLY_DEFAULT_CONFIG = {
    "font": "SourceHanSerifCN_Bold",
    "align": "left",
    "width": 1080,
    "height": 1350,
    "fontScale": 1.2,
    "ratio": "4:5",
    "padding": 30,
    "switchConfig": {
        "showIcon": False,
        "showTitle": False,
        "showContent": True,
        "showTranslation": False,
        "showAuthor": False,
        "showQRCode": False,
        "showSignature": False,
        "showQuotes": False,
        "showWatermark": False
    },
    "temp": "tempBlackSun",
    "fonts": {
        "title": 2.1329337874720125,
        "content": 1.9079435748084854,
        "translate": 1.1415042034904328,
        "author": 0.801229782035275
    },
    "textColor": "rgba(0,0,0,0.8)",
    "subTempId": "tempBlackSun",
    "borderRadius": 15,
    "color": "pure-ray-1",
    "useFont": "SourceHanSerifCN_Bold",
    "useLoadingFont": True
}

# 是否啟用圖片生成功能
ENABLE_IMAGE_GENERATION = os.getenv("ENABLE_IMAGE_GENERATION", "false").lower() == "true"


def get_theme(theme_name: str) -> dict:
    """獲取指定主題配置"""
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])


def get_category_info(category_key: str) -> dict:
    """獲取分類信息"""
    return CATEGORIES.get(category_key, CATEGORIES["model"])


def guess_theme_from_content(content_analysis: dict) -> str:
    """根據內容分析結果猜測最佳主題"""
    if not content_analysis or "categories" not in content_analysis:
        return DEFAULT_THEME

    categories = content_analysis.get("categories", [])
    if not categories:
        return DEFAULT_THEME

    # 找到包含最多資訊的分類
    max_category = max(categories, key=lambda x: len(x.get("items", [])))
    category_key = max_category.get("key", "")

    return CATEGORY_THEME_MAP.get(category_key, DEFAULT_THEME)
