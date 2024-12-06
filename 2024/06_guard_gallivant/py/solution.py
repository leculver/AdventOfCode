import numpy as np
from tqdm import tqdm

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

with open("06_input.txt", "r", encoding="utf8") as file:
    MAP = np.array([[ord(char) for char in line.strip()] for line in file.readlines()], dtype=np.int8)

def print_map(the_map):
    for row in the_map:
        print("".join([chr(char) for char in row]))


def turn_right(direction):
    return (direction + 1) % len(DIRECTIONS)

def part1():
    curr_direction = 0

    pos = np.argwhere(MAP == ord("^"))[0]
    visited = set()

    while True:
        visited.add(tuple(pos))
        next_pos = pos + DIRECTIONS[curr_direction]

        # check next_pos out of bounds:
        if next_pos[0] < 0 or next_pos[0] >= MAP.shape[0] or next_pos[1] < 0 or next_pos[1] >= MAP.shape[1]:
            break

        # check next_pos is wall:
        if MAP[next_pos[0], next_pos[1]] == ord("#"):
            curr_direction = turn_right(curr_direction)
            continue

        pos = next_pos

    return len(visited)

def part2():
    start = np.argwhere(MAP == ord("^"))[0]

    total = 0

    # walk every square

    progress_bar = tqdm(total=MAP.shape[0] * MAP.shape[1])
    for i in range(MAP.shape[0]):
        for j in range(MAP.shape[1]):
            progress_bar.update(1)
            if MAP[i, j] == ord("#"):
                continue

            pos = start
            curr_direction = 0
            visited = set()

            while True:
                pos_dir = (pos[0], pos[1], curr_direction)
                if pos_dir in visited:
                    total += 1
                    break

                visited.add(pos_dir)
                next_pos = pos + DIRECTIONS[curr_direction]

                # check next_pos out of bounds:
                if next_pos[0] < 0 or next_pos[0] >= MAP.shape[0] or next_pos[1] < 0 or next_pos[1] >= MAP.shape[1]:
                    break

                # check next_pos is wall:
                if MAP[next_pos[0], next_pos[1]] == ord("#") or (next_pos[0] == i and next_pos[1] == j):
                    curr_direction = turn_right(curr_direction)
                    continue

                pos = next_pos

    return total

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
