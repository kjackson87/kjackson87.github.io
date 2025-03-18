#!/usr/bin/env python3
"""
Generate static HTML files for each markdown post in the posts directory.
This solves the issue of GitHub Pages not serving raw markdown files.
"""

import os
import re
import json
import shutil
import markdown
from datetime import datetime

def extract_frontmatter(content):
    """Extract frontmatter from a markdown file."""
    frontmatter_match = re.match(r'^---\s+([\s\S]*?)\s+---', content)
    if not frontmatter_match:
        return {}, content
    
    frontmatter = frontmatter_match[1]
    
    # Extract title
    title_match = re.search(r'title:\s*(.+)', frontmatter)
    title = title_match.group(1).strip() if title_match else ""
    
    # Extract date
    date_match = re.search(r'date:\s*(.+)', frontmatter)
    date = date_match.group(1).strip() if date_match else ""
    
    # Extract tags
    tags = []
    tags_match = re.search(r'tags:\s*\[(.*?)\]', frontmatter)
    if tags_match:
        tags = [tag.strip().replace('"', '').replace("'", "") for tag in tags_match.group(1).split(',')]
    else:
        # Alternative format: tags on multiple lines
        tags_list_match = re.search(r'tags:\s*\n([\s\S]*?)(?:\n\w|$)', frontmatter)
        if tags_list_match:
            tags = [re.match(r'[-*]\s*(.*)', line).group(1).strip() 
                   for line in tags_list_match.group(1).split('\n') 
                   if re.match(r'[-*]\s*(.*)', line)]
    
    # Extract categories
    categories = []
    cat_match = re.search(r'categories:\s*\[(.*?)\]', frontmatter)
    if cat_match:
        categories = [cat.strip().replace('"', '').replace("'", "") for cat in cat_match.group(1).split(',')]
    
    # Extract image
    image_match = re.search(r'image:\s*(.+)', frontmatter)
    image = image_match.group(1).strip() if image_match else None
    
    # Remove frontmatter from content
    content_without_frontmatter = re.sub(r'^---\s+[\s\S]*?---\s+', '', content)
    
    return {
        'title': title,
        'date': date,
        'tags': tags,
        'categories': categories,
        'image': image
    }, content_without_frontmatter

def generate_html_posts():
    """Generate static HTML files for each markdown post."""
    posts_dir = 'posts'
    html_posts_dir = 'html_posts'
    
    # Create directory for HTML posts if it doesn't exist
    if not os.path.exists(html_posts_dir):
        os.makedirs(html_posts_dir)
    
    posts_data = []
    
    for filename in os.listdir(posts_dir):
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter and content
        metadata, content_without_frontmatter = extract_frontmatter(content)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(content_without_frontmatter, extensions=['fenced_code', 'codehilite'])
        
        # Get base filename without extension
        base_filename = os.path.splitext(filename)[0]
        html_filename = f"{base_filename}.html"
        html_filepath = os.path.join(html_posts_dir, html_filename)
        
        # Extract excerpt
        excerpt_match = re.search(r'^(.*?)\n\n', content_without_frontmatter, re.DOTALL)
        excerpt = excerpt_match.group(1) if excerpt_match else content_without_frontmatter[:150] + '...'
        excerpt = re.sub(r'^#+\s+.*$', '', excerpt, flags=re.MULTILINE).strip()
        
        # Save HTML file
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated {html_filepath}")
        
        # Combine metadata for index
        post_data = {
            'filename': base_filename,
            'title': metadata.get('title', base_filename.replace('-', ' ')),
            'date': metadata.get('date', ''),
            'categories': metadata.get('categories', []),
            'tags': metadata.get('tags', []),
            'image': metadata.get('image', ''),
            'excerpt': excerpt,
            'html_filename': html_filename
        }
        
        posts_data.append(post_data)
    
    # Sort posts by date (newest first)
    try:
        posts_data.sort(key=lambda post: datetime.strptime(post['date'], '%B %d, %Y') if post['date'] else datetime.min, reverse=True)
    except ValueError:
        # If date format varies, try a simpler sort
        posts_data.sort(key=lambda post: post['date'] if post['date'] else '', reverse=True)
    
    # Write enhanced index to JSON file
    with open('post-index.json', 'w', encoding='utf-8') as f:
        json.dump(posts_data, f, indent=2)
    
    print(f"Generated index with {len(posts_data)} posts")
    
    # Copy any image files from posts/images to html_posts/images
    if os.path.exists(os.path.join(posts_dir, 'images')):
        images_dir = os.path.join(posts_dir, 'images')
        html_images_dir = os.path.join(html_posts_dir, 'images')
        
        if not os.path.exists(html_images_dir):
            os.makedirs(html_images_dir)
        
        for image in os.listdir(images_dir):
            src = os.path.join(images_dir, image)
            dst = os.path.join(html_images_dir, image)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                print(f"Copied image {image}")

if __name__ == "__main__":
    generate_html_posts() 