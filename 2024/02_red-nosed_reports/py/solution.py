with open("02_input.txt") as file:
    data = []
    for line in file:
        data.append([int(x) for x in line.strip().split()])

def is_safe(diffs):
    if all(x > 0 for x in diffs) or all(x < 0 for x in diffs):
        MIN = min(abs(x) for x in diffs)
        MAX = max(abs(x) for x in diffs)

        result = MIN > 0 and MAX <= 3
        return result

    return False

def is_really_safe(levels):

    if is_safe(get_diffs(levels)):
        return True

    for i in range(len(levels)):
        new_levels = levels[:i] + levels[i + 1:]
        if is_safe(get_diffs(new_levels)):
            return True

    return False

def get_diffs(levels):
    diffs = []
    for i in range(len(levels) - 1):
        diffs.append(levels[i] - levels[i + 1])
    return diffs


def part1():
    return sum(1 for levels in data if is_safe(get_diffs(levels)))

def part2():
    return sum(1 for levels in data if is_really_safe(levels))

for levels in data:
    print(levels, is_really_safe(levels))

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
