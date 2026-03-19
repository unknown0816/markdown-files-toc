# 📄 Markdown Indexer  

A tiny command‑line utility that walks a directory tree, discovers every Markdown file (`*.md`) and prints a **Markdown‑formatted list** of links.
The link text is the first top‑level heading (`# …`) of each file; if a file has no heading the script gracefully falls back to the file name.

> **Why?**
When you maintain a large collection of notes, docs, or tutorials you often need a quick, auto‑generated table of contents. This script does exactly that – no external dependencies, just the Python standard library.

## Table of Contents  

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Command‑line interface](#command-line-interface)
  - [Examples](#examples)
- [How it works](#how-it-works)
- [Configuration & Extensibility](#configuration--extensibility)
- [Limitations & Known Issues](#limitations--known-issues)
- [Contributing](#contributing)
- [License](#license)

## Features  

- **Recursive discovery** of all `*.md` files beneath a given root directory.
- **First‑level heading extraction** (`# Heading`) for human‑readable link titles.
- **Graceful fallback** to the file name (without extension) when no heading is present.
- **Root‑level file exclusion** – the script ignores the Markdown file that lives directly in the root directory (commonly a README you are already editing).
- **Zero‑dependency** – pure Python (≥ 3.7).

## Prerequisites  

- Python **3.7** or newer (tested on 3.9, 3.10, 3.11).
- Access to a terminal / command prompt.

## Usage  

\`\`\`bash
python markdown\_indexer.py \<root\_directory\>
\`\`\`

| Argument | Description |
|----------|-------------|
| \`root\_directory\` | Path to the directory you want to scan. The script will walk this path recursively. |

The script writes the generated Markdown list to **STDOUT**, so you can pipe it into a file or another command.
