#!/usr/bin/env python3
"""
Create a new page with the site's header and footer components.
This script generates HTML files with the shared components.
"""

import os
import argparse
from datetime import datetime

def create_page(page_name, title, description, in_subdirectory=False):
    """
    Create a new HTML page with the site's header and footer components.
    
    Args:
        page_name: The name of the HTML file to create (without extension)
        title: The title of the page
        description: A brief description of the page content
        in_subdirectory: Whether the page will be in a subdirectory (affects component paths)
    """
    # Define the paths
    html_file = f"{page_name}.html"
    component_path = "../components/" if in_subdirectory else "components/"
    js_path = "../js/" if in_subdirectory else "js/"
    
    # Create HTML content
    html_content = f"""<!DOCTYPE html>
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

    # Write the HTML file
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    print(f"Created new page: {html_file}")
    
    # Update the header component to include a link to the new page
    update_header(page_name, title)


def update_header(page_name, title):
    """
    Ask if the user wants to update the header component to include a link to the new page.
    
    Args:
        page_name: The name of the HTML file (without extension)
        title: The title of the page
    """
    update = input(f"Do you want to add a link to '{title}' in the header navigation? (y/n): ")
    
    if update.lower() == 'y':
        header_file = "components/header.html"
        
        # Read the current header content
        with open(header_file, 'r') as f:
            header_content = f.read()
        
        # Find the navigation section
        nav_start = header_content.find('<nav>')
        nav_end = header_content.find('</nav>', nav_start)
        
        if nav_start != -1 and nav_end != -1:
            # Insert the new link before the nav closing tag
            new_link = f'        <a href="{page_name}.html">{title}</a>\n'
            
            # Check if the link already exists
            if f'href="{page_name}.html"' in header_content:
                print(f"Link to '{title}' already exists in the header.")
                return
            
            # Find the last link in the nav
            last_link_end = header_content.rfind('</a>', nav_start, nav_end)
            
            if last_link_end != -1:
                # Insert after the last link
                updated_header = (
                    header_content[:last_link_end + 4] + 
                    '\n' + new_link.rstrip() +
                    header_content[last_link_end + 4:]
                )
                
                # Write the updated header
                with open(header_file, 'w') as f:
                    f.write(updated_header)
                
                print(f"Added link to '{title}' in the header navigation.")
            else:
                print("Could not find a suitable position to add the link.")
        else:
            print("Could not find the navigation section in the header.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new page with the site's header and footer components.")
    parser.add_argument("page_name", help="Name of the HTML file to create (without extension)")
    parser.add_argument("--title", help="Title of the page", default="New Page")
    parser.add_argument("--description", help="Brief description of the page content", default="This is a new page.")
    parser.add_argument("--subdirectory", action="store_true", help="Whether the page will be in a subdirectory")
    
    args = parser.parse_args()
    
    create_page(args.page_name, args.title, args.description, args.subdirectory) 