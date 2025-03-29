# Folder Structure Visualizer

A Python script that generates visual diagrams (PNG) and text-based representations of directory structures using Graphviz.

![Example Output](folder_structure.png) *(example image)*

## Features
- 📁 **Recursive directory scanning** - Visualizes nested folder structures
- 📊 **Graphviz diagrams** - Generates clean PNG visualizations
- 📝 **Text tree output** - Creates both console and file-based text representations
- 🛡️ **Error handling** - Gracefully handles permission issues and invalid paths
- 📦 **Self-contained** - Single Python script with no complex dependencies

## Installation

### Prerequisites
- Python 3.6+
- [Graphviz](https://graphviz.org/download/) (for diagram generation)

### Setup
1. Install Graphviz:
   ```bash
   # Windows (via installer)
   Download from https://graphviz.org/download/

   # Mac (Homebrew)
   brew install graphviz

   # Linux (apt)
   sudo apt install graphviz