#!/bin/bash

# 將 repo-local writerside skill 同步到全域 skill 目錄

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat <<'EOF'
用法:
  ./scripts/sync-writerside-skill.sh [--dry-run]

可用環境變數:
  WRITERSIDE_SOURCE_SKILL_DIR   source skill 目錄
  WRITERSIDE_GLOBAL_SKILL_DIR   全域 skill 目錄
  WRITERSIDE_CODEX_SKILL_LINK   ~/.codex/skills 的符號連結位置
  WRITERSIDE_SKILL_VALIDATE_SCRIPT  quick_validate.py 路徑
EOF
}

DRY_RUN=false

if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
elif [[ $# -gt 0 ]]; then
    usage
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

SOURCE_SKILL_DIR="${WRITERSIDE_SOURCE_SKILL_DIR:-${REPO_ROOT}/.agents/skills/writerside}"
GLOBAL_TEMPLATE_DIR="${SOURCE_SKILL_DIR}/assets/global-skill"
TARGET_SKILL_DIR="${WRITERSIDE_GLOBAL_SKILL_DIR:-${HOME}/.agents/skills/writerside}"
CODEX_SKILL_LINK="${WRITERSIDE_CODEX_SKILL_LINK:-${HOME}/.codex/skills/writerside}"
VALIDATE_SCRIPT="${WRITERSIDE_SKILL_VALIDATE_SCRIPT:-${HOME}/.codex/skills/.system/skill-creator/scripts/quick_validate.py}"

if [[ ! -d "${SOURCE_SKILL_DIR}" ]]; then
    echo -e "${RED}❌ 找不到 source skill 目錄: ${SOURCE_SKILL_DIR}${NC}"
    exit 1
fi

if [[ ! -f "${SOURCE_SKILL_DIR}/SKILL.md" ]]; then
    echo -e "${RED}❌ 找不到 source SKILL.md: ${SOURCE_SKILL_DIR}/SKILL.md${NC}"
    exit 1
fi

if [[ ! -f "${GLOBAL_TEMPLATE_DIR}/SKILL.md" ]]; then
    echo -e "${RED}❌ 找不到全域模板 SKILL.md: ${GLOBAL_TEMPLATE_DIR}/SKILL.md${NC}"
    exit 1
fi

if [[ ! -f "${GLOBAL_TEMPLATE_DIR}/agents/openai.yaml" ]]; then
    echo -e "${RED}❌ 找不到全域模板 openai.yaml: ${GLOBAL_TEMPLATE_DIR}/agents/openai.yaml${NC}"
    exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
    echo -e "${RED}❌ 需要 rsync 才能執行同步${NC}"
    exit 1
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Sync Writerside Skill${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}Source:${NC} ${SOURCE_SKILL_DIR}"
echo -e "${YELLOW}Target:${NC} ${TARGET_SKILL_DIR}"
echo -e "${YELLOW}Codex link:${NC} ${CODEX_SKILL_LINK}"

mkdir -p "$(dirname "${TARGET_SKILL_DIR}")"
mkdir -p "$(dirname "${CODEX_SKILL_LINK}")"

RSYNC_ARGS=(
    -a
    --delete
    --exclude
    "assets/global-skill/"
    --exclude
    ".DS_Store"
)

if [[ "${DRY_RUN}" == "true" ]]; then
    RSYNC_ARGS=(-an --delete --itemize-changes --exclude "assets/global-skill/" --exclude ".DS_Store")
    echo -e "${YELLOW}🔍 Dry run 模式，不會修改檔案${NC}"
fi

echo -e "${YELLOW}📦 同步共用 skill 檔案...${NC}"
rsync "${RSYNC_ARGS[@]}" "${SOURCE_SKILL_DIR}/" "${TARGET_SKILL_DIR}/"

if [[ "${DRY_RUN}" == "true" ]]; then
    echo -e "${YELLOW}📝 Dry run: 會覆蓋全域版 SKILL.md 與 agents/openai.yaml${NC}"
    echo -e "${YELLOW}🔗 Dry run: 會更新 ${CODEX_SKILL_LINK} 符號連結${NC}"
    exit 0
fi

echo -e "${YELLOW}🧩 套用全域 skill 模板...${NC}"
mkdir -p "${TARGET_SKILL_DIR}/agents"
cp "${GLOBAL_TEMPLATE_DIR}/SKILL.md" "${TARGET_SKILL_DIR}/SKILL.md"
cp "${GLOBAL_TEMPLATE_DIR}/agents/openai.yaml" "${TARGET_SKILL_DIR}/agents/openai.yaml"

echo -e "${YELLOW}🔗 更新 ~/.codex/skills 符號連結...${NC}"
rm -rf "${CODEX_SKILL_LINK}"
ln -s "${TARGET_SKILL_DIR}" "${CODEX_SKILL_LINK}"

if [[ -f "${VALIDATE_SCRIPT}" ]]; then
    echo -e "${YELLOW}✅ 驗證全域 skill...${NC}"
    python3 "${VALIDATE_SCRIPT}" "${TARGET_SKILL_DIR}"
else
    echo -e "${YELLOW}⚠️  找不到驗證腳本，跳過 quick_validate: ${VALIDATE_SCRIPT}${NC}"
fi

echo -e "${GREEN}✨ writerside 全域 skill 已同步完成${NC}"
echo -e "${YELLOW}💡 可選檢查:${NC}"
echo -e "   npx markdownlint-cli2 --no-globs ${TARGET_SKILL_DIR}/SKILL.md"
