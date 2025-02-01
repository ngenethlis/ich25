from typing import List, Dict

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.documents import Document
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field

from dotenv import load_dotenv
import streamlit as st

load_dotenv()

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.5)
str_parser = StrOutputParser()


# Theme and Strength/Weakness Extraction
theme_analysis_template = """
Identify the main themes or research trends in the following research paper summary for the purpose of a literature review:
{output_text}
"""
strength_weakness_template = """
Analyze the following research paper summary. Identify the strengths, weaknesses, and any notable contributions to the field:
{output_text}
"""

theme_prompt = ChatPromptTemplate.from_template(template=theme_analysis_template)
strength_weakness_prompt = ChatPromptTemplate.from_template(
    template=strength_weakness_template
)

summary_chain = load_summarize_chain(llm)
theme_chain = theme_prompt | llm | str_parser
strength_weakness_chain = strength_weakness_prompt | llm | str_parser

extraction_chain = RunnableParallel(
    themes=theme_chain,
    strength_weakness=strength_weakness_chain,
    summary=lambda paper: summary_chain.invoke(paper)["output_text"],
)


def extraction_lambda(papers: List[Document]) -> List[Dict[str, str]]:
    return [extraction_chain.invoke(paper) for paper in papers]


parallel_extractor_chain = RunnableLambda(extraction_lambda)


# Common Topic Aggregation
class LitRevLayout(BaseModel):
    sections: List["LitRevSection"] = Field(
        ..., description="Sections of the literature review"
    )


class LitRevSection(BaseModel):
    title: str = Field(..., description="Title of the section")
    description: str = Field(..., description="Brief description of the theme")


section_parser = JsonOutputParser(pydantic_object=LitRevLayout)

theme_aggregation_template = """
You have been given the following themes extracted from various research papers:

{themes}

Identify and group similar themes into broader categories. These categories will serve as sections for a literature review that provides an overview of the current state of the field. Each section should have a title and a brief description summarizing the key trends and findings associated with that theme.

{format_instructions}
"""

theme_aggregation_prompt = ChatPromptTemplate.from_template(
    template=theme_aggregation_template,
    partial_variables={"format_instructions": section_parser.get_format_instructions()},
)


def aggregate_themes(all_analysis_results: List[Dict[str, str]]) -> str:
    """
    Aggregate themes extracted from multiple research papers into common topics for a literature review.

    Args:
        all_analysis_results (List[Dict[str, str]]): A list of dicts containing themes, s/ws, summary.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the theme title and its description.
    """
    all_themes = [result["themes"] for result in all_analysis_results]
    combined_themes = "\n".join(all_themes)
    return combined_themes


theme_aggregation_chain = (
    RunnableLambda(aggregate_themes) | theme_aggregation_prompt | llm | section_parser
)


# Section Filling
relevant_summary_template = """
Extract all information relevant to {section_title} from the following research paper, modifying as little as possible:
{paper}
"""

section_generation_template = """
You are writing a section of a literature review on {review_topic} aimed at third-year Computer Science students. Here is a list of sources relevant to the section titled "{section_title}".
{description}:

{sources}

For each source, do the following:
- Summarize and synthesize: Provide an overview of the main points and combine them into a coherent whole.
- Analyze and interpret: Add your interpretations where possible, discussing the significance of findings in relation to the literature as a whole.
- Critically evaluate: Mention the strengths and weaknesses of the sources.
- Write in well-structured paragraphs, using transition words and topic sentences to draw connections, comparisons, and contrasts.

Cite each source using its metadata. Format citations as follows: [Authors, arXiv ID].

Write at least well-organized and well cited paragraphs on the section topic, drawing from the sources provided. It should be understandable by a third year computer science student and have as many citations as possible.

Section: {section_title}
"""

# Create the PromptTemplate
section_generation_prompt = ChatPromptTemplate.from_template(
    template=section_generation_template
)

relevant_summary_prompt = ChatPromptTemplate.from_template(
    template=relevant_summary_template
)


def format_sources_for_prompt(retrieved_docs: List[Document], section: str) -> str:
    # Format the sources for the prompt, arXiv ID
    formatted_sources = ""
    for doc in retrieved_docs:
        # summary = relevant_summary_chain.invoke(
        #     {"section_title": section, "paper": doc.page_content}
        # )
        formatted_sources += f"{doc.metadata['Title']} by {doc.metadata.get('Authors', 'Unknown Authors')} {doc.metadata.get('entry_id', 'Unknown ID')}:\n{doc.page_content}\n\n"
    return formatted_sources


def populate_sections(sections: Dict[str, List[Dict[str, str]]]) -> Dict[str, str]:
    vector_db = Chroma(
        collection_name="papers_collection",
        embedding_function=OpenAIEmbeddings(),
        persist_directory="./vector_db",
    )
    filled_sections = {}
    for section in sections["sections"]:
        relevant_docs = vector_db.similarity_search(section["title"], k=5)
        formatted_sources = format_sources_for_prompt(relevant_docs, section["title"])
        body = section_generation_chain.invoke(
            {
                "section_title": section["title"],
                "description": section["description"],
                "sources": formatted_sources,
            }
        )
        filled_sections[section["title"]] = body
    return filled_sections


def populate_sections_db(
    sections: Dict[str, List[Dict[str, str]]], vector_db: Chroma
) -> Dict[str, str]:
    filled_sections = {}
    for section in sections["sections"]:
        relevant_docs = vector_db.similarity_search(section["title"], k=5)
        formatted_sources = format_sources_for_prompt(relevant_docs, section["title"])
        body = section_generation_chain.invoke(
            {
                "section_title": section["title"],
                "description": section["description"],
                "sources": formatted_sources,
            }
        )
        filled_sections[section["title"]] = body
    return filled_sections


relevant_summary_chain = relevant_summary_prompt | llm | str_parser

section_generation_chain = section_generation_prompt | llm | str_parser

populate_sections_chain = RunnableLambda(populate_sections)


full_chain = (
    parallel_extractor_chain | theme_aggregation_chain | populate_sections_chain
)
