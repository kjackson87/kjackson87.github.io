"""
Page-related commands for the blog CLI
"""

import os
from pathlib import Path

import click

from blog_cli.utils.templates import get_page_template

# Command group for page-related commands
@click.group()
def page():
    """Commands for managing static pages"""
    pass

@page.command()
@click.argument('page_name')
@click.option('--title', default="New Page", help='The title of the page')
@click.option('--description', default="This is a new page.", help='Brief description of the page content')
@click.option('--subdirectory', is_flag=True, help='Whether the page will be in a subdirectory')
def create(page_name, title, description, subdirectory):
    """Create a new HTML page with the site's header and footer components"""
    # Define the path
    html_file = f"{page_name}.html"
    
    # Create HTML content
    html_content = get_page_template(title, description, subdirectory)

    # Write the HTML file
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    click.echo(f"Created new page: {html_file}")
    
    # Ask if the user wants to update the header
    if click.confirm("Do you want to add a link to this page in the header navigation?"):
        update_header(page_name, title)
    
    return 0

def update_header(page_name, title):
    """
    Update the header component to include a link to the new page.
    
    Args:
        page_name: The name of the HTML file (without extension)
        title: The title of the page
    """
    header_file = Path.cwd() / "components" / "header.html"
    
    # Check if the header file exists
    if not header_file.exists():
        click.echo(f"Header file not found: {header_file}", err=True)
        return 1
    
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
            click.echo(f"Link to '{title}' already exists in the header.")
            return 0
        
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
            
            click.echo(f"Added link to '{title}' in the header navigation.")
            return 0
        else:
            click.echo("Could not find a suitable position to add the link.", err=True)
            return 1
    else:
        click.echo("Could not find the navigation section in the header.", err=True)
        return 1 