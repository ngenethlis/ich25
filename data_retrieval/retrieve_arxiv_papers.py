import re
import io
import requests
import json
from langchain_community.retrievers import ArxivRetriever
from openai import OpenAI
from io import BytesIO
from pdfminer.high_level import extract_text
from concurrent.futures import ProcessPoolExecutor

def format_paper(paper):
    info = paper.metadata
    arxiv_id = info["entry_id"].split("/")[-1].split("v")[0]
    references = get_references(arxiv_id)
    paper_information = {
        "name": info["Title"],
        "url": info["entry_id"],
        "authors": info["Authors"],
        "content": paper.page_content,
        "publication_date": info["Published"],
        "out_references": references,
        "num_out": len(references),
    }
    # json_format = json.dumps(paper_information)
    return paper_information


def get_papers(keywords, max_results):

    retriever = ArxivRetriever(
        load_max_docs=max_results,
        get_full_documents=True,
        load_all_available_meta=True,
        top_k_results=max_results,
    )
    query = " OR ".join(keywords)
    docs = retriever.invoke(query)
    papers_list = []

    with ProcessPoolExecutor() as executor:
        papers = list(executor.map(format_paper, docs))

    return papers

def get_references(arxiv_id):
    raw_pdf_bytes = get_arxiv_pdf_in_memory(arxiv_id)
    text = extract_text_from_pdf_bytes(raw_pdf_bytes)
    references = extract_references_from_claude(text)
    print("Got references")
    # cleansed_references = cleanse_references(references)
    return references

def get_arxiv_pdf_in_memory(arxiv_id):
    """
    Given an arXiv ID (with or without version suffix),
    returns the PDF data in-memory as bytes.
    """
    # Build the PDF URL for the arXiv paper
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    print(f"Fetching PDF from: {pdf_url}")
    
    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise ValueError(f"Failed to download PDF (HTTP {response.status_code}) from {pdf_url}.")
    print(f"Downloaded {len(response.content)} bytes.")
    
    return response.content  # Return the raw PDF bytes

def extract_text_from_pdf_bytes(pdf_bytes):
    """
    Convert PDF bytes into text using pdfminer.six, all in memory.
    """
    with BytesIO(pdf_bytes) as pdf_filelike:
        pdf_text = extract_text(pdf_filelike)

    return pdf_text


def extract_references_from_claude(text):
    client = OpenAI()

    prompt = f"""
        Extract the titles of papers referenced by the given text. You must give the titles in a list seperated by newlines. Your response must be inside <titles> tags.
        Here is the text: {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",#"claude-3-5-haiku-20241022",  
        max_tokens=6024,
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content":"[{"}
        ]
    )

    documents = extract_tag_content(response.choices[0].message.content, "titles").split("\n")
    return documents

def cleanse_references(references):
    references = references.split("name: ")
    new_references = [val for val in references if val != '' and val != '\n']
    print(new_references)
    clean_references = []
    for ref in new_references:
        ref = ref.split('"authors": ')
        name = ref[0]
        authors = ref[1]
        paper = {
            'name': ref[0],
            'authors': ref[1]
        }
        json_format = json.dumps(paper)
        clean_references.append(json_format)

    return clean_references

def extract_tag_content(text: str, tag: str) -> str:
    pattern = f"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""