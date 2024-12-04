import Graph

import Utils
from aocd import submit

day = 25
year = 2023
p1_expected_tst_result = 54
p2_expected_tst_result = -1

Utils.download_input(year, day)


class Vertex:

    def __init__(self, name):
        self.name = name
        self.edge = set()

    def add_connection(self, connection):
        self.edge.add(connection)


def create_vertex_if_not_exists(nodes, node_name):
    if node_name not in nodes:
        nodes[node_name] = Vertex(node_name)


def parse_data(data):
    graph = {}
    for d in data:
        vertex, connected_vertices = d.split(": ")
        create_vertex_if_not_exists(graph, vertex)

        for c_vertex in connected_vertices.split():
            create_vertex_if_not_exists(graph, c_vertex)
            graph[vertex].edge.add(graph[c_vertex])
            graph[c_vertex].edge.add(graph[vertex])

    V = set()
    E = set()
    for v in graph.values():
        V.add(v.name,)
        for w in v.edge:
            E.add(Graph.Edge(v.name, w.name, 1))
    G = Graph.Graph(V, E)

    return G


def solve(data):
    graph = parse_data(data)

    V = set(["a", "b", "c", "d", "e", "f"])
    E = set([Graph.Edge("a", "b", 5), Graph.Edge("b", "a", 5),
             Graph.Edge("a", "f", 4), Graph.Edge("f", "a", 4),
             Graph.Edge("a", "e", 1), Graph.Edge("e", "a", 1),
             Graph.Edge("b", "c", 2), Graph.Edge("c", "b", 2),
             Graph.Edge("c", "d", 6), Graph.Edge("d", "c", 6),
             Graph.Edge("c", "e", 1), Graph.Edge("e", "c", 1),
             Graph.Edge("d", "e", 3), Graph.Edge("e", "d", 3),
             Graph.Edge("c", "f", 1), Graph.Edge("f", "c", 1),
             ])
    graph = Graph.Graph(V, E)

    result = Graph.minimum_cut(graph)



    run_throughs = []
    global_visited = set()
    for node in graph.values():
        if node not in global_visited:
            to_visit = node.edge
            visited = set()
            while len(to_visit) > 0:
                nxt = to_visit.pop()
                visited.add(nxt)
                to_visit |= nxt.edge.difference(visited)
            global_visited |= visited
            run_throughs.append(visited)

    return 0


if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

    print("Part 1")
    p1_tst_result = solve(tst_input)
    print(f"Test solution: {p1_tst_result}.")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        p1_result = solve(puzzle_input)
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    p2_tst_result = solve(tst_input)
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        p2_result = solve(puzzle_input)
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
