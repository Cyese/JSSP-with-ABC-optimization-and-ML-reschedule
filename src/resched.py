from utilities import json, np, glob, os, end_before, get_output_sched


def make_disturbance() -> None:
    time = time_variant()
    time_data = json.dumps(time)
    operation = operate_variant()
    operation_data = json.dumps(operation)
    with open("disturbance/time.json", "w+") as time_file:
        time_file.write(time_data)
    with open("disturbance/operation.json", "w+") as operation_file:
        operation_file.write(operation_data)


# May change to more DYNAMIC way to get prob (lot more gacha)
class StaticProb:
    def __init__(self) -> None:
        self.chance = np.random.choice([False, True], p=np.array([0.95, 0.05]),
                                       size=(4,120)).tolist()  # Predawn sample size at runtime
        self.y = -1
        self.x = 0

    def randomize(self) -> bool:
        self.y += 1
        if self.y == 120:
            self.x += 1
            self.y =0
        if self.x == 4:
            self.x = 0 
        return self.chance[self.x][self.y]


class ReScheduleTime:
    count = 1

    def __init__(self, sched: list[list[int]], weeks: int) -> None:
        # self.span = None
        # self.variant = None
        # self.location = None
        self.sched = sched
        self.week = weeks
        self.span: int
        self.location: tuple[int, int]
        self.variant: int

    def set(self, data: list[int]):
        self.location = (data[0], data[1])
        self.variant = data[2]

    def reschedule(self):
        sched = self.sched.copy()
        x, y = self.location
        cur_operation = sched[x][y]
        if self.variant == 1:
            sched[x].insert(y, cur_operation)
            if sched[x][-1] == 8 or sched[x][-1] == 7:
                sched[x].pop(-1)
        elif self.variant == -1:
            sched[x].pop(y)
        self.span = max([len(_) for _ in sched])
        with open(f"./resched/week_{self.week}/time_{ReScheduleTime.count}.txt", "w+") as file:
            file.write(f"{x} {y} {self.variant}\n")
            for line in sched:
                file.writelines(' '.join(str(ele) for ele in line) + '\n')
        ReScheduleTime.count += 1


class ReScheduleOperation:
    count = 1

    def __init__(self, sched: list[list[int]], weeks: int) -> None:
        """
            @param: variants: tuple [machine: int, time: int, type/job: int]
        """
        # self.variant = None
        # self.location = None
        self.span: int
        self.sched = sched
        self.week = weeks
        self.loc: tuple[int, int]

    def set(self, data: list[int]) -> None:
        self.location = (data[0], data[1])
        self.variant = data[2]

    def reschedule(self):
        sched = self.sched.copy()
        x, y = self.location
        batch_mark = 0
        self.variant = sched[x][y]
        for _ in range(y):
            if sched[x][_] == self.variant:
                batch_mark += 1
            if batch_mark == 2:
                batch_mark = 0
        y -= batch_mark
        # sched[x].insert(y, 8)
        # sched[x].insert(y, 8)
        sched[x][y] = 8
        sched[x][y + 1] = 8
        # let changes thing up xD
        # if in phase 2 put it add the end
        if x >= 2:  # Need to reproduce
            i: int = y
            # Do sth to find an appropriate place for it
            add1 = end_before(sched, 0)
            added = False
            for i in range(y, len(sched[add1])):
                if sched[add1][i] == self.variant:
                    sched[add1].insert(i, self.variant)
                    sched[add1].insert(i, self.variant)
                    added = True
                    break
            if not added:
                popped = 0
                while sched[add1][-1] == 8:
                    sched[add1].pop()
                    popped += 1
                sched[add1].extend([7, 7, self.variant, self.variant])
                popped -= 4
                if popped > 0:
                    sched[add1].extend([8 for _ in range(popped)])
            add2 = end_before(sched, 2)
            added = False
            if i <= len(sched[add2]) - 2:
                for z in range(i, len(sched[add2]) - 2):
                    if sched[add2][z] == self.variant:
                        sched[add2].insert(z, self.variant)
                        sched[add2].insert(z, self.variant)
                        added = True
            if not added:
                popped = 0
                while sched[add2][-1] == 8:
                    sched[add2].pop()
                    popped += 1
                sched[add2].extend([7, 7, self.variant, self.variant])
                popped -= 4
                if popped > 0:
                    sched[add2].extend([8 for _ in range(popped)])
        else:
            sched[x].insert(y + 2, self.variant)
            sched[x].insert(y + 2, self.variant)
            i: int = y + 2
            added = False
            add2 = end_before(sched, 2)
            if i < len(sched[add2]):
                for z in range(i, len(sched[add2])):
                    if sched[add2][z] == self.variant:
                        sched[add2].insert(z, self.variant)
                        sched[add2].insert(z, self.variant)
                        added = True
            if not added:
                popped = 0
                while sched[add2][-1] == 8:
                    sched[add2].pop()
                    popped += 1
                sched[add2].extend([7, 7, self.variant, self.variant])
                popped -= 4
                if popped > 0:
                    sched[add2].extend([8 for _ in range(popped)])
        with open(f"./resched/week_{self.week}/operation_{ReScheduleOperation.count}.txt", "w+") as file:
            file.write(f"{x} {y} {self.variant}\n")
            for line in sched:
                file.writelines(' '.join(str(ele) for ele in line) + '\n')
        ReScheduleOperation.count += 1


