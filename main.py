from langchain_text_splitters import CharacterTextSplitter
import streamlit as st
import concurrent.futures

from langchain_community.retrievers import ArxivRetriever
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from chromadb.api import shared_system_client

from chains import (
    extraction_chain,
    theme_aggregation_chain,
    format_sources_for_prompt,
    section_generation_chain,
)

arxiv_retriever = ArxivRetriever(
    load_max_docs=60,
    get_full_documents=True,
    load_all_available_meta=True,
)
vector_db = Chroma(
    collection_name="papers_collection",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./vector_db",
)

# Step 1: Prompt Input
st.title("Literature Review Generator")
prompt = st.text_area("Enter your research project topic to start:", "")
submit_button = st.button("Submit")

if submit_button:
    st.session_state.submitted = True

if "submitted" in st.session_state and st.session_state.submitted:
    st.session_state.submitted = False
    st.rerun()

papers_tab, analyses_tab, plan_tab, review_tab = st.tabs(
    ["Papers", "Analyses", "Plan", "Review"]
)

# Step 2: Placeholder for each step's output
if prompt:
    # Step 2 - Analyze Research Papers
    with papers_tab:
        with st.spinner("Finding research papers..."):
            # paper_analyses = YourLangChainFunction(prompt)  # Returns a list of dictionaries
            docs = filter_complex_metadata(arxiv_retriever.invoke(prompt))
            # Drop all documents that have comment or review in the title
            docs = [
                doc
                for doc in docs
                if "comment" not in doc.metadata["Title"].lower()
                and "review" not in doc.metadata["Title"].lower()
            ]
        st.success("Research Papers found, proceeding to analysis")
        st.header("Research Papers")
        for paper in docs:
            with st.expander(f"{paper.metadata['Title']}"):
                st.write(f"**URL**: {paper.metadata['entry_id']}")
                st.write(f"**Authors**: {paper.metadata['Authors']}")
                st.write(f"**Summary**:\n{paper.metadata['Summary']}")

    paper_analyses = []
    with analyses_tab:
        with st.spinner("Analyzing research papers..."):
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunked_documents = text_splitter.split_documents(docs)
            vector_db.add_documents(chunked_documents)

            relevant_docs = vector_db.similarity_search(prompt, k=10)

            def analyze_document(doc):
                results = extraction_chain.invoke([doc])
                results["title"] = doc.metadata["Title"]
                results["entry_id"] = doc.metadata["entry_id"]
                return results

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_doc = {
                    executor.submit(analyze_document, doc): doc for doc in relevant_docs
                }
                for future in concurrent.futures.as_completed(future_to_doc):
                    paper_analyses.append(future.result())

        st.success("Research paper analyses complete, planning literature review")
        st.header("Sample Research Paper Analyses")
        for paper in paper_analyses:
            with st.expander(f"{paper['title']}"):
                st.write(f"**URL**: {paper['entry_id']}")
                st.write(f"**Themes**:\n{paper['themes']}")
                st.write(f"**Strengths & Weaknesses**:\n{paper['strength_weakness']}")
                st.write(f"**Summary**:\n{paper['summary']}")

    # Step 3 - Generate Literature Review Outline
    with plan_tab:
        with st.spinner("Generating Literature Review Outline..."):
            outline = theme_aggregation_chain.invoke(paper_analyses)
        st.success("Outline complete, writing review")

        # Displaying the outline
        st.markdown("# Literature Review Outline")
        for section in outline["sections"]:
            st.markdown(f"## {section['title']}")
            st.markdown(section["description"])

    # Step 4 - Generate Full Literature Review
    with review_tab:
        with st.spinner("Generating Full Literature Review..."):
            filled_sections = {}

            def generate_section(section):
                relevant_docs = vector_db.similarity_search(section["title"], k=5)
                formatted_sources = format_sources_for_prompt(
                    relevant_docs, section["title"]
                )
                body = section_generation_chain.invoke(
                    {
                        "review_topic": prompt,
                        "section_title": section["title"],
                        "description": section["description"],
                        "sources": formatted_sources,
                    }
                )
                return section["title"], body

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_section = {
                    executor.submit(generate_section, section): section
                    for section in outline["sections"]
                }
                for future in concurrent.futures.as_completed(future_to_section):
                    title, body = future.result()
                    filled_sections[title] = body
        st.success("Step 4: Full Literature Review complete!")

        # Displaying the full review
        st.markdown("# Full Literature Review")
        for title, body in filled_sections.items():
            if not body[0] == "#":
                st.markdown(f"### {title}")
            st.markdown(body)
