#!/bin/bash
set -e

echo "🚀 使用 GitHub Actions 測試 Writerside 文檔"
echo ""

# 檢查是否有未提交的變更
if [[ -n $(git status -s) ]]; then
    echo "📝 發現未提交的變更："
    git status -s
    echo ""
    read -p "是否提交並推送？(Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        # 提交變更
        read -p "請輸入 commit 訊息: " commit_msg
        if [[ -z "$commit_msg" ]]; then
            commit_msg="docs: 更新 Writerside 文檔"
        fi
        
        git add .
        git commit -m "$commit_msg"
        echo "✅ 已提交變更"
    else
        echo "❌ 已取消"
        exit 0
    fi
else
    echo "✅ 沒有未提交的變更"
fi

echo ""
echo "📤 推送到 GitHub..."
git push origin master

echo ""
echo "✅ 已推送！GitHub Actions 將自動執行測試"
echo ""
echo "📊 查看測試結果："
echo "   瀏覽器：https://github.com/jakeuj/writerside/actions"
echo ""

# 如果有安裝 gh CLI，提供更多選項
if command -v gh &> /dev/null; then
    echo "💡 使用 GitHub CLI 查看結果："
    echo "   gh run list --limit 5"
    echo "   gh run view --web"
    echo "   gh run watch"
    echo ""
    
    read -p "是否在瀏覽器中開啟 Actions 頁面？(Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        gh run view --web
    fi
    
    echo ""
    read -p "是否等待測試完成？(y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "⏳ 等待測試完成..."
        gh run watch
        
        # 檢查測試結果
        echo ""
        echo "📊 測試結果："
        gh run view
        
        # 如果測試失敗，詢問是否下載報告
        if gh run view --json conclusion -q '.conclusion' | grep -q "failure"; then
            echo ""
            echo "❌ 測試失敗"
            read -p "是否下載錯誤報告？(Y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                mkdir -p artifacts
                gh run download --name report.json --dir artifacts
                echo "📄 錯誤報告已下載到 artifacts/report.json"
                
                if command -v jq &> /dev/null; then
                    echo ""
                    echo "🔴 錯誤摘要："
                    cat artifacts/report.json | jq -r '.errors[] | "  [\(.code)] \(.file):\(.line) - \(.message)"'
                fi
            fi
        else
            echo "✅ 測試通過！"
        fi
    fi
else
    echo "💡 安裝 GitHub CLI 以獲得更多功能："
    echo "   brew install gh"
    echo "   gh auth login"
    echo ""
    
    read -p "是否在瀏覽器中開啟 Actions 頁面？(Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        open "https://github.com/jakeuj/writerside/actions"
    fi
fi

echo ""
echo "✅ 完成！"

