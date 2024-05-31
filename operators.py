from graph import Node, Graph


class Conv(Node):
    def __init__(self) -> None:
        super().__init__()


class Relu(Node):
    def __init__(self) -> None:
        super().__init__()


class Maxpool(Node):
    def __init__(self) -> None:
        super().__init__()


class Concat(Node):
    def __init__(self) -> None:
        super().__init__()


class MemAccess(Node):
    def __init__(self, tensor_id: int) -> None:
        super().__init__()
        self.tensor_id = tensor_id


class Load(MemAccess):
    def __init__(self, tensor_id: int) -> None:
        super().__init__(tensor_id)


class Store(MemAccess):
    def __init__(self, tensor_id: int) -> None:
        super().__init__(tensor_id)


class Malloc(MemAccess):
    def __init__(self, tensor_id: int) -> None:
        super().__init__(tensor_id)


class Free(MemAccess):
    def __init__(self, tensor_id: int) -> None:
        super().__init__(tensor_id)


class Tensor(Node):
    def __init__(self, name: str = '', size: int = 0) -> None:
        super().__init__()
        self.name = name
        self.size = size


if __name__ == "__main__":
    # the first inception block of GoogLeNet
    g = Graph()
    fork_node = g.add_node(Maxpool())
    start1, *_, end1 = g.add_sequence(Conv(), Relu())
    start2, *_, end2 = g.add_sequence(Conv(), Relu(), Conv(), Relu())
    start3, *_, end3 = g.add_sequence(Conv(), Relu(), Conv(), Relu())
    start4, *_, end4 = g.add_sequence(Maxpool(), Conv(), Relu())
    join_node = g.add_node(Concat())
    g.link_all_pairs([fork_node], [start1, start2, start3, start4])
    g.link_all_pairs([end1, end2, end3, end4], [join_node])
    print(g)
    g.draw()
