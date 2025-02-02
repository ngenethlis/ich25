import re
import io
import requests
from pdfminer.high_level import extract_text
import json
from langchain_community.retrievers import ArxivRetriever
import arxiv
import fitz  
import os
from io import BytesIO
import anthropic
from dotenv import load_dotenv

load_dotenv()

def get_papers(keywords, max_results):

    retriever = ArxivRetriever(
        load_max_docs=max_results,
        get_full_documents=True,
        load_all_available_meta=True,
    )
    query = " OR ".join(keywords)
    docs = retriever.invoke(query)
    papers_list = []
    for paper in docs:
        info = paper.metadata
        arxiv_id = info['entry_id'].split('/')[-1].split('v')[0]
        references = get_references(arxiv_id)
        paper_information = {
            'name': info['Title'],
            'url': info['entry_id'],
            'authors': info['Authors'],
            'publication_date': info['Published'],
            'out_references': references,
            'num_out': len(references)
        }
        json_format = json.dumps(paper_information)
        papers_list.append(json_format)

    return papers_list


def get_references(arxiv_id):
    raw_pdf_bytes = get_arxiv_pdf_in_memory(arxiv_id)
    text = extract_text_from_pdf_bytes(raw_pdf_bytes)
    references = extract_references_from_claude(text)
    cleansed_references = cleanse_references(references)
    return cleansed_references

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
    
    return response.content  # Return the raw PDF bytes

def extract_text_from_pdf_bytes(pdf_bytes):
    """
    Convert PDF bytes into text using pdfminer.six, all in memory.
    """
    with BytesIO(pdf_bytes) as pdf_filelike:
        pdf_text = extract_text(pdf_filelike)

    return pdf_text
    # pattern = re.compile(
    #     r'(?is)\b(?:References|Bibliography)\b(.*?)(?=\n[A-Z][^\n]*\n|$)'
    # )
    
    # match = pattern.search(pdf_text)
    # if match:
    #     return match.group(1).strip()
    # return ""


def extract_references_from_claude(text):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("MISSING ANTHROPIC API KEY")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
        You need to extract the following details for all the papers in the references section in this text:
            
        [
            <json object>
                "name": "Title",
                "authors": ["Author List"]
            <json object close>
        ]

        Please give your result as a list of JSON objects and don't add any text before it, just return a list of json objects

        Here is the text: {text}
    """

    response = client.messages.create(
        model="claude-3-5-haiku-20241022",  
        max_tokens=6024,
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content":"[{"}
        ]
    )

    documents = response.content[0].text
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
    #print(clean_references)
    return clean_references