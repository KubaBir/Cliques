from functools import cmp_to_key
from itertools import combinations
from time import time

import generator


def k_cliques(graph):
    cliques = []
    # Poczatkowa lista klik składa się z każdych dwóch połączonych wierzchołków
    for edge in graph.edges:
        cliques.append({edge[0], edge[1]})
    k = 2
    print(len(cliques))

    while cliques:
        yield k, cliques

        # Wyznacz wszystkie możliwe "scalone" kliki
        cliques_1 = set()
        for u, v in combinations(cliques, 2):
            # w = Wierzchołki należące do tylko jednej z klik
            w = u ^ v
            # Jeśli sa takie dokładnie 2, oraz są one połączone, tworzą nową klikę
            if len(w) == 2 and graph.has_edge(*w):
                cliques_1.add(tuple(u | w))

        # Usuwanie zduplikowanych klik
        cliques = set(list(map(frozenset, cliques_1)))
        k += 1


def get_cliques(graph):
    for k, cliques in k_cliques(graph):
        if k > 2:
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

    # Wyznacz pierwszy element otoczki (najmniejsze y oraz x) O(n)
    p0, points = find_start(inp)
    # Posortuj wierzchołki wg. kąta który tworzą z p0 i osią X (rosnąco) O(n^2)
    points = sorted(points, key=cmp_to_key(compare))

    m = 1
    # Pomiń punkty współliniowe O(n)
    for i in range(1, n):
        while ((i < n - 1) and (orientation(p0, points[i], points[i + 1]) == 0)):
            i += 1
        points[m] = points[i]
        m += 1

    res = []
    # Pierwszy wierzchołek z góry jest dobry
    res.append(points[0])
    # Ustawiamy wartość początkową kolejnych dwóch - zostaną one ewentualnie zmienione
    res.append(points[1])
    res.append(points[2])

    for i in range(3, m):
        # Jeśli mamy skręt w prawo, ostatni wierzchołek nie należy do otoczki
        while ((len(res) > 1) and (orientation(res[-2], res[-1], points[i]) != 2)):
            res.pop()
        res.append(points[i])

    return res


def calculate_area(k, kcliques):
    for clique in kcliques:
        hull = convex_hull(clique, k)
        area = 0
        for i in range(len(hull) - 1, -1, -1):
            area += hull[i-1].x * hull[i].y - hull[i].x * hull[i-1].y
        area = area/2
        yield clique, hull, area


n = 100
graph = generator.gen_graph(n, 30)
start = time()

cliques = get_cliques(graph)

f = open("results.txt", "w")
f.write("Ilosci k-klik:\n")
# print(graph)
results = []
for k, kcliques in cliques:
    print(k, ": ", len(kcliques), sep='')
    f.write(str(k) + ": " + str(len(kcliques)) + "\n")
    x = calculate_area(k, kcliques)
    for i in x:
        results.append(i)
print(len(results))
results.sort(key=lambda x: x[2], reverse=True)

print("\nRanking:")
for i in range(min(len(results), 10)):
    print(i+1)
    print(" Klika:", *results[i][0])
    print(" Otoczka:", *results[i][1])
    print(" Pole:", results[i][2])


f.write("\nWyniki w formacie (klika, otoczka, pole):\n")
for item in results:
    f.write(str(item)+"\n")
f.close()
print(time()-start)
