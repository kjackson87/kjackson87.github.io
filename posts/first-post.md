---
title: Getting Started with GitHub Pages
date: March 15, 2025
tags: [github, web-development, hosting]
---

# Getting Started with GitHub Pages

GitHub Pages is a static site hosting service that takes HTML, CSS, and JavaScript files straight from a repository on GitHub, optionally runs the files through a build process, and publishes a website.

## Why Use GitHub Pages?

GitHub Pages is a great option for hosting a personal website, portfolio, or blog for several reasons:

1. **It's completely free** - You don't have to pay for hosting.
2. **Easy to set up** - If you're already familiar with GitHub, it's just a few clicks away.
3. **Version control** - Your website is in a Git repository, so you have full version control.
4. **Custom domain support** - You can use your own domain name.
5. **HTTPS by default** - Your site gets free SSL certificate.

## Setting Up Your GitHub Pages Site

### 1. Create a Repository

First, you need to create a new repository on GitHub. For a user site, name it `yourusername.github.io`. For an organization site, name it `organizationname.github.io`.

### 2. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/yourusername.github.io.git
cd yourusername.github.io
```

### 3. Add Your Website Files

Create your website files in the repository directory. At a minimum, you'll need an `index.html` file:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My GitHub Pages Site</title>
</head>
<body>
    <h1>Hello World!</h1>
    <p>Welcome to my GitHub Pages site.</p>
</body>
</html>
```

### 4. Commit and Push

Commit your changes and push them to GitHub:

```bash
git add .
git commit -m "Initial commit"
git push -u origin main
```

### 5. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on "Settings"
3. Scroll down to the "GitHub Pages" section
4. Under "Source", select the branch you want to use (usually `main` or `master`)
5. Click "Save"

Your site will now be published at `https://yourusername.github.io`.

## Adding a Blog with Markdown

For a simple blog using Markdown files:

1. Create a `_posts` directory in your repository
2. Add Markdown files with the naming convention `YYYY-MM-DD-title.md`
3. Include front matter at the top of each file:

```markdown
---
title: My First Blog Post
date: 2025-03-15
---

Content of your blog post goes here...
```

## Next Steps

- Add a custom domain
- Create a responsive design
- Add a theme or customize your CSS
- Set up Jekyll for more advanced features

Happy coding!
