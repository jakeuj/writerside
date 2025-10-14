#!/bin/bash
set -e

# 顏色定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 配置變數（與 .github/workflows/deploy.yml 保持一致）
INSTANCE="Writerside/hi"
IS_GROUP="false"
DOCKER_VERSION="2025.04.8412"

# 檢測是否為 Apple Silicon
PLATFORM_FLAG=""
if [[ $(uname -m) == "arm64" ]] && [[ $(uname -s) == "Darwin" ]]; then
    echo -e "${BLUE}ℹ️  檢測到 Apple Silicon Mac，將使用 --platform linux/amd64${NC}"
    PLATFORM_FLAG="--platform linux/amd64"
    echo -e "${YELLOW}⚠️  注意：x86 模擬可能會比較慢，建議使用 Writerside IDE 進行本地測試${NC}"
    echo ""
fi

echo -e "${BLUE}🔨 步驟 1: 建構 Writerside 文檔...${NC}"
echo -e "${YELLOW}⏳ 這可能需要幾分鐘時間，請耐心等待...${NC}"
echo -e "${YELLOW}💡 提示: 你會看到一些 SEVERE/WARN 訊息，這些是 IDE 內部警告，可以忽略${NC}"
echo ""

# 建構文檔（保留所有輸出以便除錯）
docker run --rm \
  $PLATFORM_FLAG \
  -v "$PWD":/opt/sources \
  registry.jetbrains.team/p/writerside/builder/writerside-builder:$DOCKER_VERSION \
  /opt/builder/bin/idea.sh helpbuilderinspect \
  --source-dir /opt/sources \
  --product $INSTANCE \
  --runner other \
  --output-dir /opt/sources/artifacts/

BUILD_EXIT_CODE=$?

if [ $BUILD_EXIT_CODE -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ 建構失敗，退出碼: $BUILD_EXIT_CODE${NC}"
    exit $BUILD_EXIT_CODE
fi

echo ""
echo -e "${GREEN}✅ 建構完成!${NC}"
echo ""

# 檢查 report.json 是否存在
if [ ! -f "artifacts/report.json" ]; then
    echo -e "${RED}❌ 錯誤: artifacts/report.json 未生成${NC}"
    echo "請檢查建構過程是否有錯誤"
    exit 1
fi

echo -e "${BLUE}🔍 步驟 2: 執行文檔檢查...${NC}"
echo ""

# 方法 1: 使用 writerside-checker-action 的 entrypoint.sh 邏輯
# 下載並執行 checker JAR（與 GitHub Action 完全相同）
docker run --rm \
  -v "$PWD":/opt/sources \
  -w /opt/sources \
  openjdk:18-jdk-slim \
  bash -c "
    apt-get update -qq && apt-get install -y -qq curl > /dev/null 2>&1
    curl -s -o wrs-doc-app.jar -L https://packages.jetbrains.team/maven/p/writerside/maven/com/jetbrains/writerside/writerside-ci-checker/1.0/writerside-ci-checker-1.0.jar

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
echo -e "${BLUE}📄 詳細報告: artifacts/report.json${NC}"

