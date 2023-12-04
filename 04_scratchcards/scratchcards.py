
class Scratchcard:
    def __init__(self, line):
        line = line.strip()
        split = line[4:].split(':')
        self.card = int(split[0].strip())
        self.index = self.card - 1
        
        split = split[1].split('|')
        self.winners = self.parse(split[0])
        self.numbers = self.parse(split[1])
        
    
    def parse(self, line):
        return [int(x.strip()) for x in line.split(' ') if len(x) > 0]

    
    def getWinCount(self):
        count = 0
        for win in self.winners:
            if win in self.numbers:
                count += 1
        
        return count
    

    def value(self):
        count = self.getWinCount()
        if count == 0:
            return 0
        
        return 2 ** (count - 1)

with open("input.txt") as f:
    cards = [Scratchcard(line) for line in f.readlines()]

print(sum([card.value() for card in cards]))

def calculateCardWins(cards):
    allCards = [1] * len(cards)
    
    for card in cards:
        count = card.getWinCount()
        for i in range(card.card, card.card + count):
            allCards[i] += allCards[card.index]
            
    print(sum(allCards))

calculateCardWins(cards)