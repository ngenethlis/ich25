## TODO: MAKE THIS INTO AN API
## get data, create nodes savani side
## return nodes triggered by api call
## figure out library for visualising + format to visualize



from flask import Flask, request, jsonify
from typing import DefaultDict
from pprint import pprint

app = Flask("API")


PAPER_IDENTIFIER = DefaultDict()
# paper_name : paper_node

PAPER_REFS = DefaultDict(set)
# "paper_name" : set{paper_node}

class PaperNode:
   def __init__(self, name, url, authors,
                keywords, out_refs, publication_date
                ):
      self.name = self.val = name
      self.url = url
      self.authors = authors
      self.keywords = keywords # set of strings
      self.publication_date = publication_date

      # which papers does this paper reference
      self.out_references = out_refs # set of paper names
      self.num_out = len(out_refs)
 

      # how many papers reference this paper
      self.in_references = set()# set of strings
      self.num_in = 0 

      self.update_dict()

   def update_dict(self):
      for out in self.out_references:
         PAPER_REFS[out].add(self.name)
         # outcoming ref : out : set{papers that reference out}
      pprint(f"{PAPER_REFS=} after inserting {self.name}")
      global PAPER_IDENTIFIER
      PAPER_IDENTIFIER[self.name] = self     

   def add_in_references(self,in_refs):
      self.in_references = in_refs
      self.num_in = len(in_refs)

   def add_out_reference(self,out_ref):
      self.out_references.add(out_ref)
      self.num_out+=1

   def __repr__(self) -> str:
      return f"{self.name=}, {self.url=}, {self.num_in=}, {self.num_out=}"
    
   def to_dict(self):
       """Convert PaperNode to a JSON-serializable dictionary"""
       return {
           "name": self.name,
           "url": self.url,
           "authors": self.authors,  # Assuming it's already a list or string
           "keywords": list(self.keywords),  # Convert set to list for JSON
           "publication_date": self.publication_date,
           "out_references": list(self.out_references),  # Convert set to list
           "num_out": self.num_out,
           "in_references": list(self.in_references),  # Convert set to list
           "num_in": self.num_in
       }


@app.route('/calc_in_refs', methods=['GET'])
def in_ref_handler():
   """Call after all papers entered, calculates incoming references for every paper """
   pprint(f"vals {PAPER_REFS}")
   for (paper_name, in_refs_set) in PAPER_REFS.items():
      pprint(f" {paper_name=} , {in_refs_set=}")
      if paper_name not in PAPER_IDENTIFIER:
         continue
      paper = PAPER_IDENTIFIER[paper_name]
      paper.add_in_references(in_refs_set)
   return "0"

@app.route('/get_graph', methods=['GET'])  # Use GET instead of POST (more appropriate)
def get_graph():
    res = {name: node.to_dict() for name, node in PAPER_IDENTIFIER.items()}  # Convert to dict
    return jsonify(res)  # jsonify the entire dictionary

def add_node(name, out_refs=None):
    if not name:
        raise ValueError("Missing 'name' parameter")

    out_refs = out_refs or []  # Default to empty list if None
    url = 'fake'
    keywords = ['a']

    p = PaperNode(name, url, keywords, out_refs)

    return {"message": f"Added {name}", "paper": p.to_dict()}

@app.route('/add_node', methods=['POST'])
def add_node_api():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing 'name' parameter"}), 400

    result = add_node(data['name'], data.get('out_refs', []))
    return jsonify(result)

#def main():

#   p1 = PaperNode("p1", "fake", "a", out_refs={"p2","p3"})
 #  p2 = PaperNode("p2", "fake", "a", out_refs = {"p3"})
  # p3 = PaperNode("p3", "fake", "a", out_refs = {"p4"})
   #pprint(PAPER_REFS)
   #pprint(f"{PAPER_IDENTIFIER=}")
   #in_ref_handler()
   #pprint(PAPER_REFS)
   #pprint(p1)
   #pprint(p2)
   #pprint(p3)

if __name__ == '__main__':
   #main()
   app.run(debug=True)

#main()

