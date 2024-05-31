import sys
from typing import Iterable

import networkx as nx
import matplotlib.pyplot as plt


class Node(object):
    cnt: int = 0

    def __init__(self) -> None:
        self.id = Node.cnt
        Node.cnt += 1

    def __str__(self) -> str:
        return f"{self.__class__.__name__}:{self.id}"


class Graph(object):
    def __init__(self, *nodes: Iterable[Node]) -> None:
        self.nodes: dict[int:Node] = {} if nodes is None else {i.id: i for i in nodes}
        self.adj: dict[Node: list[Node]] = {} if nodes is None else {i: [] for i in nodes}

    def __str__(self) -> str:
        res = f"{", ".join((str(i) for i in self.nodes.values()))}\n\n"
        for k, v in self.adj.items():
            res += f"{k} -> {", ".join([str(i) for i in v])}\n"
        return res

    def __getitem__(self, idx: int) -> Node:
        return self.nodes[idx]

    def __call__(self, idx: int) -> list[Node]:
        return self.adj[self.nodes[idx]]

    def add_node(self, node: Node) -> int:
        if node.id not in self.adj.keys():
            self.nodes[node.id] = node
            self.adj[node] = []
        return node.id

    def add_edge(self, id_from: int, id_to: int) -> None:
        self.adj[self.nodes[id_from]].append(self.nodes[id_to])

    def add_nodes(self, *nodes: Iterable[Node]) -> list[int]:
        return [self.add_node(node) for node in nodes]

    def add_edges(self, *edges: tuple[int, int]) -> None:
        for edge in edges:
            self.add_edge(*edge)

    def link_sequence(self, node_ids: Iterable[int]) -> list[int]:
        self.add_edges(*zip(node_ids, node_ids[1:]))
        return node_ids

    def link_all_pairs(self, src_ids: Iterable[int], dst_ids: Iterable[int]) -> None:
        for src in src_ids:
            for dst in dst_ids:
                self.add_edge(src, dst)

    def add_sequence(self, *nodes: Iterable[Node]) -> list[int]:
        return self.link_sequence(self.add_nodes(*nodes))

    def draw(self) -> None:
        graph = nx.DiGraph()
        for node in self.nodes.values():
            graph.add_node(f'{node}')
        for src, edges in self.adj.items():
            for dst in edges:
                graph.add_edge(f'{src}', f'{dst}')

        nx.draw(graph, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', font_size=15, font_color='black')
        plt.show()


def test_plot():
    G = nx.DiGraph()
    G.add_node(1)
    G.add_node('S')
    G.add_node(3)
    G.add_node(4)
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', font_size=15, font_color='black')
    plt.show()


def test1():
    """
       0
     / |
    1  |
     \\ |
       2
    """
    g = Graph(Node(), Node())
    g.add_node(Node())
    g.add_edge(0, 1)
    g.add_edges((0, 2), (1, 2))
    print(g)
    return g


def test2():
    """
    3 -> 4 -> 5 -> 6 -> 7
    """

    g = Graph()
    idx = g.add_nodes(Node(), Node(), Node(), Node(), Node())
    g.link_sequence(idx)
    print(g)
    return g


def test3():
    """
         8
        / \\
       9   12
       |   |
       10  13
       |   |
       11  14
        \\ /
         15
    """
    g = Graph()
    n0 = g.add_node(Node())
    s1 = g.add_sequence(Node(), Node(), Node())
    s2 = g.add_sequence(Node(), Node(), Node())
    n3 = g.add_node(Node())
    g.add_edges((n0, s1[0]), (s1[-1], n3), (n0, s2[0]), (s2[-1], n3))
    print(g)
    return g


def test4():
    """
    16  17  18
     \\  |   /
       \\| /
        19
       /|\\
      / |  \\
    20  21  22
    """
    g = Graph()
    block1 = g.add_nodes(Node(), Node(), Node())
    block2 = g.add_nodes(Node())
    block3 = g.add_nodes(Node(), Node(), Node())
    g.link_all_pairs(block1, block2)
    g.link_all_pairs(block2, block3)
    print(g)
    return g



if __name__ == "__main__":
    tests = [test1, test2, test3, test4]
    if len(sys.argv) == 1:
        print(f'Usage: python3 {sys.argv[0]} <1~4>')
    else:
        g = tests[int(sys.argv[1]) - 1]()
        # g.draw()
