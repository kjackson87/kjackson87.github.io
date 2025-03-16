#!/usr/bin/env python3

"""
A simple script to add tags to an existing blog post.

Usage:
    python add-tags.py post-filename.md "tag1, tag2, tag3"

This will update the post's frontmatter to include the specified tags.
"""

import os
import sys
import re
import argparse

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Add tags to a blog post')
    parser.add_argument('post_filename', help='The filename of the blog post')
    parser.add_argument('tags', help='Comma-separated list of tags to add')
    args = parser.parse_args()
    
    post_filename = args.post_filename
    tags_string = args.tags
    
    if not post_filename or not tags_string:
        print('Please provide a post filename and tags')
        print('Usage: python add-tags.py post-filename.md "tag1, tag2, tag3"')
        sys.exit(1)
    
    # Resolve the full path to the post file
    posts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts')
    post_path = os.path.join(posts_dir, post_filename)
    
    # Check if the file exists
    if not os.path.exists(post_path):
        print(f"File not found: {post_path}")
        print("Make sure the post exists in the posts directory.")
        sys.exit(1)
    
    # Read the file content
    with open(post_path, 'r') as f:
        content = f.read()
    
    # Parse the tags
    tags = [tag.strip() for tag in tags_string.split(',')]
    
    # Check if the file has frontmatter
    front_matter_match = re.search(r'^---\s+([\s\S]*?)\s+---', content)
    
    if not front_matter_match:
        print('No frontmatter found in the post.')
        print('Make sure the post has a frontmatter section at the top.')
        sys.exit(1)
    
    # Extract the frontmatter
    front_matter = front_matter_match.group(1)
    
    # Check if the frontmatter already has tags
    tags_match = re.search(r'tags:\s*\[(.*?)\]', front_matter)
    tags_list_match = re.search(r'tags:\s*\n([\s\S]*?)(?:\n\w|$)', front_matter)
    
    updated_front_matter = None
    
    if tags_match:
        # Update existing tags in array format
        existing_tags = [tag.strip().strip('"\'') for tag in tags_match.group(1).split(',')]
        merged_tags = list(set(existing_tags + tags))  # Remove duplicates
        updated_front_matter = front_matter.replace(
            tags_match.group(0), 
            f'tags: [{", ".join(merged_tags)}]'
        )
    elif tags_list_match:
        # Update existing tags in list format
        existing_tags = []
        for line in tags_list_match.group(1).split('\n'):
            match = re.search(r'[-*]\s*(.*)', line)
            if match:
                existing_tags.append(match.group(1).strip())
        
        merged_tags = list(set(existing_tags + tags))  # Remove duplicates
        tags_list = '\n'.join([f'- {tag}' for tag in merged_tags])
        updated_front_matter = front_matter.replace(
            tags_list_match.group(0), 
            f'tags:\n{tags_list}\n'
        )
    else:
        # Add new tags field
        updated_front_matter = f'{front_matter}\ntags: [{", ".join(tags)}]'
    
    # Replace the frontmatter in the content
    updated_content = content.replace(front_matter_match.group(1), updated_front_matter)
    
    # Write the updated content back to the file
    with open(post_path, 'w') as f:
        f.write(updated_content)
    
    print(f"Updated tags for {post_filename}")
    print(f"Tags: {', '.join(tags)}")

if __name__ == "__main__":
    main() 