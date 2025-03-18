from setuptools import setup, find_packages

setup(
    name="blog-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "blog-cli=blog_cli.cli:cli",
        ],
    },
    author="Kyle Jackson",
    author_email="your-email@example.com",
    description="A CLI tool for managing a static blog site",
    keywords="blog, cli, static-site",
    python_requires=">=3.7",
) 