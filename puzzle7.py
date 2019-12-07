import itertools

##########################
#### INTCODE COMPUTER ####
##########################

# run as follows:
#   computer = IntcodeComputer(code)
#   computer.run()
#
# for programmatic inputs,
#   computer = IntcodeComputer(code, inputs=[1, 2, ...])
# or
#   computer = IntcodeComputer(code)
#   computer.setInputs([1, 2, ...])
# before running
#
# for programmatic outputs,
#   computer = IntcodeComputer(code, storeOutputs=True)
# or
#   computer = IntcodeComputer(code)
#   computer.setStoreOutputs()

class IntcodeComputer():

    NPARAM = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 99:0}

    # initialize with the program to be run
    def __init__(self, intcode, inputs=None, storeOutputs=False):
        self.intcode = intcode[:]
        self.pointer = 0
        self.halt    = False
        self.wait    = False

        self.setInputs(inputs)
        self.setStoreOutputs(storeOutputs)

    # wrapper for setting inputs
    def setInputs(self, inputs):
        if inputs is not None:
            self.inputs = list(reversed(inputs))
        else:
            self.inputs = None

    # wrapper for programmatically adding inputs
    # inputs are consumed by popping off a stack, so
    # adding inputs must be done by adding to the front
    def addInput(self, code):
        if self.inputs is not None:
            self.inputs.insert(0, code)

    # wrapper for storing outputs
    def setStoreOutputs(self, flag=True):
        self.storeOutputs = flag
        if self.storeOutputs:
            self.outputs = []

    # for debugging purposes
    # print the current pointer, the halt and wait booleans, the inputs and outputs
    # inputs should be represented in reverse order so that inputs can be popped on and off
    def inspectState(self):
        print('Pointer: {:3d} Halt: {:5s} Wait: {:5s} Inputs: {} Outputs: {}'.format(
            self.pointer,
            str(self.halt),
            str(self.wait),
            self.inputs,
            self.outputs,
        ))

    # run the computer from pointer 0 with the stored program
    # the WAIT boolean PAUSES execution if there are not enough inputs
    # the only time WAIT is currently True is if there is a pending input
    # so assert that there's at least one input before resetting WAIT and continuing
    def run(self):
        if self.wait:
            assert(len(self.inputs) > 0)
            self.wait = False
        while not self.halt and not self.wait:
            self.compute()

    # implementation of parameter modes
    # don't use for write positions (implicitly mode 0, nothing to get)
    # mode 0: position mode
    # mode 1: immediate mode
    def getValue(self, p, mode):
        if mode == 0:
            return self.intcode[p]
        if mode == 1:
            return p
        raise Exception('Unknown parameter mode {}'.format(mode))

    # given a pointer, cut up the opcode and get the modes
    # Suppose the opcode is 01102: this is opcode 2, with the params in mode 1 1 0
    # so get 110 by doing 01102 // 100 ( = 11), right justifying with 0s ( = 011), and reversing
    def getModes(self, p):
        opcode   = self.intcode[p] % 100
        if opcode not in IntcodeComputer.NPARAM:
            raise Exception('{} is not a valid op code'.format(opcode))
        parcodes = str(self.intcode[p] // 100).rjust(IntcodeComputer.NPARAM[opcode], '0')
        modes    = list( reversed([ int(i) for i in parcodes ]) )
        return modes

    # main computer
    # processes the intcode at the current pointer
    def compute(self):

        p = self.pointer

        # opcode is the last two digits of intcode[p]
        # modes are the parameter modes, in the correct order (and of the correct length of parameters)
        # parameters are just intcode[p+1] through intcode[p+1 + nParams]
        # newp is where the pointer should move to; this is usually p + nParams + 1

        opcode = self.intcode[p] % 100
        modes  = self.getModes(p)
        params = self.intcode[p + 1 : p + IntcodeComputer.NPARAM[opcode] + 1]
        newp   = p + IntcodeComputer.NPARAM[opcode] + 1

        # add
        if   opcode == 1:
            x, y, o = params
            self.intcode[o] = self.getValue(x, modes[0]) + self.getValue(y, modes[1])

        # multiply
        elif opcode == 2:
            x, y, o = params
            self.intcode[o] = self.getValue(x, modes[0]) * self.getValue(y, modes[1])

        # input
        elif opcode == 3:
            o = params[0]

            # get input from the command line if inputs is None
            if self.inputs is None:
                i = input('Provide input: ')

            # get input by popping off the inputs list if it exists
            else:

                # consume the next available input
                if len(self.inputs) > 0:
                    i = self.inputs.pop()

                # if there aren't any, pause execution
                # the run loop will break when this wait boolean is True
                # immediately end the computation
                # the next time run is called, wait will be reset to False
                # no pointers have changed, no modifications were made
                # so execution will resume from where it last left off
                else:
                    self.wait = True
                    return

            self.intcode[o] = int(i)

        # output
        elif opcode == 4:
            x = params[0]

            # print output or store the outputs
            value = self.getValue(x, modes[0])
            if not self.storeOutputs:
                print(value)
            else:
                self.outputs.append(value)

        # jump if true
        elif opcode == 5:
            t, v = params
            if self.getValue(t, modes[0]) != 0:
                newp = self.getValue(v, modes[1])

        # jump if false
        elif opcode == 6:
            t, v = params
            if self.getValue(t, modes[0]) == 0:
                newp = self.getValue(v, modes[1])

        # less than
        elif opcode == 7:
            a, b, o = params
            if self.getValue(a, modes[0]) < self.getValue(b, modes[1]):
                self.intcode[o] = 1
            else:
                self.intcode[o] = 0

        # equal to
        elif opcode == 8:
            a, b, o = params
            if self.getValue(a, modes[0]) == self.getValue(b, modes[1]):
                self.intcode[o] = 1
            else:
                self.intcode[o] = 0

        # halt
        elif opcode == 99:
            self.pointer = newp
            self.halt    = True
            return

        # error
        else:
            raise Exception('{} is not a valid op code'.format(opcode))

        self.pointer = newp
        self.halt    = False


####

master = None
with open('input7.txt') as f:
    for line in f:
        master = list(map(int, line.strip('\n').split(',')))

# part 1
# try every phase setting
# initialize an input
# loop over the amplifiers
# inputs are the phase setting and the ampInput
# run the computer, store the output into ampInput for the next round
# update the max

maxOutput = 0
for phaseSettings in itertools.permutations(range(5)):
    ampInput = 0
    for amplifier in range(5):
        computer = IntcodeComputer(master, inputs=[phaseSettings[amplifier], ampInput], storeOutputs=True)
        computer.run()
        ampInput = computer.outputs.pop()

    currentOutput = ampInput
    if currentOutput > maxOutput:
        maxOutput = currentOutput

print('Part 1:', maxOutput)

# part 2
# try every phase setting
# initialize 5 computers
# initially, all inputs are just the phase settings
# initialize an input
# start an infinite loop
# add the previous input into the list of inputs
# run the computer
# it will either halt (99) or wait
# for this problem, either halt or wait SHOULD guarantee an output
# store the output into the next input
# rest of the logic is the same as above

maxOutput = 0
for phaseSettings in itertools.permutations(range(5, 10)):

    computers = [IntcodeComputer(master, inputs=[phaseSettings[i]], storeOutputs=True) for i in range(5)]

    ampInput = 0
    for amplifier in itertools.cycle(range(5)):
        computers[amplifier].addInput(ampInput)
        computers[amplifier].run()
        ampInput = computers[amplifier].outputs.pop()
        if amplifier == 4 and computers[amplifier].halt:
            break

    currentOutput = ampInput
    if currentOutput > maxOutput:
        maxOutput = currentOutput

print('Part 2:', maxOutput)
