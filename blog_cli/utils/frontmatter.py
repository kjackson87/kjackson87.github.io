"""
Utility functions for handling frontmatter in markdown files
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

def extract_frontmatter(content: str) -> Dict[str, Any]:
    """
    Extract frontmatter from a markdown file content.
    
    Args:
        content: The content of the markdown file
        
    Returns:
        Dictionary containing the frontmatter fields
    """
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
    
    # Extract tags
    tags = []
    tags_match = re.search(r'tags:\s*\[(.*?)\]', frontmatter)
    if tags_match:
        tags = [tag.strip() for tag in tags_match.group(1).split(',')]
    
    # Extract image
    image_match = re.search(r'image:\s*(.+)', frontmatter)
    image = image_match.group(1).strip() if image_match else None
    
    return {
        'title': title,
        'date': date,
        'categories': categories,
        'tags': tags,
        'image': image
    }

def add_frontmatter(content: str, metadata: Dict[str, Any]) -> str:
    """
    Add or update frontmatter in the content.
    
    Args:
        content: The content to add frontmatter to
        metadata: Dictionary containing the frontmatter fields
        
    Returns:
        Updated content with frontmatter
    """
    # Remove existing frontmatter if present
    content_without_frontmatter = re.sub(r'^---\s+[\s\S]*?---\s+', '', content)
    
    # Format date if not provided
    if 'date' not in metadata or not metadata['date']:
        metadata['date'] = datetime.now().strftime('%B %d, %Y')
    
    # Build frontmatter
    frontmatter = "---\n"
    
    for key, value in metadata.items():
        if key in ('categories', 'tags') and isinstance(value, list) and value:
            frontmatter += f"{key}: [{', '.join(value)}]\n"
        elif value:
            frontmatter += f"{key}: {value}\n"
    
    frontmatter += "---\n\n"
    
    return frontmatter + content_without_frontmatter

def update_frontmatter(content: str, metadata: Dict[str, Any]) -> str:
    """
    Update existing frontmatter in the content.
    
    Args:
        content: The content with frontmatter to update
        metadata: Dictionary containing the frontmatter fields to update
        
    Returns:
        Updated content with modified frontmatter
    """
    frontmatter_match = re.match(r'^---\s+([\s\S]*?)\s+---', content)
    if not frontmatter_match:
        # No frontmatter found, add it
        return add_frontmatter(content, metadata)
    
    existing_metadata = extract_frontmatter(content)
    # Merge new metadata with existing
    for key, value in metadata.items():
        if value is not None:
            existing_metadata[key] = value
    
    # Replace the frontmatter
    content_without_frontmatter = re.sub(r'^---\s+[\s\S]*?---\s+', '', content)
    return add_frontmatter(content_without_frontmatter, existing_metadata) 