

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from collections import Counter

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

class AssocOne(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

class AssocNum(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,float(e2))

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None, rel_type=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) 
                and (rel_type == None or isinstance(d.relation, rel_type))
                ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))
    def list_associations(self):
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association)]))
    def list_objects(self):
        return list(set([d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]))
    def list_users(self):
        return list(set([d.user for d in self.declarations]))
    def list_types(self):
        return list(set(
            [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype)] +
            [d.relation.entity2 for d in self.declarations if isinstance(d.relation, Member) or isinstance(d.relation, Subtype)]
        ))
    def list_local_associations(self, entity):
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association) and (d.relation.entity1 == entity or d.relation.entity2 == entity)]))
    #6
    def list_relations_by_user(self, user):
        return list(set([d.relation.name for d in self.declarations if d.user == user]))
    #7
    def associations_by_user(self, user):
        return len(list(set([d.relation.name for d in self.declarations if (d.user == user) and isinstance(d.relation, Association)])))
    #8
    def list_local_associations_by_user(self, entity):
        return list(set(
            [(d.relation.name, d.user) for d in self.declarations if isinstance(d.relation, Association) and
            entity in [d.relation.entity1, d.relation.entity2]
            ]))
    #9
    def predecessor(self, a, b):
        predec_b = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member,Subtype)) and (d.relation.entity1 == b)]
        return (a in predec_b) or any([self.predecessor(a, p) for p in predec_b])
    #10
    def predecessor_path(self, a, b):
        predec_b = [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Member,Subtype)) and (d.relation.entity1 == b)]
        if a in predec_b:
            return [a, b]
        for path in [self.predecessor_path(a,p) for p in predec_b]:
            if not path is None:
                return path + [b]
        return None
    #11
    def query(self, entity, assoc_name=None):
        pds = [self.query(d.relation.entity2, assoc_name) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        return [d for sublist in pds for d in sublist] + self.query_local(e1=entity, rel=assoc_name, rel_type=Association)

    def query_predecessor(self, entity, assoc_name,first=True):
        pds = [self.query_predecessor(d.relation.entity2, assoc_name,first=False) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        if first:
            [d for sublist in pds for d in sublist]
        return [d for sublist in pds for d in sublist] + self.query_local(e1=entity, rel=assoc_name)
    
    def query2(self, entity, rel_name=None):
        return self.query(entity, rel_name) + self.query_local(e1=entity, rel=rel_name, rel_type=(Member, Subtype))

    def query_cancel(self, entity, assoc_name=None):
        pds = [self.query_cancel(d.relation.entity2, assoc_name) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        local = self.query_local(e1=entity, rel=assoc_name, rel_type=Association)
        return [d for sublist in pds for d in sublist if d.relation.name not in[l.relation.name for l in local]] + local

    #13
    def query_down(self, entity, assoc_name, first=True):
        desc = [self.query_down(d.relation.entity1, assoc_name, first=False) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity2 == entity]
        if first:
            return [d for sublist in desc for d in sublist]
        return [d for sublist in desc for d in sublist] + self.query_local(e1=entity, rel=assoc_name)

    def query_induce(self, entity, assoc_name):
        desc = self.query_down(entity, assoc_name)
        for val, _ in Counter([d.relation.entity2 for d in desc]).most_common(1):
            return val
        return None
    
    def query_local_assoc(self, entity, assoc_name):
        local = self.query_local(e1=entity, rel=assoc_name)

        for l in local:
            if isinstance(l.relation, AssocNum):
                values = [d.relation.entity2 for d in local]
                return sum(values)/len(local)
            if isinstance(l.relation, AssocOne):
                val, count = Counter([d.relation.entity2 for d in local]).most_common(1)[0]
                return val, count/len(local)
    
            if isinstance(l.relation, Association):
                mc = []
                freq = 0
                for val, count in Counter([d.relation.entity2 for d in local]).most_common():
                    mc.append((val, count/len(local)))
                    freq += count/len(local)
                    if freq > 0.75:
                        return mc
    
    def query_assoc_value(self, E, A):
        local = self.query_local(e1=E,rel=A)
        local_values = [l.relation.entity2 for l in local]

        if len(set(local_values)) == 1:
            return local_values[0]
        
        predecessor = [a for a in self.query(entity=E, assoc_name=A) if a not in local]

        def perc(lista, value):
            if lista == []:
                return 0
            return len([l for l in lista if l.relation.entity2 == value])/len(lista)

        return max(local_values + [i.relation.entity2 for i in predecessor], \
               key=lambda v: (perc(local, v) + perc(predecessor, v))/2)