def time_variant() -> dict[int, tuple[int, int, int]]:
    span: int = 120
    rate = np.array([0.05, 0.9, 0.05])
    generator = np.random.choice([-1, 0, 1], p=rate, size=(4, span))
    generator = generator.tolist()
    variants: dict[int, tuple[int, int, int]]
    variants = {}  # Matching timestep with variant
    counter = 0
    for x, machine in enumerate(generator):
        for y, changes in enumerate(machine):
            if changes != 0:
                variants.__setitem__(counter, (x, y, int(changes)))
                counter += 1
    return variants


def operate_variant() -> dict[int, tuple[int, int, int]]:
    # sched = get_output_sched(weeks)   
    prob = StaticProb()
    variants: dict[int, tuple[int, int, int]] = {}
    counter = 0
    for x in range(4):
        for y in range(120):
            if prob.randomize():
                variants.__setitem__(counter, (x, y, 0))
                counter += 1
    return variants


def clean(weeks: int):
    _dir = f"./resched/week_{weeks}"
    file_list = glob.glob(_dir + "/*.txt")
    for file in file_list:
        os.remove(file)


def gen_t_variants(weeks: int, span: int) -> None:
    t_variants: dict
    with open(r"disturbance/time.json", "r") as time:
        data = time.read()
        t_variants = json.loads(data)
    sched = get_output_sched(weeks)
    rescheduler = ReScheduleTime(sched, weeks)
    for t_variant in t_variants:
        loc = t_variant
        changes: list[int] = t_variants[loc]
        if changes[1] > span:
            break
        rescheduler.set(changes)
        rescheduler.reschedule()


def gen_o_variants(weeks: int, span: int) -> None:
    o_variants: dict
    with open(r"disturbance/operation.json", "r") as time:
        data = time.read()
        o_variants = json.loads(data)
    sched = get_output_sched(weeks)
    rescheduler = ReScheduleOperation(sched, weeks)
    for o_variant in o_variants:
        loc = o_variant
        changes = o_variants[loc]
        if changes[1] > span:
            return
        rescheduler.set(changes)
        rescheduler.reschedule()


def gen_variant_and_reschedule(weeks: int) -> None:
    clean(weeks)
    span: int
    if not os.path.exists(f"./resched/week_{weeks}"):
        os.mkdir(f"./resched/week_{weeks}")
    with open(f"sched/week_{weeks}/span.txt", "r") as file:
        span = int(file.read())

    gen_o_variants(weeks, span)
    gen_t_variants(weeks, span)
    return


# make_disturbance()
