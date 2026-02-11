#!/bin/bash

# Markdown 檢查和修復腳本

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔍 開始檢查 Markdown 文檔...${NC}"

# 檢查是否安裝 markdownlint-cli
if ! command -v markdownlint &> /dev/null; then
    echo -e "${RED}❌ markdownlint-cli 未安裝${NC}"
    echo -e "${YELLOW}請執行: brew install markdownlint-cli${NC}"
    exit 1
fi

# 檢查模式
if [ "$1" == "--fix" ]; then
    echo -e "${YELLOW}🔧 自動修復模式${NC}"
    markdownlint --fix Writerside/topics/**/*.md
    echo -e "${GREEN}✅ 已自動修復可修復的問題${NC}"
else
    echo -e "${YELLOW}📋 檢查模式（不修改檔案）${NC}"
    if markdownlint Writerside/topics/**/*.md; then
        echo -e "${GREEN}✅ 所有 Markdown 文檔格式正確！${NC}"
    else
        echo -e "${RED}❌ 發現格式問題${NC}"
        echo -e "${YELLOW}💡 執行以下指令自動修復：${NC}"
        echo -e "   ./scripts/check-markdown.sh --fix"
        exit 1
    fi
fi

