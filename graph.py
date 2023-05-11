from ultilities import *
import matplotlib.pyplot as plot

weeks = 0
path = 0
result = []
with open("D:/Project/SisThesis/population/week_{}/path_{}.txt".format(weeks, path), "r") as file:
    lines = file.readlines()
for line in lines:
    result.append([int(_) for _ in line.split()])

# print(result)

# print(result[0])

"""
    format: 
    y : [] task[x] name
    width : [] task[x] duration
    left: start time
"""

def get_sequences(lst: list[int]):
    # Initialize variables to track the current sequence
    start_index = 0
    current_value = lst[0]
    current_length = 1

    # Iterate over the list starting from the second element
    for i in range(1, len(lst)):
        if lst[i] == current_value:
            # If the current element is the same as the previous element,
            # increment the current sequence length
            current_length += 1
        else:
            # If the current element is different from the previous element,
            # yield the current sequence and start a new one
            yield (lst[start_index],start_index, current_length)
            start_index = i
            current_value = lst[i]
            current_length = 1

    # Yield the final sequence
    yield (lst[start_index],start_index, current_length)

Task = [[[] for _ in range(9)] for _ in range(4)]
# Task[x]0 = []
# Task[x]0 = []

# colorset = []
colorset = ['red','orange','yellow','green','blue','purple', '','grey', 'black']
for x in range(4):
    for value, start, length in get_sequences(result[x]):
        if value == 0:
            Task[x][0].append((start,length))
        elif value == 1:
            Task[x][1].append((start,length))
        elif value == 2:
            Task[x][2].append((start,length))
        elif value == 3:
            Task[x][3].append((start,length))
        elif value == 4:
            Task[x][4].append((start,length))
        elif value == 5:
            Task[x][5].append((start,length))
        elif value == 7:
            Task[x][7].append((start,length))
        elif value == 8:
            Task[x][8].append((start,length))

    # Task[x][8].pop()

# print(Task[x]0)

fig, ax = plot.subplots()
for y in range(4):
    for x in range(len(Task[y])):
        if x == 6: 
            continue
        for task in Task[y][x]:
            # task[x]
            ax.broken_barh([task], (y*0.5, 0.5), facecolors=colorset[x])
ytick = [0,0.5,1,1.5,2]
ylabel = ['','Phase1','','Phase2','']
ax.set_yticks(ytick)
ax.set_yticklabels(ylabel)
ax.set_xticks([_ for _ in range(0,90,5)])
ax.set_xlim(0, 90)
ax.set_xlabel('Time')
ax.grid(True)

plot.show()