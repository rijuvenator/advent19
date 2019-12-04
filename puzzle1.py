# load masses
# each one is on its own line
masses = []
with open('input1.txt') as f:
    for line in f:
        masses.append(int(line.strip('\n')))

# given a mass (of whatever), compute the fuel requirement
def fueler(m):
    return (m//3)-2

# part 1
s = sum(map(fueler, masses))
print('Part 1:', s)

# part 2
# compute the initial fuel requirement
# then, in a loop, compute the fuel requirement for the fuel of the previous step
# tack it on to a growing sum
# once the new requirement is negative, break
# then tack the growing sum onto a total sum
s = 0
for mass in masses:
    fuelForThisMass = fueler(mass)
    dummy = fuelForThisMass
    while True:
        dummy = fueler(dummy)
        if dummy > 0:
            fuelForThisMass += dummy
            continue
        break
    s += fuelForThisMass
print('Part 2:', s)
