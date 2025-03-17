#!/usr/bin/env python3

"""
Convert a Jupyter notebook to a Markdown blog post.

Usage:
    python convert_notebook.py <notebook_file> [--output <output_file>]

This will convert the notebook to Markdown and add the appropriate frontmatter.
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime
import subprocess
import shutil

def extract_metadata(notebook_json):
    """Extract metadata from notebook cells."""
    title = ""
    categories = []
    image = None
    date = None
    
    # Try to extract date from filename (format: YYYY-MM-DD-title.ipynb)
    notebook_filename = os.path.basename(args.notebook)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', notebook_filename)
    if date_match:
        date_str = date_match.group(1)
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %d, %Y')
        except ValueError:
            pass
    
    # If no date in filename, use current date
    if not date:
        date = datetime.now().strftime('%B %d, %Y')
    
    # Look for metadata in the first markdown cell
    for cell in notebook_json['cells']:
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])
            
            # Extract title from first heading
            title_match = re.search(r'# (.*?)$', content, re.MULTILINE)
            if title_match and not title:
                title = title_match.group(1).strip()
            
            # Look for fastpages-style metadata
            categories_match = re.search(r'- categories: \[(.*?)\]', content)
            if categories_match:
                categories = [cat.strip() for cat in categories_match.group(1).split(',')]
            
            image_match = re.search(r'- image: (.*?)$', content, re.MULTILINE)
            if image_match:
                image = image_match.group(1).strip()
                
            # If we found all metadata, break
            if title and categories and image:
                break
    
    return {
        'title': title,
        'date': date,
        'categories': categories,
        'image': image
    }

def main():
    # Convert the notebook to markdown using nbconvert
    output_md = args.output if args.output else os.path.splitext(args.notebook)[0] + '.md'
    subprocess.run(['jupyter', 'nbconvert', '--to', 'markdown', args.notebook, '--output', output_md])
    
    # Get the output filename (nbconvert adds .md extension)
    if not output_md.endswith('.md'):
        output_md += '.md'
    
    # Read the converted markdown
    with open(output_md, 'r') as f:
        content = f.read()
    
    # Extract notebook metadata
    with open(args.notebook, 'r') as f:
        notebook_json = json.load(f)
    
    metadata = extract_metadata(notebook_json)
    
    # Create frontmatter
    frontmatter = f"""---
title: {metadata['title']}
date: {metadata['date']}
categories: [{', '.join(metadata['categories'])}]
"""
    
    if metadata['image']:
        frontmatter += f"image: {metadata['image']}\n"
    
    frontmatter += "---\n\n"
    
    # Add frontmatter to content
    content = frontmatter + content
    
    # Create posts directory if it doesn't exist
    posts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts')
    os.makedirs(posts_dir, exist_ok=True)
    
    # Create filename from title
    if args.output:
        post_filename = os.path.basename(args.output)
    else:
        # Extract date from original filename or use today's date
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', os.path.basename(args.notebook))
        date_prefix = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
        
        # Create slug from title
        slug = re.sub(r'[^a-z0-9]+', '-', metadata['title'].lower())
        slug = re.sub(r'(^-|-$)', '', slug)
        
        post_filename = f"{date_prefix}-{slug}.md"
    
    # Save to posts directory
    post_path = os.path.join(posts_dir, post_filename)
    with open(post_path, 'w') as f:
        f.write(content)
    
    # If the markdown file was created outside the posts directory, remove it
    if os.path.abspath(output_md) != os.path.abspath(post_path):
        os.remove(output_md)
    
    print(f"Created blog post: {post_path}")
    print("You can now edit this file to adjust the content if needed.")
    
    # Extract and copy images if they exist
    notebook_dir = os.path.dirname(os.path.abspath(args.notebook))
    images_dir = os.path.join(posts_dir, f"{os.path.splitext(post_filename)[0]}_files")
    
    if os.path.exists(images_dir):
        # Make sure the images directory exists in the posts directory
        os.makedirs(os.path.join(posts_dir, 'images'), exist_ok=True)
        
        # Copy images to the posts/images directory
        for root, _, files in os.walk(images_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    src = os.path.join(root, file)
                    dst = os.path.join(posts_dir, 'images', file)
                    shutil.copy2(src, dst)
                    print(f"Copied image: {file} to posts/images/")
        
        # Update image paths in the markdown
        with open(post_path, 'r') as f:
            content = f.read()
        
        # Update image paths from relative to /posts/images/
        content = re.sub(
            r'!\[(.*?)\]\((.*?)_files/(.*?)\)',
            r'![\1](/posts/images/\3)',
            content
        )
        
        with open(post_path, 'w') as f:
            f.write(content)

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Convert a Jupyter notebook to a Markdown blog post')
    parser.add_argument('notebook', help='Path to the Jupyter notebook file')
    parser.add_argument('--output', help='Output filename (optional)')
    args = parser.parse_args()
    
    main() 