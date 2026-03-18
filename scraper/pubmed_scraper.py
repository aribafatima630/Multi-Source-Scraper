import re
from datetime import datetime
from Bio import Entrez

from utils.chunking import chunk_text
from utils.tagging import extract_topics
from utils.language_detection import detect_language
from scoring.trust_score import calculate_trust_score


# Required by NCBI
Entrez.email = "aribafatima630@gmail.com"


class PubMedScraper:

    def __init__(self, url):
        self.url = url
        self.pmid = self.extract_pmid()

    def extract_pmid(self):
        """Extract PMID from URL"""

        match = re.search(r"/(\d+)/?$", self.url)

        return match.group(1) if match else None

    def fetch_data(self):
        """Fetch data from PubMed"""

        try:
            handle = Entrez.efetch(
                db="pubmed",
                id=self.pmid,
                retmode="xml"
            )

            records = Entrez.read(handle)
            return records

        except Exception as e:
            print(f"PubMed fetch error: {e}")
            return None

    def extract_metadata(self, records):
        """Extract metadata"""

        try:
            article = records["PubmedArticle"][0]["MedlineCitation"]["Article"]

            title = article.get("ArticleTitle")

            # Abstract
            abstract = ""
            if "Abstract" in article:
                abstract = " ".join(article["Abstract"]["AbstractText"])

            # Authors
            authors_list = article.get("AuthorList", [])
            authors = []

            for author in authors_list:
                if "LastName" in author and "ForeName" in author:
                    authors.append(f"{author['ForeName']} {author['LastName']}")

            # Journal
            journal = article["Journal"]["Title"]

            # Publish Date
            pub_date = article["Journal"]["JournalIssue"]["PubDate"]
            year = pub_date.get("Year", "2000")

            return {
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "journal": journal,
                "published_date": year
            }

        except Exception as e:
            print(f"Metadata extraction error: {e}")
            return {}

    def estimate_citations(self, records):
        """
        PubMed doesn't directly give citation count easily.
        We approximate using reference count if available.
        """

        try:
            article = records["PubmedArticle"][0]
            references = article.get("PubmedData", {}).get("ReferenceList", [])

            return len(references)

        except:
            return 0

    def process(self):
        """Main pipeline"""

        if not self.pmid:
            return None

        records = self.fetch_data()

        if not records:
            return None

        metadata = self.extract_metadata(records)
        citation_count = self.estimate_citations(records)

        content_text = (metadata.get("title") or "") + " " + (metadata.get("abstract") or "")

        if not content_text.strip():
            return None

        # Language detection
        language = detect_language(content_text)

        # Topic tagging
        topic_tags = extract_topics(content_text)

        # Chunking
        content_chunks = chunk_text(content_text)

        authors = metadata.get("authors")

        author_input = ", ".join(authors) if isinstance(authors, list) else authors

        # Trust score
        trust_score = calculate_trust_score(
            url=self.url,
            author=author_input,
            citation_count=citation_count,
            published_date=metadata.get("published_date"),
            content_text=content_text,
            language=language
        )

        result = {
            "source_url": self.url,
            "source_type": "pubmed",
            "author": metadata.get("authors"),
            "published_date": metadata.get("published_date"),
            "language": language,
            "region": None,
            "topic_tags": topic_tags,
            "trust_score": trust_score,
            "content_chunks": content_chunks
        }

        return result


def scrape_pubmed(pubmed_urls):
    """Process multiple PubMed URLs"""

    results = []

    for url in pubmed_urls:
        try:
            scraper = PubMedScraper(url)
            data = scraper.process()

            if data:
                results.append(data)

        except Exception as e:
            print(f"Error processing {url}: {e}")

    return results