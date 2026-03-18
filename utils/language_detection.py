from langdetect import detect


def detect_language(text):
    """
    Detect language of the content.
    """

    try:
        return detect(text)
    except:
        return "unknown"