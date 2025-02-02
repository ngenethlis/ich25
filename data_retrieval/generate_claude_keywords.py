from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()


def generate_keywords_with_claude(topic):
    client = Anthropic()

    prompt = f"""You are given a research topic: {topic}.
        Generate a list of the 5-10 most relevant keywords or short phrases 
        that a researcher would use to find scientific papers on arXiv 
        about this topic. 
        Return these keywords in a comma-separated list only."""

    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )

    keywords = response.choices[
            0
    ].message.content.split(",")
    keywords = [kw.strip() for kw in keywords]
    print(keywords)
    return keywords
