

with open("../01_input.txt", encoding="utf8") as f:
    LIST_1 = []
    LIST_2 = []
    for line in f:
        split = line.split()
        LIST_1.append(int(split[0]))
        LIST_2.append(int(split[1]))

    LIST_1 = sorted(LIST_1)
    LIST_2 = sorted(LIST_2)

def part1():
    diff = [abs(LIST_1[i] - LIST_2[i]) for i in range(len(LIST_1))]
    return sum(diff)


def part2():
    counts = {}
    for entry in LIST_2:
        if entry in counts:
            counts[entry] += 1
        else:
            counts[entry] = 1

    total = 0
    for entry in LIST_1:
        total += entry * counts.get(entry, 0)

    return total

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")

