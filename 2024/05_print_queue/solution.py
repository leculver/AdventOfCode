from functools import cmp_to_key

PAGE_ORDERING = {}
PAGES_REQUESTED = []

with open("05_input.txt", encoding="utf8") as f:
    for line in f:
        line = line.strip()
        if line:
            if '|' in line:
                split = line.split('|')
                PAGE_ORDERING.setdefault(int(split[0]), set()).add(int(split[1]))

            elif ',' in line:
                PAGES_REQUESTED.append([int(x) for x in line.split(',')])

def is_valid_ordering(ordering):
    previous = set()
    for page in ordering:
        after = PAGE_ORDERING.get(page, [])

        if any(previous & after):
            return False

        previous.add(page)

    return True

def part1():
    total = 0
    for pages in PAGES_REQUESTED:
        if is_valid_ordering(pages):
            total += pages[len(pages) // 2]

    return total

def page_comparator(a, b):
    return -1 if b in PAGE_ORDERING.get(a, []) else 0

KEY = cmp_to_key(page_comparator)

def part2():
    total = 0
    for pages in PAGES_REQUESTED:
        pages = list(pages)
        if not is_valid_ordering(pages):
            pages.sort(key=KEY)
            total += pages[len(pages) // 2]

    return total

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
