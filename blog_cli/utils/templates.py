"""
Utility functions for template handling
"""

import os
from datetime import datetime

def get_page_template(title, description, in_subdirectory=False):
    """
    Get the HTML template for a new page.
    
    Args:
        title: The title of the page
        description: A brief description of the page content
        in_subdirectory: Whether the page will be in a subdirectory (affects component paths)
        
    Returns:
        HTML template string
    """
    # Define the paths
    component_path = "../components/" if in_subdirectory else "components/"
    js_path = "../js/" if in_subdirectory else "js/"
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Kyle Jackson</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 1rem;
            background-color: #fafafa;
        }}
        header {{
            margin-bottom: 2rem;
        }}
        nav {{
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }}
        nav a {{
            text-decoration: none;
            color: #0366d6;
            font-weight: 500;
        }}
        nav a:hover {{
            text-decoration: underline;
        }}
        main {{
            margin-bottom: 2rem;
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }}
        h2 {{
            font-size: 1.8rem;
            margin: 1.5rem 0 1rem;
            color: #333;
            border-bottom: 1px solid #eee;
            padding-bottom: 0.5rem;
        }}
        p {{
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }}
        section {{
            margin-bottom: 2.5rem;
        }}
        footer {{
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 0.9rem;
        }}
        .social-links {{
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
        }}
    </style>
    <!-- Include the component loader script -->
    <script src="{js_path}include.js"></script>
</head>
<body>
    <!-- Include the header component -->
    <div data-include="{component_path}header.html"></div>

    <main>
        <h2>{title}</h2>
        
        <section>
            <p>{description}</p>
            
            <!-- Your content goes here -->
            <p>This is a new page created on {datetime.now().strftime('%Y-%m-%d')}.</p>
            <p>Replace this placeholder content with your actual content.</p>
        </section>
    </main>

    <!-- Include the footer component -->
    <div data-include="{component_path}footer.html"></div>
</body>
</html>
"""

def get_post_template(title, date=None):
    """
    Get the markdown template for a new blog post.
    
    Args:
        title: The title of the post
        date: The date of the post (defaults to current date)
        
    Returns:
        Markdown template string
    """
    if not date:
        date = datetime.now().strftime('%B %d, %Y')
    
    return f"""---
title: {title}
date: {date}
---

# {title}

Write your post content here...
""" 