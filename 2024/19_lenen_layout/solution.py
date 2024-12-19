def read_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        parts = lines[0].strip().split(', ')
        patterns = [x.strip() for x in lines[2:]]
        return parts, patterns

def can_build_word(parts, word, seen):
    if not word:
        return 1

    if word in seen:
        return seen[word]

    count = 0
    for part in parts:
        if word.startswith(part):
            count += can_build_word(parts, word[len(part):], seen)
    seen[word] = count
    return count

def part1(parts, patterns):
    seen = {}
    return sum(1 if can_build_word(parts, word, seen) else 0 for word in patterns)


def part2(parts, patterns):
    seen = {}
    return sum(can_build_word(parts, word, seen) for word in patterns)

PARTS, PATTERNS = read_input('19_input.txt')

print(f"part1: {part1(PARTS, PATTERNS)}")
print(f"part2: {part2(PARTS, PATTERNS):,}")
