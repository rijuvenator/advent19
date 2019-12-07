planets = {'COM':None}

# input is of the form parent)child
# children have one and only one parent
# so every line must specify a new, unique child
# the problems given only require that a child know its parent
# so a simple dictionary with the child name as a key and the parent name as value will suffice

with open('input6.txt') as f:
    for line in f:
        parent, child = line.strip('\n').split(')')
        planets[child] = parent

# all walking functions involve a two line idiom of the form
# planet = name
# parent = parent of name
# where "name" can be the previous parent
# so initialization can be done with planet, parent = update(name)
# and steps can be done with planet, parent = update(parent)

def update(newName):
    return newName, planets[newName]

# function to count how many steps it takes to walk to COM (which has no parent)
# every step, add one, and update. once the parent is None, we're done
# this helpfully returns 0 for COM as well
def countOrbits(name):
    count = 0
    planet, parent = update(name)
    while parent is not None:
        count += 1
        planet, parent = update(parent)

    return count

# part 1:
# add up all the counts for all the planets
count = 0
for name in planets:
    count += countOrbits(name)

print('Part 1:', count)

# part 2:
# solution is in two parts
# first: store a list of planets from YOU to COM
# second: start walking down the path from SAN to COM, keep track of how many bodies
# as SOON as the parent is in the YOU path, we've found the common parent
# the index tells you # steps from YOU to common parent;
# the count tells you # steps from SAN to common parent
# return the sum of the two
def transfersFromYOUToSAN():
    name = 'YOU'
    path = []
    planet, parent = update(name)
    while parent is not None:
        path.append(parent)
        planet, parent = update(parent)

    name = 'SAN'
    count = 0
    planet, parent = update(name)
    while parent not in path:
        count += 1
        planet, parent = update(parent)

    return path.index(parent) + count

print('Part 2:', transfersFromYOUToSAN())
