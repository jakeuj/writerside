# 點部落文章遷移總結

## 📊 遷移統計

- **遷移日期**: 2025-01-13
- **來源**: https://www.dotblogs.com.tw/jakeuj/
- **文章總數**: 20 篇
- **成功遷移**: 20 篇
- **失敗**: 0 篇

## 📁 文件結構

```
Writerside/
├── topics/
│   └── dotblog/              # 遷移的文章目錄
│       ├── *.md              # 20 篇 Markdown 文章
│       └── _articles_info.json  # 文章元數據
├── images/
│   └── dotblog/              # 文章圖片目錄(如有)
└── hi.tree                   # 已更新目錄結構
```

## 📝 遷移的文章列表

1. HTTP 301 Moved Permanently https://jakeuj.com/ (2024-09-24)
2. [2021] ABP.IO WEB應用程式框架 新手教學 No.00 全篇索引 (2021-07-15)
3. ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.0 全篇索引 (2016-07-28)
4. ABP.IO File System (2025-04-09)
5. ABP.IO File Management (2025-04-09)
6. Powershell Test-NetConnection Port (2024-05-15)
7. 如何在收到 PFX 或 CER 憑證檔之後使用 OpenSSL 進行常見的格式轉換 (2024-03-26)
8. 常見的PowerShell 輸出訊息的 2 種方法 (2024-03-26)
9. Docker 程序無法存取檔案,因為另一個程序已鎖定檔案的一部分 (2024-03-07)
10. Git Credential Manager for Windows (2024-03-06)
11. Nuget Restore 找不到自己設定的 Nuget Config Sources (2024-03-04)
12. Azure App Service Deploy 錯誤 System.UnauthorizedAccessException (2024-02-21)
13. Windows Terminal 加入 Git Bash (2024-02-19)
14. GCP 虛擬私有雲網路對等互連(VPC peering) vs Cloud SQL (2024-02-19)
15. Jetbrains Writerside CI/CD 自動化部署 Markdown 到 GIthub Pages (2024-02-06)
16. CI/CD Github workflow 使用私人庫的子模組 (2024-02-05)
17. 在 Windows 使用 Docker 跑 ML tensorflow 並啟用 GPU (2024-01-29)
18. GCP Cloud SQL Postgres 向量搜尋 (2024-01-24)
19. the virtual path maps to another application, which is not allowed (2024-01-04)
20. EDGE 刪除 localhost 的 HSTS (2024-01-03)

## 🔧 使用的工具

### 1. migrate_dotblog.py
主要的遷移腳本,功能包括:
- 爬取點部落文章列表
- 提取文章內容和元數據
- 將 HTML 轉換為 Markdown
- 下載並保存圖片
- 生成文章元數據 JSON

### 2. update_hi_tree.py
更新 Writerside 目錄結構的腳本(未使用,改為手動更新)

## ✅ 完成的工作

1. ✅ 爬取所有文章列表
2. ✅ 提取文章標題、日期、標籤
3. ✅ 轉換 HTML 內容為 Markdown
4. ✅ 保存文章到 `Writerside/topics/dotblog/`
5. ✅ 更新 `Writerside/hi.tree` 目錄結構
6. ✅ 保留原文連結和發布日期

## 📋 文章格式

每篇遷移的文章都包含:

```markdown
# 文章標題

> **原文發布日期:** YYYY-MM-DD
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/...
> **標籤:** 標籤1, 標籤2, ...

---

[文章內容]

---

*本文章從點部落遷移至 Writerside*
```

## 🔍 已知問題

1. **標籤提取**: 部分文章的標籤未能正確提取(顯示為"無")
   - 原因: 點部落的 HTML 結構中標籤位置不固定
   - 影響: 不影響文章內容,僅元數據不完整

2. **圖片**: 部分文章可能包含外部圖片連結
   - 狀態: 保留原始連結,未下載到本地

3. **程式碼高亮**: 原文的程式碼語言標記可能未完整保留
   - 建議: 後續手動檢查並添加語言標記

## 🎯 後續建議

1. **手動檢查**: 建議瀏覽每篇文章,確認格式正確
2. **分類整理**: 可以根據技術主題將文章分類到不同的子目錄
3. **標籤補充**: 手動為文章添加適當的標籤
4. **圖片優化**: 檢查圖片連結是否有效,考慮下載到本地
5. **程式碼優化**: 為程式碼區塊添加語言標記以啟用語法高亮

## 📚 參考資料

- 點部落原站: https://www.dotblogs.com.tw/jakeuj/
- Writerside 文檔: https://www.jetbrains.com/writerside/
- Markdownify: https://github.com/matthewwithanm/python-markdownify

## 🙏 致謝

感謝點部落提供的技術分享平台,這些文章記錄了寶貴的技術經驗和解決方案。

