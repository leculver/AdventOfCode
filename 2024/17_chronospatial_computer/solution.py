from itertools import product

def parse_input(filename):
    ctx = {'a': 0, 'b': 0, 'c': 0, 'ip': 0, 'instructions': []}
    with open(filename, encoding="ascii") as f:
        for line in f:
            if line.startswith("Register A: "):
                ctx['a'] = int(line.split(': ')[1])
            elif line.startswith("Program: "):
                ctx['instructions'] = [int(x) for x in line.split(': ')[1].split(',')]

    return ctx


def run_opcode(ctx : dict, instructions : list[int], output : list[int]):
    ip = ctx['ip']
    if ip >= len(instructions) - 1:
        return False

    opcode, operand = instructions[ip:ip+2]
    ctx['ip'] = ip + 2

    match opcode:
        case 0: adv(ctx, operand)
        case 1: bxl(ctx, operand)
        case 2: bst(ctx, operand)
        case 3: jnz(ctx, operand)
        case 4: bcx(ctx, operand)
        case 5: out(ctx, operand, output)
        case 6: bdv(ctx, operand)
        case 7: cdv(ctx, operand)
        case _: raise ValueError(f"Unknown opcode {opcode}")

    return True

def adv(ctx, operand):
    ctx['a'] //= 2 ** get_combo_operand(ctx, operand)

def bxl(ctx, operand):
    ctx['b'] ^= operand

def bst(ctx, operand):
    ctx['b'] = get_combo_operand(ctx, operand) & 7


def jnz(ctx, operand):
    if ctx['a'] == 0:
        return False

    ctx['ip'] = operand
    return True

def bcx(ctx, _):
    ctx['b'] ^= ctx['c']

def out(ctx, operand, output):
    output.append(get_combo_operand(ctx, operand) & 7)

def bdv(ctx, operand):
    ctx['b'] = ctx['a'] // 2 ** get_combo_operand(ctx, operand)

def cdv(ctx, operand):
    ctx['c'] = ctx['a'] // 2 ** get_combo_operand(ctx, operand)

def get_combo_operand(ctx, operand):
    match operand:
        case 0:
            return 0

        case 1:
            return 1

        case 2:
            return 2

        case 3:
            return 3

        case 4:
            return ctx['a']

        case 5:
            return ctx['b']

        case 6:
            return ctx['c']

        case _:
            raise ValueError(f"Unknown combo operand {operand}")

def simulate_program(a, c):
    # bst 4
    b = a & 7

    # bxl 5
    b ^= 5

    # bxl 6
    b ^= 6

    # bxc
    b ^= c

    return b & 7

def simulate(ctx, a):
    ctx = ctx.copy()
    ctx['a'] = a
    output = []
    while run_opcode(ctx, ctx['instructions'], output):
        pass

    return output


def available_numbers(target):
    result = set()

    for a in range(0, 8):
        for c in range(0, 8):
            shift = a ^ 5           # bxl 5
            if simulate_program(a, c) == target:
                result.add(a | (c << shift))

    return result

ALL_AVAILABLE_NUMBERS = {b: available_numbers(b) for b in range(0, 8)}

def available_numbers(target):
    return ALL_AVAILABLE_NUMBERS[target].copy()

def find_sequence(instructions):
    if len(instructions) == 1:
        return available_numbers(instructions[0])

    result = []
    curr = find_sequence(instructions[1:])

    for first, second in product(curr, available_numbers(instructions[0])):
        a = (first << 3) | second
        simulated = simulate(CONTEXT, a)
        if simulated == instructions:
            result.append(a)

    return result

def part1(ctx):
    ctx = ctx.copy()
    output = []
    while run_opcode(ctx, ctx['instructions'], output):
        pass

    return output

def part2(ctx):
    return min(find_sequence(ctx['instructions']))

CONTEXT = parse_input("17_input.txt")
print(f"Part 1: {part1(CONTEXT)}")
print(f"Part 2: {part2(CONTEXT):,}")
