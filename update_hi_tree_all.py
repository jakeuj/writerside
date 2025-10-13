#!/usr/bin/env python3
"""
更新 hi.tree 將所有遷移的文章加入目錄
"""

import json
import os
from xml.etree import ElementTree as ET

# 讀取文章資訊
articles_info_file = 'Writerside/topics/_articles_info.json'
hi_tree_file = 'Writerside/hi.tree'

print("讀取文章資訊...")
with open(articles_info_file, 'r', encoding='utf-8') as f:
    articles_info = json.load(f)

print(f"找到 {len(articles_info)} 篇文章")

# 解析 hi.tree
print("解析 hi.tree...")
tree = ET.parse(hi_tree_file)
root = tree.getroot()

# 找到 Dot-Blog 節點
dot_blog_node = None
for toc_element in root.findall('.//toc-element'):
    if toc_element.get('topic') == 'Dot-Blog.md':
        dot_blog_node = toc_element
        break

if not dot_blog_node:
    print("❌ 找不到 Dot-Blog.md 節點")
    exit(1)

print(f"找到 Dot-Blog 節點")

# 清空現有的子節點
for child in list(dot_blog_node):
    dot_blog_node.remove(child)

# 按日期排序文章(新到舊)
articles_sorted = sorted(articles_info, key=lambda x: x.get('date', ''), reverse=True)

# 添加所有文章
added_count = 0
skipped_count = 0

for article in articles_sorted:
    filename = article['filename']
    title = article['title']
    
    # 跳過已經被標記為跳過的文章
    if article.get('skipped'):
        skipped_count += 1
        continue
    
    # 創建新的 toc-element
    new_element = ET.Element('toc-element', topic=filename)
    new_element.set('toc-title', title)
    dot_blog_node.append(new_element)
    added_count += 1

print(f"\n✓ 已添加 {added_count} 篇文章到 hi.tree")
print(f"✓ 跳過 {skipped_count} 篇已存在的文章")

# 格式化 XML
ET.indent(tree, space='    ')

# 保存
print("保存 hi.tree...")
tree.write(hi_tree_file, encoding='utf-8', xml_declaration=True)

print("\n✅ 完成!")

