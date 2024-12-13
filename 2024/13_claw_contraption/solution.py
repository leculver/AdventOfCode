import re

PATTERN = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"

def parse_input(fn):
    with open(fn, encoding='ascii') as f:
        data = f.read()

    matches = re.findall(PATTERN, data)
    patterns = [[int(x) for x in match] for match in matches]
    return [list(pattern) for pattern in patterns]

def solve_for_presses(data, max_val):
    solutions = []
    for row in data:
        a, c, b, d, x, y = row

        determinant = a * d - b * c
        if determinant == 0:
            continue

        x_sol = (d * x - b * y) / determinant
        y_sol = (-c * x + a * y) / determinant

        x_sol_int = round(x_sol)
        y_sol_int = round(y_sol)

        if max_val is not None:
            if x_sol_int > max_val or y_sol_int > max_val:
                continue

        if a * x_sol_int + b * y_sol_int == x and c * x_sol_int + d * y_sol_int == y:
            solutions.append([x_sol_int, y_sol_int])

    return solutions

def part1(fn):
    tensor = parse_input(fn)
    solution = solve_for_presses(tensor, 1000)
    tokens = [3, 1]
    price = sum(sum(row[i] * tokens[i] for i in range(2)) for row in solution)
    return int(price)


def part2(fn):
    modifier = 10_000_000_000_000
    tensor = parse_input(fn)
    for l in tensor:
        l[-1] += modifier
        l[-2] += modifier

    solution = solve_for_presses(tensor, None)
    tokens = [3, 1]
    price = sum(sum(row[i] * tokens[i] for i in range(2)) for row in solution)
    return int(price)


INPUT = "13_input.txt"
print(f"part1: {part1(INPUT):,}")
print(f"part2: {part2(INPUT):,}")
