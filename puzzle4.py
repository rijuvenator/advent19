INPUT = [183564, 657474]

def test(num, part2=False):

    # range criterion
    if num < INPUT[0] or num > INPUT[1]:
        return False

    snum = str(num)

    # 6 digit criterion
    if len(snum) != 6:
        return False

    # non-decreasing criterion
    if snum != ''.join(sorted(snum)):
        return False

    # count how many there are of each digit
    # i.e. quick implementation of counter
    counts = {}
    for char in snum:
        if char not in counts:
            counts[char] = 0
        counts[char] += 1

    # part 1:
    # if there are any counts > 1, there must be
    # adjacent repeated digits
    # in particular, it is NOT necessary to step through
    # digit by digit
    # so set-ify the counts and compare to set(1)
    # if they're not equal, there is at least one 2+ count
    if not part2:
        if set(counts.values()) == set([1]):
            return False
        return True

    # part 2:
    # now we must ensure there is at least one count
    # of exactly 2
    # so simply check if 2 is in the set of counts
    if part2:
        if 2 in set(counts.values()):
            return True
        return False

count1 = 0
count2 = 0

for i in range(INPUT[1]+2):
    if test(i, False):
        count1 += 1

    if test(i, True):
        count2 += 1

print('Part 1:', count1)
print('Part 2:', count2)
