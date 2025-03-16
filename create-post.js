#!/usr/bin/env node

/**
 * A simple script to create a new blog post with the correct frontmatter.
 * 
 * Usage:
 *   node create-post.js "My Post Title"
 * 
 * This will create a new file in the posts directory with the correct frontmatter.
 */

const fs = require('fs');
const path = require('path');

// Get the post title from the command line arguments
const title = process.argv[2];

if (!title) {
  console.error('Please provide a post title');
  console.error('Usage: node create-post.js "My Post Title"');
  process.exit(1);
}

// Create a filename from the title
const filename = title
  .toLowerCase()
  .replace(/[^a-z0-9]+/g, '-')
  .replace(/(^-|-$)/g, '') + '.md';

// Get the current date in a nice format
const date = new Date().toLocaleDateString('en-US', {
  year: 'numeric',
  month: 'long',
  day: 'numeric'
});

// Create the frontmatter and initial content
const content = `---
title: ${title}
date: ${date}
---

# ${title}

Write your post content here...
`;

// Make sure the posts directory exists
const postsDir = path.join(__dirname, 'posts');
if (!fs.existsSync(postsDir)) {
  fs.mkdirSync(postsDir);
}

// Write the file
const filePath = path.join(postsDir, filename);
fs.writeFileSync(filePath, content);

console.log(`Created new post: ${filePath}`);
console.log(`You can now edit this file to add your content.`); 