from dataclasses import dataclass
from anthropic import Anthropic
from openai import OpenAI
from typing import List, Dict, Any
import re

MODEL_NAME = "claude-3-5-sonnet-20241022"


@dataclass
class AnalysisResponse:
    summary: str
    methodological_issues: str
    conflict_of_interest: str
    future_research: List[str]


@dataclass
class SearchResult:
    """mock container to represent papers/entries returned by IRIS vector DB"""

    text: str
    metadata: Dict[str, Any]


class PaperAnalyser:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.client = Anthropic()

        self.analyse_prompt = f"""
            Please do the following:
            1. Write a quick and simple 2 sentence summary of the paper. (In <summary> tags.)
            2. If the methods in the paper have any issues or assumptions write them in short bullet points. (In <methodological_issues> tags.)
            3. If there is a section outlining conflicts of interest, summarise them. (In <conflict_of_interest> tags.)
            4. If the paper poses any open question or states any areas of future research, give them in a list seperated only by newlines. (In <future_research> tags.)
        """

    def summarize(self, text: str) -> AnalysisResponse:
        """summarises the paper into a structured AnalysisResponse using custom parsng"""
        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": self.analyse_prompt + text}],
            }
        ]
        response = self.client.messages.create(
            max_tokens=500, temperature=0, model=self.model_name, messages=messages
        )
        raw_text = response.content[0].text  # " ".join(chunk.text for chunk in response.content)

        summary = self.extract_tag_content(raw_text, "summary")
        methodological_issues = self.extract_tag_content(
            raw_text, "methodological_issues"
        )
        conflict_of_interest = self.extract_tag_content(
            raw_text, "conflict_of_interest"
        )
        future_research_text = self.extract_tag_content(raw_text, "future_research")

        future_research_list = [
            line.strip() for line in future_research_text.split("\n") if line.strip()
        ]

        return AnalysisResponse(
            summary=summary,
            methodological_issues=methodological_issues,
            conflict_of_interest=conflict_of_interest,
            future_research=future_research_list,
        )

    def extract_tag_content(self, text: str, tag: str) -> str:
        pattern = f"<{tag}>(.*?)</{tag}>"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    # IRIS VECTOR CHECKING LOGIC

    def check_gaps_against_iris(
        self, analysis: AnalysisResponse, top_k: int = 3
    ) -> None:
        """
        For each 'future research' gap in the analysis, perform:
            1. Embedding
            2. Vector search in IRIS
            3. Summarize & evaluate how well the search results address that gap.

        Prints the results, but you could also return them if desired.
        """
        # 1. If there are no future research items, just return
        if not analysis.future_research:
            print("No future research gaps identified. Nothing to check against IRIS.")
            return

        for i, gap in enumerate(analysis.future_research, start=1):
            print(f"\n=== Checking Future Research Gap #{i}: ===\n{gap}")

            # (a) Get naive embedding for the gap
            gap_embedding = self.embed_text(gap)

            # (b) Query IRIS vector DB for top_k results
            results = self.iris_vector_search(gap_embedding, top_k=top_k)

            # (c) Evaluate each result to see if it addresses the gap
            for idx, result in enumerate(results, start=1):
                eval_output = self.evaluate_gap_against_paper(gap, result)
                print(f"\n--- IRIS Result #{idx} ---")
                print(f"Title: {result.metadata.get('title', 'Unknown')}")
                print(
                    f"Summary: {result.metadata.get('summary', 'No summary available')}"
                )
                print(f"Evaluation: {eval_output}")

    def evaluate_gap_against_paper(self, gap: str, search_result: SearchResult) -> str:
        """
        Uses Claude to see if the given `search_result` addresses the research gap.
        """
        eval_prompt = (
            f"Research Gap: {gap}\n"
            f"Paper Summary: {search_result.metadata.get('summary', '')}\n\n"
            "Question: Does this paper address the research gap? Provide a short explanation."
        )
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=300,
            messages=[{"role": "user", "content": eval_prompt}],
        )
        raw_text = " ".join(chunk.text for chunk in response.content)
        return raw_text.strip()

    # mock embedding and iris vector search
    @staticmethod
    def embed_text(text: str) -> List[float]:
        """
        Converts the text into a vector embedding (mock/placeholder).

        In a real system, plug in an actual embeddings model
        (like sentence-transformers or an API call).
        """
        return [float(ord(c)) % 50 for c in text[:16]]  # Very naive placeholder

    @staticmethod
    def iris_vector_search(
        embedding: List[float], top_k: int = 3
    ) -> List[SearchResult]:
        """
        Mock function that simulates searching in a vector DB.
        In reality, you'd call your actual vector DB or API here.
        """
        # Return some static dummy results for demonstration
        mock_results = [
            SearchResult(
                text="Paper on scaling XYZ to large-scale environments...",
                metadata={
                    "title": "Scaling XYZ",
                    "summary": "Explores performance aspects of scaling XYZ technology.",
                },
            ),
            SearchResult(
                text="Comparative study of XYZ vs. old method",
                metadata={
                    "title": "Comparative Study",
                    "summary": "Compares XYZ with previous approaches, focusing on performance trade-offs.",
                },
            ),
            SearchResult(
                text="New frontiers in ABC domain with advanced XYZ",
                metadata={
                    "title": "New Frontiers",
                    "summary": "Discusses advanced features and future directions for XYZ in ABC domain.",
                },
            ),
        ]
        return mock_results[:top_k]


if __name__ == "__main__":
    # 3.1 Instantiate the analyser
    analyser = PaperAnalyser()

    # 3.2 Some mock paper text
    mock_paper_text = """
    Title: An Exploration of Method XYZ in Domain ABC
    Methods: We tested the method on a small scale...
    Results: We found that XYZ outperforms older approaches in limited settings...
    Conflicts of Interest: The authors have no conflicts to disclose.
    Future Work: We propose investigating its scalability to large data sets...
    """

    # 3.3 Summarize the paper
    analysis_response = analyser.summarize(mock_paper_text)
    print("=== SUMMARY ===")
    print(analysis_response.summary)
    print("=== METHODOLOGICAL ISSUES ===")
    print(analysis_response.methodological_issues)
    print("=== CONFLICTS OF INTEREST ===")
    print(analysis_response.conflict_of_interest)
    print("=== FUTURE RESEARCH ===")
    print(analysis_response.future_research)
    print("=========================")

    # 3.4 Check each identified gap against the IRIS DB
    analyser.check_gaps_against_iris(analysis_response, top_k=3)
