from random import randint, sample


class Graph():
    n = 0
    # saturation in percent
    adjecency_matrix = []
    points = []
    # degrees = []
    edges = []
    nedges = 0

    def __init__(self, n, saturation=50):
        self.n = n
        self.adjecency_matrix = [[0 for i in range(n)] for i in range(n)]
        self.points = [
            Point(i, randint(0, 100), randint(0, 100)) for i in range(n)]
        # self.degrees = [0 for _ in range(n)]
        temp = []
        self.nedges = int((n*(n-1)*saturation)/200)
        self.edges = []
        for i in range(n):
            for j in range(i+1, n):
                temp.append([i, j])
        temp = sample(temp, self.nedges)

        for i in temp:
            self.adjecency_matrix[i[0]][i[1]] = 1
            self.adjecency_matrix[i[1]][i[0]] = 1
            # self.points[i[1]].degree += 1
            # self.points[i[0]].degree += 1
            # self.degrees[i[0]] += 1
            # self.degrees[i[1]] += 1
            # self.points[i[0]].next.append(self.points[i[1]])
            # self.points[i[1]].next.append(self.points[i[0]])

        for row_id, row in enumerate(self.adjecency_matrix):
            for el_id, el in enumerate(row):
                if el == 1:
                    self.edges.append(
                        (self.points[row_id], self.points[el_id]))

    def __str__(self):
        res = "Adjecency matrix:\n"
        res += "\n".join([f" {row}" for row in self.adjecency_matrix])
        res += "\n\nSuccessor list:\n"
        for point in self.points:
            res += f" {point}: ["
            for x in point.next:
                res += str(x) + ", "
            if point.next != []:
                res = res[:-2]

            res += ']\n'
        res += "\nDegrees:\n"
        res += "\n".join([f" {id}: {d} " for id, d in enumerate(self.degrees)])

        return res

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
# print(*graph.adjecency_matrix, sep='\n')
