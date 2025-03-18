#!/usr/bin/env python3
"""
Generate a JSON index of all blog posts in the posts directory.
This should be run before deploying to GitHub Pages.
"""

import os
import re
import json
from datetime import datetime

def extract_frontmatter(content):
    """Extract frontmatter from a markdown file."""
    frontmatter_match = re.match(r'^---\s+([\s\S]*?)\s+---', content)
    if not frontmatter_match:
        return {}
    
    frontmatter = frontmatter_match[1]
    
    # Extract title
    title_match = re.search(r'title:\s*(.+)', frontmatter)
    title = title_match.group(1).strip() if title_match else ""
    
    # Extract date
    date_match = re.search(r'date:\s*(.+)', frontmatter)
    date = date_match.group(1).strip() if date_match else ""
    
    # Extract categories/tags
    categories = []
    cat_match = re.search(r'categories:\s*\[(.*?)\]', frontmatter)
    if cat_match:
        categories = [cat.strip() for cat in cat_match.group(1).split(',')]
    
    # Extract image
    image_match = re.search(r'image:\s*(.+)', frontmatter)
    image = image_match.group(1).strip() if image_match else None
    
    return {
        'title': title,
        'date': date,
        'categories': categories,
        'image': image
    }

def generate_post_index():
    """Generate a JSON index of all posts."""
    posts = []
    posts_dir = 'posts'
    
    for filename in os.listdir(posts_dir):
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = extract_frontmatter(content)
        
        # Extract excerpt
        content_without_frontmatter = re.sub(r'^---\s+[\s\S]*?---\s+', '', content)
        excerpt_match = re.search(r'^(.*?)\n\n', content_without_frontmatter, re.DOTALL)
        excerpt = excerpt_match.group(1) if excerpt_match else content_without_frontmatter[:150] + '...'
        excerpt = re.sub(r'^#+\s+.*$', '', excerpt, flags=re.MULTILINE).strip()
        
        posts.append({
            'filename': filename,
            'title': metadata.get('title', filename.replace('.md', '').replace('-', ' ')),
            'date': metadata.get('date', ''),
            'categories': metadata.get('categories', []),
            'image': metadata.get('image', ''),
            'excerpt': excerpt
        })
    
    # Sort posts by date (newest first)
    try:
        posts.sort(key=lambda post: datetime.strptime(post['date'], '%B %d, %Y') if post['date'] else datetime.min, reverse=True)
    except ValueError:
        # If date format varies, try a simpler sort
        posts.sort(key=lambda post: post['date'] if post['date'] else '', reverse=True)
    
    # Write index to JSON file
    with open('post-index.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2)
    
    print(f"Generated index with {len(posts)} posts")

if __name__ == "__main__":
    generate_post_index()