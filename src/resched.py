from utilities import *

# May change to more DYNAMIC way to get prob (lot more gacha)
class StaticProb:
    def __init__(self) -> None:
        self.chance = np.random.choice([False, True], p=np.array([0.95,0.05]), size = 1000).tolist() # Predrawned samplesize at runtime
        self.iter = -1
    
    def randomize(self)-> bool:
        self.iter+= 1
        return self.chance[self.iter]

class ReScheduleTime:
    count = 1
    def __init__(self, sched: list[list[int]], weeks: int) -> None:        
        self.sched = sched
        self.week = weeks
        self.span : int 
        self.location : tuple[int, int]
        self.variant : int

    def set(self, loc: tuple[int, int], variant : int):
        self.location = loc
        self.variant = variant


    def inplace_mod(self):
        sched = self.sched.copy()
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
        with open(f"./resched/week_{self.week}/time_{ReScheduleTime.count}.txt", "w+") as file:
            file.write(f"{x} {y} {self.variant}\n")
            for line in sched:
                file.writelines(' '.join(str(ele) for ele in line) + '\n')
        ReScheduleTime.count += 1


class ReScheduleGood:
    count = 1
    def __init__(self, sched: list[list[int]], weeks: int) -> None:
        """
            @param: variants: tuple [machine: int, time: int, type/job: int]
        """
        self.span : int 
        self.sched = sched
        self.week = weeks
        self.loc : tuple[int, int]


    def set(self,loc: tuple[int, int], variant : int)-> None:
        self.location = loc
        self.variant = variant

    def inplace_mod(self):
        sched = self.sched.copy()
        x,y = self.location
        batch_mark = 0
        for _ in range(y):
            if sched[x][y] == self.variant:
                batch_mark += 1
            if batch_mark ==2:
                batch_mark = 0 
        y -= batch_mark

def time_variant(weeks: int) -> dict[tuple[int,int], int]:
    span: int
    with open(f"./sched/week_{weeks}/span.txt", "r") as file:
        span = int(file.read())
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


def operate_variant(weeks: int) -> dict[tuple[int, int], int]:
    sched = get_output_sched(weeks)   
    prob = StaticProb()
    variants : dict[tuple[int, int], int] = {}
    for x, line in enumerate(sched):
        for y, item in enumerate(line):
            if prob.randomize() and item != 7 and item != 8: # Some guard case
                variants.__setitem__((x,y), item)
    return variants


def clean(weeks :int):
    _dir = f"./resched/week_{weeks}"
    file_list = glob.glob(_dir+ "/*.txt")
    for file in file_list:
        os.remove(file)

def gen_t_variants(weeks :int) -> None:
    t_variants=  time_variant(weeks)
    sched = get_output_sched(weeks)
    rescheduler = ReScheduleTime(sched,weeks)
    for t_variant in t_variants:
        loc = t_variant
        changes = t_variants[loc]
        rescheduler.set(loc,changes)
        rescheduler.inplace_mod()

def gen_o_variants(weeks: int) -> None:
    o_variants= operate_variant(weeks)
    sched = get_output_sched(weeks)
    rescheduler = ReScheduleGood(sched,weeks)
    for o_variant in o_variants:
        loc = o_variant
        changes= o_variants[loc]
        rescheduler.set(loc,changes)

    
