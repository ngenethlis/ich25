## TODO: MAKE THIS INTO AN API
## get data, create nodes savani side
## return nodes triggered by api call
## figure out library for visualising + format to visualize


import types
from typing import DefaultDict
from pprint import pprint

PAPER_IDENTIFIER = DefaultDict()
# paper_name : paper_node

PAPER_REFS = DefaultDict(set)
# "paper_name" : set{paper_node}

class PaperNode:
   def __init__(self, name, url, keywords, out_refs):
      self.name = self.val = name
      self.url = url
      self.keywords = keywords # set of strings
      # how many papers reference this paper
      self.in_references = set()# set of strings
      self.num_in = 0 
      # which papers does this paper reference
      self.out_references = out_refs # set of paper names
      self.num_out = len(out_refs)
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


def in_ref_handler():
   """Call after all papers entered, calculates incoming references for every paper """
   pprint(f"vals {PAPER_REFS}")
   for (paper_name, in_refs_set) in PAPER_REFS.items():
      pprint(f" {paper_name=} , {in_refs_set=}")
      if paper_name not in PAPER_IDENTIFIER:
         continue
      paper = PAPER_IDENTIFIER[paper_name]
      paper.add_in_references(in_refs_set)
   return 

def main():
   p1 = PaperNode("p1", "fake", "a", out_refs={"p2","p3"})
   p2 = PaperNode("p2", "fake", "a", out_refs = {"p3"})
   p3 = PaperNode("p3", "fake", "a", out_refs = {"p4"})
   pprint(PAPER_REFS)
   pprint(f"{PAPER_IDENTIFIER=}")
   in_ref_handler()
   pprint(PAPER_REFS)
   pprint(p1)
   pprint(p2)
   pprint(p3)

main()

