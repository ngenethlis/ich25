import types
from typing import DefaultDict

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
         PAPER_REFS[out].add(self)
         # outcoming ref : out : set{papers that reference out}
      print(f"{PAPER_REFS=} after inserting {self.name}")
      global PAPER_IDENTIFIER
      PAPER_IDENTIFIER[self.name] = self     

   def add_in_references(self,in_refs):
      self.in_references = in_refs
      self.num_in = len(in_refs)

   def add_out_reference(self,out_ref):
      self.out_references.add(out_ref)
      self.num_out+=1


def in_ref_handler():
   """Call after all papers entered, calculates incoming references for every paper """
   print(PAPER_REFS.values())
   for (paper_name,in_refs_set) in PAPER_REFS.values():
      print(f" {paper_name} , {in_refs_set}")
      paper = PAPER_IDENTIFIER[paper_name]
      paper.add_in_references(in_refs_set)
   return 

def main():
   p1 = PaperNode("p1", "fake", "a", out_refs={"p2","p3"})
   p2 = PaperNode("p2", "fake", "a", out_refs = {"p3"})
   p2 = PaperNode("p3", "fake", "a", out_refs = {"p4"})
   print(PAPER_REFS)
   print(PAPER_IDENTIFIER)
   in_ref_handler()
   print(PAPER_REFS)

main()

