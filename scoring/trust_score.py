import datetime
from urllib.parse import urlparse


# -----------------------------
# Known credible organizations
# -----------------------------
TRUSTED_ORGANIZATIONS = {
    "who", "world health organization",
    "cdc", "centers for disease control",
    "nih", "national institutes of health",
    "harvard", "stanford", "mit",
    "mayo clinic",
    "nature",
    "lancet"
}


# -----------------------------
# Known low quality domains
# -----------------------------
LOW_AUTHORITY_DOMAINS = {
    "medium.com",
    "blogspot.com",
    "wordpress.com"
}


# -----------------------------
# Domain authority estimation
# -----------------------------
def get_domain_authority(url):
    """
    Estimate domain authority based on domain type.
    """

    domain = urlparse(url).netloc.lower()

    if ".gov" in domain or ".edu" in domain:
        return 0.9

    if "pubmed" in domain or "nih" in domain:
        return 0.95

    if any(low in domain for low in LOW_AUTHORITY_DOMAINS):
        return 0.4

    return 0.6


# -----------------------------
# Author credibility
# -----------------------------
def calculate_author_credibility(author):
    """
    Estimate credibility of the author.
    """

    if not author:
        return 0.3

    author_lower = author.lower()

    for org in TRUSTED_ORGANIZATIONS:
        if org in author_lower:
            return 0.9

    if len(author.split()) >= 2:
        return 0.6

    return 0.4


# -----------------------------
# Citation count estimation
# -----------------------------
def calculate_citation_score(citation_count):
    """
    Normalize citation count between 0 and 1.
    """

    if citation_count is None:
        return 0.3

    if citation_count > 100:
        return 1.0

    if citation_count > 50:
        return 0.8

    if citation_count > 10:
        return 0.6

    if citation_count > 0:
        return 0.4

    return 0.2


# -----------------------------
# Recency scoring
# -----------------------------
def calculate_recency_score(published_date):
    """
    Penalize outdated content.
    """

    if not published_date:
        return 0.4

    try:
        if isinstance(published_date, str):
            published_date = published_date[:10]
            published_date = datetime.datetime.strptime(
                published_date, "%Y-%m-%d"
            )

        current_year = datetime.datetime.now().year
        age = current_year - published_date.year

        if age <= 1:
            return 1.0

        if age <= 3:
            return 0.8

        if age <= 5:
            return 0.6

        if age <= 10:
            return 0.4

        return 0.2

    except Exception:
        return 0.4


# -----------------------------
# Medical disclaimer detection
# -----------------------------
def detect_medical_disclaimer(text):
    """
    Detect presence of medical disclaimer.
    """

    if not text:
        return 0

    text_lower = text.lower()

    disclaimer_keywords = [
        "not medical advice",
        "consult a doctor",
        "for informational purposes",
        "seek professional medical advice"
    ]

    for keyword in disclaimer_keywords:
        if keyword in text_lower:
            return 1

    return 0


# -----------------------------
# Main Trust Score Function
# -----------------------------
def calculate_trust_score(
        url,
        author=None,
        citation_count=None,
        published_date=None,
        content_text=None,
        language="en"
):
    """
    Calculate overall trust score between 0 and 1.
    """

    # Author credibility
    author_score = calculate_author_credibility(author)

    # Citation score
    citation_score = calculate_citation_score(citation_count)

    # Domain authority
    domain_score = get_domain_authority(url)

    # Recency
    recency_score = calculate_recency_score(published_date)

    # Medical disclaimer
    disclaimer_score = detect_medical_disclaimer(content_text)

    # Penalize non-English content
    if language != "en":
        language_penalty = 0.9
    else:
        language_penalty = 1.0

    # Weighted trust score
    trust_score = (
        0.25 * author_score +
        0.20 * citation_score +
        0.20 * domain_score +
        0.20 * recency_score +
        0.15 * disclaimer_score
    )

    trust_score = trust_score * language_penalty

    return round(min(max(trust_score, 0), 1), 3)