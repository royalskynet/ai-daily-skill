"""
INSTAGRAM風格封面生成模塊
生成適合INSTAGRAM分享的 3:4 比例封面
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from src.config import OUTPUT_DIR


class InstagramGenerator:
    """INSTAGRAM封面生成器"""

    # 帳號信息
    ACCOUNT_NAME = "極客傑尼"
    ACCOUNT_SLOGAN = "AI實戰派"

    # 尺寸配置
    COVER_WIDTH = 750
    COVER_HEIGHT = 1000  # 3:4 比例

    def __init__(self, output_dir: str = None):
        """
        初始化生成器

        Args:
            output_dir: 輸出目錄
        """
        self.output_dir = Path(output_dir or OUTPUT_DIR) / "instagram"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, analysis_result: Dict[str, Any]) -> str:
        """
        生成INSTAGRAM風格封面 HTML

        Args:
            analysis_result: Claude 分析結果

        Returns:
            生成的 HTML 文件路徑
        """
        date = analysis_result.get("date", "")
        summary = analysis_result.get("summary", [])
        keywords = analysis_result.get("keywords", [])

        # 格式化日期
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = f"{dt.month}.{dt.day}"
        except:
            formatted_date = date

        # 提取關鍵信息
        main_title = self._extract_main_title(summary)
        subtitle = self._extract_subtitle(summary)
        highlights = summary[:3] if summary else []

        # 生成 HTML
        html_content = self._build_html(
            date=formatted_date,
            main_title=main_title,
            subtitle=subtitle,
            highlights=highlights,
            keywords=keywords
        )

        # 保存文件
        filename = f"xhs-{date}.html"
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(filepath)

    def _extract_main_title(self, summary: list) -> str:
        """
        從摘要中提取主標題（2-3個關鍵詞）

        Args:
            summary: 摘要列表

        Returns:
            主標題
        """
        if not summary:
            return "AI日報"

        # 取前兩條摘要，提取關鍵詞
        text = " ".join(summary[:2])

        # 常見的高價值關鍵詞
        priority_keywords = [
            "Claude", "GPT", "OpenAI", "Anthropic", "Google",
            "發布", "開源", "更新", "突破", "首個", "首次",
            "Agent", "模型", "AI", "大模型", "多模態"
        ]

        # 提取優先關鍵詞
        found_keywords = []
        for keyword in priority_keywords:
            if keyword in text:
                found_keywords.append(keyword)
                if len(found_keywords) >= 3:
                    break

        if found_keywords:
            return " · ".join(found_keywords[:2])

        # 如果沒有找到關鍵詞，使用第一條摘要的前兩個字
        first = summary[0]
        if len(first) >= 4:
            return first[:4]

        return "AI日報"

    def _extract_subtitle(self, summary: list) -> str:
        """
        提取副標題

        Args:
            summary: 摘要列表

        Returns:
            副標題
        """
        if not summary:
            return f"{self.ACCOUNT_SLOGAN}每日更新"

        # 使用第一條摘要作為副標題，截取合適長度
        first = summary[0]
        if len(first) > 25:
            return first[:25] + "..."
        return first

    def _build_html(
        self,
        date: str,
        main_title: str,
        subtitle: str,
        highlights: list,
        keywords: list
    ) -> str:
        """
        構建 HTML 內容

        Args:
            date: 日期
            main_title: 主標題
            subtitle: 副標題
            highlights: 亮點列表
            keywords: 關鍵詞列表

        Returns:
            HTML 字符串
        """
        # 高亮關鍵詞
        highlight_spans = ""
        for i, item in enumerate(highlights[:3]):
            # 提取關鍵詞（取前6個字）
            key_text = item[:6] if len(item) > 6 else item
            highlight_spans += f'<span class="highlight-item">{key_text}</span>'

        # 關鍵詞標籤
        keyword_tags = ""
        for kw in keywords[:5]:
            keyword_tags += f'<span class="keyword-tag">#{kw}</span>'

        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Daily - INSTAGRAM封面</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans SC', sans-serif;
            background: #1a1a1a;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }}

        /* 封面畫布 - 3:4 比例 */
        .cover-canvas {{
            width: {self.COVER_WIDTH}px;
            height: {self.COVER_HEIGHT}px;
            background: #000000;
            position: relative;
            overflow: hidden;
        }}

        /* 網格背景線 */
        .grid-lines {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image:
                linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
        }}

        /* 裝飾性幾何元素 */
        .geo-circle {{
            position: absolute;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 50%;
        }}

        .geo-circle-1 {{
            width: 300px;
            height: 300px;
            top: -100px;
            right: -100px;
        }}

        .geo-circle-2 {{
            width: 200px;
            height: 200px;
            bottom: 100px;
            left: -50px;
            border-color: rgba(0, 255, 136, 0.1);
        }}

        .geo-square {{
            position: absolute;
            border: 1px solid rgba(255,255,255,0.05);
        }}

        .geo-square-1 {{
            width: 80px;
            height: 80px;
            top: 150px;
            left: 30px;
        }}

        /* 內容區域 */
        .content {{
            position: relative;
            z-index: 10;
            height: 100%;
            display: flex;
            flex-direction: column;
            padding: 50px 40px;
        }}

        /* 頂部信息 */
        .top-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 60px;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .brand-dot {{
            width: 8px;
            height: 8px;
            background: #00ff88;
        }}

        .brand-name {{
            font-size: 14px;
            font-weight: 300;
            color: rgba(255,255,255,0.6);
            letter-spacing: 2px;
        }}

        .date-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            color: rgba(255,255,255,0.4);
            font-weight: 400;
        }}

        /* 主標題區域 */
        .title-section {{
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .main-title {{
            font-size: 72px;
            font-weight: 900;
            color: #ffffff;
            line-height: 1.1;
            letter-spacing: -2px;
            margin-bottom: 30px;
            word-break: keep-all;
        }}

        .main-title .highlight {{
            color: #00ff88;
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
        }}

        /* 分割線 */
        .divider {{
            width: 60px;
            height: 3px;
            background: #00ff88;
            margin: 30px 0;
        }}

        /* 副標題 */
        .subtitle {{
            font-size: 24px;
            font-weight: 300;
            color: rgba(255,255,255,0.7);
            line-height: 1.5;
            margin-bottom: 40px;
            max-width: 80%;
        }}

        /* 亮點標籤區域 */
        .highlights {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 40px;
        }}

        .highlight-item {{
            font-size: 16px;
            color: rgba(255,255,255,0.5);
            padding: 8px 16px;
            border: 1px solid rgba(255,255,255,0.1);
            font-weight: 300;
        }}

        /* 底部區域 */
        .bottom-section {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}

        .keywords {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            max-width: 70%;
        }}

        .keyword-tag {{
            font-size: 13px;
            color: #00ff88;
            font-weight: 400;
        }}

        .account-info {{
            text-align: right;
        }}

        .account-name {{
            font-size: 14px;
            color: rgba(255,255,255,0.4);
            font-weight: 300;
            letter-spacing: 1px;
        }}

        .account-slogan {{
            font-size: 12px;
            color: #00ff88;
            margin-top: 4px;
            font-weight: 400;
        }}

        /* 裝飾性指示線 */
        .indicator-line {{
            position: absolute;
            bottom: 50px;
            left: 40px;
            width: 100px;
            height: 1px;
            background: linear-gradient(90deg, rgba(255,255,255,0.3), transparent);
        }}

        .indicator-line::after {{
            content: '';
            position: absolute;
            right: 0;
            top: -3px;
            width: 7px;
            height: 7px;
            background: #00ff88;
            border-radius: 50%;
        }}

        /* 控制面板 */
        .controls {{
            display: flex;
            gap: 15px;
            align-items: center;
        }}

        .btn {{
            padding: 12px 30px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            color: #fff;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
            font-family: 'Noto Sans SC', sans-serif;
            border-radius: 4px;
        }}

        .btn:hover {{
            background: rgba(255,255,255,0.15);
            border-color: rgba(255,255,255,0.3);
        }}

        .btn-primary {{
            background: #00ff88;
            color: #000;
            border: none;
            font-weight: 500;
        }}

        .btn-primary:hover {{
            background: #00cc6a;
        }}

        .status {{
            color: rgba(255,255,255,0.5);
            font-size: 13px;
            min-width: 150px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="cover-canvas" id="cover">
            <!-- 網格背景 -->
            <div class="grid-lines"></div>

            <!-- 幾何裝飾 -->
            <div class="geo-circle geo-circle-1"></div>
            <div class="geo-circle geo-circle-2"></div>
            <div class="geo-square geo-square-1"></div>

            <!-- 內容 -->
            <div class="content">
                <!-- 頂部信息 -->
                <div class="top-info">
                    <div class="brand">
                        <span class="brand-dot"></span>
                        <span class="brand-name">{self.ACCOUNT_NAME.upper()}</span>
                    </div>
                    <div class="date-badge">{date}</div>
                </div>

                <!-- 主標題區域 -->
                <div class="title-section">
                    <div class="main-title">{main_title}</div>
                    <div class="divider"></div>
                    <div class="subtitle">{subtitle}</div>

                    <!-- 亮點 -->
                    <div class="highlights">
                        {highlight_spans}
                    </div>
                </div>

                <!-- 底部區域 -->
                <div class="bottom-section">
                    <div class="keywords">
                        {keyword_tags}
                    </div>
                    <div class="account-info">
                        <div class="account-name">{self.ACCOUNT_NAME}</div>
                        <div class="account-slogan">{self.ACCOUNT_SLOGAN}</div>
                    </div>
                </div>

                <!-- 指示線 -->
                <div class="indicator-line"></div>
            </div>
        </div>

        <!-- 控制面板 -->
        <div class="controls">
            <button class="btn btn-primary" onclick="saveImage()">保存封面</button>
            <div class="status" id="status">點擊保存按鈕下載封面</div>
        </div>
    </div>

    <script>
        async function saveImage() {{
            const cover = document.getElementById('cover');
            const status = document.getElementById('status');

            status.textContent = '生成中...';

            try {{
                const canvas = await html2canvas(cover, {{
                    scale: 2,
                    useCORS: true,
                    backgroundColor: '#000000',
                    logging: false
                }});

                const link = document.createElement('a');
                link.download = 'ai-daily-xhs-{date}.png';
                link.href = canvas.toDataURL('image/png');
                link.click();

                status.textContent = '✓ 封面已保存';
            }} catch (error) {{
                console.error(error);
                status.textContent = '保存失敗，請重試';
            }}
        }}
    </script>
</body>
</html>'''
        return html


def generate_instagram_cover(analysis_result: Dict[str, Any], output_dir: str = None) -> str:
    """
    便捷函數：生成INSTAGRAM封面

    Args:
        analysis_result: 分析結果
        output_dir: 輸出目錄

    Returns:
        生成的 HTML 文件路徑
    """
    generator = InstagramGenerator(output_dir)
    return generator.generate(analysis_result)
