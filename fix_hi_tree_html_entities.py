#!/usr/bin/env python3
"""
修復 hi.tree 中的 HTML 實體編碼
將 toc-title 屬性中的 HTML 實體轉換為實際字符
"""

import html
import re
from xml.etree import ElementTree as ET

hi_tree_file = 'Writerside/hi.tree'

print("讀取 hi.tree...")
tree = ET.parse(hi_tree_file)
root = tree.getroot()

# 統計
fixed_count = 0

# 遍歷所有 toc-element
for toc_element in root.findall('.//toc-element'):
    toc_title = toc_element.get('toc-title')
    if toc_title:
        # 解碼 HTML 實體
        decoded_title = html.unescape(toc_title)
        
        # 如果有變化,更新
        if decoded_title != toc_title:
            print(f"修復: {toc_title}")
            print(f"  -> {decoded_title}")
            toc_element.set('toc-title', decoded_title)
            fixed_count += 1

print(f"\n✓ 已修復 {fixed_count} 個標題")

# 格式化 XML
ET.indent(tree, space='    ')

# 保存
print("保存 hi.tree...")
tree.write(hi_tree_file, encoding='utf-8', xml_declaration=True)

print("\n✅ 完成!")

