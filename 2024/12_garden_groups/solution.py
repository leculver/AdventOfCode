with open("12_input.txt") as f:
    PLOT = [x.strip() for x in f.readlines()]

def is_equal(plot, x, y, seed):
    return 0 <= x < len(plot) and 0 <= y < len(plot[0]) and plot[x][y] == seed

def is_not_equal_or_off_map(plot, x, y, seed):
    return x < 0 or y < 0 or x >= len(plot) or y >= len(plot[0]) or plot[x][y] != seed

def consider_fence(plot, x, y, dx, dy, fence_considered):
    if (x, y, dx, dy) in fence_considered:
        return 0

    fence_considered.add((x, y, dx, dy))

    # walk perpendicular to the direction of the edge
    seed = plot[x][y]
    step_x, step_y = dy, dx

    # walk one direction
    curr_x, curr_y = x + step_x, y + step_y
    while is_equal(plot, curr_x, curr_y, seed) and is_not_equal_or_off_map(plot, curr_x + dx, curr_y + dy, seed):
        fence_considered.add((curr_x, curr_y, dx, dy))
        curr_x += step_x
        curr_y += step_y

    # walk the other direction
    curr_x, curr_y = x - step_x, y - step_y
    while is_equal(plot, curr_x, curr_y, seed) and is_not_equal_or_off_map(plot, curr_x + dx, curr_y + dy, seed):
        fence_considered.add((curr_x, curr_y, dx, dy))
        curr_x -= step_x
        curr_y -= step_y

    return 1

def find_area_perimeter(plot):
    regions = {}
    visited = set()
    for i, row in enumerate(plot):
        for j, seed in enumerate(row):
            if (i, j) in visited:
                continue

            area = 0
            perimeter = 0
            edges = 0

            fence_considered = set()

            todo = [(i, j)]
            visited.add((i, j))
            while todo:
                x, y = todo.pop()
                area += 1

                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy

                    if is_equal(plot, nx, ny, seed):
                        if (nx, ny) not in visited:
                            todo.append((nx, ny))
                            visited.add((nx, ny))
                    else:
                        perimeter += 1
                        edges += consider_fence(plot, x, y, dx, dy, fence_considered)

            regions.setdefault(seed, []).append((area, perimeter, edges))

    return regions

def part1(plot):
    regions = find_area_perimeter(plot)
    total = 0
    for items in regions.values():
        total += sum(x[0] * x[1] for x in items)

    return total

def part2(plot):
    regions = find_area_perimeter(plot)
    total = 0

    for items in regions.values():
        total += sum(x[0] * x[2] for x in items)

    return total

print(f"Part 1: {part1(PLOT):,}")
print(f"Part 2: {part2(PLOT):,}")
