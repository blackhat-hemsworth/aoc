class ElfList:
    sorted_list: list

    def __init__(self, random_list: list):
        self.sorted_list = sorted(random_list)

    def dist_list(self, other):
        return [abs(self_item - other_item) for self_item, other_item in zip(self.sorted_list, other.sorted_list)]

    def sim_score_list(self, other):
        return [self_item * other.sorted_list.count(self_item) for self_item in self.sorted_list]


jumble_left = []
jumble_right = []
with open("input.txt", "r") as f:
    for line in f.readlines():
        one, two = line.split("  ")
        jumble_left.append(int(one.strip()))
        jumble_right.append(int(two.strip()))

elf_list_left = ElfList(jumble_left)
elf_list_right = ElfList(jumble_right)

print(sum(elf_list_left.dist_list(elf_list_right)))
print(elf_list_left.sim_score_list(elf_list_right))
print(sum(elf_list_left.sim_score_list(elf_list_right)))
