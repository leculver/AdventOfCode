class Schematic:
    def __init__(self, file):
        with open(file) as f:
            self.data = [line.strip() for line in f.readlines()]
        
        self.width = len(self.data[0])
        self.length = len(self.data)
    
    def get(self, x, y):
        if (x < 0 or x >= self.width):
            return None
        
        if (y < 0 or y >= self.length):
            return None
        
        value = self.data[y][x]
        if value == '.':
            return None
        
        return value

    def findValidPartNumbers(self):
        for part in self.findPartNumbers():
            if self.isValidPart(part):
                yield part

    def findPartNumbers(self):
        coords = None
        num = None
        for y in range(self.length):
            for x in range(self.width):
                value = self.get(x, y)
                if value is not None and value.isdigit():
                    if num == None:
                        num = int(value)
                        coords = (x, y)
                    else:
                        num = num * 10 + int(value)
                elif num is not None:
                    yield (*coords, num)
                    num = None
                    coords = None
            if num != None:
                yield (*coords, num)
                num = None
                coords = None

    def getRatioAt(self, x, y):
        gears = []
        
        for ny in range(y-1, y+2):
            nx = x - 1
            while nx <= x + 1 and len(gears) <= 2:
                val = self.get(nx, ny)
                if val is not None and val.isdigit():
                    start = nx
                    c = self.get(start - 1, ny)
                    while c is not None and c.isdigit():
                        start -= 1
                        c = self.get(start - 1, ny)
                    
                    end = nx
                    c = self.get(end + 1, ny)
                    while c is not None and c.isdigit():
                        end += 1
                        c = self.get(end + 1, ny)
                    
                    val = self.data[ny][start:end + 1]
                    gears.append(int(val))
                    
                    nx = end
                nx += 1
        
        if len(gears) == 2:
            return gears[0] * gears[1]

    def findGearRatio(self):
        for y in range(self.length):
            for x in range(self.width):
                if self.get(x, y) == '*':
                    result = self.getRatioAt(x, y)
                    if result is not None:
                        yield result


    def isPartIndicator(self, value):
        return value != None and not value.isdigit()

    def isValidPart(self, part):
        (x, y, num) = part

        num_len = len(str(num))  # Get the length of the number

        for offset in range(num_len):
            for dx, dy in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
                nx, ny = x + offset + dx, y + dy
                val = self.get(nx, ny)
                if self.isPartIndicator(val):
                    return True

        return False


print(f"part1: {sum((x[2] for x in Schematic('input.txt').findValidPartNumbers()))}")
print(f"part2: {sum(Schematic('input.txt').findGearRatio())}")