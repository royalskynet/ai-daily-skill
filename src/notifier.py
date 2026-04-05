"""
郵件通知模塊
發送任務執行結果的郵件通知
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional

from src.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    NOTIFICATION_TO,
    GITHUB_PAGES_URL
)


class EmailNotifier:
    """郵件通知器"""

    def __init__(
        self,
        host: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
        to_email: str = None
    ):
        """
        初始化郵件通知器

        Args:
            host: SMTP 伺服器地址
            port: SMTP 埠
            user: 發件郵箱
            password: 郵箱密碼/授權碼
            to_email: 收件郵箱
        """
        self.host = host or SMTP_HOST
        self.port = port or SMTP_PORT
        self.user = user or SMTP_USER
        self.password = password or SMTP_PASSWORD
        self.to_email = to_email or NOTIFICATION_TO

        # GitHub Actions 環境變量（用於生成日誌連結）
        self.github_repository = os.getenv("GITHUB_REPOSITORY")
        self.github_run_id = os.getenv("GITHUB_RUN_ID")
        self.github_server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com")

    def _get_actions_url(self) -> Optional[str]:
        """獲取 GitHub Actions 運行日誌連結"""
        if self.github_repository and self.github_run_id:
            return f"{self.github_server_url}/{self.github_repository}/actions/runs/{self.github_run_id}"
        return None

    def _get_page_url(self, date: str) -> str:
        """獲取生成的頁面 URL"""
        base_url = GITHUB_PAGES_URL or os.getenv("GITHUB_PAGES_URL", "")
        if base_url:
            return f"{base_url.rstrip('/')}/{date}.html"
        return f"{date}.html"

    def send_success(self, date: str, summary_count: int) -> bool:
        """
        發送成功通知

        Args:
            date: 日期
            summary_count: 資訊條數

        Returns:
            是否發送成功
        """
        page_url = self._get_page_url(date)
        subject = f"✅ AI Daily 生成成功 - {date}"

        body = f"""
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif; margin: 0; padding: 0; background: #f5f5f5;">
    <div style="max-width: 600px; margin: 40px auto; padding: 0; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 20px rgba(0,0,0,0.08);">
        <!-- 頭部 -->
        <div style="background: linear-gradient(135deg, #42A5F5, #1A3A52); padding: 30px; text-align: center;">
            <span style="font-size: 48px;">✅</span>
            <h1 style="color: white; margin: 16px 0 0; font-size: 24px;">AI Daily 生成成功</h1>
        </div>

        <!-- 內容 -->
        <div style="padding: 30px;">
            <div style="background: #E3F2FD; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                <p style="margin: 5px 0; color: #1565C0;"><strong>📅 日期:</strong> {date}</p>
                <p style="margin: 5px 0; color: #1565C0;"><strong>📊 資訊條數:</strong> {summary_count} 條</p>
            </div>

            <p style="color: #555; margin-bottom: 16px;"><strong>🔗 訪問連結:</strong></p>
            <a href="{page_url}" style="display: block; padding: 14px 24px; background: #42A5F5; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-weight: 500;">查看 AI Daily 頁面</a>

            <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">

            <p style="color: #999; font-size: 12px; margin: 0;">
                此郵件由 GitHub Actions 自動發送<br>
                時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
            </p>
        </div>
    </div>
</body>
</html>
"""

        return self._send(subject, body)

    def send_empty(self, date: str, reason: str = "RSS中未找到對應日期的資訊") -> bool:
        """
        發送空數據通知

        Args:
            date: 日期
            reason: 原因

        Returns:
            是否發送成功
        """
        subject = f"📭 AI Daily 無數據 - {date}"
        actions_url = self._get_actions_url()

        actions_button = ""
        if actions_url:
            actions_button = f'<a href="{actions_url}" style="display: inline-block; padding: 10px 20px; background: #FFA726; color: white; text-decoration: none; border-radius: 6px;">查看 Actions 日誌</a>'

        body = f"""
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif; margin: 0; padding: 0; background: #f5f5f5;">
    <div style="max-width: 600px; margin: 40px auto; padding: 0; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 20px rgba(0,0,0,0.08);">
        <!-- 頭部 -->
        <div style="background: linear-gradient(135deg, #FFA726, #3D2415); padding: 30px; text-align: center;">
            <span style="font-size: 48px;">📭</span>
            <h1 style="color: white; margin: 16px 0 0; font-size: 24px;">今日暫無資訊</h1>
        </div>

        <!-- 內容 -->
        <div style="padding: 30px;">
            <div style="background: #FFF3E0; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                <p style="margin: 5px 0; color: #E65100;"><strong>📅 目標日期:</strong> {date}</p>
                <p style="margin: 5px 0; color: #E65100;"><strong>📝 原因:</strong> {reason}</p>
            </div>

            <div style="text-align: center;">
                {actions_button}
            </div>

            <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">

            <p style="color: #999; font-size: 12px; margin: 0; text-align: center;">
                此郵件由 GitHub Actions 自動發送
            </p>
        </div>
    </div>
