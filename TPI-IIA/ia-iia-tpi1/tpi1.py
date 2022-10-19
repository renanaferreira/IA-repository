'''
ALUNO: Renan Alves Ferreira
NMEC:  93168
Pessoas com a qual discuti o problema:
mariana santos, pedro bastos, andre morais, alexandre rodrigues,
leandro silva e anthony pereira.
'''
from typing import Counter
from tree_search import *
from cidades import *
from strips import *


class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth'): 
        super().__init__(problem,strategy)

    def hybrid1_add_to_open(self,lnewnodes):
        #https://www.programiz.com/python-programming/methods/list/reverse
        #Legivel para pessoas com experiencia em manipulação de listas. Usei para compactar codigo
        #e só declarei even porque é mais facil criar a lista da cauda depois, ao inves de ficar a fazer
        #calculos matematicos para descobrir paridade
        even = ([node for node in lnewnodes if lnewnodes.index(node) % 2 == 0])[::-1]
        self.open_nodes[:0] = even
        self.open_nodes.extend([node for node in lnewnodes if node not in even])

    def hybrid2_add_to_open(self,lnewnodes):        
        self.open_nodes = sorted(self.open_nodes + lnewnodes, key=lambda node: node.depth - node.offset)

    def search2(self):
        counters = {}
        self.root.depth = 0
        self.root.offset = 0

        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            self.closed_nodes.append(node)
            if self.problem.goal_test(node.state):
                self.terminal = len(self.open_nodes)+1
                self.solution = node
                return self.get_path(node)
            self.non_terminal+=1
            node.children = []

            if(node.depth not in counters.keys()):
                counters[node.depth] = 0

            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    newnode = SearchNode(newstate,node)

                    newnode.depth = node.depth + 1
                    newnode.offset = counters[node.depth]
                    counters[node.depth] += 1
                    
                    node.children.append(newnode)
            self.add_to_open(node.children)
        return None


    def search_from_middle(self):
        middle = self.problem.domain.middle(self.problem.initial, self.problem.goal)
        #Significa que domain só contem duas cidades, a initial e a goal, que devem ter caminho direto
        if(middle is None):
            return self.search2()
        self.from_init = MyTree(SearchProblem(self.problem.domain, self.problem.initial, middle), self.strategy)
        self.to_goal   = MyTree(SearchProblem(self.problem.domain, middle, self.problem.goal)   , self.strategy)
        return self.from_init.search2() + self.to_goal.search2()[1:]

class MinhasCidades(Cidades):

    # state that minimizes heuristic(state1,middle)+heuristic(middle,state2)
    def middle(self,city1,city2):
        lcities = [(city, self.heuristic(city1, city) + self.heuristic(city, city2)) for city in self.coordinates.keys() if city != city1 and city != city2]
        #usei para se adaptar a diferentes tipos de dominio de cidades, incluindo aqueles que podem só conter 2 cidades
        if(lcities == []): 
            return None
        return sorted(lcities, key=lambda city:city[1])[0][0]

class MySTRIPS(STRIPS):
    def result(self, state, action):
        if not all(p in state for p in action.pc):
            return None
        newstate = [p for p in state if p not in action.neg]
        newstate.extend(action.pos)
        return newstate
    def sort(self,state):
        return sorted(state, key=lambda predicate: str(predicate))


