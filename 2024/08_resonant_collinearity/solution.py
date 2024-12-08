import numpy as np

def get_input():
    with open("08_input.txt", encoding="ascii") as f:
        lines = f.readlines()

    result = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):

            if c not in ("#", '.', '\n'):
                result.setdefault(c, []).append((y, x))

    max_y = len(lines)
    max_x = len(lines[0]) - 1
    return result, max_y, max_x

ANTENNA, MAX_Y, MAX_X = get_input()

def diff_pos(resonance, first, second):
    diff = second - first
    pos = first - diff

    if 0 <= pos[0] < MAX_Y and 0 <= pos[1] < MAX_X:
        resonance.add(tuple(pos))


def part1():
    resonance = set()
    for positions in ANTENNA.values():
        for i, (y, x) in enumerate(positions):
            pos1 = np.array([y, x])

            for j in range(i + 1, len(positions)):
                pos2 = np.array([*positions[j]])

                diff_pos(resonance, pos1, pos2)
                diff_pos(resonance, pos2, pos1)

    return len(resonance)

def is_on_line(p1, p2, point):
    x1, y1 = p1
    x2, y2 = p2
    x, y = point

    return (y - y1) * (x2 - x1) == (y2 - y1) * (x - x1)

def part2():
    resonance = set()
    for positions in ANTENNA.values():
        for i, (y, x) in enumerate(positions):
            pos1 = (y, x)

            for j in range(i + 1, len(positions)):
                pos2 = positions[j]

                for y3 in range(MAX_Y):
                    for x3 in range(MAX_X):
                        if is_on_line(pos1, pos2, (y3, x3)):
                            resonance.add((y3, x3))

    return len(resonance)

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
