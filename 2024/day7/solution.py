from itertools import chain


class Calibration():
    test_value = int
    input = tuple

    def __init__(self, test_value: int, int_input: tuple):
        self.test_value = test_value
        self.input = int_input

    def get_possibilities(self):
        round_input = [0]
        for i in self.input:
            round_input = list(chain.from_iterable((r + i, r * i, int(str(r) + str(i))) for r in round_input))
        round_input.remove(0)
        return round_input

    def calibrate(self):
        return self.test_value if self.test_value in self.get_possibilities() else 0


assert 190 in Calibration(190, (19,10)).get_possibilities()
assert 29 in Calibration(190, (19,10)).get_possibilities()
assert Calibration(3267, (81, 40, 27)).get_possibilities().count(3267) >= 2

with open("val.txt","r") as f:
    lines = f.readlines()

calibrations = [Calibration(int(line.split(":")[0]), (int(v) for v in line.split(":")[1].strip().split(" "))) for line in lines]
assert sum([calibration.calibrate() for calibration in calibrations]) == 11387

with open("input.txt", "r") as f:
    lines = f.readlines()

calibrations = [Calibration(int(line.split(":")[0]), (int(v) for v in line.split(":")[1].strip().split(" "))) for line in lines]

print(sum([calibration.calibrate() for calibration in calibrations]))
