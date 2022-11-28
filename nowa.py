from itertools import combinations

import networkx as nx

import generator


def k_cliques(graph):
    # cliques = [{i, j} for i, j in graph.edges() if i != j]
    cliques = []
    for edge in graph.edges:
        cliques.append({edge[0], edge[1]})
    k = 2

    while cliques:
        yield k, cliques

        # merge k-cliques into (k+1)-cliques
        cliques_1 = set()
        for u, v in combinations(cliques, 2):
            # w = wierzcholki nienalezace do 2 klik na raz
            w = u ^ v
            # jesli sa takie 2, oraz są one połączone, tworzą one nową klikę
            if len(w) == 2 and graph.has_edge(*w):
                cliques_1.add(tuple(u | w))

        # remove duplicates
        cliques = list(map(set, cliques_1))
        k += 1


def get_cliques(graph):
    graph.get_adj()
    for k, cliques in k_cliques(graph):
        if k > 2:
            # print('%d-cliques = %d, %s.' % (k, len(cliques), cliques))
            yield k, cliques


def calculate_area(k, cliques):
    for clique in cliques:
        print(clique)


nodes, edges = 6, 10
graph = generator.gen_graph(6, 80)

for k, cliques in get_cliques(graph):
    calculate_area(k, cliques)
    # print(*cliques)
    # print(cliques[0])
    # for el in cliques[0]:
    #     print(el.x)
