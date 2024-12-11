from math import log10
from time import time

with open("11_input.txt", encoding="ascii") as f:
    line = f.readline().strip()
    STONES = [int(x) for x in line.split(' ')]

def count_digits(number):
    return int(log10(number)) + 1

def apply_rule(stone):
    if stone == 0:
        return (1, )

    if (digits := count_digits(stone)) % 2 == 0:
        half = digits // 2
        return int(str(stone)[:half]), int(str(stone)[half:])

    return (stone * 2024, )

def apply_rules_to_list(stones : list):
    result = []
    for stone in stones:
        result.extend(apply_rule(stone))

    return result

def dumb_solution(stones, steps):
    start = time()
    for _ in range(steps):
        stones = apply_rules_to_list(stones)

    print(f"Total time: {time() - start}, with {len(stones)} stones")

    return len(stones)

def smart_solution(stones, steps):
    curr = {}
    for stone in stones:
        curr[stone] = curr.get(stone, 0) + 1

    start = time()
    for _ in range(steps):
        next_stones = {}
        for stone, count in curr.items():
            for new_stone in apply_rule(stone):
                next_stones[new_stone] = next_stones.get(new_stone, 0) + count

        curr = next_stones

    result = sum(curr.values())
    print(f"Total time: {time() - start}, with {result} stones")

    return result


print(STONES)

print(f"part1 dumb:  {dumb_solution(STONES, 25)}")
print(f"part1 smart: {smart_solution(STONES, 25)}")
print(f"part2: {smart_solution(STONES, 75):_}")
