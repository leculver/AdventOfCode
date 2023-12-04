from functools import reduce


with open('input.txt', 'r') as f:
    data = [line.strip() for line in f.readlines()]

class Game:
    def __init__(self, gameText, rounds):
        self.game = int(gameText[len("Game "):])
        self.red = 0
        self.green = 0
        self.blue = 0

        for rnd in rounds:
            for entry in rnd.split(', '):
                colorParts =entry.split(' ')
                count = int(colorParts[0])
                color = colorParts[1]
                if color == 'red':
                    self.red = max(count, self.red)
                elif color == 'green':
                    self.green = max(count, self.green)
                elif color == 'blue':
                    self.blue = max(count, self.blue)
                else:
                    raise Exception(f'Unknown color {color}')
                    
    def __str__(self):
        return f'Game {self.game}: red:{self.red}, green:{self.green}, blue:{self.blue}'

def getGames(data):
    games = []
    for line in data:
        line = line.split(': ')
        games.append(Game(line[0], line[1].split('; ')))
    return games

(red, green, blue) = (12, 13, 14)

part1Answer = reduce(lambda x, y: x + y, (x.game for x in getGames(data) if x.red <= red and x.green <= green and x.blue <= blue))
print(f"part1 = {part1Answer}")


part2Answer = reduce(lambda x, y: x + y, (x.red * x.green * x.blue for x in getGames(data)))
print(f"part2 = {part2Answer}")
