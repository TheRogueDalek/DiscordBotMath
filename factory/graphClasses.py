import math

LABELS = {'C': 'Customer', 'F': 'Factory', 'M': 'Mail Station', 'P': 'Potential Factory'}


class Vertex:

    def __init__(self, label_type, name):
        Vertex.check_type(label_type, name)
        self.type = label_type.upper()
        self.name = name
        self.distanceValue = float('inf')

    # TODO: May have to make this use '<' instead of '<=', but changes behavior
    def __lt__(self, other):
        return self.distanceValue <= other.distanceValue

    def __repr__(self):
        return LABELS[self.type] + ": " + self.name + " " + str(self.distanceValue)

    @staticmethod
    def check_type(potential_type, potential_name):
        if potential_type.upper() not in LABELS.keys():
            raise TypeError("Not a valid type for vertex ", potential_name)


class Edge:
    def __init__(self, vertex1: Vertex, vertex2: Vertex, cost=0.0):
        if not Edge.is_valid_pairing(vertex1, vertex2):
            v1_full, v2_full = LABELS[vertex1.type], LABELS[vertex2.type]
            exception_str = "Locations of types {} and {} cannot be directly connected".format(v1_full, v2_full)
            raise TypeError(exception_str)

        # Store a set to allow edge's vertices to be referenced in either order
        self.pair = {vertex1.name, vertex2.name}
        self.cost = cost

    @staticmethod
    def is_valid_pairing(first: Vertex, second: Vertex):
        pairing = {first.type, second.type}
        # Mail stations can connect to any other location
        if 'M' in pairing:
            return True
        elif len(pairing) == 1:
            # No other pair of vertices can have the same type
            # That is, customers can't deliver to each other
            # Factories can't connect to each other, etc.
            return False
        elif 'C' in pairing:
            # Can connect to F or P
            return True
        elif 'F' in pairing and 'P' in pairing:
            # Factories cannot directly connect to potential factories
            return False

    def __repr__(self):
        return "|" + str(self.pair) + ", with transport cost " + str(self.cost) + "|"

    def __lt__(self, other):
        return self.cost < other.cost


class Graph:
    def __init__(self, vertices: dict, edges: set):
        self.vertices = vertices
        self.edges = edges

        # The lookup dictionary generated maps strings combining
        # the names of an edge's vertices to the edges themselves
        # E.g. an edge e1, connect vertices with names a and b,
        # would be stored in this dictionary as lookup[a_b] = e1

        # TODO: Need a function to take in vertex names and return hashable string in correct order
        #  i.e. if vertices' names are given as (b,a), the string key should still be a_b
        self.lookup = self.create_edge_lookup()
        self.alt_lookup = self.alt_lookup_creation()

    # Create lookup dictionary for finding edges given a string representing end vertices
    def create_edge_lookup(self):
        ret_dict = dict()
        for edge in self.edges:
            v1, v2 = tuple(edge.pair)
            ret_dict[str(v1 + "_" + v2)] = edge
            ret_dict[str(v2 + "_" + v1)] = edge
            edge_vertices = edge.pair
            name_hash = "_".join(edge_vertices)
            # ret_dict[name_hash] = edge
        return ret_dict

    def alt_lookup_creation(self):
        ret_dict = dict()
        for edge in self.edges:
            v1, v2 = tuple(edge.pair)

            if v1 not in ret_dict.keys():
                ret_dict[v1] = dict()
            if v2 not in ret_dict.keys():
                ret_dict[v2] = dict()

            ret_dict[v1][v2] = float(edge.cost)
            ret_dict[v2][v1] = float(edge.cost)
        return ret_dict

    def getNeighboringNodes(self, aNode):
        # Linear search to get list of all nodes adjacent to a given node. Quick and dirty implementation since I just
        # need it done to move forward. To be improved later.
        if aNode.name not in self.vertices:
            raise TypeError('Given vertex not present in this graph.')
        neighborNodes = []
        for edge in self.edges:
            # Get set difference - if it is size 1, the edge contains aNode and we should add the other node.
            setDif = edge.pair - {aNode.name}
            if len(setDif) == 1:
                neighborNodes.append(self.vertices[setDif.pop()])

        return neighborNodes

    def resetDistances(self):
        for name in self.vertices:
            vertex = self.vertices[name]
            # TODO: Create Vertex member function to reset distanceValue
            vertex.distanceValue = math.inf


if __name__ == '__main__':
    vert1 = Vertex('C', 'Athreya')
    vert2 = Vertex('M', 'UPS_Store')
    vert3 = Vertex('F', 'Bakersfield_Factory')
    vert4 = Vertex('P', 'Newtown_Factory_potential')
    vertex_set = {vert1, vert2, vert3, vert4}
    vertices_dict = dict()
    for v in vertex_set:
        vertices_dict[v.name] = v

    e1 = Edge(vert1, vert2)
    e2 = Edge(vert2, vert3)
    e3 = Edge(vert1, vert3)
    edges = {e1, e2, e3}

    g = Graph(vertices_dict, edges)
    print(g.alt_lookup)