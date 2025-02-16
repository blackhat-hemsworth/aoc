from math import sin, cos, pi
from collections import defaultdict
import asyncio
from unittest.mock import inplace


def rotate(vector: tuple[int,int], degrees: int = 90) -> tuple:
    radians = degrees * (pi/180)

    new_dir = (int(round(vector[0] * cos(radians) + vector[1] * sin(radians), 1)),
               int(round(vector[1] * cos(radians) - vector[0] * sin(radians), 1)))
    return new_dir


class Guard:
    position = tuple[int, int]
    direction = tuple[int, int]
    territory = dict

    def __init__(self, starting_position: tuple, starting_direction: tuple, territory: dict):
        self.position = starting_position
        self.direction = starting_direction
        self.territory = territory

    def take_turn(self):
        next_spot = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])

        if self.territory[next_spot] == "#":
            self.direction = rotate(self.direction, 90)
            return self.position

        self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])

        if self.territory[self.position] == "":
            return "done!"
        else:
            return self.position


with open("input.txt","r") as f:
    flipped = [line.strip("\n") for line in f.readlines()[::-1]]
    dd = defaultdict(str) | {(j,i): c for i, r in enumerate(flipped)
                                      for j, c in enumerate(r)}


starting_location = [loc for loc in dd if dd[loc] == "^"][0]
path = []
guard = Guard(starting_location, (0,1), dd)

while True:
    path.append(guard.position)
    if guard.take_turn() == "done!":
        break

print(len(set(path)))

empty_spots = list(set(path))
empty_spots.remove(starting_location)

stuck_list = []
for spot in empty_spots:
    print(spot)
    dd_with_obstruction = dd.copy()
    dd_with_obstruction[spot] = "#"

    guard = Guard(starting_location, (0,1), dd_with_obstruction)
    path = []

    while True:
        if (guard.position, guard.direction) in path:
            stuck_list.append(spot)
            break
        path.append((guard.position, guard.direction))
        if guard.take_turn() == "done!":
            break

print(stuck_list)
print(len(stuck_list))