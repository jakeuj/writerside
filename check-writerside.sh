#!/bin/bash
set -e

INSTANCE="Writerside/hi"
DOCKER_VERSION="2025.04.8412"
OUTPUT_DIR="$PWD/artifacts"

echo "🔍 Building and checking Writerside docs for instance: $INSTANCE"
echo "🐳 Using Docker image: jetbrains/writerside-builder:$DOCKER_VERSION"
echo ""
echo "⚠️  警告：在 Mac M4 (ARM) 上執行可能需要 10-30 分鐘"
echo "💡 建議：使用 GitHub Actions 測試更快速（2-3 分鐘）"
echo "📖 詳見：WRITERSIDE-TEST-STRATEGY.md"
echo ""
read -p "是否繼續本地測試？(y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    echo "💡 建議使用：git push origin master 然後查看 GitHub Actions"
    exit 0
fi
echo ""

# 檢查 Docker 是否運行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "   Please start Docker Desktop"
    exit 1
fi

# 確保 artifacts 目錄存在
mkdir -p "$OUTPUT_DIR"

# 執行 Writerside builder（會生成文檔和 report.json）
echo "🔨 Building documentation..."
docker run --rm \
  -v "$PWD:/opt/sources" \
  -e SOURCE_DIR=/opt/sources \
  -e MODULE_INSTANCE="$INSTANCE" \
  -e OUTPUT_DIR=/opt/sources/artifacts \
  -e RUNNER=other \
  jetbrains/writerside-builder:$DOCKER_VERSION

echo ""
echo "✅ Writerside build finished!"

# 檢查 report.json 是否存在
REPORT_PATH="$OUTPUT_DIR/report.json"
if [ ! -f "$REPORT_PATH" ]; then
    echo "⚠️  Warning: report.json not found at $REPORT_PATH"
    echo "   Build may have failed or report was not generated"
    exit 1
fi

echo "📄 Report: $REPORT_PATH"

# 如果有安裝 jq，顯示錯誤摘要
if command -v jq &> /dev/null; then
    echo ""
    echo "📊 Error Summary:"
    ERROR_COUNT=$(cat "$REPORT_PATH" | jq '.errors | length')
    WARNING_COUNT=$(cat "$REPORT_PATH" | jq '.warnings | length')
    echo "   Errors: $ERROR_COUNT"
    echo "   Warnings: $WARNING_COUNT"

    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo ""
        echo "🔴 Errors found:"
        cat "$REPORT_PATH" | jq -r '.errors[] | "  [\(.code)] \(.file):\(.line) - \(.message)"' | head -20
        if [ "$ERROR_COUNT" -gt 20 ]; then
            echo "  ... and $((ERROR_COUNT - 20)) more errors"
        fi
        exit 1
    else
        echo ""
        echo "🎉 No errors found!"
    fi
else
    echo ""
    echo "💡 Tip: Install jq to see error summary: brew install jq"
    echo "   brew install jq"
fi

