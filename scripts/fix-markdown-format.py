#!/usr/bin/env python3
"""
全面修復 Markdown 文件格式問題
根據 markdownlint-cli2 規則進行自動修復
"""
import os
import re
import glob
from pathlib import Path

def fix_file(filepath):
    """修復單個 Markdown 文件的格式問題"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_issues = []
        
        # 確保文件以換行符結尾 (MD047)
        if content and not content.endswith('\n'):
            content += '\n'
            fixed_issues.append('文件末尾缺少換行符')
        
        # 移除多餘的行尾空白 (MD009) - 保留需要的
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            # 保留代碼區塊和特殊格式
            if line.startswith('```') or line.startswith('    '):
                new_lines.append(line)
            else:
                stripped = line.rstrip()
                if stripped != line:
                    fixed_issues.append('移除行尾空白')
                new_lines.append(stripped)
        content = '\n'.join(new_lines)
        
        # 只在內容有變化時寫入文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, fixed_issues
        
        return False, []
        
    except Exception as e:
        print(f"❌ 處理文件時出錯 {filepath}: {e}")
        return False, []

def main():
    print("🔧 開始修復 Markdown 文件格式問題...\n")
    
    # 獲取所有 Markdown 文件
    pattern = 'Writerside/topics/**/*.md'
    md_files = glob.glob(pattern, recursive=True)
    
    print(f"📋 找到 {len(md_files)} 個 Markdown 文件\n")
    
    fixed_count = 0
    total_issues = 0
    
    for filepath in md_files:
        modified, issues = fix_file(filepath)
        if modified:
            fixed_count += 1
            total_issues += len(set(issues))
            print(f"✅ {filepath}")
            for issue in set(issues):
                print(f"   - {issue}")
    
    print(f"\n{'='*60}")
    print(f"✨ 修復完成！")
    print(f"📊 修改了 {fixed_count} 個文件")
    print(f"{'='*60}\n")
    
    if fixed_count > 0:
        print("💡 提示：請執行以下命令進行完整的格式檢查：")
        print("   npm run lint:md:fix")
        print("   或")
        print("   ./scripts/check-markdown.sh --fix")

if __name__ == '__main__':
    main()

