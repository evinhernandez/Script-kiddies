"""
SK Framework — Package Setup
Install: pip install -e .
CLI command 'sk' becomes available after install.
"""

from setuptools import setup, find_packages

setup(
    name="sk-framework",
    version="0.1.0",
    description="AI Security Testing & Training Framework by Script-Kiddies",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="SK Labs — Script-Kiddies",
    author_email="hello@scriptkiddies.ai",
    url="https://github.com/script-kiddies/sk-framework",
    license="MIT",
    packages=find_packages(where="."),
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1.0",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "textual>=0.47.0",
        "openai>=1.10.0",
        "anthropic>=0.18.0",
        "google-generativeai>=0.3.0",
        "litellm>=1.20.0",
        "httpx>=0.26.0",
        "tiktoken>=0.5.0",
        "regex>=2023.12.0",
        "sqlalchemy>=2.0.18",
        "aiosqlite>=0.19.0",
        "structlog>=23.3.0",
    ],
    entry_points={
        "console_scripts": [
            "sk=src.cli.main:sk",
            "skconsole=src.cli.console:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
    ],
    keywords="ai security owasp llm red-team jailbreak prompt-injection",
)
