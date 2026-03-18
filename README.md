# Multi-Source Data Scraping & Trust Scoring System

## Overview

This project implements a **production-ready data pipeline** that:

* Scrapes content from **multiple sources**

  * Blogs
  * YouTube
  * PubMed
* Extracts structured metadata and content
* Automatically generates **topic tags**
* Computes a **Trust Score (0–1)** based on credibility factors

---

## Features

### Multi-Source Scraping

* Blog articles (clean text extraction)
* YouTube videos (metadata + transcript)
* PubMed research papers (scientific metadata)

### Metadata Extraction

* Author / Channel / Organization
* Published date
* Abstract / Description / Content

### NLP Processing

* Language detection
* Topic tagging using LLM
* Content chunking for downstream AI tasks

### Trust Scoring System

A rule-based scoring system evaluating:

```
Trust Score = f(
  author_credibility,
  citation_count,
  domain_authority,
  recency,
  medical_disclaimer_presence
)
```

---

## Project Structure

```
project/
│
├── scraper/
│   ├── blog_scraper.py
│   ├── youtube_scraper.py
│   ├── pubmed_scraper.py
│
├── scoring/
│   └── trust_score.py
│
├── utils/
│   ├── tagging.py
│   ├── chunking.py
│   ├── language_detection.py
│
├── scraped_data/
│   ├── blogs.json
│   ├── youtube.json
│   ├── pubmed.json
│  
│
├── main.py
└── README.md
```

---

## Tech Stack

* **Web Scraping**: `requests`, `BeautifulSoup`, `trafilatura`
* **YouTube Extraction**: `yt-dlp`, `youtube-transcript-api`
* **Scientific Data**: `BioPython (Entrez)`
* **NLP / AI**:

  * `LangChain`
  * OpenAI-compatible LLM
* **Utilities**:

  * Language detection
  * Custom chunking pipeline

---

## Scraping Approach

### Blogs

* HTML fetched using `requests`
* Content cleaned using `trafilatura`
* Metadata extracted via `<meta>` tags

### YouTube

* Metadata via `yt-dlp`
* Transcript via `youtube-transcript-api`
* Combined transcript + description used as content

### PubMed

* Data fetched using `Entrez API`
* Extracted:

  * Title
  * Abstract
  * Authors
  * Journal
  * Publication year

---

## Topic Tagging

* Implemented using **LLM via LangChain**
* Generates high-level semantic tags
* Output format:

```python
["AI", "machine learning", "healthcare"]
```

---

## Content Chunking

* Long content split into smaller chunks
* Ensures compatibility with:

  * LLM pipelines
  * Embedding systems

---

## Trust Score Design

Each source is evaluated using weighted factors:

| Factor             | Weight |
| ------------------ | ------ |
| Author Credibility | 0.25   |
| Citation Count     | 0.20   |
| Domain Authority   | 0.20   |
| Recency            | 0.20   |
| Medical Disclaimer | 0.15   |

Final score is normalized between **0 and 1**.

---

## Edge Case Handling

### Missing Metadata

* Author missing → default score applied
* Publish date missing → fallback recency score

### Multiple Authors

* Authors combined and evaluated collectively

### Non-English Content

* Automatically detected
* Slight penalty applied

### Long Content

* Chunking ensures scalability

### Transcript Missing (YouTube)

* Fallback to description

---

## Abuse Prevention Logic

| Risk                       | Mitigation                             |
| -------------------------- | -------------------------------------- |
| Fake Authors               | Cross-check with trusted organizations |
| SEO Spam Blogs             | Penalize low-authority domains         |
| Misleading Medical Content | Penalize missing disclaimer            |
| Outdated Info              | Strong recency penalty                 |

---

## Output Format

Each source is stored as:

```json
{
  "source_url": "",
  "source_type": "",
  "author": "",
  "published_date": "",
  "language": "",
  "region": null,
  "topic_tags": [],
  "trust_score": 0.0,
  "content_chunks": []
}
```

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set environment variables

```bash
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=your_base_url
```

### 3. Run the pipeline

```bash
python main.py
```

---

## Output

Generated file:

```
scraped_data/
blogs.json
youtube.json
pubmed.json
```

---

## Limitations

* Citation count for PubMed is approximated
* Topic tagging depends on LLM quality
* YouTube transcripts may not always be available
* Region field is currently not inferred

---

## Future Improvements

* Add real citation APIs
* Improve domain authority scoring (e.g., Moz API)
* Use embeddings for topic tagging

---
