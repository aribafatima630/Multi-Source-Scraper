from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    api_key = api_key,
    base_url = base_url,
    temperature=0  
)

prompt = ChatPromptTemplate.from_template("""
Extract {max_topics} meaningful topic tags from the following article.

Rules:
- Return ONLY a Python list
- No explanation
- Each tag should be 1-3 words
- High-level topics only

Text:
{text}
""")

def extract_topics(text, max_topics=5):

    text = text[:3000]

    messages = prompt.format_messages(
        text=text,
        max_topics=max_topics
    )

    response = llm.invoke(messages)

    content = response.content.strip()

    try:
        topics = eval(content)  # convert string → list
    except:
        topics = [content]

    return topics