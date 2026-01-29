# Find the Path! (Graph Search + Web Scraping)

## Overview
Implements graph search (DFS/BFS) across multiple graph representations and uses Selenium to crawl a Flask-hosted website, collect table fragments, and reveal a final “secret” location.

## What’s Included
You submit a single Python module: **`scrape.py`**, containing:

- **GraphSearcher** (base class)
- **MatrixSearcher** (graph from adjacency matrix / DataFrame)
- **FileSearcher** (graph from files in `file_nodes/`)
- **WebSearcher** (graph of web pages via Selenium)
- **reveal_secrets(driver, url, travellog)** (automation + final output)

## Key Features
- **DFS + BFS** search support via `GraphSearcher`
- **Matrix search**: traverse a graph represented as a matrix
- **File search**: each node is a `.txt` file with:
  - line 1: node value
  - line 2: comma-separated children
- **Web crawling**:
  - uses Selenium (headless Chrome)
  - visits linked pages, stores table fragments
  - `table()` concatenates fragments into one DataFrame (`ignore_index=True`)
- **Secret reveal**:
  - builds a password from the `clue` column of the travel log
  - automates form entry + button clicks
  - downloads `Current_Location.jpg`
  - returns the final location string

## Testing
Run frequently:
```bash
python3 tester.py

