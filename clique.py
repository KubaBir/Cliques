from generator import gen_graph


def is_clique(b):

    # Run a loop for all the set of edges
    # for the select vertex
    for i in range(1, b):
        for j in range(i + 1, b):

            # If any edge is missing
            if (graph[store[i]][store[j]] == 0):
                return False

    return True


graph = gen_graph(5, 20)
print(graph)
