import json

from scraper.blog_scraper import scrape_blogs
from scraper.youtube_scraper import scrape_youtube
from scraper.pubmed_scraper import scrape_pubmed


def main():

    # Input Sources
    blog_urls = [
        "https://machinelearningmastery.com/what-is-machine-learning/",
        "https://machinelearningmastery.com/everything-you-need-to-know-about-recursive-language-models/",
        "https://machinelearningmastery.com/setting-up-a-google-colab-ai-assisted-coding-environment-that-actually-works/"
    ]

    youtube_urls = [
        "https://www.youtube.com/watch?v=aircAruvnKk",
        "https://www.youtube.com/watch?v=qYNweeDHiyU"
    ]

    pubmed_urls = [
        "https://pubmed.ncbi.nlm.nih.gov/31452104/"
    ]

    # Run Scrapers
    blogs = scrape_blogs(blog_urls)
    videos = scrape_youtube(youtube_urls)
    papers = scrape_pubmed(pubmed_urls)

    # Combine All Results
    final_output = {
        "blogs": blogs,
        "youtube": videos,
        "pubmed": papers
    }

    # Save JSON
    with open("scraped_data/blogs.json", "w", encoding="utf-8") as f:
        json.dump(final_output.get("blogs"), f, indent=4, ensure_ascii=False)

    with open("scraped_data/youtube.json", "w" , encoding="utf-8") as f:
        json.dump(final_output.get("youtube"), f, indent=4, ensure_ascii=False)

    with open("scraped_data/pubmed.json", "w" , encoding="utf-8") as f:
        json.dump(final_output.get("pubmed"), f, indent=4, ensure_ascii=False)


    print("Data successfully saved to scraped_data")


if __name__ == "__main__":
    main()