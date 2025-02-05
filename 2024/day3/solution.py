import re  # cheating but not doing this one without regex


class Multiplier:  # this is very stupid
    product: int
    multiplicand: int
    multiplier: int

    def __init__(self, junk_string: str):
        self.multiplicand = int(junk_string.split(",")[0].split("(")[1])
        self.multiplier = int(junk_string.split(",")[1].split(")")[0])
        self.product = self.multiplicand * self.multiplier


with open("input.txt", "r") as f:
    muls = re.findall(r"mul\(.{1,3},.{1,3}\)", f.read())

print(sum([Multiplier(mul).product for mul in muls]))

with open("input.txt", "r") as f:
    junk = f.read()

junk_list = junk.split("don't()")

do_nots = re.findall(r"(don't\(\))((.|\n)*?)(do\(\)|\Z)", junk)  # vile
print(do_nots)
for do_not in do_nots:
    junk = junk.replace(do_not[1], "")  # dumb

new_muls = re.findall(r"mul\(.{1,3},.{1,3}\)", junk)
print(sum([Multiplier(mul).product for mul in new_muls]))
