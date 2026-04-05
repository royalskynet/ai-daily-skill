"""
圖片生成模塊
使用 Firefly Card API 將 Markdown 內容轉換為精美圖片
根據內容長度和結構智能調整尺寸和排版參數
"""
import os
import base64
import requests
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

from src.config import (
    FIREFLY_API_URL,
    FIREFLY_API_KEY,
    FIREFLY_DEFAULT_CONFIG,
    ENABLE_IMAGE_GENERATION,
    OUTPUT_DIR
)


@dataclass
class ContentAnalysis:
    """內容分析結果"""
    total_lines: int          # 總行數
    content_lines: int        # 內容行數（不含空行）
    headings: Dict[str, int]  # 各級標題數量
    list_items: int           # 列表項數量
    categories: int           # 分類數量
    max_line_length: int      # 最長行字符數
    total_chars: int          # 總字符數
    complexity: str           # 複雜度：simple/standard/detailed/complete


class ImageGenerator:
    """Firefly Card API 圖片生成器"""

    # 尺寸配置
    MIN_WIDTH = 1080
    MAX_WIDTH = 1080
    MIN_HEIGHT = 1350
    MAX_HEIGHT = 3000

    # 排版常量（基於中文閱讀習慣）
    # 中文閱讀舒適寬度：每行 20-28 個漢字
    CHAR_PER_LINE = 24        # 每行目標字符數
    AVG_CHAR_WIDTH = 16       # 平均字符寬度（像素）- 增加以適應實際渲染
    LINE_HEIGHT_RATIO = 1.8   # 行高與字號比 - 增加以獲得更好效果
    PADDING_RATIO = 0.08      # 邊距佔寬度比例 - 減少 padding

    def __init__(self, api_url: str = None, api_key: str = None):
        """
        初始化圖片生成器

        Args:
            api_url: Firefly API 地址
            api_key: API 密鑰（如果需要）
        """
        self.api_url = api_url or FIREFLY_API_URL
        self.api_key = api_key or FIREFLY_API_KEY
        self.default_config = FIREFLY_DEFAULT_CONFIG.copy()
        self.enabled = ENABLE_IMAGE_GENERATION

    def _analyze_content(self, content: str) -> ContentAnalysis:
        """
        分析內容結構

        Args:
            content: Markdown 內容

        Returns:
            內容分析結果
        """
        lines = content.split('\n')
        analysis = ContentAnalysis(
            total_lines=len(lines),
            content_lines=0,
            headings={"#": 0, "##": 0, "###": 0},
            list_items=0,
            categories=0,
            max_line_length=0,
            total_chars=0,
            complexity="simple"
        )

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            analysis.content_lines += 1
            analysis.total_chars += len(stripped)
            analysis.max_line_length = max(analysis.max_line_length, len(stripped))

            # 統計標題
            if stripped.startswith("# "):
                analysis.headings["#"] += 1
            elif stripped.startswith("## "):
                analysis.headings["##"] += 1
            elif stripped.startswith("### "):
                analysis.headings["###"] += 1
                analysis.categories += 1
            # 統計列表項
            elif stripped.startswith("- ") or stripped.startswith("* "):
                analysis.list_items += 1

        # 判斷複雜度
        if analysis.content_lines < 12:
            analysis.complexity = "simple"
        elif analysis.content_lines < 22:
            analysis.complexity = "standard"
        elif analysis.content_lines < 38:
            analysis.complexity = "detailed"
        else:
            analysis.complexity = "complete"

        return analysis

    def _get_optimal_config(self, analysis: ContentAnalysis) -> Dict[str, Any]:
        """
        根據內容分析結果獲取最優配置

        Args:
            analysis: 內容分析結果

        Returns:
            最優配置字典
        """
        configs = {
            "simple": {
                "width": 1080,
                "padding": 60,
                "fontScale": 1.4,
                "base_height": 200,
                "line_height": 40,
            },
            "standard": {
                "width": 1080,
                "padding": 60,
                "fontScale": 1.4,
                "base_height": 200,
                "line_height": 40,
            },
            "detailed": {
                "width": 1080,
                "padding": 60,
                "fontScale": 1.3,
                "base_height": 220,
                "line_height": 38,
            },
            "complete": {
                "width": 1080,
                "padding": 50,
                "fontScale": 1.2,
                "base_height": 240,
                "line_height": 36,
            }
        }

        base_config = configs.get(analysis.complexity, configs["standard"])

        # 根據最長行調整寬度
        # 確保最長行能舒適顯示（每行約 CHAR_PER_LINE 個字符）
        min_width_for_content = analysis.max_line_length * self.AVG_CHAR_WIDTH
        adjusted_width = max(base_config["width"], min_width_for_content)
        adjusted_width = min(adjusted_width, self.MAX_WIDTH)

        # 動態調整 padding（保持 5-10% 的比例，更節省空間）
        adjusted_padding = int(adjusted_width * self.PADDING_RATIO)
        adjusted_padding = max(14, min(adjusted_padding, 28))

        return {
            "width": adjusted_width,
            "padding": adjusted_padding,
            "fontScale": base_config["fontScale"],
            "base_height": base_config["base_height"],
            "line_height": base_config["line_height"],
            "complexity": analysis.complexity
        }

    def _calculate_dimensions(self, content: str) -> Tuple[int, int, str, Dict[str, Any]]:
        """
        計算最佳圖片尺寸和配置

        Args:
            content: Markdown 內容

        Returns:
            (width, height, ratio, config)
        """
        # 分析內容
        analysis = self._analyze_content(content)

        # 獲取最優配置
        opt_config = self._get_optimal_config(analysis)

        width = opt_config["width"]
        padding = opt_config["padding"]
        base_height = opt_config["base_height"]
        line_height = opt_config["line_height"]

        # 計算有效內容寬度
        content_width = width - 2 * padding

        # 計算需要的行數（考慮換行，使用保守估算）
        estimated_lines = 0

        for line in content.split('\n'):
            stripped = line.strip()
            if not stripped:
                # 空行也佔用空間
                estimated_lines += 0.5
                continue

            # 去除 Markdown 標記後的純文本長度
            text_len = len(stripped)

            # 根據元素類型估算行數（使用保守值，乘以係數增加餘量）
            if stripped.startswith("# "):
                estimated_lines += 3.0  # 一級標題佔位更多
            elif stripped.startswith("## "):
                estimated_lines += 2.5
            elif stripped.startswith("### "):
                estimated_lines += 2.0
            elif stripped.startswith("- ") or stripped.startswith("* "):
                # 列表項需要考慮換行，使用 1.5 倍餘量
                lines_needed = max(1.5, (text_len * self.AVG_CHAR_WIDTH * 1.5) / content_width)
                estimated_lines += lines_needed
            elif stripped.startswith("**"):
                # 粗體標題
                lines_needed = max(1.5, (text_len * self.AVG_CHAR_WIDTH * 1.3) / content_width)
                estimated_lines += lines_needed
            else:
                # 普通文本，使用 1.3 倍餘量
                lines_needed = max(1.3, (text_len * self.AVG_CHAR_WIDTH * 1.3) / content_width)
                estimated_lines += lines_needed

        # 計算高度，增加 20% 安全餘量
        content_height = int(estimated_lines * line_height * 1.2)
        total_height = base_height + content_height

        # 限制高度範圍
        total_height = max(self.MIN_HEIGHT, min(total_height, self.MAX_HEIGHT))

        # 強制使用 4:5 比例適合 Instagram
        ratio = "4:5"

        # 列印調試信息
        print(f"   內容分析: 複雜度={analysis.complexity}, 行數={analysis.content_lines}")
        print(f"   尺寸配置: {width}x{total_height}, padding={padding}, ratio={ratio}")

        return width, total_height, ratio, opt_config

    def generate(
        self,
        markdown_content: str,
        output_path: str = None,
        custom_config: Dict[str, Any] = None
    ) -> Optional[str]:
        """
        生成圖片

        Args:
            markdown_content: Markdown 格式的內容
            output_path: 圖片保存路徑，默認為 docs/images/{date}.png
            custom_config: 自定義配置，會與智能配置合併

        Returns:
            成功返回圖片保存路徑，失敗返回 None
        """
        if not self.enabled:
            print("   圖片生成功能未啟用，跳過")
            return None

        if not markdown_content or not markdown_content.strip():
            print("   內容為空，跳過圖片生成")
            return None

        # 構建請求數據
        request_data = self.default_config.copy()

        # 計算最佳尺寸和配置
        width, height, ratio, opt_config = self._calculate_dimensions(markdown_content)

        # 應用智能配置
        request_data["width"] = width
        request_data["height"] = height
        request_data["ratio"] = ratio
        request_data["padding"] = opt_config["padding"]
        request_data["fontScale"] = opt_config["fontScale"]

        # 用戶自定義配置可以覆蓋
        if custom_config:
            request_data.update(custom_config)

        request_data["content"] = markdown_content

        # 如果有 API Key，添加到請求頭
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            print(f"   正在調用 Firefly API 生成圖片...")
            print(f"   API URL: {self.api_url}")

            response = requests.post(
                self.api_url,
                json=request_data,
                headers=headers,
                timeout=60
            )

            # 檢查響應狀態
            response.raise_for_status()

            # 檢查 Content-Type
            content_type = response.headers.get('Content-Type', '')

            # 如果直接返回二進位圖片流
            if 'image/' in content_type:
                image_bytes = response.content

                # 確定保存路徑
                if not output_path:
                    output_dir = Path(OUTPUT_DIR) / "images"
                    output_dir.mkdir(parents=True, exist_ok=True)
                    # 使用日期作為文件名
                    from datetime import datetime
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    output_path = str(output_dir / f"{date_str}.png")

                # 保存圖片
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(image_bytes)

                print(f"   圖片已保存: {output_path}")
                print(f"   文件大小: {len(image_bytes)} bytes")
                return output_path

            # 如果返回 JSON（兼容其他可能的響應格式）
            else:
                result = response.json()

                # API 返回的數據可能是 base64 編碼的圖片，或者是圖片 URL
                if "data" in result:
                    image_data = result["data"]

                    if isinstance(image_data, str) and image_data.startswith("http"):
                        print(f"   圖片 URL: {image_data}")
                        return image_data

                    if isinstance(image_data, str):
                        if image_data.startswith("data:image/"):
                            image_data = image_data.split(",", 1)[1]

                        image_bytes = base64.b64decode(image_data)

                        if not output_path:
                            output_dir = Path(OUTPUT_DIR) / "images"
                            output_dir.mkdir(parents=True, exist_ok=True)
                            output_path = str(output_dir / "daily-card.png")

                        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, 'wb') as f:
                            f.write(image_bytes)

                        print(f"   圖片已保存: {output_path}")
                        return output_path

                if "imageUrl" in result:
                    print(f"   圖片 URL: {result['imageUrl']}")
                    return result["imageUrl"]

                if "url" in result:
                    print(f"   圖片 URL: {result['url']}")
                    return result["url"]

                print(f"   響應 Content-Type: {content_type}")
                print(f"   響應內容: {result}")
                print("   無法從響應中提取圖片數據")
                return None

        except requests.exceptions.RequestException as e:
            print(f"   API 請求失敗: {e}")
            return None
        except Exception as e:
            print(f"   圖片生成失敗: {e}")
            return None

    def generate_from_analysis_result(
        self,
        analysis_result: Dict[str, Any],
        output_path: str = None
    ) -> Optional[str]:
        """
        從分析結果生成 Markdown 並轉換為圖片

        Args:
            analysis_result: Claude 分析結果
            output_path: 圖片保存路徑

        Returns:
            成功返回圖片路徑，失敗返回 None
        """
        markdown = self._build_card_markdown(analysis_result)
        return self.generate(markdown, output_path)

    def _build_card_markdown(self, result: Dict[str, Any]) -> str:
        """
        構建適合卡片顯示的精簡 Markdown

        Args:
            result: 分析結果

        Returns:
            Markdown 格式的字符串
        """
        date = result.get("date", "")
        summary = result.get("summary", [])
        categories = result.get("categories", [])
        keywords = result.get("keywords", [])

        # 格式化日期
        try:
            from datetime import datetime
            dt = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = f"{dt.year}年{dt.month}月{dt.day}日"
        except:
            formatted_date = date

        # 構建標題
        lines = [f"# AI Daily\n## {formatted_date}\n"]

        # 核心摘要
        if summary:
            lines.append("### 核心摘要")
            for item in summary[:5]:
                lines.append(f"- {item}")
            lines.append("")

        # 分類資訊
        for cat in categories:
            if not cat.get("items"):
                continue

            cat_name = cat.get("name", "")
            cat_items = cat.get("items", [])

            lines.append(f"### {cat_name}")
            for item in cat_items[:3]:
                title = item.get("title", "")
                lines.append(f"**{title}**")
            lines.append("")

        # 關鍵詞
        if keywords:
            lines.append(f"{' '.join(['#' + kw for kw in keywords[:8]])}")

        return "\n".join(lines)


def generate_card_image(
    markdown_content: str,
    output_path: str = None
) -> Optional[str]:
    """便捷函數：生成卡片圖片"""
    generator = ImageGenerator()
    return generator.generate(markdown_content, output_path)


def generate_card_from_analysis(
    analysis_result: Dict[str, Any],
    output_path: str = None
) -> Optional[str]:
    """便捷函數：從分析結果生成卡片圖片"""
    generator = ImageGenerator()
    return generator.generate_from_analysis_result(analysis_result, output_path)
