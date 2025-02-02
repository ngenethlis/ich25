import re
import io
import requests
from pdfminer.high_level import extract_text
import json
from langchain_community.retrievers import ArxivRetriever
#import arxiv


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
        references = get_references_from_semantic_scholar(arxiv_id)
        if len(references) != 0:
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

def get_references_from_semantic_scholar(arxiv_id: str) -> dict:

    # Base URL without a trailing slash
    base_url = "https://api.semanticscholar.org/graph/v1/paper/"
    fields = (
        "references.title"
    )
    url = f"{base_url}arXiv:{arxiv_id}?fields={fields}"
    headers = {
        "User-Agent": "apps/1.0"  
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return {}
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code} {response.text}")
        return {}
    
    data = response.json()
    reference_titles = [ref.get("title", "") for ref in data.get("references", [])]

    return reference_titles

def get_references_with_crossrefapi():
    pass