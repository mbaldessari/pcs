import sys

class Graph(object):
    def __init__(self, graph_attributes=None):
        self.__graph = {}
        self.__graph_attributes = graph_attributes
        self.__vertex_attributes = {}
        self.__edge_attributes = {}

    def vertices(self):
        vertices = set(self.__graph.keys())
        for i in self.__graph:
            for j in xrange(len(self.__graph[i])):
                vertices.add(self.__graph[i][j])
        return list(vertices)

    def edges(self):
        edges = []
        for vertex in self.__graph:
            for neighbour in self.__graph[vertex]:
                if tuple([vertex, neighbour]) not in edges:
                    edges.append(tuple([vertex, neighbour]))
        return edges

    def add_vertex(self, vertex, attributes=None):
        if vertex not in self.__graph:
            self.__graph[vertex] = []
            self.__vertex_attributes[vertex] = attributes

    def add_edge(self, vertex1, vertex2=None, edge_attrs=None,
                 v1_attrs=None, v2_attrs=None):
        if not vertex2: # A loop towards itself
            vertex2 = vertex1
        if vertex1 in self.__graph:
            self.__graph[vertex1].append(vertex2)
        else:
            self.__graph[vertex1] = [vertex2]

        # Set vertex and edge attributes
        if vertex1 not in self.__vertex_attributes:
            self.__vertex_attributes[vertex1] = v1_attrs
        else:
            self.__vertex_attributes[vertex1].update(v1_attrs)

        if vertex2 not in self.__vertex_attributes:
            self.__vertex_attributes[vertex2] = v2_attrs
        else:
            self.__vertex_attributes[vertex2].update(v2_attrs)

        index = tuple([vertex1, vertex2])
        self.__edge_attributes[tuple([vertex1, vertex2])] = edge_attrs

    def subgraph(self, vertex):
        """Returns the subgraph of all the edges and vertexes reachabled
        from 'vertex'
        """
        subgraph = Graph(self.__graph_attributes)
        for edge in self.edges():
            pass


    def get_graph_attributes(self):
        if self.__graph_attributes:
            return self.__graph_attributes
        return ""

    def get_vertex_attributes(self, vertex):
        if vertex in self.__vertex_attributes:
            return self.__vertex_attributes[vertex]
        return ""

    def get_edge_attributes(self, vertex1, vertex2):
        index = tuple([vertex1, vertex2])
        if index in self.__edge_attributes:
            return self.__edge_attributes[index]
        return ""

    def __dict_to_dot(self, d):
        s = ""
        for i in d:
            s = s + "%s=\"%s\", " % (i, d[i])
        s = s.rstrip(', ')
        return "[%s];" % s

    def todot(self, output=None, title=""):
        with open(output, 'w+') if output else sys.stdout as fd:
            print >>fd, 'digraph %s {' % title
            print >>fd, '%s' % self.get_graph_attributes()
            for vertex in self.vertices():
                print >>fd,  '\"%s\" %s' % (vertex, self.__dict_to_dot(self.get_vertex_attributes(vertex)))
            for edge in self.edges():
                l = list(edge)
                if len(l) > 1:
                    attr = self.__dict_to_dot(self.get_edge_attributes(l[0], l[1]))
                    print >>fd, '\"%s\" -> \"%s\" %s' % (l[0], l[1], attr)
                else:
                    attr = self.__dict_to_dot(self.get_edge_attributes(l[0], l[0]))
                    print >>fd, '\"%s\" -> \"%s\" %s' % (l[0], l[0], attr)
            print >>fd, '}'

if __name__ == "__main__":
    graph = Graph()
    graph.add_edge("a", "x")
    print(graph.vertices())
    graph.todot()
