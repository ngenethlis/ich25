# ich25

Current ideas:

Anthropic: Use claude
- Jury + RAG

MW:
- code path generator


NoCode:
-



Story linking and analysis
- Vector DB - intersystems
- find out which article is about the same news story (scrape and use rss feeds, link news stories, and how we do it)
- compile a list of rss fields
- use react, display a timeline of events and then have that event blow up so that it shows left and right views using news cards -> click on the card to access the news story

# How to Run
Store an Anthropic API key in the ANTHROPIC_API_KEY environment variable.
This can be done either with the command line, or creating a .env file with the following line in it:
```
ANTHROPIC_API_KEY=sk-proj-4PYN.......
```

Install the requirements using
```bash
pip install -r requirements.txt
```

Run the program with:
```bash
streamlit run main.py
```
