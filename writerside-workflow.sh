#!/bin/bash
set -e

echo "🚀 Writerside Complete Workflow"
echo "================================"
echo ""
echo "This script will:"
echo "  1. Run Writerside checker"
echo "  2. Analyze errors"
echo "  3. Apply automatic fixes (if needed)"
echo "  4. Re-run checker to verify"
echo "  5. Optionally commit changes"
echo ""

REPORT_PATH="artifacts/report.json"

# 步驟 1: 執行檢查
echo "【Step 1/5】Running Writerside checker..."
echo ""
./check-writerside.sh

# 檢查是否有錯誤
if [ ! -f "$REPORT_PATH" ]; then
    echo "❌ Error: Report file not found"
    exit 1
fi

ERROR_COUNT=$(cat "$REPORT_PATH" | jq '.errors | length' 2>/dev/null || echo "0")

if [ "$ERROR_COUNT" -eq 0 ]; then
    echo ""
    echo "🎉 No errors found! Your documentation is perfect!"
    exit 0
fi

echo ""
echo "【Step 2/5】Analyzing errors..."
echo ""

# 分析錯誤類型
MRK002_COUNT=$(cat "$REPORT_PATH" | jq '[.errors[] | select(.code == "MRK002")] | length' 2>/dev/null || echo "0")
MRK003_COUNT=$(cat "$REPORT_PATH" | jq '[.errors[] | select(.code == "MRK003")] | length' 2>/dev/null || echo "0")
CTT004_COUNT=$(cat "$REPORT_PATH" | jq '[.errors[] | select(.code == "CTT004")] | length' 2>/dev/null || echo "0")

echo "Error breakdown:"
echo "  MRK002 (Syntax errors): $MRK002_COUNT"
echo "  MRK003 (Duplicate IDs): $MRK003_COUNT"
echo "  CTT004 (Undefined vars): $CTT004_COUNT"
echo "  Other errors: $((ERROR_COUNT - MRK002_COUNT - MRK003_COUNT - CTT004_COUNT))"
echo ""

# 步驟 3: 詢問是否自動修復
if [ "$MRK002_COUNT" -gt 0 ]; then
    echo "【Step 3/5】Auto-fix available for MRK002 errors"
    echo ""
    read -p "Do you want to apply automatic fixes? (y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        ./fix-writerside-errors.sh
        echo ""
        
        # 步驟 4: 重新檢查
        echo "【Step 4/5】Re-running checker to verify fixes..."
        echo ""
        ./check-writerside.sh
        
        NEW_ERROR_COUNT=$(cat "$REPORT_PATH" | jq '.errors | length' 2>/dev/null || echo "0")
        FIXED_COUNT=$((ERROR_COUNT - NEW_ERROR_COUNT))
        
        echo ""
        echo "📊 Results:"
        echo "  Errors before: $ERROR_COUNT"
        echo "  Errors after: $NEW_ERROR_COUNT"
        echo "  Fixed: $FIXED_COUNT"
        echo ""
        
        if [ "$NEW_ERROR_COUNT" -eq 0 ]; then
            echo "🎉 All errors fixed!"
        elif [ "$FIXED_COUNT" -gt 0 ]; then
            echo "✅ Some errors fixed, but $NEW_ERROR_COUNT remain"
            echo "   Please review the remaining errors manually"
        else
            echo "⚠️  No errors were automatically fixed"
            echo "   Manual intervention required"
        fi
        
        # 步驟 5: 詢問是否提交
        if [ "$FIXED_COUNT" -gt 0 ]; then
            echo ""
            echo "【Step 5/5】Commit changes?"
            echo ""
            read -p "Do you want to commit and push the fixes? (y/n) " -n 1 -r
            echo ""
            
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo ""
                git add Writerside/topics/
                git commit -m "🐛 修復(docs): 自動修正 Writerside 檢查器錯誤

- 修正 MRK002 錯誤: 移除程式碼區塊中錯誤的反引號包裹
- 修復 $FIXED_COUNT 個錯誤
- 剩餘 $NEW_ERROR_COUNT 個錯誤需手動處理"
                
                read -p "Push to remote? (y/n) " -n 1 -r
                echo ""
                
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    git push origin master
                    echo ""
                    echo "✅ Changes pushed to GitHub"
                    echo "🔗 Check GitHub Actions: https://github.com/jakeuj/writerside/actions"
                fi
            fi
        fi
    else
        echo ""
        echo "ℹ️  Skipping auto-fix. Please fix errors manually."
    fi
else
    echo "【Step 3/5】No auto-fixable errors found"
    echo ""
    echo "ℹ️  The errors require manual intervention:"
    echo ""
    cat "$REPORT_PATH" | jq -r '.errors[] | "  [\(.code)] \(.file):\(.line) - \(.message)"' | head -10
    echo ""
    echo "Please fix these errors manually and run this script again."
fi

echo ""
echo "================================"
echo "Workflow completed!"

