# given input position p and full intcode program intcode
# return the new memory and a boolean for whether or not to break
def compute(p, intcode):
    four = intcode[p:p+4]

    if four[0] == 1:
        p1, p2, o = four[1], four[2], four[3]
        intcode[o] = intcode[p1] + intcode[p2]

    elif four[0] == 2:
        p1, p2, o = four[1], four[2], four[3]
        intcode[o] = intcode[p1] * intcode[p2]

    elif four[0] == 99:
        return intcode, True

    else:
        raise ValueError

    return intcode, False

# part 1
# replace positions 1 and 2 with 12 and 2
# then return the number in position 0 once the program halts

code = None
with open('input2.txt') as f:
    for line in f:
        code = list(map(int, line.strip('\n').split(',')))

code[1] = 12
code[2] = 2

currentPos = 0
while True:
    newCode, halt = compute(currentPos, code)
    if not halt:
        code = newCode
        currentPos += 4
    else:
        break

print('Part 1:', code[0])

# part 2
# for pairs of inputs placed at positions 1 and 2, figure out the one that produces 19690720
# give the answer as 100*i1 + i2

# master code
code = None
with open('input2.txt') as f:
    for line in f:
        code = list(map(int, line.strip('\n').split(',')))

# master check
CHECKCODE = 19690720

for i1 in range(100):
    for i2 in range(100):
        tempCode = code[:]
        tempCode[1] = i1
        tempCode[2] = i2

        # this part is the same as above
        currentPos = 0
        while True:
            newCode, halt = compute(currentPos, tempCode)
            if not halt:
                tempCode = newCode
                currentPos += 4
            else:
                break

        if tempCode[0] != CHECKCODE: continue

        print('Part 2:', 100*i1 + i2)

        # weird shenanigans
        # so the loop continues if it's not broken
        # else executes continue if it's not broken
        # so the "default" operation is to break unless continued
        # even though the continue happens most of the time

        break
    else:
        continue
    break
