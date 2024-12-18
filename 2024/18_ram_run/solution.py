from collections import deque

class Ram:
    def __init__(self, coordinates):
        self.corrupted = coordinates
        dim_x = 0
        dim_y = 0
        for x, y in coordinates:
            dim_x = max(dim_x, x)
            dim_y = max(dim_y, y)

        self.dim_x = dim_x + 1
        self.dim_y = dim_y + 1

    def get_start(self):
        return (0, 0)

    def get_end(self):
        return (self.dim_x - 1, self.dim_y - 1)

    def get_valid_next_pos(self, pos, invalid):
        curr_x, curr_y = pos
        for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (x, y) == (6, 0):
                pass
            new_x = curr_x + x
            new_y = curr_y + y
            if (new_x, new_y) not in invalid and 0 <= new_x < self.dim_x and 0 <= new_y < self.dim_y:
                yield (new_x, new_y)

    def solve(self, start_at):
        corrupted = set(self.corrupted[:start_at])
        visited = set()
        todo = deque()

        start = self.get_start()
        visited.add(start)
        todo.append((start, 0))

        while todo:
            pos, d = todo.popleft()

            if pos == self.get_end():
                return d

            for next_pos in self.get_valid_next_pos(pos, visited | corrupted):
                if next_pos not in visited and next_pos not in corrupted:
                    visited.add(next_pos)
                    todo.append((next_pos, d + 1))

        return None

def load_input(filename):
    with open(filename, 'r') as f:
        return [tuple(map(int, line.strip().split(','))) for line in f.readlines()]

def part1(filename, start_at):
    corrupted = load_input(filename)
    ram = Ram(corrupted)
    return ram.solve(start_at)

def part2(filename, start_at):
    corrupted = load_input(filename)
    ram = Ram(corrupted)
    last = None

    bot = start_at
    top = len(corrupted)
    while bot < top:
        mid = (bot + top) // 2
        if ram.solve(mid) is None:
            top = mid
        else:
            bot = mid + 1
            last = mid

    return corrupted[last]

print(f"Part 1: {part1('18_input.txt', 1024)}")
print(f"Part 2: {part2('18_input.txt', 1024)}")
