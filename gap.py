import anthropic
import os
import re
from typing import List, Dict, Any


client = anthropic.Anthropic(
    # api_key=api_key
)


def call_claude(prompt: str) -> str:
    """
    Calls the Claude API with the given prompt.
    """
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=messages,
    )
    if not response.content:
        return ""

    combined_text = " ".join(block.text for block in response.content)
    return combined_text.strip()


def embed_text(text: str) -> List[float]:
    """
    Converts the text into a vector embedding.
    NEED TOOOO Replace this with your actual embedding logic or service. 
    """
    # example  gpt
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

    # def embed_text(text: str) -> List[float]:
    #     embedding = model.encode(text)
    #     return embedding.tolist()
    return [float(ord(c)) % 50 for c in text[:16]]  # Very naive placeholder


class SearchResult:
    def __init__(self, text: str, metadata: Dict[str, Any]):
        self.text = text
        self.metadata = metadata


def iris_vector_search(embedding: List[float], top_k: int = 3) -> List[SearchResult]:
    """
    Queries the IRIS Vector DB with the provided embedding and returns top_k matches.
    In a real system, you'd have code like:
      results = iris_client.query(embedding, top_k=top_k)
    """
    # Here we just return a mock result
    return [
        SearchResult(
            text="Paper on scaling XYZ to large-scale environments...",
            metadata={
                "title": "Scaling XYZ",
                "summary": "A paper that explores some aspects of scaling XYZ technology."
            }
        ),
        SearchResult(
            text="Another paper comparing XYZ to other methods...",
            metadata={
                "title": "Comparative Study",
                "summary": "This study compares XYZ with older techniques, focusing on performance."
            }
        )
    ][:top_k]


def parse_questions(gaps_str: str) -> List[str]:
    """
    Parses Claude's output that contains potential research gaps (in bullet points or enumerated format).
    Returns a list of questions.
    """
    # Example: If the gaps_str is enumerated, we can split by lines and strip.
    lines = gaps_str.strip().split("\n")
    questions = []
    for line in lines:
        # A simple regex that tries to capture lines that start with a digit or bullet,
        # then captures the rest of the line as a question.
        match = re.match(r"^\s*[\d\-\*\.\)]*\s*(.*)", line)
        if match:
            question_text = match.group(1).strip()
            if question_text:
                questions.append(question_text)
    return questions


def process_paper(paper_text: str) -> List[str]:
    """
    Main pipeline for:
    1) Summarizing the paper
    2) Identifying potential research gaps
    3) Checking each gap against IRIS to see if it is addressed
    """

    # Step 1. Summarize the paper
    summary_prompt = f"Summarize the following paper in 300 words:\n{
        paper_text}"
    paper_summary = call_claude(summary_prompt)
    print("=== PAPER SUMMARY ===")
    print(paper_summary)
    print("---------------------")

    # Step 2. Identify research gaps
    gap_prompt = (
        f"From this summary, what are 3-5 open research questions?\n"
        f"Summary:\n{paper_summary}"
    )
    potential_gaps_text = call_claude(gap_prompt)
    print("=== POTENTIAL RESEARCH GAPS ===")
    print(potential_gaps_text)
    print("-------------------------------")

    # Parse the output into a list of questions
    questions = parse_questions(potential_gaps_text)

    # Step 3. For each question, check IRIS
    for idx, q in enumerate(questions, start=1):
        print(f"\n--- Checking Gap #{idx}: {q} ---")

        # (a) embed the question
        q_embedding = embed_text(q)

        # (b) retrieve top matches from IRIS
        results = iris_vector_search(q_embedding, top_k=3)

        # (c) Summarize each relevant paper or chunk and evaluate
        for res_idx, res in enumerate(results, start=1):
            # If there's a stored summary, we can just use it
            paper_summary = res.metadata.get("summary", "No summary available")

            # Evaluate if it addresses the question
            eval_prompt = (
                f"Question: {q}\n"
                f"Paper summary: {paper_summary}\n"
                f"Does this paper address the question? Provide reasoning."
            )
            evaluation = call_claude(eval_prompt)

            print(f"Result #{res_idx} - Title: {res.metadata.get('title')}")
            print(f"Evaluation: {evaluation}")

    return questions


if __name__ == "__main__":
    # Mock paper text
    mock_paper_text = """
    Title: An Exploration of Method XYZ in Domain ABC
    Authors: ...
    Abstract: This paper studies the performance of XYZ in the context of ABC. We find ...
    Introduction: ...
    Methods: ...
    Results: ...
    Conclusion: More large-scale tests needed ...
    """

    # Run the pipeline
    final_questions = process_paper(mock_paper_text)

    print("\n=== FINAL QUESTIONS ===")
    for q in final_questions:
        print("-", q)
