# Data Scraping & Trust Scoring System — Short Report

## 1. Scraping Strategy

The system is designed as a **multi-source data extraction pipeline** capable of collecting structured information from three different platforms: blogs, YouTube, and PubMed.

### Blog Scraping

For blog sources, HTML content is fetched using the `requests` library and parsed using `BeautifulSoup`. To extract clean article text while removing noise such as ads and navigation elements, the `trafilatura` library is used. Metadata such as author and publication date is extracted from meta tags (e.g., `author`, `article:published_time`).

### YouTube Scraping

YouTube metadata is extracted using `yt-dlp`, which provides reliable access to video details such as title, channel name, publish date, and description. Transcripts are retrieved using `youtube-transcript-api`. The transcript and description are combined to form the content for further processing. In cases where transcripts are unavailable, the system gracefully falls back to using only the description.

### PubMed Scraping

Scientific articles are fetched using the Entrez API from BioPython. The scraper extracts structured metadata including title, abstract, authors, journal, and publication year. Citation count is approximated using the number of references available in the article metadata.

---

## 2. Topic Tagging Method

Topic tagging is implemented using a **Large Language Model (LLM)** through LangChain. A prompt-based approach is used to extract high-level semantic topics from the content.

The model is instructed to:

* Return a Python list
* Generate concise tags (1–3 words)
* Focus on high-level concepts

To ensure performance and cost efficiency, the input text is truncated to a fixed length before being sent to the model. This approach provides flexible and context-aware topic extraction compared to traditional keyword-based methods.

---

## 3. Trust Score Algorithm

The trust scoring system evaluates the credibility of each source using a weighted combination of five factors:

* **Author Credibility (25%)**
  Evaluates whether the author is associated with known trusted organizations or has a realistic identity.

* **Citation Count (20%)**
  Measures the number of references or citations, especially relevant for scientific content.

* **Domain Authority (20%)**
  Assigns higher scores to trusted domains (e.g., `.gov`, `.edu`, PubMed) and penalizes low-quality blogging platforms.

* **Recency (20%)**
  Newer content is prioritized, while outdated information receives lower scores.

* **Medical Disclaimer Presence (15%)**
  Detects whether content includes disclaimers such as “not medical advice,” which increases reliability in health-related contexts.

The final trust score is normalized between **0 and 1** and adjusted with a slight penalty for non-English content.

---

## 4. Edge Case Handling

The system is designed to handle real-world inconsistencies in web data:

* **Missing Metadata**
  Default scores are applied when author, publication date, or transcript is unavailable.

* **Multiple Authors**
  Authors are combined into a single string and evaluated collectively.

* **Non-English Content**
  Language detection is performed automatically, and a small penalty is applied to maintain consistency.

* **Long Content**
  Content is split into smaller chunks to ensure compatibility with downstream AI systems such as LLMs and embedding pipelines.

---

## 5. Abuse Prevention Logic

To prevent manipulation and ensure reliable scoring, the system incorporates several safeguards:

* **Fake Authors**
  Author names are cross-checked against a list of trusted organizations.

* **SEO Spam Blogs**
  Domains known for low-quality content (e.g., free blogging platforms) are penalized.

* **Misleading Medical Content**
  Articles lacking medical disclaimers receive lower scores.

* **Outdated Information**
  Strong recency penalties are applied to older content.

---

## 6. Limitations and Future Improvements

While the system performs effectively, there are some limitations:

* Citation counts for PubMed are approximated rather than exact.
* Topic tagging depends on LLM performance and prompt quality.
* Region detection is not currently implemented.
* Domain authority scoring is heuristic-based.

Future improvements may include:

* Integration with external APIs for accurate citation and domain authority metrics
* More robust author verification mechanisms
* Embedding-based topic modeling

---

## 7. Conclusion

This project demonstrates a scalable and production-oriented approach to multi-source data scraping and trust evaluation. By combining web scraping, NLP techniques, and rule-based scoring, the system provides structured, reliable, and AI-ready data suitable for downstream applications such as search, summarization, and recommendation systems.
