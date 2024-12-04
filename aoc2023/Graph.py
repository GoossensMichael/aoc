from collections import namedtuple
from copy import deepcopy

# Graph model
# Contains a list of vertices and a dictionary mapping a vertex to another one along with a weight for the edge.
# The vertices are considered strings
# Edge = namedtuple("Edge", "v w weight")
# Graph = namedtuple("Graph", "V E")

class Edge:

    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight


class Graph:

    def __init__(self, V, E):
        self.V = V
        self.E = E


def most_tightly_connected_vertex():
    pass

# Assumes that the Graph is undirected (An edge must be defined twice, once in each direction!)
def minimum_cut_phase(G, a):
    # Init A set with chosen vertex
    # Init E as a map containing all edges and weights that go from vertex 'a' to outside of set A.
    A = set([a])
    E = {(e.v, e.w): e.weight for e in G.E if e.v == a}
    # Map of all vertices outside A connected to A.
    C_E = {e.w: (e.v, e.w) for e in G.E if e.v == a}

    while A != G.V:
        # Get the most tightly connected vertex. This will be 't'.
        s, t = max(E, key=E.get)
        # Update E by removing the used edge and adding all edges now connected from t to any vertex outside A.
        for e in G.E:
            if e.v == t and e.w not in A:
                if e.w in C_E:
                    E[(C_E[e.w][0], C_E[e.w][1])] += e.weight
                else:
                    C_E[e.w] = (e.v, e.w)
                    E[(e.v, e.w)] = e.weight

        min_cut = E[(s, t)]
        del E[(s, t)]
        del C_E[t]
        min_phase = A.copy()
        A.add(t)

    # Adjust graph by merging s and t together
    G.V.remove(s)
    G.V.remove(t)
    st = "_".join((s, t))
    G.V.add(st)

    # Merge two last nodes together
    E_ = set()
    st_map = {}
    for e in G.E:
        if e.v not in (s, t) and e.w not in (s, t):
            E_.add(Edge(e.v, e.w, e.weight))
        elif e.v in (s, t) and e.w not in (s, t):
            if e.w not in st_map:
                st_map[e.w] = 0
            st_map[e.w] += e.weight
    for vw, weight in st_map.items():
        E_.add(Edge(st, vw, weight))
        E_.add(Edge(vw, st, weight))
    G.E = E_

    return min_cut, min_phase

def minimum_cut(G):
    G_ = deepcopy(G)
    a = next(iter(G_.V))

    c_min_cut = None
    c_min_phase = None
    while len(G_.V) > 1:
        min_cut, min_phase = minimum_cut_phase(G_, a)
        if c_min_cut == None or c_min_cut < min_cut:
            c_min_cut = min_cut
            c_min_phase = min_phase

    return c_min_cut, c_min_phase
