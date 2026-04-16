#!/usr/bin/env python3
"""
自动整理项目文件脚本。
根据文件扩展名将文件归类到对应文件夹中。
如果遇到新类型，则自动创建新文件夹。
"""

import os
import shutil
from pathlib import Path

# 定义要忽略的文件夹和文件
IGNORE_DIRS = {'.git', '.vscode', '__pycache__', 'node_modules', '.idea'}
IGNORE_FILES = {'organize_files.py'}  # 忽略脚本本身

# 定义文件类型映射：扩展名 -> 文件夹名
FILE_TYPE_MAP = {
    '.html': 'html',
    '.htm': 'html',
    '.css': 'css',
    '.js': 'js',
    '.py': 'python',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.ipynb': 'notebooks',
    '.md': 'docs',
    '.txt': 'docs',
    '.json': 'config',
    '.xml': 'config',
    '.yaml': 'config',
    '.yml': 'config',
    '.png': 'images',
    '.jpg': 'images',
    '.jpeg': 'images',
    '.gif': 'images',
    '.svg': 'images',
    '.pdf': 'docs',
    '.zip': 'archives',
    '.tar': 'archives',
    '.gz': 'archives',
}

def get_folder_name(extension):
    """
    根据文件扩展名获取文件夹名。
    如果扩展名不在映射中，则使用扩展名（去掉点）作为文件夹名。
    """
    if extension in FILE_TYPE_MAP:
        return FILE_TYPE_MAP[extension]
    else:
        # 新类型：使用扩展名作为文件夹名（去掉点）
        return extension.lstrip('.')

def organize_files(root_dir):
    """
    整理指定目录下的文件。
    只处理当前目录的文件，不递归处理子目录。
    """
    root_path = Path(root_dir)
    
    # 遍历目录，只处理文件
    for item in root_path.iterdir():
        if item.is_file():
            # 检查是否忽略
            if item.name in IGNORE_FILES:
                continue
            
            # 获取扩展名
            extension = item.suffix.lower()
            
            # 获取文件夹名
            folder_name = get_folder_name(extension)
            
            # 创建文件夹（如果不存在）
            folder_path = root_path / folder_name
            folder_path.mkdir(exist_ok=True)
            
            # 移动文件
            dest_path = folder_path / item.name
            print(f"移动 {item.name} 到 {folder_name}/")
            shutil.move(str(item), str(dest_path))

def main():
    # 获取当前脚本所在目录
    script_dir = Path(__file__).parent
    print(f"开始整理目录: {script_dir}")
    
    # 整理文件
    organize_files(script_dir)
    
    print("文件整理完成！")

if __name__ == "__main__":
    main()
