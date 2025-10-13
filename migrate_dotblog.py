#!/usr/bin/env python3
"""
點部落文章遷移腳本
從 https://www.dotblogs.com.tw/jakeuj/ 爬取文章並轉換為 Markdown 格式
"""

import requests
from bs4 import BeautifulSoup
import os
import re
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse
import time
from markdownify import markdownify as md

# 配置
BASE_URL = "https://www.dotblogs.com.tw/jakeuj/"
OUTPUT_DIR = "Writerside/topics/dotblog"
IMAGES_DIR = "Writerside/images/dotblog"
TOTAL_PAGES = 1  # 實際上每頁都顯示相同的文章,只需爬取第1頁

# 技術分類映射
CATEGORY_MAPPING = {
    'ABP': 'ABP',
    'ASP.NET': 'C-Sharp',
    'C#': 'C-Sharp',
    '.NET': 'C-Sharp',
    'Azure': 'Azure',
    'GCP': 'gcp',
    'Docker': 'Docker',
    'Git': 'Git',
    'PowerShell': 'PowerShell',
    'Flutter': 'Flutter',
    'Python': 'Python',
    'SQL': 'SQL',
    'Machine Learning': 'LLM',
    'ML': 'LLM',
    'Jetbrains': 'JetBrains',
    'JetBrains': 'JetBrains',
    'Rider': 'JetBrains',
    'Windows': 'Windows',
    'Ubuntu': 'Ubuntu',
    'WSL': 'WSL',
    'Node.js': 'Node-js',
    'iOS': 'Flutter',
    'Android': 'Flutter',
}

def sanitize_filename(title):
    """將標題轉換為合法的檔案名稱"""
    # 移除特殊字符
    filename = re.sub(r'[<>:"/\\|?*]', '', title)
    # 替換空格和其他字符
    filename = re.sub(r'\s+', '-', filename)
    # 移除多餘的破折號
    filename = re.sub(r'-+', '-', filename)
    # 限制長度
    if len(filename) > 100:
        filename = filename[:100]
    return filename.strip('-')

def download_image(img_url, article_id):
    """下載圖片並返回本地路徑"""
    try:
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()
        
        # 解析圖片檔名
        parsed_url = urlparse(img_url)
        img_name = os.path.basename(parsed_url.path)
        if not img_name:
            img_name = f"image_{int(time.time())}.png"
        
        # 確保圖片目錄存在
        os.makedirs(IMAGES_DIR, exist_ok=True)
        
        # 保存圖片
        img_filename = f"article_{article_id}_{img_name}"
        img_path = os.path.join(IMAGES_DIR, img_filename)
        
        with open(img_path, 'wb') as f:
            f.write(response.content)
        
        # 返回相對於 Writerside 的路徑
        return f"dotblog/{img_filename}"
    except Exception as e:
        print(f"  ⚠️  下載圖片失敗: {img_url} - {e}")
        return img_url

