#!/bin/bash
set -e

# 顏色定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 配置變數
INSTANCE="Writerside/hi"
IS_GROUP="false"

echo -e "${BLUE}🔍 執行 Writerside 文檔檢查...${NC}"
echo ""

# 檢查 report.json 是否存在
if [ ! -f "artifacts/report.json" ]; then
    echo -e "${RED}❌ 錯誤: artifacts/report.json 不存在${NC}"
    echo ""
    echo "請先使用以下方法之一建構文檔："
    echo "1. 使用 Writerside IDE: Build → Build Documentation"
    echo "2. 推送到 GitHub 讓 CI/CD 建構"
    echo "3. 從 GitHub Actions 下載 artifacts"
    echo ""
    exit 1
fi

echo -e "${BLUE}📄 找到 report.json，開始檢查...${NC}"
echo ""

# 使用與 entrypoint.sh 相同的邏輯執行檢查
docker run --rm \
  -v "$PWD":/opt/sources \
  -w /opt/sources \
  openjdk:18-jdk-slim \
  bash -c "
    echo '下載 Writerside checker...'
    apt-get update -qq && apt-get install -y -qq curl > /dev/null 2>&1
    curl -s -o wrs-doc-app.jar -L https://packages.jetbrains.team/maven/p/writerside/maven/com/jetbrains/writerside/writerside-ci-checker/1.0/writerside-ci-checker-1.0.jar
    
    echo ''
    echo '執行檢查...'
    echo ''
    
    # 使用與 entrypoint.sh 相同的邏輯
    IS_GROUP_LOWER=\$(echo \"$IS_GROUP\" | tr '[:upper:]' '[:lower:]')
    
    if [ -n \"$IS_GROUP\" ] && [ \"\$IS_GROUP_LOWER\" != \"false\" ]; then
      echo \"Processing as a group with -g flag\"
      java -jar wrs-doc-app.jar artifacts/report.json $INSTANCE -g
    else
      echo \"Processing as an instance without -g flag\"
      java -jar wrs-doc-app.jar artifacts/report.json $INSTANCE
    fi
  "

CHECKER_EXIT_CODE=$?

echo ""
if [ $CHECKER_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ 檢查完成! 沒有發現錯誤。${NC}"
else
    echo -e "${RED}❌ 檢查發現錯誤或警告，請查看上方輸出。${NC}"
    exit $CHECKER_EXIT_CODE
fi

echo ""
echo -e "${BLUE}💡 提示: 你可以直接查看 artifacts/report.json 了解詳細結果${NC}"

