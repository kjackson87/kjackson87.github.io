# Blog CLI

A command-line tool for managing static blog content.

## Installation

Clone this repository and install using pip:

```bash
pip install -e .
```

## Usage

The CLI tool provides commands for managing blog posts, pages, and Jupyter notebooks:

### Post Commands

Create a new blog post:

```bash
blog-cli post create "My Blog Post Title"
```

Add tags to an existing post:

```bash
blog-cli post add-tags my-post.md "tag1, tag2, tag3"
```

Generate a JSON index of all posts:

```bash
blog-cli post generate-index
```

### Page Commands

Create a new HTML page:

```bash
blog-cli page create about --title "About Me" --description "Information about the author"
```

### Notebook Commands

Convert a Jupyter notebook to a blog post:

```bash
blog-cli notebook convert my-notebook.ipynb
```

Use a custom output filename:

```bash
blog-cli notebook convert my-notebook.ipynb --output custom-name
```

## Command Documentation

For detailed documentation on each command, use the built-in help:

```bash
blog-cli --help
blog-cli post --help
blog-cli page --help
blog-cli notebook --help
```

## Features

- Create blog posts with proper frontmatter
- Add tags to existing posts
- Generate a JSON index of all posts for the site
- Create HTML pages with standardized layouts
- Convert Jupyter notebooks to blog posts
- Extract and process images from notebooks

## Development

To contribute to this project:

1. Fork the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request 