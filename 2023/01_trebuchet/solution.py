import random
from functools import reduce

numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

with open("input.txt") as file:
    inp = [x.strip() for x in file.readlines()]
    

def convertToIntsSecond(line):
    result = []
    i = 0
    while i < len(line):
        if line[i] >= '0' and line[i] <= '9':
            result.append(int(line[i]))
    
        for n in numbers:
            if line[i:i+len(n)].lower() == n:
                result.append(numbers.index(n))
                break
            
        i += 1
        
    return result

def getAnswerFirst(line):
    values = convertToIntsFirst(line)
    return (values[0], values[-1])

def getAnswerSecond(line):
    values = convertToIntsSecond(line)
    return (values[0], values[-1])

def convertToIntsFirst(line):
    return [int(x) for x in line if x >= '0' and x <= '9']

def first():
    values = [convertToIntsFirst(line) for line in inp]
    ints = [array[0]*10+array[-1] for array in values]
    total = reduce(lambda x,y: x+y, ints)
    
    return total

def second():
    values = [convertToIntsSecond(line) for line in inp]
    ints = [array[0]*10+array[-1] for array in values]
    
    for x, i in zip(inp, ints):
        print(f"{x.strip()} - {convertToIntsSecond(x)} - {i}")

    total = reduce(lambda x,y: x+y, ints)
    
    return total

if __name__ == "__main__":    
    print(f"first = {first()}")
    print(f"second = {second()}")
    print(f"min = {min([len(x) for x in inp])}")
    print(f"max = {max([len(x) for x in inp])}")