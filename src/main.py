#!/usr/bin/env python3
"""
AI Daily 主入口
自動獲取 AI 資訊並生成精美的 HTML 頁面
"""
import sys
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 添加項目根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import (
    CLAUDE_API_KEY,
    OUTPUT_DIR,
    ENABLE_IMAGE_GENERATION,
    GITHUB_PAGES_URL
)
from src.brave_fetcher import BraveFetcher
from src.claude_analyzer import ClaudeAnalyzer
from src.html_generator import HTMLGenerator
from src.notifier import EmailNotifier
from src.tg_notifier import TelegramNotifier
from src.image_generator import ImageGenerator
from src.instagram_generator import InstagramGenerator


def print_banner():
    """列印程序橫幅"""
    banner = """
╔════════════════════════════════════════════════════════════╗
║                                                              ║
║   AI Daily - AI 資訊日報自動生成器                          ║
║                                                              ║
║   自動獲取全球重點新聞 · Claude 智能分析                    ║
║   精美 HTML 頁面 · 自動部署                                 ║
║                                                              ║
╚════════════════════════════════════════════════════════════╝
"""
    print(banner)


def get_target_date(days_offset: int = 2) -> str:
    """
    獲取目標日期

    Args:
        days_offset: 向前偏移的天數，默認2天

    Returns:
        格式化的日期字符串 (YYYY-MM-DD)
    """
    target_date = (datetime.now(timezone.utc) - timedelta(days=days_offset))
    return target_date.strftime("%Y-%m-%d")


def main():
    """主函數"""
    print_banner()

    # 檢查環境變量
    if not CLAUDE_API_KEY:
        print("❌ 錯誤: CLAUDE_API_KEY 環境變量未設置")
        print("   請設置 Claude 的 API Key")
        sys.exit(1)

    # 初始化組件
    notifier = EmailNotifier()
    tg_notifier = TelegramNotifier()
    email_enabled = notifier._is_configured()
    tg_enabled = tg_notifier.is_enabled
    image_enabled = ENABLE_IMAGE_GENERATION
    total_steps = 6 if (email_enabled or tg_enabled) else 5
    if image_enabled:
        total_steps += 1

    try:
        # 1. 計算目標日期 (今天 - 2天)
        target_date = get_target_date(days_offset=2)
        print(f"[目標日期] {target_date}")
        print(f"   (北京時間: {datetime.now(timezone.utc) + timedelta(hours=8)} + 8h)")
        print()

        # 2. 獲取資訊 (使用 Brave Search)
        print(f"[步驟 1/{total_steps}] 透過 Brave 獲取最新全球新聞...")
        fetcher = BraveFetcher()
            
        fetched_data = fetcher.fetch()

        # 顯示日期範圍資訊
        date_range = fetcher.get_date_range(fetched_data)
        if date_range[0] and date_range[1]:
            print(f"   來源搜尋/日期範圍: {date_range[0]} ~ {date_range[1]}")
        print()

        # 3. 查找目標日期的內容
        print(f"[步驟 2/{total_steps}] 整理目標日期的資訊內容...")
        content = fetcher.get_content_by_date(target_date, fetched_data)

        if not content:
            print("   目標日期無內容，生成空頁面")
            if email_enabled:
                notifier.send_empty(
                    target_date,
                    f"未找到 {target_date} 的全球新聞內容。"
                    f"可分析的日期範圍: {date_range[0]} ~ {date_range[1]}"
                )

            # 生成空頁面
            generator = HTMLGenerator()
            generator.generate_css()
            generator.generate_empty(target_date)
            generator.update_index(target_date, {"summary": ["暫無資訊"]})

            print("   完成")
            return

        print(f"   找到資訊: {content.get('title', '')[:60]}...")
        print()

        # 4. 調用 Claude 分析
        print(f"[步驟 3/{total_steps}] 調用 Claude 進行智能分析...")
        analyzer = ClaudeAnalyzer()
        result = analyzer.analyze(content, target_date)

        # 檢查分析狀態
        if result.get("status") == "empty":
            print("   分析結果為空")
            if email_enabled:
                notifier.send_empty(target_date, result.get("reason", "內容分析為空"))
            return

        print()

        # 5. 生成 HTML
        print(f"[步驟 4/{total_steps}] 生成 HTML 頁面...")
        generator = HTMLGenerator()
        generator.generate_css()

        # 生成日報頁面
        html_path = generator.generate_daily(result)
        print(f"   文件路徑: {html_path}")
        print()

        # 計算總資訊數
        total_items = sum(
            len(cat.get('items', []))
            for cat in result.get('categories', [])
        )

        # 6. 生成分享圖片（可選）
        image_path = None
        xhs_path = None
        if image_enabled:
            print(f"[步驟 5/{total_steps}] 生成分享卡片圖片...")
            image_gen = ImageGenerator()
            image_path = image_gen.generate_from_analysis_result(
                result,
                output_path=str(Path(OUTPUT_DIR) / "images" / f"{target_date}.png")
            )
            if image_path:
                print(f"   圖片已保存: {image_path}")
            else:
                print("   圖片生成失敗或跳過")

            # 生成 INSTAGRAM 封面
            print(f"   生成 INSTAGRAM 封面...")
            ig_gen = InstagramGenerator()
            ig_path = ig_gen.generate(result)
            print(f"   INSTAGRAM 封面: {ig_path}")
            print()
        else:
            print("   (圖片生成未啟用，跳過)")
            print()

        # 7. 發送成功通知（可選）
        if email_enabled or tg_enabled:
            step_num = 6 if image_enabled else 5
            print(f"[步驟 {step_num}/{total_steps}] 發送通知...")
            if email_enabled:
                print("   發郵件送通知...")
                notifier.send_success(target_date, total_items)
            if tg_enabled:
                url = f"{GITHUB_PAGES_URL}/{target_date}.html" if GITHUB_PAGES_URL else None
                tg_notifier.send_daily_summary(result, target_date, url)
            print()
        else:
            print("   (通知未配置，跳過)")
            print()

        # 完成
        print("╔════════════════════════════════════════════════════════════╗")
        print("║                                                              ║")
        print("║   ✅ 任務完成!                                              ║")
        print("║                                                              ║")
        print(f"║   日期: {target_date}                                        ║")
        print(f"║   資訊數: {total_items} 條                                          ║")
        print(f"║   主題: {result.get('theme', 'blue')}                                                ║")
        print("║                                                              ║")
        print("╚════════════════════════════════════════════════════════════╝")

    except KeyboardInterrupt:
        print("\n⚠️ 用戶中斷")
        sys.exit(130)

    except Exception as e:
        print(f"\n[錯誤] 執行過程出錯: {e}")
        import traceback
        traceback.print_exc()

        # 發送錯誤通知（如果配置了郵件）
        if email_enabled:
            try:
                target_date = get_target_date(days_offset=2)
                notifier.send_error(target_date, str(e))
            except:
                pass

        sys.exit(1)


if __name__ == "__main__":
    main()
