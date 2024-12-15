import numpy as np

class Object:
    def __init__(self, position, kind):
        self.position = position
        self.kind = kind

    @property
    def gps(self):
        return 100 * self.position[0] + self.position[1]

class Map:
    def __init__(self, robot, objects):
        self.robot = robot
        self.objects = objects

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
            curr_x += 1
            curr_obj += 1

        print()

    def move_robot(self, direction):
        vector = None
        objs_in_direction = None
        match direction:
            case '^':
                vector = np.array((-1, 0))
                objs_in_direction = [obj for obj in self.objects if obj.position[1] == self.robot.position[1]
                                     and obj.position[0] < self.robot.position[0]]

            case 'v':
                vector = np.array((1, 0))
                objs_in_direction = [obj for obj in self.objects if obj.position[1] == self.robot.position[1]
                                     and obj.position[0] > self.robot.position[0]]

            case '<':
                vector = np.array((0, -1))
                objs_in_direction = [obj for obj in self.objects if obj.position[0] == self.robot.position[0]
                                     and obj.position[1] < self.robot.position[1]]

            case '>':
                vector = np.array((0, 1))
                objs_in_direction = [obj for obj in self.objects if obj.position[0] == self.robot.position[0]
                                     and obj.position[1] > self.robot.position[1]]

            case _:
                raise ValueError(f"Invalid direction: {direction}")

        objs_in_direction.sort(key=lambda obj: manhattan_distance(obj.position, self.robot.position))
        curr_pos = self.robot.position
        for i, obj in enumerate(objs_in_direction):
            expected_pos = (i+1) * vector + curr_pos
            if obj.position[0] != expected_pos[0] or obj.position[1] != expected_pos[1]:
                objs_in_direction = objs_in_direction[:i]
                break

        if any(o.kind == '#' for o in objs_in_direction):
            return False

        self.robot.position += vector
        for obj in objs_in_direction:
            obj.position += vector

        return True


def parse_input(filename):
    y = 0
    objects = []
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
                match char:
                    case '#':
                        objects.append(Object(pos, '#'))
                    case 'O':
                        objects.append(Object(pos, 'O'))
                    case '@':
                        assert robot is None
                        robot = Object(pos, '@')
            y += 1

        assert robot is not None
        return Map(robot, objects), instructions

def manhattan_distance(a, b):
    return np.sum(np.abs(a - b))

INPUT = parse_input("15_input.txt")

def part1(floor, instr):
    for direction in instr:
        floor.move_robot(direction)

    return sum(obj.gps for obj in floor.objects if obj.kind == 'O')

print(f"Part 1: {part1(*INPUT):,}")
