import requests
import trafilatura
from bs4 import BeautifulSoup
from datetime import datetime

from utils.chunking import chunk_text
from utils.tagging import extract_topics
from utils.language_detection import detect_language

from scoring.trust_score import calculate_trust_score


class BlogScraper:

    def __init__(self, url):
        self.url = url

    def fetch_html(self):
        """Download webpage HTML"""

        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Failed to fetch {self.url}: {e}")
            return None

    def extract_metadata(self, html):
        """Extract metadata like author and publish date"""

        soup = BeautifulSoup(html, "html.parser")

        author = None
        published_date = None

        # Author
        author_meta = soup.find("meta", {"name": "author"})
        if author_meta:
            author = author_meta.get("content")

        if not author:
            author_meta = soup.find("meta", {"property": "article:author"})
            if author_meta:
                author = author_meta.get("content")

        # Publish Date
        date_meta = soup.find("meta", {"property": "article:published_time"})
        if date_meta:
            published_date = date_meta.get("content")

        if not published_date:
            date_meta = soup.find("meta", {"name": "pubdate"})
            if date_meta:
                published_date = date_meta.get("content")

        return author, published_date

    def parse_date(self, date_str):
        """Convert ISO datetime → YYYY-MM-DD"""

        if not date_str:
            return None

        try:
            return datetime.fromisoformat(date_str).strftime("%Y-%m-%d")
        except:
            return None

    def extract_content(self, html):
        """Extract clean article text"""

        try:
            content = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=False
            )
            return content
        except Exception as e:
            print(f"Content extraction failed: {e}")
            return ""

    def process(self):
        """Main scraping pipeline"""

        html = self.fetch_html()

        if not html:
            return None

        # Metadata
        author, published_date = self.extract_metadata(html)
        date = self.parse_date(published_date)

        # Article Content
        content = self.extract_content(html)

        if not content:
            content = ""

        # Language detection
        language = detect_language(content)

        # Topic tagging
        topic_tags = extract_topics(content)

        # Content chunking
        content_chunks = chunk_text(content)

        # Trust score calculation
        trust_score = calculate_trust_score(
            url=self.url,
            author=author,
            citation_count=None,
            published_date=date,
            content_text=content,
            language=language
        )

        result = {
            "source_url": self.url,
            "source_type": "blog",
            "author": author,
            "published_date": date,
            "language": language,
            "region": None,
            "topic_tags": topic_tags,
            "trust_score": trust_score,
            "content_chunks": content_chunks
        }

        return result


def scrape_blogs(blog_urls):
    """Scrape multiple blog URLs"""

    results = []

    for url in blog_urls:

        try:
            scraper = BlogScraper(url)

            data = scraper.process()

            if data:
                results.append(data)

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return results