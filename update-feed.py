#!/usr/bin/env python3

"""
A script to update the RSS feed with existing posts.

Usage:
    python update-feed.py "Post Title" --link URL [--description "Description"] [--date "YYYY-MM-DD"]

This will add or update an entry in the RSS feed for an existing post.
"""

import os
import sys
import argparse
from datetime import datetime
import xml.etree.ElementTree as ET

def update_rss_feed(title, link, description, pub_date=None):
    """Update the RSS feed with a post."""
    rss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rss.xml')
    
    # Parse the existing RSS feed
    tree = ET.parse(rss_path)
    root = tree.getroot()
    channel = root.find('channel')
    
    # Check if item with this link already exists
    existing_item = None
    for item in channel.findall('item'):
        if item.find('link').text == link:
            existing_item = item
            break
    
    if existing_item is not None:
        # Update existing item
        existing_item.find('title').text = title
        existing_item.find('description').text = description
        if pub_date:
            existing_item.find('pubDate').text = pub_date
        print(f"Updated existing RSS feed entry: {title}")
    else:
        # Create new item
        item = ET.SubElement(channel, 'item')
        
        # Add item elements
        title_elem = ET.SubElement(item, 'title')
        title_elem.text = title
        
        link_elem = ET.SubElement(item, 'link')
        link_elem.text = link
        
        desc_elem = ET.SubElement(item, 'description')
        desc_elem.text = description
        
        # Add publication date
        if not pub_date:
            pub_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        pub_date_elem = ET.SubElement(item, 'pubDate')
        pub_date_elem.text = pub_date
        
        # Add GUID
        guid_elem = ET.SubElement(item, 'guid')
        guid_elem.text = link
        
        print(f"Added new RSS feed entry: {title}")
    
    # Update lastBuildDate
    last_build_date = channel.find('lastBuildDate')
    if last_build_date is not None:
        last_build_date.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # Write the updated RSS feed
    tree.write(rss_path, encoding='UTF-8', xml_declaration=True)

def parse_date(date_str):
    """Parse date string in YYYY-MM-DD format to RSS date format."""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date.strftime('%a, %d %b %Y %H:%M:%S GMT')
    except ValueError:
        print(f"Error: Invalid date format. Please use YYYY-MM-DD")
        sys.exit(1)

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Update RSS feed with existing post')
    parser.add_argument('title', help='The title of the post')
    parser.add_argument('--link', required=True, help='URL for the post')
    parser.add_argument('--description', help='Description for the RSS feed', default='')
    parser.add_argument('--date', help='Publication date in YYYY-MM-DD format', default='')
    args = parser.parse_args()
    
    # Parse date if provided
    pub_date = parse_date(args.date) if args.date else None
    
    # If no description provided, use a default one
    description = args.description or f"Post: {args.title}"
    
    # Update the RSS feed
    update_rss_feed(args.title, args.link, description, pub_date)

if __name__ == "__main__":
    main() 