#encoding: utf8

from semantic_network import *
from bayes_net import *
from constraintsearch import *

import collections

class MyBN(BayesNet):

    def conjuctions(self, vars):
        if len(vars) == 1:
            return [[(vars[0], True)], [(vars[0], False)]]
        l = []
        for c in self.conjuctions(vars[1:]):
            l.append([(vars[0], True)] + c)
            l.append([(vars[0], False)] + c)
        return l

    def individual_probabilities(self):
        variables = list(self.dependencies.keys())
        joinProbs = {frozenset(conj): self.jointProb(conj) for conj in self.conjuctions(variables)}
        return {var: sum([joinProbs[frozenset(conj)] for conj in list(joinProbs.keys()) if (var, True) in conj]) for var in variables}

class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)

    def translate(self, super, subtypes):
        phrase = ""
        for prop in subtypes[:-1]:
            phrase+= str(prop).capitalize()+"(x) or "
        phrase += str(subtypes[-1]).capitalize()+"(x)"
        return "Qx "+phrase+" => "+str(super).capitalize()+"(x)"

    def query_inherit2(self, entity, assoc_name=None):
        pds = [self.query_inherit2(d.relation.entity2, assoc_name) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        return [d for sublist in pds for d in sublist] + [d for d in self.query_local(e1=entity, relname=assoc_name) if isinstance(d.relation, Association)]

    def query_cancel(self, entity, assoc_name=None):
        pds = [self.query_cancel(d.relation.entity2, assoc_name) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        local = self.query_local(e1=entity, relname=assoc_name)
        return [d for sublist in pds for d in sublist if d.relation.name not in[l.relation.name for l in local]] + local

    #https://stackoverflow.com/questions/9001509/how-can-i-sort-a-dictionary-by-key
    def translate_ontology(self):
        subtypes = {decl2.relation.entity2: 
                sorted(list(set([d.relation.entity1 for d in self.declarations 
                if isinstance(d.relation,Subtype) and d.relation.entity2 == decl2.relation.entity2]))) 
            for decl2 in self.declarations if isinstance(decl2.relation, Subtype)}

        return [self.translate(super, subtypes[super]) 
            for super in {k: v for k, v in sorted(subtypes.items())}]

    def query_inherit(self,entity,assoc):
        pds=[self.query_inherit(d.relation.entity2, assoc) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1==entity]
        return [d for sublist in pds for d in sublist] + [d for d in self.declarations if 
                    entity in [d.relation.entity1,d.relation.entity2] and 
                    isinstance(d.relation, Association) and 
                    (assoc in [d.relation.name, d.relation.inverse])]

    def query(self,entity,relname):
        if relname in ['member', 'subtype']:
            return sorted(list(set([d.relation.entity2 for d in self.query_local(e1=entity, relname=relname)])), reverse=True)
        assoc_decl = self.query_inherit2(entity, relname)
        majority_props = collections.Counter([d.relation.assoc_properties() for d in assoc_decl]).most_common(1)[0][0]
        if majority_props[0] == 'single':
            return [collections.Counter([d.relation.entity2 for d in self.query_cancel(entity, relname) if d.relation.assoc_properties()==majority_props]).most_common(1)[0][0]]
        else:
            return sorted(list(set([d.relation.entity2 for d in assoc_decl if d.relation.assoc_properties()==majority_props])), reverse=True)

class MyCS(ConstraintSearch):

    def search_all(self,domains=None,xpto=None):
        if domains==None:
            domains = self.domains

        if any([lv==[] for lv in domains.values()]):
            return None

        if all([len(lv)==1 for lv in list(domains.values())]):
            sol = {v:lv[0] for (v,lv) in domains.items()}
            if sol in xpto:
                return None
            return [sol]
               
        for var in domains.keys():
            if len(domains[var])>1:
                solutions = []
                for val in domains[var]:
                    newdomains = dict(domains)
                    newdomains[var] = [val]
                    edges = [(v1,v2) for (v1,v2) in self.constraints if v2==var]
                    newdomains = self.constraint_propagation(newdomains,edges)
                    solution = self.search_all(newdomains, xpto=solutions)
                    if solution != None:
                        solutions+=solution
                return solutions
        return None