from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text):
    """
    Chunk text using LangChain RecursiveTextSplitter
    """

    if not text:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=" "
    )

    chunks = splitter.split_text(text)

    return chunks