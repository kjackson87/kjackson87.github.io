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

### 3. Blog CLI Tool

This repository includes a command-line tool for managing blog content. The tool helps you:

- Create new blog posts with proper frontmatter
- Add tags to existing posts
- Generate a JSON index of all posts
- Create new pages with standardized layout
- Convert Jupyter notebooks to blog posts

#### Installation

```bash
pip install -e .
```

#### Usage Examples

Create a new blog post:
```bash
blog-cli post create "My New Blog Post"
```

Generate post index:
```bash
blog-cli post generate-index
```

For more details, check the [Blog CLI documentation](blog_cli/README.md).

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
├── blog.html           # Blog listing page
├── components/         # Reusable HTML components
│   ├── header.html     # Shared header with navigation
│   └── footer.html     # Shared footer with links
├── js/                 # JavaScript files
│   └── include.js      # Component inclusion system
├── posts/              # Markdown content for blog posts
│   ├── first-post.md
│   └── second-post.md
├── templates/          # Templates for rendering content
│   └── post.html       # Blog post template
├── blog_cli/           # Blog CLI tool
│   ├── commands/       # CLI commands
│   ├── utils/          # Utility functions
│   └── README.md       # CLI documentation
└── README.md           # This file
```

## Component System

This site uses a simple component system to share common elements like the header and footer across pages:

1. **Components**: HTML snippets stored in the `components/` directory
2. **Include Script**: A JavaScript file (`js/include.js`) that loads components into pages
3. **Component Inclusion**: Pages include components using `<div data-include="components/header.html"></div>`

### Benefits

- **Maintainability**: When you need to update the header or footer, you only need to make changes in one place
- **Consistency**: All pages will have the exact same header and footer
- **Easier Page Creation**: Use the Blog CLI tool to generate new pages with components already included

### How It Works

The `include.js` script:
1. Finds all elements with the `data-include` attribute on the page
2. Fetches the HTML content from the specified file
3. Replaces the element's inner HTML with the loaded content

## Adding New Pages

You can add new pages to your site using the Blog CLI tool:

```bash
blog-cli page create about --title "About Me" --description "Learn more about my background and interests."
```

## Adding New Blog Posts

Use the Blog CLI tool to create and manage blog posts:

```bash
blog-cli post create "My New Blog Post" 
```

## Customization

- Edit the CSS within the `<style>` tags in each HTML file to customize the appearance
- Add additional pages by creating new HTML files and updating the navigation links
- Consider adding a custom domain by configuring it in your GitHub Pages settings

## License

This template is available for free use under the MIT License.

# Markdown Blog

A simple static blog that uses markdown files for content. This makes it easy to write and maintain blog posts without having to write HTML.

## How It Works

1. All blog posts are stored as markdown files in the `posts` directory
2. The blog homepage (`blog.html`) automatically lists all posts from the `posts` directory
3. Each post is rendered using the template in `templates/post.html`

## Blog Content Management

The Blog CLI tool provides a set of commands to make managing blog content easier. See the [CLI documentation](blog_cli/README.md) for more details.

### Post Format

Each post should start with YAML frontmatter that includes at least a title and date:

```markdown
---
title: Your Post Title
date: January 1, 2025
tags: [tag1, tag2, tag3]
---

Your post content goes here...
```

You can also specify tags in a list format:

```markdown
---
title: Your Post Title
date: January 1, 2025
tags:
- tag1
- tag2
- tag3
---

Your post content goes here...
```

The frontmatter is enclosed by three dashes (`---`) at the beginning and end. After the frontmatter, you can write your post content in markdown format.

### Markdown Features

You can use all standard markdown features in your posts:

- **Headers**: Use `#` for h1, `##` for h2, etc.
- **Bold**: Use `**bold text**`
- **Italic**: Use `*italic text*`
- **Lists**: Use `- ` for unordered lists or `1. ` for ordered lists
- **Links**: Use `[link text](url)`
- **Images**: Use `![alt text](image-url)`
- **Code blocks**: Use triple backticks (```) to create code blocks
- **Inline code**: Use single backticks (`) for inline code

### Code Syntax Highlighting

For code blocks, you can specify the language for syntax highlighting:

