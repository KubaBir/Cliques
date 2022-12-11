from functools import cmp_to_key
from itertools import combinations

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
        cliques = [set(item)
                   for item in set(frozenset(item) for item in cliques)]

        k += 1


def get_cliques(graph):
    # graph.get_adj()
    for k, cliques in k_cliques(graph):
        if k > 2:
            # print('%d-cliques = %d, %s.' % (k, len(cliques), cliques))
            yield k, cliques


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

    # for el in stack:
    #     print(el.x, el.y)

    return stack


def calculate_area(k, kcliques):
    for clique in kcliques:
        hull = convex_hull(clique, k)
        area = 0
        for i in range(len(hull) - 1, -1, -1):
            area += hull[i-1].x * hull[i].y - hull[i].x * hull[i-1].y
        area = area/2
        yield clique, hull, area


n = 10
graph = generator.gen_graph(n, 80)
cliques = get_cliques(graph)

f = open("results.txt", "w")
f.write("Ilosci k-klik:\n")

results = []
for k, kcliques in cliques:
    print(k, ": ", len(kcliques), sep='')
    f.write(str(k) + ": " + str(len(kcliques)) + "\n")
    x = calculate_area(k, kcliques)
    for i in x:
        results.append(i)
results.sort(key=lambda x: x[2])
for item in results:
    print(*item)

f.write("\nWyniki w formacie (klika, otoczka, pole):\n")
for item in results:
    f.write(str(item)+"\n")
f.close()
