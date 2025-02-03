class LockKey:
    s : str
    t : tuple

    def __init__(self, text_block: str):
        self.s = text_block
        self.t = tuple([[row[i] for row in text_block.split("\n")].count("#") - 1 for i in range(5)])

    def matches(self, other):
        return max(tuple(pin + peg for pin, peg in zip(self.t, other.t))) <= 5


with open("input.txt", "r") as input_file:
    item_list = input_file.read().split("\n\n")

keys = [LockKey(item) for item in item_list if item[:5] == r'.....']
locks = [LockKey(item) for item in item_list if item[:5] == r'#####']

print(len(keys), len(locks))
print(sum([sum(item) for item in [[key.matches(lock) for lock in locks] for key in keys]]))