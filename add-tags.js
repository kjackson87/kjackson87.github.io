#!/usr/bin/env node

/**
 * A simple script to add tags to an existing blog post.
 * 
 * Usage:
 *   node add-tags.js post-filename.md "tag1, tag2, tag3"
 * 
 * This will update the post's frontmatter to include the specified tags.
 */

const fs = require('fs');
const path = require('path');

// Get the post filename and tags from the command line arguments
const postFilename = process.argv[2];
const tagsString = process.argv[3];

if (!postFilename || !tagsString) {
  console.error('Please provide a post filename and tags');
  console.error('Usage: node add-tags.js post-filename.md "tag1, tag2, tag3"');
  process.exit(1);
}

// Resolve the full path to the post file
const postsDir = path.join(__dirname, 'posts');
const postPath = path.join(postsDir, postFilename);

// Check if the file exists
if (!fs.existsSync(postPath)) {
  console.error(`File not found: ${postPath}`);
  console.error('Make sure the post exists in the posts directory.');
  process.exit(1);
}

// Read the file content
let content = fs.readFileSync(postPath, 'utf8');

// Parse the tags
const tags = tagsString.split(',').map(tag => tag.trim());

// Check if the file has frontmatter
const frontMatterMatch = content.match(/^---\s+([\s\S]*?)\s+---/);

if (!frontMatterMatch) {
  console.error('No frontmatter found in the post.');
  console.error('Make sure the post has a frontmatter section at the top.');
  process.exit(1);
}

// Extract the frontmatter
const frontMatter = frontMatterMatch[1];

// Check if the frontmatter already has tags
const tagsMatch = frontMatter.match(/tags:\s*\[(.*?)\]/);
const tagsListMatch = frontMatter.match(/tags:\s*\n([\s\S]*?)(?:\n\w|$)/);

let updatedFrontMatter;

if (tagsMatch) {
  // Update existing tags in array format
  const existingTags = tagsMatch[1].split(',').map(tag => tag.trim().replace(/["']/g, ''));
  const mergedTags = [...new Set([...existingTags, ...tags])]; // Remove duplicates
  updatedFrontMatter = frontMatter.replace(tagsMatch[0], `tags: [${mergedTags.join(', ')}]`);
} else if (tagsListMatch) {
  // Update existing tags in list format
  const existingTags = tagsListMatch[1].split('\n').map(line => {
    const match = line.match(/[-*]\s*(.*)/);
    return match ? match[1].trim() : null;
  }).filter(Boolean);
  const mergedTags = [...new Set([...existingTags, ...tags])]; // Remove duplicates
  const tagsList = mergedTags.map(tag => `- ${tag}`).join('\n');
  updatedFrontMatter = frontMatter.replace(tagsListMatch[0], `tags:\n${tagsList}\n`);
} else {
  // Add new tags field
  updatedFrontMatter = `${frontMatter}\ntags: [${tags.join(', ')}]`;
}

// Replace the frontmatter in the content
const updatedContent = content.replace(frontMatterMatch[1], updatedFrontMatter);

// Write the updated content back to the file
fs.writeFileSync(postPath, updatedContent);

console.log(`Updated tags for ${postFilename}`);
console.log(`Tags: ${tags.join(', ')}`); 