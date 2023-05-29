"""Parameter:
    population = 400
    best_site_No = 10
    number_of_elite_site = 6
    recruited_for_best = 10
    recruited_for_elite = 10
    neighbour_size = 10
    q1 = 0.7
"""
# from utilities import *
from populate import *


class Bee:
    def __init__(self, arr: list[list[int]]) -> None:
        """ Expect arr to have 2 list of int each represent phase1 
            Scout class will have to use schedule module to re-phrase the schedule in to usable state
        """
        self.solution = [[x for x in y] for y in arr]
        self.save = self.solution.copy()
        self.Key = self.calc_fitness()

    def search(self) -> tuple[list, int]:
        for __ in range(10):
            for _ in range(5):
                q2 = np.random.random()
                if q2 <= 0.3:
                    self.interchange()
                elif 0.3 < q2 <= 0.7:
                    self.shift()
                else:
                    self.inverse() 
            new_key =self.calc_fitness()
            if new_key < self.Key:
                self.Key = new_key
                self.save = self.solution
                self.solution = self.save.copy()
        return self.save, self.Key

    def interchange(self):
        """Has 2 random behaviour and randomly run one of the 2 ():
            @ (1): exchange 2 random part in side the operation string
            @ (2): slice the longer end into smaller part
        """
        series_1 = node_encode(self.solution[0])
        series_2 = node_encode(self.solution[1])
        inter_type = np.random.randint(0, 2)
        if inter_type >= 1:
            # Exchange in between
            x = np.random.choice(range(len(series_1)))
            y = np.random.choice(range(len(series_2)))
            series_1[x], series_2[y] = series_2[y], series_1[x]
        else:
            # Extend one with part of other diff
            l1, l2 = sum([_[1] for _ in series_1]), sum(_[1] for _ in series_2)
            if l1 > l2:
                snd, rcv = series_1, series_2
            else:
                rcv, snd = series_1, series_2
            end_node = snd.pop()
            split = np.random.choice(range(end_node[1]))
            snd.append((end_node[0], end_node[1] - split))
            add = True
            for i,x in enumerate(rcv):
                if x[0] == end_node[0]:
                    rcv.insert(i,(end_node[0], split))
                    add = False 
                    break
            if add:
                rcv.append((end_node[0], split))
        self.solution[0] = node_decode(series_1)
        self.solution[1] = node_decode(series_2)
        return

    def inverse(self):
        """Get a piece of a random set of node \n
        Inverse that and re-insert
        """
        line = np.random.randint(0, 2)
        series = node_encode(self.solution[line])
        if len(series) <= 1:
            return
        start_index, end_index = sorted(np.random.choice(range(len(series)), size=2, replace=False))
        hold = series[start_index: end_index]
        hold.reverse()
        series[start_index: end_index] = hold
        self.solution[line] = node_decode(series)
        return

    def shift(self):
        """Choose a sequence and randomly move it to other place in the sequence
        """
        line = np.random.randint(0, 2)
        series = node_encode(self.solution[line])
        if len(series) == 1:
            return
        seq = series.pop(np.random.choice(range(len(series))))
        # series.insert(np.random.choice(range(len(series) + 1), p=mod_rate), seq)
        add = True
        for i,x in enumerate(series):
            if x[0] == seq[0]:
                series.insert(i,seq)
                add = False 
                break
        if add:
            series.insert(np.random.choice(range(len(series) + 1)), seq)
        self.solution[line] = node_decode(series)
        return

    def calc_fitness(self) -> int:
        lines: list[int] = [0,0]
        for k, line in enumerate(self.solution):
            for i,batch in enumerate(line):
                prev = 0
                if i==0:
                    prev = batch
                elif batch != prev:
                    prev = batch
                    lines[k] +=2
                lines[k] += 2
        return max(lines)
                
class Scout:
    def __init__(self, weeks: int, _path: int, fitness: int) -> None:
        self.solution = ORead(weeks, _path)
        self.fitness = self.cal_fitness()
        # self.OriginalKey = [self.solution[0].count(_) + self.solution[0].count(_) for _ in range(6)]

    def cal_fitness(self)-> int:
        lines: list[int] = [0,0]
        for k, line in enumerate(self.solution):
            for i,batch in enumerate(line):
                prev = 0
                if i==0:
                    prev = batch
                elif batch != prev:
                    prev = batch
                    lines[k] +=2
                lines[k] += 2
        return max(lines)

    def get(self):
        return self.solution, self.fitness

    def set(self, solution: list[list[int]], fitness):
        self.solution = solution
        self.fitness = fitness


class BeeColony:
    def __init__(self, weeks: int) -> None:
        populated(weeks)
        self.population = 400
        self.best_site_No = 10
        self.elite_site_No = 6
        self.recruited_for_best = 10
        self.recruited_for_elite = 10
        self.neighbour_size = 40
        self.path, self.fitness = get_initial_fitness(weeks, 10)
        self.para = weeks
        self.abandon = []
        self.ScoutBee: list[Scout] = []

    def neighbour_optimize(self):
        best_site = self.fitness.index(min(self.fitness))
        scout = Scout(self.para, self.path.pop(best_site), self.fitness.pop(best_site))
        for _ in range(self.neighbour_size):
            cur_sol, cur_fit = scout.get()
            new_Bee = Bee(cur_sol)
            new_sol, new_fit = new_Bee.search()
            if new_fit < cur_fit:
                scout.set(new_sol, new_fit)
        return scout

    def global_search(self):
        # To improve: try to implement sth Wheel / Crossover
        best = self.ScoutBee[0]
        for scout in self.ScoutBee:
            if scout.fitness < best.fitness:
                best = scout
        return best

    def optimize(self) -> int:
        for x in range(10):
            self.ScoutBee.append(self.neighbour_optimize())
        best = self.global_search()
        solution, cycle = PhaseBaseSchedule(best.solution).run()
        if not os.path.exists(f"./sched/week_{self.para}"):
            os.mkdir(f"./sched/week_{self.para}")
        with open(r'./sched/week_{}/raw.txt'.format(self.para), "w+") as file:
            for x in solution:
                file.writelines(' '.join(str(_) for _ in x) + '\n')
        with open(r'./sched/week_{}/span.txt'.format(self.para), "w+") as file:
            file.write(str(cycle))
        return cycle
