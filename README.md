# Simple GitHub Pages Website

This is a simple website template for GitHub Pages with a CV page and a markdown blog.

## Getting Started

### 1. Fork or Clone This Repository

Start by forking this repository to your GitHub account or clone it directly:

```bash
git clone https://github.com/yourusername/yourusername.github.io.git
cd yourusername.github.io
```

### 2. Customize Your Website

1. Edit the HTML files to include your information:
   - `index.html` - Homepage
   - `cv.html` - Your CV/resume
   - `blog.html` - Blog listing page

2. Update your personal information:
   - Your name
   - Contact information
   - Skills
   - Work experience
   - Education
   - Social media links

### 3. Add Blog Posts

1. Create a `posts` folder in the root directory:

```bash
mkdir posts
```

2. Add your markdown blog posts to the `posts` folder with the `.md` extension. Each post should have front matter at the top:

```markdown
---
title: Your Post Title
date: YYYY-MM-DD
---

Your content here...
```

3. For each blog post, create a corresponding HTML file in the `blog` folder using the template provided in `blog/first-post.html`. The filename should match the markdown filename (without the `.md` extension).

4. Update the blog list in `blog.html` to include your new posts.

### 4. Push to GitHub

Commit your changes and push them to GitHub:

```bash
git add .
git commit -m "Update website content"
git push
```

### 5. Enable GitHub Pages

1. Go to your repository settings on GitHub
2. Scroll down to the "GitHub Pages" section
3. Select the branch you want to use (usually `main`)
4. Click "Save"

Your website will be available at `https://yourusername.github.io`

## Structure

```
yourusername.github.io/
├── index.html          # Homepage
├── cv.html             # CV/Resume page
├── blog.html           # Blog listing page
├── blog/               # Individual blog post pages
│   ├── first-post.html
│   └── second-post.html
├── posts/              # Markdown content for blog posts
│   ├── first-post.md
│   └── second-post.md
└── README.md           # This file
```

## Adding New Blog Posts

1. Create a new markdown file in the `posts` folder with front matter
2. Copy one of the existing blog post HTML files in the `blog` folder and update the filename
3. Update the blog listing in `blog.html` to include the new post

## Customization

- Edit the CSS within the `<style>` tags in each HTML file to customize the appearance
- Add additional pages by creating new HTML files and updating the navigation links
- Consider adding a custom domain by configuring it in your GitHub Pages settings

## License

This template is available for free use under the MIT License.
