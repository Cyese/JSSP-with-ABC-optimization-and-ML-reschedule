from ultilities import *

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

Task = [[[] for _ in range(9)] for _ in range(4)]
# Task[x]0 = []
# Task[x]0 = []

Color_pallet = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', '', 'grey', 'white']
for x in range(4):
    for value, start, length in get_sequences(result[x]):
        if value == 0:
            Task[x][0].append((start, length))
        elif value == 1:
            Task[x][1].append((start, length))
        elif value == 2:
            Task[x][2].append((start, length))
        elif value == 3:
            Task[x][3].append((start, length))
        elif value == 4:
            Task[x][4].append((start, length))
        elif value == 5:
            Task[x][5].append((start, length))
        elif value == 7:
            Task[x][7].append((start, length))
        elif value == 8:
            Task[x][8].append((start, length))

    # Task[x][8].pop()

# print(Task[x]0)

fig, ax = plot.subplots()
for y in range(4):
    for x in range(len(Task[y])):
        if x == 6:
            continue
        for task in Task[y][x]:
            # task[x]
            ax.broken_barh([task], (y + 0.25, 0.5), facecolors=Color_pallet[x])
y_tick = [0.25 + _*0.5 for _ in range(8)]
y_label = [f"Machine {_//2 + 1}" if _ % 2 == 1 else "" for _ in range(8)]
ax.set_yticks(y_tick)
plot.yticks(rotation=90)
ax.set_yticklabels(y_label)
ax.set_xticks([_ for _ in range(0, 90, 5)])
ax.set_xlim(0, 90)
ax.set_xlabel('Time')
ax.grid(True)

plot.show()
