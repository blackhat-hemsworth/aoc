import itertools
from collections import defaultdict
from math import gcd


class Node:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __add__(self, other):
        if isinstance(other, tuple):
            return Node(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        if isinstance(other, tuple):
            return Node(self.x - other[0], self.y - other[1])

    def get_vector_to(self, other) -> tuple[int, int]:
        return other.x - self.x, other.y - self.y

    def get_unit_vector_to(self, other) -> tuple[int, int]:
        g = gcd(other.x - self.x, other.y - self.y)
        return int((other.x - self.x)/g), int((other.y - self.y)/g)


class RadarMap:
    max_x: int
    max_y: int

    def __init__(self, max_x: int, max_y: int):
        self.max_x, self.max_y = max_x, max_y

    def _get_antinode_pair(self, node_1: Node, node_2: Node) -> set:
        v = node_1.get_vector_to(node_2)
        return {node_1 - v, node_2 + v}

    def _get_antinode_vector(self, node_1: Node, node_2: Node) -> set:
        v = node_1.get_unit_vector_to(node_2)
        s = set()

        for node in node_1, node_2:
            for dir in -1, 1:
                new_node = node
                while self._inbounds(new_node):
                    s.add(new_node)
                    new_node += (v[0] * dir, v[1] * dir)

        return s

    def _inbounds(self, node: Node):
        return True if 0 <= node.x <= self.max_x and 0 <= node.y <= self.max_y else False

    def get_antinodes(self, node_list: list[Node]):
        antinodes = set()
        for node_1, node_2 in itertools.combinations(node_list, 2):
            antinodes.update(self._get_antinode_vector(node_1, node_2))

        return {a for a in antinodes if self._inbounds(a)}


assert RadarMap(99,98)._get_antinode_pair(Node(1,1),Node(1,2)) == {Node(1, 0), Node(1, 3)}
assert RadarMap(99,98).max_x == 99
assert RadarMap(99,98).max_y == 98
print([vars(item) for item in RadarMap(2,2).get_antinodes([Node(1,1),Node(1,2)])])
assert RadarMap(2,2).get_antinodes([Node(1,1),Node(1,2)]) == {Node(1, 0), Node(1, 2), Node(1, 1)}
assert Node(1,2).get_unit_vector_to(Node(4,5)) == (1,1)
assert Node(1,2).get_unit_vector_to(Node(4,8)) == (1,2)
print(RadarMap(32,12).get_antinodes([Node(1,1),Node(1,2)]))

with open("val.txt","r") as f:
    flipped = [line.strip("\n") for line in f.readlines()[::-1]]
    dd = defaultdict(str) | {(j,i): c for i, r in enumerate(flipped)
                                      for j, c in enumerate(r)}

print(list(dd.keys())[-1] )
radar_map = RadarMap(*list(dd.keys())[-1])

frequencies = set(dd.values())
frequencies.remove(".")
print(frequencies)

node_dict = dict()
node_dict["antinodes"] = set()
for frequency in frequencies:
    node_dict[frequency] = [Node(x, y) for x, y in dd if dd[x, y] == frequency]
    node_dict["antinodes"].update(radar_map.get_antinodes(node_dict[frequency]))

assert len(node_dict["antinodes"]) == 34

with open("input.txt", "r") as f:
    flipped = [line.strip("\n") for line in f.readlines()[::-1]]
    dd = defaultdict(str) | {(j, i): c for i, r in enumerate(flipped)
                             for j, c in enumerate(r)}

print(list(dd.keys())[-1])
radar_map = RadarMap(*list(dd.keys())[-1])

frequencies = set(dd.values())
frequencies.remove(".")
print(frequencies)

node_dict = dict()
node_dict["antinodes"] = set()
for frequency in frequencies:
    node_dict[frequency] = [Node(x, y) for x, y in dd if dd[x, y] == frequency]
    node_dict["antinodes"].update(radar_map.get_antinodes(node_dict[frequency]))

# print([vars(a) for a in node_dict["antinodes"]])
print(len(node_dict["antinodes"]))