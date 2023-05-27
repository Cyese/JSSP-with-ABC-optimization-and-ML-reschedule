from utilities import *


def clean(weeks: int):
    _directory = f"./sched/week_{weeks}"
    images_list = glob.glob(_directory + "/*.png")
    for image in images_list:
        os.remove(image)


def draw_chart(weeks: int, limit: int):
    clean(weeks)
    result = []
    with open("./sched/week_{}/raw.txt".format(weeks), "r") as file:
        lines = file.readlines()
    for line in lines:
        result.append([int(_) for _ in line.split()])
    """
        format: 
        y : [] task[x] name
        width : [] task[x] duration
        left: start time
    """
    Task = [[[] for _ in range(9)] for _ in range(4)]
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
    fig, ax = plot.subplots()
    for y in range(4):
        for x in range(len(Task[y])):
            if x == 6:
                continue
            for task in Task[y][x]:
                # task[x]
                ax.broken_barh([task], (y + 0.25, 0.5), facecolors=Color_pallet[x])
    y_tick = [0.25 + _ * 0.5 for _ in range(8)]
    y_label = [f"Machine {_ // 2 + 1}" if _ % 2 == 1 else "" for _ in range(8)]
    ax.set_yticks(y_tick)
    plot.yticks(rotation=90)
    ax.set_yticklabels(y_label)
    limit = (int(limit / 5) + 2) * 5
    ax.set_xticks([_ for _ in range(0, limit, 5)])  # Need fixing
    ax.set_xlim(0, limit)
    ax.set_xlabel('Time')
    ax.set_title("GBA")
    ax.grid(True)
    plot.savefig(r'./sched/week_{}/result'.format(weeks))
    plot.close()


def draw_sample(weeks: int):
    result, limit = [], None
    _path = np.random.randint(0, 100)
    with open("./sample/week_{}/span.txt".format(weeks), "r") as file:
        lines = file.readlines()
        sth = [int(line.strip()) for line in lines]
        limit = sth[_path]
    with open("./sample/week_{}/path_{}.txt".format(weeks, _path), "r") as file:
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
    y_tick = [0.25 + _ * 0.5 for _ in range(8)]
    y_label = [f"Machine {_ // 2 + 1}" if _ % 2 == 1 else "" for _ in range(8)]
    ax.set_yticks(y_tick)
    plot.yticks(rotation=90)
    ax.set_yticklabels(y_label)
    limit = (int(limit / 5) + 2) * 5
    ax.set_xticks([_ for _ in range(0, limit, 5)])  # Need fixing
    ax.set_xlim(0, limit)
    ax.set_xlabel('Time')
    ax.grid(True)
    ax.set_title("GA")
    plot.savefig(r'./sched/week_{}/sample_{}'.format(weeks, _path))
    plot.close()


def display(weeks: int):
    _directory = f"./sched/week_{weeks}"
    fig, axes = plot.subplots(nrows=1, ncols=2)
    images_list = glob.glob(_directory + "/*.png")
    for i, image in enumerate(images_list):
        _image = Image.open(image)
        axes[i].imshow(_image)
        axes[i].axis('off')
        _image.close()
    plot.tight_layout()
    plot.show()
    return
