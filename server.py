from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any
from paper_evaluator import PaperAnalyser, AnalysisResponse
from data_retrieval.retrieve_arxiv_papers import get_papers
from data_retrieval.generate_claude_keywords import generate_keywords_with_claude
from pprint import pprint
import asyncio

app = Flask(__name__)
CORS(app)

vector_db = None
#paper_analyser = PaperAnalyser()
graph_generator = None


# Error handling
class APIError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

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
    
    papers = None # vector_db.get_related_papers(query)
    if not papers:
        kw = generate_keywords_with_claude(query)
        papers = get_papers(kw, 1)
        print(papers)

        async def analyze_paper(paper):
            analysis = paper_analyser.summarize(paper['content'])
            paper['summary'] = analysis.summary
            paper['method_issues'   ] = analysis.methodological_issues
            paper['coi'] = analysis.conflict_of_interest
            paper['future_research'] = analysis.future_research
            return paper
        
        # Create tasks for all papers and run them in parallel
        tasks = [analyze_paper(paper) for paper in papers]
        papers = await asyncio.gather(*tasks)
        # vector_db.add_paper(paper)
        # All papers in the same state after this, assume they have refs
        papers = apply_in_refs(papers)
    
    print([paper['summary'] for paper in papers])
    
    # graph = graph_generator.generate_graph(papers)
    
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

def main():
    papers = [
    {
        'name': 'Paper 1',
        'url': 'http://example.com/paper1',
        'authors': 'Author A, Author B',
        'content': 'Content of Paper 1',
        'publication_date': '2023-01-01',
        'out_references': ['http://example.com/paper2', 'http://example.com/paper3'],
        'num_out': 2,
        'summary': 'Summary of Paper 1',
        'method_issues': 'None',
        'coi': 'None',
        'future_research': 'Future research directions'
    },
    {
        'name': 'Paper 2',
        'url': 'http://example.com/paper2',
        'authors': 'Author C, Author D',
        'content': 'Content of Paper 2',
        'publication_date': '2023-02-01',
        'out_references': ['http://example.com/paper4', 'http://example.com/paper5'],
        'num_out': 2,
        'summary': 'Summary of Paper 2',
        'method_issues': 'None',
        'coi': 'None',
        'future_research': 'Future research directions'
    },
    {
        'name': 'Paper 3',
        'url': 'http://example.com/paper3',
        'authors': 'Author E, Author F',
        'content': 'Content of Paper 3',
        'publication_date': '2023-03-01',
        'out_references': ['http://example.com/paper6'],
        'num_out': 1,
        'summary': 'Summary of Paper 3',
        'method_issues': 'None',
        'coi': 'None',
        'future_research': 'Future research directions'
    },
    {
        'name': 'Paper 4',
        'url': 'http://example.com/paper4',
        'authors': 'Author G, Author H',
        'content': 'Content of Paper 4',
        'publication_date': '2023-04-01',
        'out_references': ['http://example.com/paper7'],
        'num_out': 1,
        'summary': 'Summary of Paper 4',
        'method_issues': 'None',
        'coi': 'None',
        'future_research': 'Future research directions'
    },
    {
        'name': 'Paper 5',
        'url': 'http://example.com/paper5',
        'authors': 'Author I, Author J',
        'content': 'Content of Paper 5',
        'publication_date': '2023-05-01',
        'out_references': ['http://example.com/paper8'],
        'num_out': 1,
        'summary': 'Summary of Paper 5',
        'method_issues': 'None',
        'coi': 'None',
        'future_research': 'Future research directions'
    },
    {
        'name': 'Paper 6',
        'url': 'http://example.com/paper6',
        'authors': 'Author K, Author L',
        'content': 'Content of Paper 6',
        'publication_date': '2023-06-01',
        'out_references': ['http://example.com/paper9'],
        'num_out': 1,
        'summary': 'Summary of Paper 6',
        'method_issues': 'None',
        'coi': 'None',
        'future_research': 'Future research directions'
    },
    {
        'name': 'Paper 7',
        'url': 'http://example.com/paper7',
        'authors': 'Author M, Author N',
        'content': 'Content of Paper 7',
        'publication_date': '2023-07-01',
        'out_references': ['http://example.com/paper10'],
        'num_out': 1,
        'summary': 'Summary of Paper 7',
        'method_issues': 'None',
        'coi': 'None',
        'future_research': 'Future research directions'
    },
    {
        'name': 'Paper 8',
        'url': 'http://example.com/paper8',
        'authors': 'Author O, Author P',
        'content': 'Content of Paper 8',
        'publication_date': '2023-08-01',
        'out_references': [],  # No references
        'num_out': 0,
        'summary': 'Summary of Paper 8',
        'method_issues': 'None',
        'coi': 'None',
        'future_research': 'Future research directions'
    },
    {
        'name': 'Paper 9',
        'url': 'http://example.com/paper9',
        'authors': 'Author Q, Author R',
        'content': 'Content of Paper 9',
        'publication_date': '2023-09-01',
        'out_references': [],  # No references
        'num_out': 0,
        'summary': 'Summary of Paper 9',
        'method_issues': 'None',
        'coi': 'None',
        'future_research': 'Future research directions'
    },
    {
        'name': 'Paper 10',
        'url': 'http://example.com/paper10',
        'authors': 'Author S, Author T',
        'content': 'Content of Paper 10',
        'publication_date': '2023-10-01',
        'out_references': [],  # No references
        'num_out': 0,
        'summary': 'Summary of Paper 10',
        'method_issues': 'None',
        'coi': 'None',
        'future_research': 'Future research directions'
    }
]
    papers = apply_in_refs(papers)

    pprint(papers)

main()
#    app.run(debug=True)