</body>
</html>
"""

        return self._send(subject, body)

    def send_error(self, date: str, error: str) -> bool:
        """
        發送錯誤通知（帶 GitHub Actions 日誌連結）

        Args:
            date: 日期
            error: 錯誤信息

        Returns:
            是否發送成功
        """
        subject = f"❌ AI Daily 生成失敗 - {date}"
        actions_url = self._get_actions_url()

        actions_section = ""
        if actions_url:
            actions_section = f'''
                <div style="text-align: center; margin-top: 24px;">
                    <a href="{actions_url}" style="display: inline-block; padding: 14px 28px; background: linear-gradient(135deg, #F06292, #E91E63); color: white; text-decoration: none; border-radius: 8px; font-weight: 500;">🔍 查看 GitHub Actions 日誌</a>
                </div>
            '''

        body = f"""
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif; margin: 0; padding: 0; background: #fafafa;">
    <div style="max-width: 600px; margin: 40px auto; padding: 0; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 20px rgba(0,0,0,0.08);">
        <!-- 頭部 -->
        <div style="background: linear-gradient(135deg, #F06292, #C62828); padding: 30px; text-align: center;">
            <span style="font-size: 48px;">❌</span>
            <h1 style="color: white; margin: 16px 0 0; font-size: 24px;">生成過程出錯</h1>
        </div>

        <!-- 內容 -->
        <div style="padding: 30px;">
            <div style="background: #FFEBEE; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                <p style="margin: 5px 0; color: #C62828;"><strong>📅 目標日期:</strong> {date}</p>
                <p style="margin: 5px 0; color: #C62828;"><strong>⏰ 時間:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
            </div>

            <p style="color: #555; margin-bottom: 12px;"><strong>錯誤信息:</strong></p>
            <pre style="background: #263238; color: #ECEFF1; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 13px; line-height: 1.5; margin-bottom: 20px;">{self._escape_html(error)}</pre>

            {actions_section}

            <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">

            <p style="color: #999; font-size: 12px; margin: 0; text-align: center;">
                請檢查 GitHub Actions 日誌獲取詳細信息
            </p>
        </div>
    </div>
</body>
</html>
"""

        return self._send(subject, body)

    def _is_configured(self) -> bool:
        """檢查郵件是否已配置"""
        return all([self.host, self.user, self.password, self.to_email])

    def _send(self, subject: str, html_body: str) -> bool:
        """
        發送郵件的底層方法

        Args:
            subject: 郵件主題
            html_body: HTML 郵件正文

        Returns:
            是否發送成功
        """
        # 檢查配置，未配置則靜默跳過
        if not self._is_configured():
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.user
            msg['To'] = self.to_email

            msg.attach(MIMEText(html_body, 'html', 'utf-8'))

            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)

            print(f"✅ 郵件已發送: {subject}")
            return True

        except Exception as e:
            print(f"❌ 郵件發送失敗: {e}")
            return False

    def _escape_html(self, text: str) -> str:
        """轉義 HTML 特殊字符"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#x27;'))


def send_success_email(date: str, summary_count: int) -> bool:
    """便捷函數：發送成功通知"""
    notifier = EmailNotifier()
    return notifier.send_success(date, summary_count)


def send_empty_email(date: str, reason: str = "") -> bool:
    """便捷函數：發送空數據通知"""
    notifier = EmailNotifier()
    return notifier.send_empty(date, reason)


def send_error_email(date: str, error: str) -> bool:
    """便捷函數：發送錯誤通知"""
    notifier = EmailNotifier()
    return notifier.send_error(date, error)
