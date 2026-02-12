#!/usr/bin/env python3
"""
修復 Markdown 文件末尾換行符
"""
import os
import glob

def fix_file_ending(filepath):
    """確保文件以換行符結尾"""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        if content and not content.endswith(b'\n'):
            with open(filepath, 'ab') as f:
                f.write(b'\n')
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # 獲取所有 Markdown 文件
    md_files = glob.glob('Writerside/topics/**/*.md', recursive=True)
    
    fixed_count = 0
    for filepath in md_files:
        if fix_file_ending(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1
    
    print(f"\n總共修復了 {fixed_count} 個文件")

if __name__ == '__main__':
    main()

