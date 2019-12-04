########################
#### POSITION CLASS ####
########################

# the heart of this solution: a Position class
class Position():
    # initialize with the current position, the direction it came from, and the amount it came from
    # the amount is not necessary for part 1, but it is for part 2
    def __init__(self, x, y, lastDir, amount):
        self.x = x
        self.y = y
        self.lastDir = lastDir
        self.amount = amount

    # increment makes a new position with that information given one of the LRDU + number tags
    def increment(self, direction, amount):
        newX, newY = self.x, self.y

        if   direction == 'L':
            newX -= amount

        elif direction == 'R':
            newX += amount

        elif direction == 'D':
            newY -= amount

        elif direction == 'U':
            newY += amount

        return Position(newX, newY, direction, amount)

    # displacement computes a displacement vector between this position and another position
    # (initially conceived to be the next position)
    # that vector is returned with a 0 for amount and lastDir = which way the displacement was
    def displacement(self, other):
        disp = Position(other.x - self.x, other.y - self.y, None, 0)

        if disp.x == 0:
            if disp.y > 0:
                disp.lastDir = 'U'
            else:
                disp.lastDir = 'D'
        elif disp.y == 0:
            if disp.x > 0:
                disp.lastDir = 'R'
            else:
                disp.lastDir = 'L'

        return disp

    # given two displacements, determine if they are orthogonal
    def isOrthogonal(self, other):
        if   self.lastDir in 'LR' and other.lastDir in 'UD':
            return True
        elif self.lastDir in 'UD' and other.lastDir in 'LR':
            return True
        return False

    # compute manhattan distance from (0, 0) -- interpret carefully if this is a displacement
    def manhattan(self):
        return abs(self.x) + abs(self.y)

    # string representations
    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

###################
#### FUNCTIONS ####
###################

# functions that operate on multiple positions or require context

# abstracts away checking whether things are LRDU etc.
# an x coordinate lies between 2 points on a wire if it is between the min of the x's and the max of the x's
# same for y
def checkIfPosBetween(pos1, pos2, pos, coord):
    return min(getattr(pos1, coord), getattr(pos2, coord)) < getattr(pos, coord) < max(getattr(pos1, coord), getattr(pos2, coord))

# given segment of wire 1 (pos11 to pos12) and of wire 2 (pos21 to pos22)
# compute the displacement vectors (so recovering the LRDU code)
# if they're orthogonal, find the coordinates in common for each of two cases
# return the position if it all works out; otherwise False
def checkIfCross(pos11, pos12, pos21, pos22):
    disp1 = pos11.displacement(pos12)
    disp2 = pos21.displacement(pos22)

    if disp1.isOrthogonal(disp2):
        if disp1.lastDir in 'LR': 
            if checkIfPosBetween(pos11, pos12, pos21, 'x') and \
               checkIfPosBetween(pos21, pos22, pos11, 'y'):
                return Position(pos21.x, pos11.y, None, 0)
            return False
        if disp1.lastDir in 'UD':
            if checkIfPosBetween(pos11, pos12, pos21, 'y') and \
               checkIfPosBetween(pos21, pos22, pos11, 'x'):
                return Position(pos11.x, pos21.y, None, 0)
            return False

    return False

# given a wire segment list and a pos, compute the number of grid points
# the wire passes through to get to that position FIRST
# i.e. loop over all the segments from the beginning again, check for the common coordinate,
# compute the number of steps up until that position (including the current amount),
# then add on the displacement -- extra steps for the LAST segment under consideration
def nStepsTillPos(wires, pos):
    for i in range(len(wires)-1):
        pos1, pos2 = wires[i], wires[i+1]
        steps = sum([w.amount for w in wires[:i+1]])
        if pos1.x == pos2.x and pos1.x == pos.x and checkIfPosBetween(pos1, pos2, pos, 'y'):
            return steps + pos1.displacement(pos).manhattan()
        if pos1.y == pos2.y and pos1.y == pos.y and checkIfPosBetween(pos1, pos2, pos, 'x'):
            return steps + pos1.displacement(pos).manhattan()
    return None

##############
#### MAIN ####
##############

wire_dirs = {}

# test cases
#wire_dirs[1] = ['R8','U5','L5','D3']
#wire_dirs[2] = ['U7','R6','D4','L4']
#wire_dirs[1] = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
#wire_dirs[2] = ['U62','R66','U55','R34','D71','R55','D58','R83']

# i+1 because I call it wire 1 and 2
# strip the newline and split on , to get a list of direction/amounts
with open('input3.txt') as f:
    for i, line in enumerate(f):
        wire_dirs[i+1] = line.strip('\n').split(',')

# prepare to compute positions instead of segments
wire_pos = {}
wire_pos[1] = [Position(0, 0, None, 0)]
wire_pos[2] = [Position(0, 0, None, 0)]

# hard work is now done by the class
# segments are of the form [LRDU]\d+
# so get the direction and the amount
# get the previous position
# increment by the direction and amount
# tack on the new position
for wire in (1, 2):
    for move in wire_dirs[wire]:
        direction = move[0]
        amount = int(move[1:])

        currentPos = wire_pos[wire][-1]
        newPos = currentPos.increment(direction, amount)
        wire_pos[wire].append(newPos)


################
#### PART 1 ####
################

# for each position in wire 1, look at it + the next one
# for each position in wire 2, look at it + the next one
# compute a possible crossing -- it's either None or a Position
# if it's Position, update minDist if the Manhattan distance of the crossing is smaller than the current min
minDist = float('inf')

# loop over pairs
for i in range(len(wire_pos[1])-1):
    pos11, pos12 = wire_pos[1][i], wire_pos[1][i+1]
    for j in range(len(wire_pos[2])-1):
        pos21, pos22 = wire_pos[2][j], wire_pos[2][j+1]

        # compute crossing
        possibleCross = checkIfCross(pos11, pos12, pos21, pos22)
        if possibleCross:

            #print(pos11, 'to', pos12, 'crosses', pos21, pos22, 'at', possibleCross, ':', possibleCross.manhattan())

            # update
            if possibleCross.manhattan() < minDist:
                minDist = possibleCross.manhattan()

print('Part 1:', minDist)

################
#### PART 2 ####
################

# the tricky part here is "use the FIRST time the wire passes through the grid point to compute the number of steps"
# so this is a slow solution. again, compute a possible intersection
# then, compute the number of steps for each wire separately, stopping at the FIRST one
# then add them together, etc.
minDelay = float('inf')

# loop over pairs
for i in range(len(wire_pos[1])-1):
    pos11, pos12 = wire_pos[1][i], wire_pos[1][i+1]
    for j in range(len(wire_pos[2])-1):
        pos21, pos22 = wire_pos[2][j], wire_pos[2][j+1]

        # compute crossing
        possibleCross = checkIfCross(pos11, pos12, pos21, pos22)
        if possibleCross:

            # compute nSteps
            wire1Steps = nStepsTillPos(wire_pos[1], possibleCross)
            wire2Steps = nStepsTillPos(wire_pos[2], possibleCross)
            candidateDelay = wire1Steps + wire2Steps

            # update
            if candidateDelay < minDelay:
                minDelay = candidateDelay

print('Part 2:', minDelay)
