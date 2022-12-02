import math
from functools import cmp_to_key
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


def get_convex_hullw(points):

    TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

    def turn(p, q, r):
        res = (q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1])
        if res == 0:
            return 0
        elif res > 0:
            return 1
        else:
            return 2

    def _keep_left(hull, r):
        while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
            hull.pop()
        if not len(hull) or hull[-1] != r:
            hull.append(r)
        return hull

    points = sorted(points)
    l = reduce(_keep_left, points, [])
    u = reduce(_keep_left, reversed(points), [])
    return l.extend(u[i] for i in range(1, len(u) - 1)) or l


def convex_hull(inp, n):
    def find_start(points):
        start = generator.Point(-1, 0, 0)
        miny, minx = 100, 100
        for point in points:
            if point.y == miny and point.x < minx:
                minx = point.x
                start = point
            elif point.y < miny:
                miny = point.y
                minx = point.x
                start = point

        p = []
        for x in points:
            p.append(x)
        return start, p

    def orientation(p, q, r):
        val = ((q.y - p.y) * (r.x - q.x) -
               (q.x - p.x) * (r.y - q.y))
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def distSq(p1, p2):
        return ((p1.x - p2.x) * (p1.x - p2.x) +
                (p1.y - p2.y) * (p1.y - p2.y))

    def compare(p1, p2):
        o = orientation(p0, p1, p2)
        if o == 0:
            if distSq(p0, p2) >= distSq(p0, p1):
                return -1
            return 1
        else:
            if o == 2:
                return -1
            return 1

    p0, points = find_start(inp)
    points = sorted(points, key=cmp_to_key(compare))
    m = 1
    for i in range(1, n):
        while ((i < n - 1) and
               (orientation(p0, points[i], points[i + 1]) == 0)):
            i += 1
            # nie dodawaj punktow wspoliniowych
        points[m] = points[i]
        m += 1
    if m < 3:
        return 0

    stack = []
    stack.append(points[0])
    stack.append(points[1])
    stack.append(points[2])

    for i in range(3, m):
        while ((len(stack) > 1) and
               (orientation(stack[-2], stack[-1], points[i]) != 2)):
            stack.pop()
        stack.append(points[i])

    for el in stack:
        print(el.x, el.y)

    return stack


def calculate_area(k, cliques):
    for clique in cliques:
        convex_hull(clique, k)


input_points = [(0, 3), (1, 1), (2, 2), (4, 4),
                (0, 0), (1, 2), (3, 1), (3, 3)]
points = []
for point in input_points:
    points.append(generator.Point(0, point[0], point[1]))
n = len(points)
calculate_area(n, [points])


# graph = generator.gen_graph(6, 80)
# for k, cliques in get_cliques(graph):
#     calculate_area(k, cliques)
# print(*cliques)
# print(cliques[0])
# for el in cliques[0]:
#     print(el.x)
