from dataclasses import dataclass
from anthropic import Anthropic
from typing import List
import re

# For now, only claude-3-5-sonnet-20241022 supports PDFs
MODEL_NAME = "claude-3-5-sonnet-20241022"

@dataclass
class AnalysisResponse:
    summary: str
    methodological_issues: str
    conflict_of_interest: str
    future_research: List[str]

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
        messages = [
            {
                "role": 'user',
                "content": [
                    {"type": "text", "text": self.analyse_prompt + text}
                ]
            }
        ]
        response =  self.client.messages.create(
            max_tokens=500,
            temperature=0,
            model=self.model_name,
            messages=messages
        ).content[0].text

        summary = self.extract_tag_content(response, "summary")
        methodological_issues = self.extract_tag_content(response, "methodological_issues")
        conflict_of_interest = self.extract_tag_content(response, "conflict_of_interest")
        future_research = self.extract_tag_content(response, "future_research").split("\n")

        return AnalysisResponse(
            summary=summary,
            methodological_issues=methodological_issues,
            conflict_of_interest=conflict_of_interest,
            future_research=future_research
        )
    
    def extract_tag_content(self, text: str, tag: str) -> str:
        pattern = f"<{tag}>(.*?)</{tag}>"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""