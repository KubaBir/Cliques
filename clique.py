from generator import gen_graph


def is_clique(b):

    for i in range(1, b):
        for j in range(i + 1, b):

            # If any edge is missing
            if (graph.adjecency_matrix[store[i]][store[j]] == 0):
                return False

    return True


# Function to find all the cliques of size s
# l = number of current nodes
# s = size of wanted clique
# i = starting node
def findCliques(i, l, s):

    # Check if any vertices from i+1 can be inserted
    for j in range(i + 1, n - (s - l) + 1):

        # If the degree of the node is sufficient
        if (graph.degrees[j] >= s - 1):

            # Add the vertex to store
            store[l] = j

            # If the graph is not a clique of size k
            # then it cannot be a clique
            # by adding another edge
            if (is_clique(l + 1)):

                # If the length of the clique is
                # still less than the desired size
                if (l < s):

                    # Recursion to add vertices
                    findCliques(j, l + 1, s)

                # Size is met
                else:
                    print_cli(l + 1)


def nx_all_cliques(graph):
    index = []
    nbrs = []

    for node in graph.points:
        index[node] = len(index)
        nbrs[node] = {v for v in node.next if v not in index}


n = 5
graph = gen_graph(size, 50)
print(graph)
