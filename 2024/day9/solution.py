class DiskMap:
    initial_dm: str
    blocks: list[str] # string of DIGITS to storage system for numbers!

    def __init__(self, input_str: str):
        self.initial_dm = input_str
        self.blocks = [x for xs in [['.'] * int(c) if i % 2 else [i // 2] * int(c)
                       for i,c in enumerate(input_str)] for x in xs]

        blocks = self.blocks.copy()
        for i in [i for i, item in enumerate(blocks) if item == '.']:
            while blocks[-1] == '.':
                blocks.pop()
            try:
                if i >= len(blocks) - 1:
                    print(i, len(blocks))
                    break
                blocks[i] = blocks.pop()
            except Exception as e:
                print(e)
                print(i, len(blocks))
                break
        self.compact = blocks
        self.checksum = sum([i * c for i, c in enumerate(self.compact) if c != '.'])

        new_blocks = self.blocks.copy()
        for file_id in list(reversed(sorted(set([b for b in new_blocks if b != '.'])))):
            string_rep = ''.join(['1' if b == '.' else '0' for b in new_blocks])
            num_blocks = new_blocks.count(file_id)
            spaces_needed = new_blocks.count(file_id) * len(str(file_id))
            # print(file_id, new_blocks.count(file_id))
            # print(string_rep)
            idx = string_rep.find('1' * num_blocks)
            if 0 <= idx <= new_blocks.index(file_id):
                new_blocks = ['.' if b == file_id else b for b in new_blocks]
                new_blocks[idx:(idx + num_blocks)] = [file_id] * num_blocks
                # print(new_blocks[idx:(idx + spaces_needed)])
                # print(idx, file_id)

        self.compact_defrag = new_blocks
        self.checksum_defrag = sum([i * c for i, c in enumerate(self.compact_defrag) if c != '.'])


print(DiskMap('12345').compact)
#assert DiskMap('12345').blocks == ['0', '.', '.', '1', '1', '1', '.', '.', '.', '.', '2', '2', '2', '2', '2']
#assert DiskMap('12345').compact == list('022111222')
print(DiskMap('12345').checksum)

with open("val.txt","r") as f:
    input_string = f.read()

print(DiskMap(input_string).blocks)
print(DiskMap(input_string).compact)
print(DiskMap(input_string).checksum)
assert DiskMap(input_string).checksum == 1928
assert DiskMap(input_string).checksum_defrag == 2858

with open("input.txt", "r") as f:
    input_string = f.read().strip()

dm = DiskMap(input_string)

print(dm.compact_defrag[:100])
print(dm.blocks[:100])
print(dm.blocks[-100:])
print(dm.checksum_defrag)