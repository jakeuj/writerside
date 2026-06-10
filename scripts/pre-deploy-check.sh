#!/bin/bash

# Writerside 部署前檢查腳本
# 在本地模擬 GitHub Actions 的檢查流程

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Writerside 部署前檢查${NC}"
echo -e "${BLUE}========================================${NC}\n"

# 檢查 1: Markdown 格式
echo -e "${YELLOW}🔍 [1/4] 檢查 Markdown 格式...${NC}"
if npx markdownlint-cli2 "Writerside/topics/**/*.md" 2>/dev/null; then
    echo -e "${GREEN}✅ Markdown 格式檢查通過${NC}\n"
else
    echo -e "${RED}❌ Markdown 格式有問題${NC}"
    echo -e "${YELLOW}💡 執行以下指令自動修復：${NC}"
    echo -e "   npm run lint:md:fix${NC}\n"
    exit 1
fi

# 檢查 2: Writerside 配置文件
echo -e "${YELLOW}🔍 [2/4] 檢查 Writerside 配置文件...${NC}"
required_files=(
    "Writerside/writerside.cfg"
    "Writerside/hi.tree"
    "Writerside/cfg/buildprofiles.xml"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ 缺少文件: $file${NC}"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = true ]; then
    echo -e "${GREEN}✅ 所有必要的配置文件都存在${NC}\n"
else
    echo -e "${RED}❌ 缺少必要的配置文件${NC}\n"
    exit 1
fi

# 檢查 3: 檢查 hi.tree 是否為有效的 XML
echo -e "${YELLOW}🔍 [3/4] 檢查 TOC 結構 (hi.tree)...${NC}"
if command -v xmllint &> /dev/null; then
    if xmllint --noout Writerside/hi.tree 2>/dev/null; then
        echo -e "${GREEN}✅ hi.tree XML 格式正確${NC}\n"
    else
        echo -e "${RED}❌ hi.tree XML 格式錯誤${NC}\n"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  xmllint 未安裝，跳過 XML 驗證${NC}"
    echo -e "${YELLOW}   可選安裝: brew install libxml2${NC}\n"
fi

# 檢查 4: SEO metadata 摘要
echo -e "${YELLOW}🔍 [4/4] 檢查 SEO metadata 摘要...${NC}"
required_web_summary_files=(
    "Writerside/topics/Default.md"
    "Writerside/topics/ABP.md"
    "Writerside/topics/AI-Search-Service.md"
    "Writerside/topics/CloudWatch.md"
    "Writerside/topics/Deploy-FastAPI-on-Azure-App-Service.md"
    "Writerside/topics/Docker.md"
    "Writerside/topics/Flutter-Azure-AD-Login.md"
    "Writerside/topics/Ollama.md"
    "Writerside/topics/PowerShell-Script-Tool-for-Migrations.md"
    "Writerside/topics/Share-Wifi.md"
    "Writerside/topics/Studio.md"
    "Writerside/topics/Swagger.md"
    "Writerside/topics/writerside-sitemap-seo.md"
)

missing_web_summary=false
for file in "${required_web_summary_files[@]}"; do
    if ! grep -q "<web-summary" "$file"; then
        echo -e "${RED}❌ 缺少 <web-summary>: $file${NC}"
        missing_web_summary=true
    fi
done

new_topic_files=()
if command -v git &> /dev/null; then
    while IFS= read -r file; do
        if [ -n "$file" ]; then
            new_topic_files+=("$file")
        fi
    done < <(
        {
            git diff --name-only --diff-filter=A -- "Writerside/topics/*.md"
            git diff --cached --name-only --diff-filter=A -- "Writerside/topics/*.md"
            if git rev-parse --verify origin/master &> /dev/null; then
                git diff --name-only --diff-filter=A origin/master...HEAD -- "Writerside/topics/*.md"
            elif git rev-parse --verify HEAD~1 &> /dev/null; then
                git diff --name-only --diff-filter=A HEAD~1..HEAD -- "Writerside/topics/*.md"
            fi
        } | sort -u
    )
fi

for file in "${new_topic_files[@]}"; do
    if [ -f "$file" ] && ! grep -q "<web-summary" "$file"; then
        echo -e "${RED}❌ 新增 topic 缺少 <web-summary>: $file${NC}"
        missing_web_summary=true
    fi
done

if command -v git &> /dev/null; then
    while IFS= read -r file; do
        if [ -f "$file" ] && ! grep -q "<web-summary" "$file"; then
            echo -e "${YELLOW}⚠️  未追蹤 topic 缺少 <web-summary>，加入 Git 前建議補上: $file${NC}"
        fi
    done < <(git ls-files --others --exclude-standard -- "Writerside/topics/*.md")
fi

if [ "$missing_web_summary" = true ]; then
    echo -e "${YELLOW}💡 請在 H1 下方加入 <web-summary>，避免搜尋與分享預覽 description 為空。${NC}\n"
    exit 1
else
    echo -e "${GREEN}✅ SEO metadata 摘要檢查通過${NC}\n"
fi

# 總結
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✨ 所有本地檢查通過！${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${YELLOW}💡 下一步：${NC}"
echo -e "   git add ."
echo -e "   git commit -m \"your message\""
echo -e "   git push"
echo -e "\n${YELLOW}📝 GitHub Actions 將會執行完整的 Writerside 建構和測試${NC}\n"
