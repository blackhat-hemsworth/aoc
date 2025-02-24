from collections import defaultdict


class Spot:
    x: int
    y: int
    options: list[tuple[int,int]]
    height: int

    def __init__(self, position: tuple[int,int], m: defaultdict):
        self.x, self.y = position
        self.height = m[position]
        self.options =  self._get_options(m)

    def _get_options(self, m: defaultdict):
        possibilities = [(-1, 0), (1,0), (0, -1), (0, 1)]
        return [possibility for possibility in possibilities if m.get((self.x + possibility[0], self.y + possibility[1]),[]) == self.height + 1]


def get_paths(s: Spot, d: defaultdict):
    cur_spots = {(s.x,s.y): s}
    paths = []
    while cur_spots:
        try:
            cur_spots = {path + (spot.x + option[0], spot.y + option[1]): d[spot.x + option[0], spot.y + option[1]] for path, spot in cur_spots.items() for option in spot.options}
        except Exception as e:
            print(e)
            break
        paths.extend([set(path) for path, spot in cur_spots.items() if spot.height == 9])

    return paths


def get_peaks(s: Spot, d: defaultdict):
    cur_spots = [s]
    peaks = []
    while cur_spots:
        try:
            cur_spots = [d[spot.x + option[0], spot.y + option[1]] for spot in cur_spots for option in spot.options]
        except Exception as e:
            print(e)
            break
        peaks.extend([spot for spot in cur_spots if spot.height == 9])

    return set(peaks)


with open("val.txt", "r") as f:
    flipped = [line.strip("\n") for line in f.readlines()[::-1]]
    top = defaultdict(str) | {(j, i): int(c) for i, r in enumerate(flipped)
                              for j, c in enumerate(r)}

top_spots = {k: Spot(k,top) for k, v in top.items()}
trailheads = {spot for k, spot in top_spots.items() if spot.height == 0}
print(trailheads)
print([len(get_paths(trailhead, top_spots)) for trailhead in trailheads])


assert (-1,0) in Spot((1,0), top).options

print([path for path in get_paths(top_spots[(2,7)], top_spots)])
print(len([path for path in get_paths(top_spots[(2,7)], top_spots)]))
assert sum([len(get_peaks(trailhead, top_spots)) for trailhead in trailheads]) == 36
assert sum([len(get_paths(trailhead, top_spots)) for trailhead in trailheads]) == 81

with open("input.txt", "r") as f:
    flipped = [line.strip("\n") for line in f.readlines()[::-1]]
    top = defaultdict(str) | {(j, i): int(c) for i, r in enumerate(flipped)
                              for j, c in enumerate(r)}

top_spots = {k: Spot(k,top) for k, v in top.items()}
trailheads = {spot for k, spot in top_spots.items() if spot.height == 0}
print(sum([len(get_paths(trailhead, top_spots)) for trailhead in trailheads]))
