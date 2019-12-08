DIMENSIONS = (25, 6)
LAYERSIZE = DIMENSIONS[0] * DIMENSIONS[1]

with open('input8.txt') as f:
    for line in f:
        pixels = list(map(int, list(line.strip('\n'))))

# part 1
# store 1D arrays for each LAYER (which have 2D structure, but I don't need it yet)
# keep track of which layer has the fewest zeros: in index, it's just the current nLayers-1
# do this by keeping track of the min number of zeroes in the usual way with inf --> update
# loop over indices messily with range(0, nPixels, LayerSize)
# cut up pixels with pixels[ i : i+LAYERSIZE ]
# count zeroes, etc.
# answer is the fewest 0 layer count 0 * count 1

layers = []
which = 0
nZeros = float('inf')

for i in range(0, len(pixels), LAYERSIZE):
    layers.append(pixels[i:i+LAYERSIZE])
    x = layers[-1].count(0)
    if x < nZeros:
        nZeros = x
        which = len(layers)-1

print('Part 1:', layers[which].count(1)*layers[which].count(2))


# part 2
# compute the top pixel for each position -- there are LAYERSIZE such positions
# for each position, loop through the layers until you hit something that isn't 2
# then tack that on to the image and move on

image = []
for pos in range(LAYERSIZE):
    for layer in layers:
        if layer[pos] != 2:
            image.append(layer[pos])
            break

# convert takes a 0 and prints a black __; 1 prints and white __
def convert(c):
    if c == 0:
        return '\033[40m  \033[m'
    else:
        return '  '

# for each row in the computed image
# the row is image [ row * dimX : (row+1) * dimX ]
# now print it prettily:  convert every integer in the row to a black/white box with convert
# then join them all together and print

print('Part 2:')
for row in range(DIMENSIONS[1]):
    imagerow = image[row*DIMENSIONS[0]:(row+1)*DIMENSIONS[0]]
    print(''.join(map(convert, imagerow)))
