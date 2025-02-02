from generate_claude_keywords import generate_keywords_with_claude
from retrieve_arxiv_papers import get_papers
#kws = []

def main():
    topics = ["artificial intelligence"]
    for t in topics:
        kw = generate_keywords_with_claude(t)
        #kws.append(kw)
        papers = get_papers(kw, 100)
        print(papers)
        

if __name__ == "__main__":
    main()