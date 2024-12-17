import heapq
import numpy as np
import time
from tqdm import tqdm

def load_maze(filename):
    with open(filename, encoding='ascii') as f:
        return np.array([list(line.strip().replace('.', ' ')) for line in f], dtype='str')

def get_start(maze):
    return tuple(np.argwhere(maze == 'S')[0])

def get_end(maze):
    return tuple(np.argwhere(maze == 'E')[0])

def get_valid_next_pos(maze, path):
    current = path[-1]
    moves = []
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_pos = current[0] + direction[0], current[1] + direction[1]
        if new_pos[0] < 0 or new_pos[0] >= maze.shape[0] or new_pos[1] < 0 or new_pos[1] >= maze.shape[1]:
            continue

        if maze[tuple(new_pos)] in (' ', 'E') and not any(np.array_equal(new_pos, pos) for pos in path):
            moves.append(new_pos)

    return moves

def get_direction(pos1, pos2):
    direction = pos2[0] - pos1[0], pos2[1] - pos1[1]
    if direction[0] == 1:
        return 'V'
    if direction[0] == -1:
        return '^'
    if direction[1] == 1:
        return '>'
    if direction[1] == -1:
        return '<'

def print_maze(maze, path):
    solved = maze.copy()
    for i, pos in enumerate(path):
        if i:
            solved[tuple(pos)] = get_direction(path[i - 1], pos)

    for row in solved:
        print(''.join(row))

def dijkstra_solve_maze(maze, start = None, end = None):
    if start is None:
        start = get_start(maze)

    if end is None:
        end = get_end(maze)

    start_path = [start]

    todo = []
    distances = {}
    paths = {}

    distances[start] = 0
    paths[start] = [start_path]
    heapq.heappush(todo, (score_path(start_path), start_path))

    while todo:
        _, path = heapq.heappop(todo)
        current = path[-1]
        if (distances.get(current, 1e9) < score_path(path)):
            continue

        for next_pos in get_valid_next_pos(maze, path):
            new_path = path + [next_pos]
            new_distance = score_path(new_path)

            if next_pos not in distances or new_distance <= distances[next_pos]:
                distances[next_pos] = new_distance
                if next_pos not in paths:
                    paths[next_pos] = [new_path]
                else:
                    curr_score = score_path(paths[next_pos][0])
                    if new_distance < curr_score:
                        paths[next_pos] = [new_path]
                    elif new_distance == curr_score:
                        paths[next_pos].append(new_path)

                if next_pos != end:
                    heapq.heappush(todo, (new_distance, new_path))

    return paths[end]

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def build_path_from_moves(moves, start):
    direction = (0, 1)
    path = [start]

    for move in moves:
        match move:
            case 'c':
                direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]

            case 'cc':
                direction = DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 4]

            case 'f':
                path.append((path[-1][0] + direction[0], path[-1][1] + direction[1]))

            case _:
                raise ValueError(f"Invalid move: {move}")

    return path, direction

def score_moves(moves):
    return sum(1 if move == 'f' else 1000 for move in moves)

def facing_wall(maze, path, direction):
    position = path[-1]
    new_pos = position[0] + direction[0], position[1] + direction[1]
    return maze[tuple(new_pos)] == '#' or new_pos in path

def get_valid_moves(maze, moves):
    path, direction = build_path_from_moves(moves, get_start(maze))
    result = []

    if not facing_wall(maze, path, direction):
        result.append('f')

    if moves[-1] == 'f':
        next_direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]
        if not facing_wall(maze, path, next_direction):
            result.append('c')

        next_direction = DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 4]
        if not facing_wall(maze, path, next_direction):
            result.append('cc')

    return result


def dijkstra_solve_maze_moves(maze):
    start = get_start(maze)
    direction = (0, 1)
    end = get_end(maze)

    todo = []
    scores = {}
    locations = {}

    scores[(start, direction)] = 0
    total = 0

    init_queue(maze, todo)
    progress = tqdm(total=0, dynamic_ncols=True)
    while todo:
        total += 1
        if total % 100 == 0:
            progress.update(100)
            progress.set_description(f"Todo: {len(todo):,}, solutions: {len(locations.get(end, [])):,}")

        _, moves = heapq.heappop(todo)
        path, direction = build_path_from_moves(moves, start)
        pos = path[-1]
        if (scores.get((pos, direction), 1e9) < score_path(path)):
            continue

        for move in get_valid_moves(maze, moves):
            new_moves = moves + [move]
            new_score = score_moves(new_moves)
            new_path, new_direction = build_path_from_moves(new_moves, start)
            new_pos = new_path[-1]
            scores_key = (new_pos, new_direction)

            if scores_key not in scores or new_score <= scores[scores_key]:
                scores[scores_key] = new_score

                if new_pos not in locations:
                    locations[new_pos] = [new_moves]
                else:
                    curr_score = score_moves(locations[new_pos][0])
                    if new_score < curr_score:
                        locations[new_pos] = [new_moves]
                    elif new_score == curr_score:
                        locations[new_pos].append(new_moves)

                if new_pos != end:
                    heapq.heappush(todo, (new_score, new_moves))

    return locations[end]

def init_queue(maze, todo):
    path = [get_start(maze)]
    direction = (0, 1)
    if not facing_wall(maze, path, direction):
        next_moves = ['f']
        heapq.heappush(todo, (score_moves(next_moves), next_moves))

    left = DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 4]
    if not facing_wall(maze, path, left):
        next_moves = ['cc']
        heapq.heappush(todo, (score_moves(next_moves), next_moves))

    right = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]
    if not facing_wall(maze, path, right):
        next_moves = ['c']
        heapq.heappush(todo, (score_moves(next_moves), next_moves))

def turns_needed(direction, new_direction):
    if direction == new_direction:
        return 0
    # (0, 1) -> (1, 0) -> (0, -1) -> (-1, 0) -> (0, 1)

    dist = max(abs(direction[0] - new_direction[0]), abs(direction[1] - new_direction[1]))
    return dist

def score_path(path):
    score = 0
    direction = (0, 1) # east
    for i in range(1, len(path)):
        previous = path[i - 1]
        current = path[i]
        new_direction = current[0] - previous[0], current[1] - previous[1]

        score += 1 + turns_needed(direction, new_direction) * 1000
        direction = new_direction
    return score

def path_contains_targets(path, targets):
    return all(any(np.array_equal(target, pos) for pos in path) for target in targets)

def part1(solutions):
    moves = solutions[0]
    path, _ = build_path_from_moves(moves, get_start(maze))
    return score_path(path)

def part2(solutions):
    seen = set()
    start = get_start(MAZE)
    for solution in solutions:
        path, _ = build_path_from_moves(solution, start)
        for pos in path:
            seen.add(pos)

    return len(seen)

MAZE = load_maze('16_input.txt')

SOLUTIONS = dijkstra_solve_maze_moves(MAZE)
print(f"part1: {part1(SOLUTIONS):,}")
print(f"part2: {part2(SOLUTIONS):,}")
