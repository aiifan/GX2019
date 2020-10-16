


size = 7
array = [[0] * size]

for i in range(size - 1):
    array += [[0] * size]
orient = 0
j = 0
k = 0
for i in range(1, size * size + 1):
    array[j][k] = i
    if j + k == size - 1:
        if j > k:
            orient = 1
        else:
            orient = 2
    elif (k == j) and (k >= size / 2):
        orient = 3
    elif 