```javascript
function hello() {
  console.log("Hello, world!");
}
```

## Customization

### Changing the Site Title and Information

Edit the following files to change the site title and information:

- `index.html`: Main page
- `blog.html`: Blog listing page
- `templates/post.html`: Blog post template

Look for "Your Name" and replace it with your own name. Also update the footer links to point to your own social media profiles.

### Styling

The CSS styles are embedded in each HTML file. You can modify them to change the appearance of your site.

## Deployment

This site is designed to work with GitHub Pages or any static site hosting service. Simply push the files to your repository and enable GitHub Pages in the repository settings.

For GitHub Pages:

1. Create a repository named `yourusername.github.io`
2. Push your files to the repository
3. Your site will be available at `https://yourusername.github.io`

## Local Development

To test your site locally, you can use any local server. For example, with Python:

```bash
# Python 3
python -m http.server

# Python 2
python -m SimpleHTTPServer
```

Then open `http://localhost:8000` in your browser.

## Python Scripts

This site includes several Python scripts to help you manage your blog posts and site pages:

### Create Page Script

The `create_page.py` script helps you create new pages that automatically use the shared header and footer components:

```bash
# Basic usage
./create_page.py projects

# Advanced usage with custom title and description
./create_page.py research --title "Research Projects" --description "Explore my current and past research projects in AI safety."

# Create a page that will be in a subdirectory (adjusts component paths)
./create_page.py profile --title "My Profile" --description "Learn more about me" --subdirectory
```

This script will:
1. Create a new HTML file with your header and footer components included
2. Ask if you want to add a link to your navigation menu
3. If you say yes, it will update the `components/header.html` file automatically

Script options:
- `page_name`: Name of the HTML file to create (without extension) - required
- `--title`: Title of the page (default: "New Page")
- `--description`: Brief description of the page content (default: "This is a new page.")
- `--subdirectory`: Flag indicating the page will be in a subdirectory (affects component paths)

### Create Post Script

The `create-post.py` script helps you create a new blog post with the correct frontmatter:

```bash
python create-post.py "My New Post Title"
```

This will create a new file in the `posts` directory with a filename derived from the title and the correct frontmatter.

### Add Tags Script

The `add-tags.py` script helps you add tags to an existing blog post:

```bash
python add-tags.py post-filename.md "tag1, tag2, tag3"
```

This will add the specified tags to the post, merging with any existing tags.

## Limitations

- This is a client-side solution, so it requires JavaScript to be enabled in the browser
- On GitHub Pages, there's no way to automatically list all files in a directory, so the blog page uses a fallback mechanism to find posts
- For the best experience, use a local server or a hosting service that allows directory listing

### Adding and Managing Tags

You can add tags to your posts in the frontmatter section using either the array format or the list format:

1. **Adding tags to a new post:**
   Simply include the tags in the frontmatter as shown above.

2. **Adding tags to an existing post:**
   You can manually edit the frontmatter, or use the provided script:

   ```bash
   python add-tags.py post-filename.md "tag1, tag2, tag3"
   ```

   This will add the specified tags to the post, merging with any existing tags.

3. **Filtering by tags:**
   The blog page includes a tag filter system that allows readers to filter posts by tag.

## Blog Setup

This blog is designed to work with GitHub Pages. Since GitHub Pages doesn't serve raw markdown files by default, we need to pre-generate HTML files from the markdown blog posts.

### Setup Process

1. Install required dependencies and generate HTML files:

```bash
./setup_blog.sh
```

This script will:
- Install required Python packages (markdown)
- Generate the post index (post-index.json)
- Convert markdown posts to HTML files

2. After running the setup, commit and push your changes to GitHub:

```bash
git add .
git commit -m "Generate HTML blog posts"
git push
```

### Adding New Posts

1. Add your new markdown post to the `posts/` directory
2. Run the setup script again to regenerate the HTML files:

```bash
./setup_blog.sh
```

3. Commit and push your changes

### Troubleshooting

If you're experiencing 404 errors when trying to view blog posts:
- Ensure you've run the setup script to generate HTML files
- Check that the HTML files exist in the `html_posts/` directory
- Verify that the paths in the templates are correct for your GitHub Pages setup
