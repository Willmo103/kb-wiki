# kb-image Overview

`kb-image` is the image explorer, metadata extractor, and semantic tagging component of the `kb` ecosystem. It monitors and indexes folders of image assets, extracts EXIF coordinates, generates compact thumbnails, and coordinates with Ollama local LLMs to describe and auto-tag images.

---

## Key Features

- **Local Scanning**: Scans directories for supported formats (`.jpg`, `.jpeg`, `.png`, `.webp`) larger than 10KB.
- **EXIF Extraction**: Extracts metadata tags (camera model, lens, exposure time, aperture, ISO, and GPS location if available).
- **Classification Engine**: Automatically classifies images into standard categories: `nature`, `people`, `screenshots`, `diagrams`, `memes`, or `other`.
- **AI Describer**: Utilizes Ollama's vision model to write rich descriptions of image contents.
- **AI Tagger**: Processes the image descriptions to create semantic keywords/tags, making non-text assets searchable.
- **Electron Client**: Desktop browser UI featuring infinite scroll, categorization grid, and metadata explorer drawer.
