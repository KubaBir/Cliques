from random import randint, sample


class Graph():
    n = 0
    adjecency_matrix = []
    points = []
    edges = []
    nedges = 0

    def __init__(self, n, saturation=50):
        self.n = n
        self.edges = []
        self.adjecency_matrix = [[0 for i in range(n)] for i in range(n)]
        # Generowanie n punktów w układzie współrzędnych
        self.points = [
            Point(i, randint(0, 100), randint(0, 100)) for i in range(n)]
        # Oblicza ilość krawędzi dla danego nasycenia podanego w procentach
        self.n_edges = int((n*(n-1)*saturation)/200)

        # Generowanie wszystkich możliwych krawędzi
        possible_edges = []
        for i in range(n):
            for j in range(i+1, n):
                possible_edges.append([i, j])

        # Wybieranie odpowiedniej ilości krawędzi
        edges = sample(possible_edges, self.n_edges)
        # Wpisanie krawędzi do grafu
        for edge in edges:
            # Tablica sąsiedztwa
            self.adjecency_matrix[edge[0]][edge[1]] = 1
            self.adjecency_matrix[edge[1]][edge[0]] = 1
            # Lista krawędzi
            self.edges.append((self.points[edge[0]], self.points[edge[1]]))

    def __str__(self):
        res = "Adjecency matrix:\n"
        res += "\n".join([f" {row}" for row in self.adjecency_matrix])
        # res += "\n\nSuccessor list:\n"
        # for point in self.points:
        #     res += f" {point}: ["
        #     for x in point.next:
        #         res += str(x) + ", "
        #     if point.next != []:
        #         res = res[:-2]

        # res += ']\n'
        # res += "\nDegrees:\n"
        # res += "\n".join([f" {id}: {d} " for id, d in enumerate(self.degrees)])

        return res + "\nAdjecancy list:\n " + str(self.edges) + "\n\n"

    def has_edge(self, u, v):
        if self.adjecency_matrix[u.id][v.id] == 1:
            return True
        return False

    def get_adj(self):
        print("--"*2*self.n)
        print("    ", end='')
        for c in range(self.n):
            print(c, '', end='')
        print()
        print('    ', end='')
        for c in range(self.n):
            print('- ', end='')
        print()
        for id, row in enumerate(self.adjecency_matrix):
            print(id, '|', *row)
        print("--"*2*self.n)


class Point:
    id = 0
    x = 0
    y = 0
    # next = []

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        # self.next = []

    def __str__(self):
        return str(self.id)

    def __repr__(self) -> str:
        return str(self.id)


def gen_graph(n, s=50):
    return Graph(n, s)
