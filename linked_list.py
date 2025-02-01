import types


class PaperNode:
   def __init__(self, name, url, keywords, out_refs, in_refs = set()):
      self.name = self.val = name
      self.url = url
      self.keywords = keywords # set of strings
      # how many papers reference this paper
      self.in_references = in_refs # set of strings
      self.num_in = len(in_refs)
      # which papers does this paper reference
      self.out_references = out_refs # set of urls for paper.
      self.num_out = len(out_refs)

   def add_in_reference(self,in_ref):
      self.in_references.add(in_ref)
      self.num_in+=1

   def add_out_reference(self,out_ref):
      self.out_references.add(out_ref)
      self.num_out+=1


# 


