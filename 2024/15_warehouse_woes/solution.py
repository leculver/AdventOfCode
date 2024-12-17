import numpy as np
from tqdm import tqdm

class Object:
    def __init__(self, position, kind):
        self.map = None
        self.position = position
        self.kind = kind

    @property
    def gps(self):
        return 100 * self.position[0] + self.position[1]

    def __str__(self):
        return f"{self.kind} at {self.position}"

    def __repr__(self):
        return str(self)

    def get_vector(self, direction):
        match direction:
            case '^':
                return np.array((-1, 0))
            case 'v':
                return np.array((1, 0))
            case '<':
                return np.array((0, -1))
            case '>':
                return np.array((0, 1))
            case _:
                raise ValueError(f"Invalid direction: {direction}")


    def get_touching_objects(self, direction):
        vector = self.get_vector(direction)

        result = set()
        if direction == '<':
            next_obj = self.map.get_object(self.position + vector)
            if next_obj is not None:
                result.add(next_obj)
        elif direction == '>':
            next_obj = self.map.get_object(self.position + vector * len(self.kind))
            if next_obj is not None:
                result.add(next_obj)


        # our coordinates are the top left of the object
        elif direction in ('^', 'v'):
            right_vector = np.array((0, 1))

            for i in range(len(self.kind)):
                next_obj = self.map.get_object(self.position + vector + i * right_vector)
                if next_obj is not None:
                    result.add(next_obj)

        else:
            raise ValueError(f"Invalid direction: {direction}")

        return result

    def move(self, direction):
        if self.kind == '#':
            assert False

        all_touching = []
        todo = [self]
        while todo:
            obj = todo.pop()
            if obj in all_touching:
                continue

            all_touching.append(obj)
            todo.extend(obj.get_touching_objects(direction))

        if all(obj.kind != "#" for obj in all_touching):
            vector = self.get_vector(direction)
            for obj in all_touching:
                obj.position += vector

class Map:
    def __init__(self, robot, objects):
        self.robot = robot
        self.objects = objects

        self.robot.map = self
        for obj in self.objects:
            obj.map = self

    def get_object(self, position):
        for obj in self.objects:
            obj_len = len(obj.kind)

            if obj.position[0] == position[0] and obj.position[1] <= position[1] < obj.position[1] + obj_len:
                return obj

        return None

    def print(self):
        sorted_objects = sorted(self.objects + [self.robot], key=lambda obj: (obj.position[0], obj.position[1]))
        curr_obj = 0
        curr_y = 0
        curr_x = 0

        while curr_obj < len(sorted_objects):
            obj = sorted_objects[curr_obj]
            while curr_y < obj.position[0]:
                print()
                curr_y += 1
                curr_x = 0

            while curr_x < obj.position[1]:
                print(' ', end='')
                curr_x += 1

            print(obj.kind, end='')
            curr_x += len(obj.kind)
            curr_obj += 1

        print()

    def move_robot(self, direction):
        self.robot.move(direction)

def parse_input(filename):
    y = 0
    objects = []
    objects2 = []
    robot = None
    instructions = None

    with open(filename, encoding='ascii') as file:
        for line in file:
            line = line.strip()

            if instructions is not None:
                instructions += line
                continue

            if not line:
                assert instructions is None
                instructions = ''
                continue

            for x, char in enumerate(line):
                pos = np.array((y, x))
                pos2 = np.array((y, 2 * x))
                match char:
                    case '#':
                        objects.append(Object(pos, '#'))
                        objects2.append(Object(pos2, '#'))
                        objects2.append(Object(pos2 + (0, 1), '#'))
                    case 'O':
                        objects.append(Object(pos, 'O'))
                        objects2.append(Object(pos2, "[]"))
                    case '@':
                        assert robot is None
                        robot = Object(pos, '@')
                        robot2 = Object(pos2, '@')
            y += 1

        assert robot is not None
        return Map(robot, objects), Map(robot2, objects2), instructions

def manhattan_distance(a, b):
    return np.sum(np.abs(a - b))

def trace(floor, instr):
    floor.print()
    for i, direction in enumerate(instr):
        print(f"Step: {i + 1} Direction: {direction}")
        floor.move_robot(direction)

        floor.print()
        print()

    return sum(obj.gps for obj in floor.objects if obj.kind in ('O', '[', '[]'))


def solve(floor, instr):
    for direction in tqdm(instr):
        floor.move_robot(direction)

    return sum(obj.gps for obj in floor.objects if obj.kind in ('O', '[', '[]'))

#EXAMPLE_MAP1, EXAMPLE_MAP2, EXAMPLE_INSTRUCTIONS = parse_input("15_example.txt")
MAP1, MAP2, INSTRUCTIONS = parse_input("15_input.txt")

#print(trace(EXAMPLE_MAP1, EXAMPLE_INSTRUCTIONS))
#print(trace(EXAMPLE_MAP2, EXAMPLE_INSTRUCTIONS))
print(f"Part 1: {solve(MAP1, INSTRUCTIONS):,}")
print(f"Part 2: {solve(MAP2, INSTRUCTIONS):,}")
