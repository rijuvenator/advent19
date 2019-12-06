NPARAM = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 99:0}

# implement parameter modes
# don't use this for write positions: those are implicitly mode 0, but
# there is nothing to get; one writes to the position, instead
def getValue(intcode, p, mode):
    if mode == 0:
        return intcode[p]
    if mode == 1:
        return p

# given an intcode and a pointer, cut up the opcode and get the modes
# Suppose the opcode is 01102: this is opcode 2, with the params in mode 1 1 0
# so get 110 by doing 01102 // 100 ( = 11), right justifying with 0s ( = 011), and reversing
def getModes(intcode, p):
    opcode   = intcode[p] % 100
    parcodes = str(intcode[p] // 100).rjust(NPARAM[opcode], '0')
    modes    = list( reversed([ int(i) for i in parcodes ]) )
    return modes

# intcode computer
def compute(intcode, p):

    # opcode is the last two digits of intcode[p]
    # modes are the parameter modes, in the correct order (and of the correct length of parameters)
    # parameters are just intcode[p+1] through intcode[p+1 + nParams]
    # newp is where the pointer should move to; this is usually p + nParams + 1

    opcode = intcode[p] % 100
    modes  = getModes(intcode, p)
    params = intcode[p + 1 : p + NPARAM[opcode] + 1]
    newp   = p + NPARAM[opcode] + 1

    # add
    if   opcode == 1:
        x, y, o = params
        intcode[o] = getValue(intcode, x, modes[0]) + getValue(intcode, y, modes[1])

    # multiply
    elif opcode == 2:
        x, y, o = params
        intcode[o] = getValue(intcode, x, modes[0]) * getValue(intcode, y, modes[1])

    # input
    elif opcode == 3:
        o = params[0]
        i = input('Provide input: ')
        intcode[o] = int(i)

    # output
    elif opcode == 4:
        x = params[0]
        print(getValue(intcode, x, modes[0]))

    # jump if true
    elif opcode == 5:
        t, v = params
        if getValue(intcode, t, modes[0]) != 0:
            newp = getValue(intcode, v, modes[1])

    # jump if false
    elif opcode == 6:
        t, v = params
        if getValue(intcode, t, modes[0]) == 0:
            newp = getValue(intcode, v, modes[1])

    # less than
    elif opcode == 7:
        a, b, o = params
        if getValue(intcode, a, modes[0]) < getValue(intcode, b, modes[1]):
            intcode[o] = 1
        else:
            intcode[o] = 0

    # equal to
    elif opcode == 8:
        a, b, o = params
        if getValue(intcode, a, modes[0]) == getValue(intcode, b, modes[1]):
            intcode[o] = 1
        else:
            intcode[o] = 0

    # halt
    elif opcode == 99:
        return intcode, newp, True

    # error
    else:
        raise ValueError

    return intcode, newp, False

# part 1
# input should be 1
print('Part 1: Input 1; answer is final diagnostic code')
code = None
with open('input5.txt') as f:
    for line in f:
        code = list(map(int, line.strip('\n').split(',')))
halt    = False
pointer = 0
while not halt:
    code, pointer, halt = compute(code, pointer)

# part 2
# input should be 5
print('Part 2: Input 5; answer is final diagnostic code')
code = None
with open('input5.txt') as f:
    for line in f:
        code = list(map(int, line.strip('\n').split(',')))
halt    = False
pointer = 0
while not halt:
    code, pointer, halt = compute(code, pointer)
