from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any
from paper_evaluator import PaperAnalyser, AnalysisResponse
from data_retrieval.retrieve_arxiv_papers import get_papers
from data_retrieval.generate_claude_keywords import generate_keywords_with_claude
from pprint import pprint
from vector_db.InCiteOOP import InCiteIRISDatabase
import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial

app = Flask(__name__)
CORS(app)   

vector_db = InCiteIRISDatabase()
paper_analyser = PaperAnalyser()
graph_generator = None

# Error handling
class APIError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

def analyze_paper(paper):
    analysis = paper_analyser.summarize(paper['content'])
    paper['summary'] = analysis.summary
    paper['method_issues'] = analysis.methodological_issues
    paper['coi'] = analysis.conflict_of_interest
    paper['future_research'] = analysis.future_research
    return paper

@app.errorhandler(APIError)
def handle_api_error(error: APIError) -> tuple[Dict[str, Any], int]:
    response = {
        'error': error.message
    }
    return jsonify(response), error.status_code

@app.route('/get_graph', methods=['POST'])
async def get_graph():
    data = request.get_json()
    
    if not data or 'query' not in data:
        raise APIError('Missing required field: query')
    
    query = data['query']
    if not isinstance(query, str):
        raise APIError('Query must be a string')
    
    papers = vector_db.query_articles_json(query, 100)
    if not papers:
        print("Cache Miss")
        kw = generate_keywords_with_claude(query)
        papers = get_papers(kw, 10)
        print([paper['name'] for paper in papers])
        print("Analyzing papers")
        # Use ProcessPoolExecutor for CPU-intensive tasks
        with ProcessPoolExecutor() as executor:
            # Create a partial function with the paper_analyser instance
            papers = list(executor.map(analyze_paper, papers))
        print("Inserting papers into DB")
        for paper in papers:
            vector_db.insert_article_json(paper)
    else:
        print("Cache Hit")

    papers = apply_in_refs(papers)
    
    print([paper['summary'] for paper in papers])
    
    try:
        # Process the query and generate graph
        # Replace this with your actual graph generation logic
        result = {
            'query': query,
            'graph': papers
        }
        return jsonify(result)
    except Exception as e:
        raise APIError(f'Error generating graph: {str(e)}')

def apply_in_refs(papers):
    # Step 1: Create a mapping from paper URLs to their indices
    url_to_index = {paper['url']: i for i, paper in enumerate(papers)}
    
    # Initialize in_refs for each paper
    for paper in papers:
        paper['in_refs'] = []
        paper['num_in'] = 0
    
    # Step 2: Iterate through the list of papers
    for paper in papers:
        for out_ref in paper['out_references']:
            if out_ref in url_to_index:
                referenced_paper_index = url_to_index[out_ref]
                papers[referenced_paper_index]['in_refs'].append(paper['url'])
                papers[referenced_paper_index]['num_in'] += 1
    
    return papers

@app.route('/get_paper', methods=['POST'])
def get_paper():
    data = request.get_json()
    
    if not data or 'id' not in data:
        raise APIError('Missing required field: id')
    
    paper_id = data['id']
    if not isinstance(paper_id, str):
        raise APIError('Paper ID must be a string')
    
    # paper = vector_db.get_paper(paper_id)
    # if not paper:
    #     raise APIError('Paper not found', status_code=404)
    
    try:
        # Process the paper ID and retrieve paper
        # Replace this with your actual paper retrieval logic
        result = {
            'id': paper_id,
            'title': f'Paper with ID: {paper_id}',
            'content': 'Paper content goes here'
        }
        return jsonify(result)
    except Exception as e:
        raise APIError(f'Error retrieving paper: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)