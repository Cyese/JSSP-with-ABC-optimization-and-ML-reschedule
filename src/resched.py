from utilities import *


class ReScheduleTime:
    counter = 1

    def __init__(self, sched: list[list[int]], loc: tuple[int, int], variant : int, weeks: int) -> None:
        
        self.sched = sched
        self.span : int 
        self.week = weeks
        self.location = loc
        self.variant = variant


    def inplace_mod(self):
        """xD hmmm
            This is weird to have because it technical affect the other as starvation of 
        """
        sched = self.sched
        x, y = self.location
        cur_oper = sched[x][y]
        if self.variant == 1: 
            sched[x].insert(y,cur_oper)
            if sched[x][-1] == 8 or sched[x][-1] == 7:
                sched[x].pop(-1)
        elif self.variant == -1: 
            sched[x].pop(y)
        self.span = max([len(_) for _ in sched])
        if not os.path.exists(f"./resched/week_{self.week}"):
            os.mkdir(f"./resched/week_{self.week}")
        with open(f"./resched/week_{self.week}/time_{ReScheduleTime.counter}.txt", "w+") as file:
            file.write(f"{x} {y} {self.variant}\n")
            for line in sched:
                file.writelines(' '.join(str(ele) for ele in line) + '\n')
        ReScheduleTime.counter += 1
        

def time_variant(weeks: int) -> dict[tuple[int,int], int]:
    span: int
    # og_sched = get_output_sched(weeks)
    # for line in og_sched:
    #     print(len(line))
    with open(f"./sched/week_{weeks}/span.txt", "r") as file:
        span = int(file.read())
    print(span)
    rate = np.array([0.05, 0.9, 0.05])
    generator = np.random.choice([-1, 0, 1], p=rate, size=(4, span))
    generator = generator.tolist()
    variants : dict[tuple[int,int], int]
    variants = {} # Matching timestep with variant 
    for x,machine in enumerate(generator):
        for y, changes in enumerate(machine):
            if changes != 0:
                variants.__setitem__((x,y) ,int(changes))
    return variants

def clean(weeks :int):
    _dir = f"./resched/week_{weeks}"
    file_list = glob.glob(_dir+ "/*.txt")
    for file in file_list:
        os.remove(file)

def gen_variants(weeks :int):
    variants=  time_variant(weeks)
    clean(weeks)
    for variant in variants:
        loc = variant
        changes = variants[loc]
        sched = get_output_sched(weeks)
        rescheduler = ReScheduleTime(sched,loc,changes,0)
        rescheduler.inplace_mod()


class ReScheduleGood:
    def __init__(self) -> None:
        pass