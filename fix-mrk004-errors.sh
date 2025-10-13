#!/bin/bash
set -e

echo "🔧 修復 MRK004 錯誤 - Topic ID 不符合檔案名稱"
echo ""

# 需要修復的檔案列表
files=(
    "ABP.IO-Azure-App-Service-解決-Could-not-find-the-bundle-file-&#x27;libsabpcoreabp.css&#x27;.md"
    "ABP.IO-Could-not-find-the-bundle-file-&#x27;libsabpcoreabp.css&#x27;.md"
    "ABP.IO-WEB應用程式框架-Override-UI&#x3001;控制器&#x3001;服務&#x3001;DTO.md"
    "ABP.IO-WEB應用程式框架-新手教學-No.04-開發教學-第-3-部分-創建&#x3001;更新和刪除圖書.md"
    "ABP.IO-WEB應用程式框架-新手教學-No.07-開發教學-第-6-部分-作者&#xFF1A;領域層.md"
    "ABP.IO-WEB應用程式框架-新手教學-No.08-開發教學-第-7-部分&#xFF1A;作者&#xFF1A;數據庫集成.md"
    "ABP.IO-WEB應用程式框架-新手教學-No.09-開發教學-第-8-部分&#xFF1A;作者&#xFF1A;應用服務層.md"
    "ABP.IO-WEB應用程式框架-新手教學-No.10-開發教學-第-9-部分&#xFF1A;作者&#xFF1A;用戶界面.md"
    "ABP.IO-WEB應用程式框架-新手教學-No.11-開發教學-第-10-部分&#xFF1A;書籍與作者的關係.md"
    "ABP.IO-WEB應用程式框架-烤肉串命名&#xFF08;Kebab-case&#xFF09;.md"
    "Angular-Function-calls-are-not-supported-in-decorators-but-&#x27;InjectionToken&#x27;-was-called-in.md"
    "Angular-woff-json-404-&amp;-the-web.config-asset-path-must-start-with-the-project-source-root.md"
    "Azure-DevOps-Pipeline-合併-Vue-&amp;-.NetCore-Project-並-Build-&amp;-Release.md"
    "C#-delegate,-Func&lt;TResult&gt;,-Action&lt;T&gt;.md"
    "DotNetCore-HttpClient-User-Agent-&amp;-Encoding.md"
    "Drone-阿里雲-Web&#x2B;-DotnetCore-3.1-CICD-&amp;-DockerHub-Images-CICD.md"
    "HSTS-(HTTP-Strict-Transport-Security)-&amp;-HTTPS-redirection-(Enforce-HTTPS-in-ASP.NET-Core).md"
    "LDAP-Admin-&amp;-C#-.Net-Core-Identity-Server-4.md"
    "Linq-Left-Join-(GroupJoin-&#x2B;-SelectMany)-Repository.md"
    "MSSQL-2012-&amp;-2008-分頁與計數.md"
    "NSwag-Settings-&amp;-HttpClient-Startup.md"
    "SignalR-2.0-與-Unity-Game-的-WebSocket&#xA0;連線筆記.md"
    "Unknown-column-&#x27;Discriminator&#x27;-in-&#x27;where-clause&#x27;.md"
    "svn-E140000-Can&#x27;t-read-length-line-dbtxn-current-&amp;-E2000002-Cant&#xA0;not-parse-lock-entrie.md"
    "如何利用&#x300C;磁碟清理&#x300D;工具-安全的騰出系統硬碟的多餘空間.md"
    "發布技術文章-(Windows-Live-Writer-&#x2B;-程式碼插入外掛程式).md"
    "阿里雲-Web&#x2B;-(Aliyun-Cloud-Web-Plus)-使用筆記.md"
    "阿里雲-Web&#x2B;-使用-Cli-部署-DotnetCore-3.1-專案筆記.md"
)

TOPICS_DIR="Writerside/topics"
FIXED_COUNT=0
SKIPPED_COUNT=0

for file in "${files[@]}"; do
    filepath="$TOPICS_DIR/$file"
    
    if [ ! -f "$filepath" ]; then
        echo "⚠️  檔案不存在: $file"
        ((SKIPPED_COUNT++))
        continue
    fi
    
    # 從檔案名稱生成預期的 topic ID（移除 .md 後綴）
    expected_id="${file%.md}"
    
    # 讀取第一行（標題）
    first_line=$(head -n 1 "$filepath")
    
    # 檢查是否已經有 {id="..."} 屬性
    if [[ $first_line =~ \{id= ]]; then
        echo "✓ 已有 ID: $file"
        continue
    fi
    
    # 在標題末尾添加 {id="..."} 屬性
    # 移除可能的尾隨空白
    title_without_newline=$(echo "$first_line" | sed 's/[[:space:]]*$//')
    new_first_line="$title_without_newline {id=\"$expected_id\"}"
    
    # 建立備份
    cp "$filepath" "$filepath.bak"
    
    # 替換第一行
    tail -n +2 "$filepath.bak" > "$filepath.tmp"
    echo "$new_first_line" > "$filepath"
    cat "$filepath.tmp" >> "$filepath"
    rm "$filepath.tmp"
    
    echo "✅ 已修復: $file"
    ((FIXED_COUNT++))
done

# 清理備份檔案
find "$TOPICS_DIR" -name "*.bak" -delete

echo ""
echo "📊 修復統計："
echo "   已修復: $FIXED_COUNT 個檔案"
echo "   已跳過: $SKIPPED_COUNT 個檔案"
echo ""
echo "✅ 完成！"

