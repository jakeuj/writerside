#!/usr/bin/env python3
"""
更新 hi.tree 文件,將遷移的文章加入目錄結構
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# 讀取文章資訊
with open('Writerside/topics/dotblog/_articles_info.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 解析 hi.tree
tree = ET.parse('Writerside/hi.tree')
root = tree.getroot()

# 找到 "Dot-Blog.md" 的 toc-element
dot_blog_elem = None

def find_element(parent, topic_name):
    """遞迴尋找指定 topic 的元素"""
    for elem in parent:
        if elem.tag == 'toc-element' and elem.get('topic') == topic_name:
            return elem
        # 遞迴搜尋子元素
        found = find_element(elem, topic_name)
        if found is not None:
            return found
    return None

dot_blog_elem = find_element(root, 'Dot-Blog.md')

if not dot_blog_elem:
    print("❌ 找不到 Dot-Blog.md 的 toc-element")
    print("   嘗試列出所有 topic:")
    for elem in root.iter('toc-element'):
        topic = elem.get('topic')
        if topic:
            print(f"   - {topic}")
    exit(1)

# 清空現有的子元素(如果有的話)
for child in list(dot_blog_elem):
    dot_blog_elem.remove(child)

# 按分類組織文章
categories = {}
for article in articles:
    category = article.get('category', 'Other')
    if category not in categories:
        categories[category] = []
    categories[category].append(article)

# 添加文章到 hi.tree
print(f"\n📝 更新 hi.tree...")
print(f"   找到 {len(articles)} 篇文章")
print(f"   分為 {len(categories)} 個分類")

# 如果只有一個分類或所有文章都是 Other,直接添加
if len(categories) == 1 or (len(categories) == 1 and 'Other' in categories):
    for article in articles:
        article_elem = ET.SubElement(dot_blog_elem, 'toc-element')
        article_elem.set('topic', f"dotblog/{article['filename']}")
        print(f"   ✓ 添加: {article['title']}")
else:
    # 按分類添加
    for category, cat_articles in sorted(categories.items()):
        if category == 'Other':
            # Other 分類的文章直接添加到根層級
            for article in cat_articles:
                article_elem = ET.SubElement(dot_blog_elem, 'toc-element')
                article_elem.set('topic', f"dotblog/{article['filename']}")
                print(f"   ✓ 添加: {article['title']}")
        else:
            # 創建分類節點
            category_elem = ET.SubElement(dot_blog_elem, 'toc-element')
            category_elem.set('toc-title', category)
            print(f"   ✓ 分類: {category}")
            
            for article in cat_articles:
                article_elem = ET.SubElement(category_elem, 'toc-element')
                article_elem.set('topic', f"dotblog/{article['filename']}")
                print(f"      - {article['title']}")

# 美化 XML 輸出
def prettify(elem, level=0):
    """美化 XML 縮排"""
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            prettify(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

prettify(root)

# 保存更新後的 hi.tree
tree.write('Writerside/hi.tree', encoding='utf-8', xml_declaration=True)

# 添加 DOCTYPE
with open('Writerside/hi.tree', 'r', encoding='utf-8') as f:
    content = f.read()

# 插入 DOCTYPE
if '<!DOCTYPE' not in content:
    lines = content.split('\n')
    lines.insert(1, '<!DOCTYPE instance-profile')
    lines.insert(2, '        SYSTEM "https://resources.jetbrains.com/writerside/1.0/product-profile.dtd">')
    lines.insert(3, '')
    content = '\n'.join(lines)
    
    with open('Writerside/hi.tree', 'w', encoding='utf-8') as f:
        f.write(content)

print("\n✅ hi.tree 更新完成!")
print(f"   文件位置: Writerside/hi.tree")

