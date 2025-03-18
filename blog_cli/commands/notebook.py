"""
Notebook-related commands for the blog CLI
"""

import os
import re
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

import click

from blog_cli.utils.frontmatter import update_frontmatter

# Command group for notebook-related commands
@click.group()
def notebook():
    """Commands for working with Jupyter notebooks"""
    pass

@notebook.command()
@click.argument('notebook_path')
@click.option('--output', help='Output filename (optional)')
def convert(notebook_path, output):
    """Convert a Jupyter notebook to a Markdown blog post"""
    notebook_path = Path(notebook_path)
    
    # Check if the notebook exists
    if not notebook_path.exists():
        click.echo(f"Notebook not found: {notebook_path}", err=True)
        return 1
        
    # Ensure the notebook is a .ipynb file
    if notebook_path.suffix != '.ipynb':
        click.echo(f"File is not a Jupyter notebook: {notebook_path}", err=True)
        return 1
    
    try:
        # Check if jupyter is installed
        subprocess.run(['jupyter', '--version'], check=True, capture_output=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        click.echo("Jupyter is not installed or not in PATH. Please install it with: pip install jupyter", err=True)
        return 1
    
    # Extract metadata from the notebook
    with open(notebook_path, 'r') as f:
        notebook_json = json.load(f)
    
    metadata = extract_notebook_metadata(notebook_json, notebook_path.name)
    
    # Convert the notebook to markdown using nbconvert
    temp_output = f"{notebook_path.stem}_temp.md"
    click.echo(f"Converting notebook to markdown...")
    
    try:
        subprocess.run(
            ['jupyter', 'nbconvert', '--to', 'markdown', str(notebook_path), '--output', temp_output],
            check=True,
            capture_output=True
        )
    except subprocess.SubprocessError as e:
        click.echo(f"Error converting notebook: {e}", err=True)
        return 1
    
    # Get the full path to the converted file (nbconvert adds .md extension)
    temp_md_path = notebook_path.parent / f"{temp_output}.md"
    if not temp_md_path.exists():
        temp_md_path = notebook_path.parent / temp_output
    
    if not temp_md_path.exists():
        click.echo(f"Converted markdown file not found", err=True)
        return 1
    
    # Read the converted markdown
    with open(temp_md_path, 'r') as f:
        content = f.read()
    
    # Add frontmatter to content
    content = update_frontmatter(content, metadata)
    
    # Create posts directory if it doesn't exist
    posts_dir = Path.cwd() / 'posts'
    posts_dir.mkdir(exist_ok=True)
    
    # Create the output filename
    if output:
        post_filename = output if output.endswith('.md') else f"{output}.md"
    else:
        # Extract date from original filename or use today's date
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', notebook_path.name)
        date_prefix = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
        
        # Create slug from title
        slug = re.sub(r'[^a-z0-9]+', '-', metadata['title'].lower())
        slug = re.sub(r'(^-|-$)', '', slug)
        
        post_filename = f"{date_prefix}-{slug}.md"
    
    # Save to posts directory
    post_path = posts_dir / post_filename
    with open(post_path, 'w') as f:
        f.write(content)
    
    # Remove the temporary markdown file
    temp_md_path.unlink()
    
    click.echo(f"Created blog post: {post_path}")
    
    # Handle images
    handle_notebook_images(notebook_path, post_path, posts_dir)
    
    return 0

def extract_notebook_metadata(notebook_json, notebook_filename):
    """Extract metadata from notebook cells."""
    title = ""
    categories = []
    image = None
    date = None
    
    # Try to extract date from filename (format: YYYY-MM-DD-title.ipynb)
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
    
    # If no title found, use the notebook filename
    if not title:
        title = notebook_filename.replace('.ipynb', '').replace('-', ' ').title()
    
    return {
        'title': title,
        'date': date,
        'categories': categories,
        'image': image
    }

def handle_notebook_images(notebook_path, post_path, posts_dir):
    """Extract and copy images from the notebook"""
    images_dir = notebook_path.parent / f"{notebook_path.stem}_files"
    
    if not images_dir.exists() or not images_dir.is_dir():
        return
    
    # Make sure the images directory exists in the posts directory
    post_images_dir = posts_dir / 'images'
    post_images_dir.mkdir(exist_ok=True)
    
    # Find all images in the notebook files directory
    click.echo("Processing notebook images...")
    image_files = []
    for ext in ['.png', '.jpg', '.jpeg', '.gif']:
        image_files.extend(list(images_dir.glob(f"**/*{ext}")))
    
    if not image_files:
        return
    
    # Copy images to the posts/images directory
    for img_file in image_files:
        target_path = post_images_dir / img_file.name
        shutil.copy2(img_file, target_path)
        click.echo(f"  Copied: {img_file.name}")
    
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
    
    click.echo(f"Updated image paths in the blog post") 