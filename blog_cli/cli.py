#!/usr/bin/env python3
"""
Main entry point for the blog CLI tool
"""

import click
from blog_cli import __version__

@click.group()
@click.version_option(version=__version__)
def cli():
    """Blog CLI - A command-line tool for managing static blog content"""
    pass

# Import command groups
from blog_cli.commands.post import post
from blog_cli.commands.page import page
from blog_cli.commands.notebook import notebook

# Add command groups to the CLI
cli.add_command(post)
cli.add_command(page)
cli.add_command(notebook)

if __name__ == "__main__":
    cli() 