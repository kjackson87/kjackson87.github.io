#!/bin/bash
# Setup script for the blog

# Install required dependencies
echo "Installing required dependencies..."
pip install markdown

# Generate post index
echo "Generating post index..."
python generate_post_index.py

# Generate HTML posts
echo "Generating HTML posts..."
python generate_html_posts.py

echo "Blog setup complete!"
echo "To deploy your blog, commit and push these changes to GitHub." 