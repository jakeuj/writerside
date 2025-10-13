#!/bin/bash
set -e

TOPICS_DIR="Writerside/topics"
BACKUP_DIR=".writerside-backup-$(date +%Y%m%d-%H%M%S)"

echo "🔧 Writerside Auto-Fix Tool"
echo "=========================="
echo ""

# 檢查是否有 topics 目錄
if [ ! -d "$TOPICS_DIR" ]; then
    echo "❌ Error: $TOPICS_DIR directory not found"
    exit 1
fi

# 建立備份
echo "📦 Creating backup in $BACKUP_DIR..."
mkdir -p "$BACKUP_DIR"
cp -r "$TOPICS_DIR" "$BACKUP_DIR/"
echo "✅ Backup created"
echo ""

# 計數器
FIXED_FILES=0
TOTAL_FIXES=0

# 修正函數
fix_file() {
    local file="$1"
    local fixes=0
    local temp_file="${file}.tmp"
    
    # 讀取檔案內容
    if [ ! -f "$file" ]; then
        return 0
    fi
    
    # 使用 sed 進行修正（macOS 相容版本）
    # 1. 修正程式碼區塊中錯誤的反引號包裹泛型標記
    #    例如：`IOptions<IdentityOptions>` -> IOptions<IdentityOptions>
    sed -E 's/`([A-Z][a-zA-Z0-9]*)<([^`>]+)>`/\1<\2>/g' "$file" > "$temp_file"
    
    # 檢查是否有變更
    if ! cmp -s "$file" "$temp_file"; then
        mv "$temp_file" "$file"
        fixes=$((fixes + 1))
    else
        rm "$temp_file"
    fi
    
    echo "$fixes"
}

# 處理所有 Markdown 檔案
echo "🔍 Scanning and fixing Markdown files..."
echo ""

while IFS= read -r -d '' file; do
    echo "Processing: $file"
    fixes=$(fix_file "$file")
    if [ "$fixes" -gt 0 ]; then
        FIXED_FILES=$((FIXED_FILES + 1))
        TOTAL_FIXES=$((TOTAL_FIXES + fixes))
        echo "  ✅ Fixed $fixes issue(s)"
    fi
done < <(find "$TOPICS_DIR" -name "*.md" -type f -print0)

echo ""
echo "=========================="
echo "📊 Summary:"
echo "   Files processed: $(find "$TOPICS_DIR" -name "*.md" -type f | wc -l | tr -d ' ')"
echo "   Files fixed: $FIXED_FILES"
echo "   Total fixes: $TOTAL_FIXES"
echo ""
echo "💾 Backup location: $BACKUP_DIR"
echo ""

if [ "$TOTAL_FIXES" -gt 0 ]; then
    echo "✅ Auto-fix completed! Please review the changes and run check-writerside.sh again."
    echo ""
    echo "To restore from backup:"
    echo "  rm -rf $TOPICS_DIR && cp -r $BACKUP_DIR/topics $TOPICS_DIR"
else
    echo "ℹ️  No automatic fixes were applied."
    echo "   You may need to manually fix the errors reported by check-writerside.sh"
fi

