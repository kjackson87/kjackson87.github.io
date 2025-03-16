#!/usr/bin/env python3

"""
A simple script to create a new blog post with the correct frontmatter.

Usage:
    python create-post.py "My Post Title"

This will create a new file in the posts directory with the correct frontmatter.
"""

import os
import sys
import re
from datetime import datetime
import argparse

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Create a new blog post')
    parser.add_argument('title', help='The title of the blog post')
    args = parser.parse_args()
    
    title = args.title
    
    if not title:
        print('Please provide a post title')
        print('Usage: python create-post.py "My Post Title"')
        sys.exit(1)
    
    # Create a filename from the title
    filename = re.sub(r'[^a-z0-9]+', '-', title.lower())
    filename = re.sub(r'(^-|-$)', '', filename) + '.md'
    
    # Get the current date in a nice format
    date = datetime.now().strftime('%B %d, %Y')
    
    # Create the frontmatter and initial content
    content = f"""---
title: {title}
date: {date}
---

# {title}

Write your post content here...
"""
    
    # Make sure the posts directory exists
    posts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts')
    os.makedirs(posts_dir, exist_ok=True)
    
    # Write the file
    file_path = os.path.join(posts_dir, filename)
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created new post: {file_path}")
    print("You can now edit this file to add your content.")

if __name__ == "__main__":
    main() 