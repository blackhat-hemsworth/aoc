class Rule:
    first: str
    last: str

    def __init__(self, order_str: str):
        self.first, self.last = order_str.split("|")

    def validate(self, input_str: str):
        if not (input_str.__contains__(self.first) and input_str.__contains__(self.last)):
            return True
        else:
            if input_str.index(self.first) > input_str.index(self.last):
                raise Rule.OutOfOrder(f"last came first for {self.first} {self.last}")

    def validate_list(self, input_list: list[str]):
        if not (self.first in input_list and self.last in input_list):
            return True
        else:
            if input_list.index(self.first) > input_list.index(self.last):
                raise Rule.OutOfOrder(f"last came first for {self.first}|{self.last}")

    class OutOfOrder(Exception):
        pass


class PrinterInput:
    input_pages: str
    input_page_list: list[str]
    middle: int

    def __init__(self, input_str: str):
        self.input_pages = input_str
        self.input_page_list = input_str.split(",")
        self.middle = int(self.input_page_list[int((len(self.input_page_list) - 1) / 2)])

    def print_attempt(self, print_rules: list[Rule]):
        for r in print_rules:
            r.validate(self.input_pages)
        return self.middle

    def print_attempt_with_generative_ai(self, print_rules: list[Rule]):
        print("starting: ", self.input_pages)
        while True:
            for r in print_rules: # sequential fix
                try:
                    r.validate(self.input_pages)
                except Rule.OutOfOrder:
                    print(f"flipping {r.first} & {r.last}")
                    self.flip_places(r.first, r.last)
                    print(self.input_pages)
            try: # make sure they all pass
                [r.validate(self.input_pages) for r in print_rules]
                break
            except Rule.OutOfOrder as e:
                pass

        return self.middle

    def flip_places(self, page_one: str, page_two: str):
        i1, i2 = self.input_page_list.index(page_one), self.input_page_list.index(page_two)
        self.input_page_list[i1], self.input_page_list[i2] = page_two, page_one
        self.input_pages = ",".join(self.input_page_list)
        self.middle = int(self.input_page_list[int((len(self.input_page_list) - 1) / 2)])


with open("input.txt","r") as f:
    full = f.read()

rule_str, print_str = full.split("\n\n")

rules = [Rule(line) for line in rule_str.split("\n")]
prints = [PrinterInput(line) for line in print_str.split("\n")]

middles = []
bad_prints = []
for p in prints:
    try:
        middles.append(p.print_attempt(rules))
    except Rule.OutOfOrder as e:
        print(p.input_pages)
        print(e)
        bad_prints.append(p)
print(sum(middles))
print(bad_prints)

print(sum([bad_print.print_attempt_with_generative_ai(rules) for bad_print in bad_prints]))