def html_to_markdown(html_content, article_url):
    """將 HTML 內容轉換為 Markdown"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # 移除腳本、樣式和廣告
    for element in soup(["script", "style", "iframe", "noscript"]):
        element.decompose()

    # 移除廣告相關的 div
    for ad in soup.find_all('div', class_=re.compile(r'ad|advertisement', re.I)):
        ad.decompose()

    # 使用 markdownify 轉換
    markdown_text = md(str(soup), heading_style="ATX")

    # 清理多餘的空行
    lines = []
    prev_empty = False
    for line in markdown_text.split('\n'):
        line = line.rstrip()
        if line:
            lines.append(line)
            prev_empty = False
        elif not prev_empty:
            lines.append('')
            prev_empty = True

    return '\n'.join(lines)

def get_article_links_from_page(page_num):
    """從列表頁面獲取所有文章連結"""
    if page_num == 1:
        url = BASE_URL
    else:
        url = f"{BASE_URL}?page={page_num}"

    print(f"\n📄 正在爬取第 {page_num} 頁: {url}")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # 找到所有文章連結
        article_links = []

        # 尋找文章區塊 - 根據實際 HTML 結構調整
        articles = soup.find_all('div', class_='post-item') or soup.find_all('article')

        if not articles:
            # 嘗試其他可能的選擇器
            articles = soup.find_all('div', class_='post')

        for article in articles:
            # 尋找文章標題連結
            title_link = article.find('a', href=re.compile(r'/jakeuj/\d{4}/\d{2}/\d{2}/'))

            if not title_link:
                # 嘗試其他可能的連結格式
                title_link = article.find('a', href=re.compile(r'/jakeuj/'))

            if title_link:
                href = title_link.get('href')
                if href and '/jakeuj/' in href and not href.endswith('/jakeuj/'):
                    full_url = urljoin(BASE_URL, href)
                    title = title_link.get_text().strip()

                    # 提取日期
                    date_elem = article.find('time') or article.find(string=re.compile(r'\d{4}-\d{2}-\d{2}'))
                    date = date_elem if isinstance(date_elem, str) else (date_elem.get_text().strip() if date_elem else "")

                    article_links.append({
                        'url': full_url,
                        'title': title,
                        'date': date
                    })

        print(f"  ✓ 找到 {len(article_links)} 篇文章")
        return article_links

    except Exception as e:
        print(f"  ❌ 爬取失敗: {e}")
        return []

def fetch_article(article_info):
    """爬取單篇文章"""
    url = article_info['url']
    print(f"\n📖 正在爬取文章: {article_info['title']}")
    print(f"   URL: {url}")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # 從 JSON-LD 結構化數據中提取標題(更準確)
        json_ld = soup.find('script', type='application/ld+json')
        title = article_info['title']
        if json_ld:
            try:
                data = json.loads(json_ld.string)
                if 'headline' in data:
                    title = data['headline']
            except:
                pass

        # 如果 JSON-LD 沒有,嘗試從 meta 標籤或 h2 提取
        if not title or title == article_info['title']:
            meta_title = soup.find('meta', property='og:title')
            if meta_title:
                title = meta_title.get('content', article_info['title'])
            else:
                # 尋找文章標題 h2
                title_h2 = soup.find('h2')
                if title_h2:
                    title = title_h2.get_text().strip()

        print(f"  ✓ 標題: {title}")

        # 提取發布日期
        date_match = re.search(r'(\d{4})/(\d{2})/(\d{2})', url)
        if date_match:
            publish_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
        else:
            publish_date = article_info.get('date', '未知日期')
        print(f"  ✓ 日期: {publish_date}")

        # 提取標籤 - 從文章底部的標籤區域
        tags = []
        # 尋找包含標籤的 section 或 div
        tag_links = soup.find_all('a', href=re.compile(r'/tag/'))
        seen_tags = set()
        for tag_elem in tag_links:
            tag_text = tag_elem.get_text().strip()
            if tag_text and tag_text not in seen_tags and len(tag_text) < 50:
                tags.append(tag_text)
                seen_tags.add(tag_text)
        print(f"  ✓ 標籤: {', '.join(tags) if tags else '無'}")

        # 提取文章內容 - 尋找主要內容區域
        # 點部落的文章內容通常在特定的 div 中
        content_elem = None

        # 方法1: 尋找包含文章內容的主要 div
        main_content = soup.find('div', class_='post-item')
        if main_content:
            # 移除不需要的部分
            for unwanted in main_content.find_all(['header', 'footer', 'nav', 'aside']):
                unwanted.decompose()
            content_elem = main_content

        # 方法2: 如果找不到,嘗試其他選擇器
        if not content_elem:
            content_elem = soup.find('article') or soup.find('div', class_='content')

        if not content_elem:
            print(f"  ⚠️  使用整個 body 作為內容")
            content_elem = soup.find('body')

        if not content_elem:
            print(f"  ❌ 找不到文章內容")
            return None

        # 移除頁首、頁尾、側邊欄等
        for unwanted_class in ['navbar', 'header', 'footer', 'sidebar', 'side-sticky', 'page-footer', 'navbar-top']:
            for elem in content_elem.find_all(class_=re.compile(unwanted_class, re.I)):
                elem.decompose()

        # 轉換為 Markdown
        markdown_content = html_to_markdown(str(content_elem), url)

        # 判斷分類
        category = 'Other'
        for tag in tags:
            for key, value in CATEGORY_MAPPING.items():
                if key.lower() in tag.lower():
                    category = value
                    break
            if category != 'Other':
                break

        return {
            'title': title,
            'date': publish_date,
            'tags': tags,
            'category': category,
            'content': markdown_content,
            'url': url
        }

    except requests.exceptions.RequestException as e:
        print(f"  ❌ 請求失敗: {e}")
        return None
    except Exception as e:
        print(f"  ❌ 處理失敗: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_article_to_markdown(article):
    """將文章保存為 Markdown 檔案"""
    # 生成檔案名稱
    filename = sanitize_filename(article['title'])
    if not filename:
        # 從 URL 提取檔名
        url_parts = article['url'].rstrip('/').split('/')
        filename = url_parts[-1] if url_parts else f"article_{int(time.time())}"

    filepath = os.path.join(OUTPUT_DIR, f"{filename}.md")

    # 確保目錄存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 生成 Markdown 內容
    md_content = f"""# {article['title']}

> **原文發布日期:** {article['date']}
> **原文連結:** {article['url']}
> **標籤:** {', '.join(article['tags']) if article['tags'] else '無'}

---

{article['content']}

---

*本文章從點部落遷移至 Writerside*
"""

    # 保存檔案
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"  ✓ 已保存: {filepath}")

    return {
        'filename': f"{filename}.md",
        'category': article['category'],
        'title': article['title']
    }

def main():
    """主程式"""
    print("=" * 60)
    print("點部落文章遷移工具")
    print("=" * 60)

    all_article_links = []

    # 第一步:爬取所有頁面的文章列表
    print("\n🔍 第一階段:收集所有文章連結...")
    for page_num in range(1, TOTAL_PAGES + 1):
        links = get_article_links_from_page(page_num)
        all_article_links.extend(links)
        time.sleep(1)  # 避免請求過快

    print(f"\n✓ 總共找到 {len(all_article_links)} 篇文章")

    # 去重
    unique_links = {}
    for link in all_article_links:
        unique_links[link['url']] = link

    all_article_links = list(unique_links.values())
    print(f"✓ 去重後剩餘 {len(all_article_links)} 篇文章")

    # 第二步:爬取每篇文章的內容
    print("\n📚 第二階段:爬取文章內容...")
    articles_info = []

    for idx, article_link in enumerate(all_article_links, 1):
        print(f"\n[{idx}/{len(all_article_links)}]")
        article = fetch_article(article_link)
        if article:
            file_info = save_article_to_markdown(article)
            articles_info.append(file_info)

        # 避免請求過快
        time.sleep(2)

    # 確保目錄存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 保存文章資訊供後續更新 hi.tree 使用
    info_file = os.path.join(OUTPUT_DIR, '_articles_info.json')
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(articles_info, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"✅ 完成! 共處理 {len(articles_info)} 篇文章")
    print(f"📁 文章保存在: {OUTPUT_DIR}")
    print(f"🖼️  圖片保存在: {IMAGES_DIR}")
    print(f"📋 文章資訊: {info_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()

