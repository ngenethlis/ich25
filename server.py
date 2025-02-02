from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any
from paper_evaluator import PaperAnalyser, AnalysisResponse
from data_retrieval.retrieve_arxiv_papers import get_papers
from data_retrieval.generate_claude_keywords import generate_keywords_with_claude
import asyncio

app = Flask(__name__)
CORS(app)

vector_db = None
paper_analyser = PaperAnalyser()
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