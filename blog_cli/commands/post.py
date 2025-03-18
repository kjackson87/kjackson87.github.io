"""
Post-related commands for the blog CLI
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

import click

from blog_cli.utils.frontmatter import extract_frontmatter, update_frontmatter
from blog_cli.utils.templates import get_post_template

# Command group for post-related commands
@click.group()
def post():
    """Commands for managing blog posts"""
    pass

@post.command()
@click.argument('title')
@click.option('--date', help='Publish date (defaults to today)')
def create(title, date):
    """Create a new blog post with the specified title"""
    # Create a filename from the title
    filename = re.sub(r'[^a-z0-9]+', '-', title.lower())
    filename = re.sub(r'(^-|-$)', '', filename) + '.md'
    
    # Format the date if provided, otherwise use today
    if date:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            click.echo("Date format should be YYYY-MM-DD", err=True)
            return 1
    else:
        date = datetime.now().strftime('%B %d, %Y')
    
    # Generate the post content
    content = get_post_template(title, date)
    
    # Make sure the posts directory exists
    posts_dir = Path.cwd() / 'posts'
    posts_dir.mkdir(exist_ok=True)
    
    # Write the file
    file_path = posts_dir / filename
    with open(file_path, 'w') as f:
        f.write(content)
    
    click.echo(f"Created new post: {file_path}")
    return 0

@post.command(name='add-tags')
@click.argument('post_filename')
@click.argument('tags')
def add_tags(post_filename, tags):
    """Add tags to an existing blog post"""
    # Parse the tags
    tag_list = [tag.strip() for tag in tags.split(',')]
    
    # Resolve the full path to the post file
    posts_dir = Path.cwd() / 'posts'
    post_path = posts_dir / post_filename
    
    # Check if the file exists
    if not post_path.exists():
        click.echo(f"File not found: {post_path}", err=True)
        return 1
    
    # Read the file content
    with open(post_path, 'r') as f:
        content = f.read()
    
    # Update the frontmatter with the new tags
    updated_content = update_frontmatter(content, {'tags': tag_list})
    
    # Write the updated content back to the file
    with open(post_path, 'w') as f:
        f.write(updated_content)
    
    click.echo(f"Updated tags for {post_filename}")
    click.echo(f"Tags: {', '.join(tag_list)}")
    return 0

@post.command(name='generate-index')
def generate_index():
    """Generate a JSON index of all blog posts"""
    posts = []
    posts_dir = Path.cwd() / 'posts'
    
    if not posts_dir.exists():
        click.echo(f"Posts directory not found: {posts_dir}", err=True)
        return 1
        
    for filepath in posts_dir.glob('*.md'):
        filename = filepath.name
        
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
            'tags': metadata.get('tags', []),
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
    
    click.echo(f"Generated index with {len(posts)} posts")
    return 0 