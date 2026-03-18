import re
from datetime import datetime
import yt_dlp

from youtube_transcript_api import YouTubeTranscriptApi

from utils.chunking import chunk_text
from utils.tagging import extract_topics
from utils.language_detection import detect_language
from scoring.trust_score import calculate_trust_score


class YouTubeScraper:

    def __init__(self, url):
        self.url = url
        self.video_id = self.extract_video_id()

    def extract_video_id(self):
        """Extract video ID from URL"""

        pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]+)"
        match = re.search(pattern, self.url)

        return match.group(1) if match else None

    def fetch_metadata(self):
        """Fetch metadata using yt-dlp"""

        try:
            ydl_opts = {
                "quiet": True,
                "skip_download": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)

            metadata = {
                "title": info.get("title"),
                "channel": info.get("channel"),
                "published_date": self.parse_date(info.get("upload_date")),
                "description": info.get("description")
            }

            return metadata

        except Exception as e:
            print(f"yt-dlp metadata error: {e}")
            return {}

    def parse_date(self, date_str):
        """Convert YYYYMMDD → YYYY-MM-DD"""

        if not date_str:
            return None

        try:
            return datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
        except:
            return None

    def fetch_transcript(self):
        """Fetch transcript"""

        try:
            transcript = YouTubeTranscriptApi.get_transcript(self.video_id)

            full_text = " ".join([item["text"] for item in transcript])

            return full_text

        except Exception:
            return ""  # fallback

    def process(self):
        """Main pipeline"""

        if not self.video_id:
            return None

        metadata = self.fetch_metadata()
        transcript_text = self.fetch_transcript()

        # Combine transcript + description
        content_text = (transcript_text or "") + " " + (metadata.get("description") or "")

        if not content_text.strip():
            return None  # skip empty videos

        # Language detection
        language = detect_language(content_text)

        # Topic tagging
        topic_tags = extract_topics(content_text)

        # Chunking
        content_chunks = chunk_text(content_text)

        # Trust score
        trust_score = calculate_trust_score(
            url=self.url,
            author=metadata.get("channel"),
            citation_count=None,
            published_date=metadata.get("published_date"),
            content_text=content_text,
            language=language
        )

        result = {
            "source_url": self.url,
            "source_type": "youtube",
            "author": metadata.get("channel"),
            "published_date": metadata.get("published_date"),
            "language": language,
            "region": None,
            "topic_tags": topic_tags,
            "trust_score": trust_score,
            "content_chunks": content_chunks
        }

        return result


def scrape_youtube(video_urls):
    """Process multiple videos"""

    results = []

    for url in video_urls:
        try:
            scraper = YouTubeScraper(url)
            data = scraper.process()

            if data:
                results.append(data)

        except Exception as e:
            print(f"Error processing {url}: {e}")

    return results