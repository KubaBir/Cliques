from random import randint, sample


class Graph():
    n = 0
    # saturation in percent
    adjecency_matrix = []
    points = []

    def __init__(self, n, saturation=50):
        self.n = n
        self.adjecency_matrix = [[0 for i in range(n)] for i in range(n)]
        self.points = [
            Point(i, randint(0, 100), randint(0, 100)) for i in range(n)]
        temp = []
        edges = int((n*(n-1)*saturation)/200)
        for i in range(n):
            for j in range(i+1, n):
                temp.append([i, j])
        temp = sample(temp, edges)
        # print(temp)
        for i in temp:
            self.adjecency_matrix[i[0]][i[1]] = 1
            self.points[i[0]].next.append(self.points[i[1]])
            self.adjecency_matrix[i[1]][i[0]] = 1
            self.points[i[1]].next.append(self.points[i[0]])

    def __str__(self):
        res = "Adjecency matrix:\n"
        res += "\n".join([f" {row}" for row in self.adjecency_matrix])
        res += "\nSuccessor list:\n"
        for point in self.points:
            res += f" {point}: ["
            for x in point.next:
                res += str(x) + ", "
            if point.next != []:
                res = res[:-2]

            res += ']\n'

        return res


class Point:
    id = 0
    x = 0
    y = 0
    next = []

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.next = []

    def __str__(self):
        return str(self.id)


def gen_graph(n, s=50):
    return Graph(n, s)
# print(*graph.adjecency_matrix, sep='\n')
