# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **圖片生成功能**
  - 集成 Firefly Card API，支持生成分享卡片圖片
  - 高度自適應：根據內容長度動態計算圖片高度（600-3000px）
  - 比例自動選擇：根據寬高比自動匹配最佳比例（1:1/3:4/2:3/9:16/9:19）
  - 智能排版配置：根據內容複雜度自動調整寬度、padding、字體縮放
  - 純黑太陽主題 (tempBlackSun)，思源宋體字體
  - 自動保存到 `docs/images/{日期}.png`
  - 支持通過環境變量 `ENABLE_IMAGE_GENERATION` 開關控制
- **INSTAGRAM封面生成**
  - 3:4 比例封面（750x1000px）
  - 極簡格柵主義設計風格
  - 黑白主色調 + 綠色點綴
  - 自動提取關鍵詞作為主標題
  - 一鍵保存為 PNG 圖片
  - 保存在 `docs/instagram/` 目錄

### Changed
- GitHub Actions 工作流新增 Firefly API 環境變量配置
- Skill 定義新增 Step 7 圖片生成流程
- README 新增圖片生成功能說明和配置文檔

### Fixed
- 修復 SKILL.md 中 API 返回格式描述不準確的問題
- 修復 image_generator.py 中未定義變量的 bug
- 修復圖片高度計算不足導致內容顯示不全的問題
  - 增加高度計算餘量（20% 安全緩衝）
  - 增加字符寬度估算（16px）
  - 降低 padding 比例到 8%
  - 空行也計入高度計算

[Unreleased]: https://github.com/geekjourneyx/ai-daily-skill/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/geekjourneyx/ai-daily-skill/releases/tag/v1.0.0

---

## [1.0.0] - 2026-01-15

### Added
- 自動從 smol.ai 獲取 AI 資訊
- Claude AI 智能分析分類和摘要提取
- 8 種智能主題配色，根據內容類型自動選擇
- 精美 HTML 頁面生成，支持響應式設計
- 郵件通知功能（可選配置）
  - 成功通知：包含資訊數量和頁面連結
  - 空數據通知：當日無資訊時提醒
  - 錯誤通知：失敗時附帶 GitHub Actions 日誌連結
- GitHub Actions 定時任務
  - 每天 UTC 02:00（北京時間 10:00）自動運行
  - 支持手動觸發
  - 自動部署到 GitHub Pages
- 資訊智能分類（模型發布、產品動態、研究論文、工具框架、融資併購、行業事件）
- 索引頁面，按日期倒序展示所有日報
- 關鍵詞提取和標籤展示
- Claude Code Skill 插件支持
  - 在 Claude Code 中直接查詢 AI 資訊
  - 支持相對日期查詢（昨天、前天、今天）
  - 支持絕對日期查詢（YYYY-MM-DD）
  - 內置 Claude AI 智能摘要和分類
  - 可選生成精美網頁（蘋果風/深海藍/秋日暖陽主題）
  - 友好的用戶無數據提示

### Configuration
- 支持 8 種主題配色：柔和藍色、深靛藍、優雅紫色、清新綠色、溫暖橙色、玫瑰粉色、冷色青綠、中性灰色
- 支持通過環境變量自定義 RSS 源
- 支持通過環境變量配置 SMTP 郵件通知

### Documentation
- 完整的 README.md 使用文檔
- 常見問題（FAQ）章節
- 本地開發指南
