#!/usr/bin/env python3
"""
修復 Writerside hi.tree 中重複的 toc-title 屬性
當 toc-title 與 Markdown 文件的實際標題相同時，移除該屬性
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

def get_markdown_title(md_file_path):
    """從 Markdown 文件中提取第一個 # 標題"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    # 移除開頭的 # 和空格
                    title = line.lstrip('#').strip()
                    return title
    except FileNotFoundError:
        print(f"警告: 找不到文件 {md_file_path}")
        return None
    except Exception as e:
        print(f"錯誤: 讀取文件 {md_file_path} 時發生錯誤: {e}")
        return None
    return None

def fix_toc_tree(tree_file_path, topics_dir):
    """修復 hi.tree 文件中的重複 toc-title"""
    
    # 讀取 XML 文件
    tree = ET.parse(tree_file_path)
    root = tree.getroot()
    
    fixed_count = 0
    checked_count = 0
    
    # 遍歷所有 toc-element
    for elem in root.iter('toc-element'):
        topic = elem.get('topic')
        toc_title = elem.get('toc-title')
        
        # 只處理有 topic 和 toc-title 的元素
        if topic and toc_title:
            checked_count += 1
            
            # 構建 Markdown 文件路徑
            md_file = topics_dir / topic
            
            # 獲取 Markdown 文件的實際標題
            actual_title = get_markdown_title(md_file)
            
            if actual_title:
                # 比較 toc-title 和實際標題
                if toc_title == actual_title:
                    # 移除 toc-title 屬性
                    del elem.attrib['toc-title']
                    fixed_count += 1
                    print(f"✓ 移除重複的 toc-title: {topic}")
    
    # 保存修改後的 XML
    # 保持原有的格式
    tree.write(tree_file_path, encoding='utf-8', xml_declaration=True)
    
    print(f"\n完成！")
    print(f"檢查了 {checked_count} 個條目")
    print(f"修復了 {fixed_count} 個重複的 toc-title")
    
    return fixed_count

def main():
    # 設定路徑
    workspace_root = Path('/Users/jakeuj/WritersideProjects/writerside')
    tree_file = workspace_root / 'Writerside' / 'hi.tree'
    topics_dir = workspace_root / 'Writerside' / 'topics'
    
    print(f"開始修復 {tree_file}")
    print(f"主題目錄: {topics_dir}\n")
    
    # 執行修復
    fixed_count = fix_toc_tree(tree_file, topics_dir)
    
    if fixed_count > 0:
        print(f"\n已修復 {fixed_count} 個重複的 toc-title 屬性")
    else:
        print("\n沒有找到需要修復的重複 toc-title")

if __name__ == '__main__':
    main()

