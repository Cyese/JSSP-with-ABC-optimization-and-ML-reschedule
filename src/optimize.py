"""Parameter:
    population = 400
    best_site_No = 10
    number_of_elite_site = 6
    recruited_for_best = 10
    recruitedfor_elite = 10
    neighboor_size = 10
    q1 = 0.7
"""
from utilities import *
from schedule import PhaseBaseSchedule

class Bee:
    def __init__(self, arr: list[list[int]]) -> None:
        """ Expect arr to have 2 list of int each represent phase1 
            Scout class will have to use schedule module to re-phrase the schedule in to usable state
        """
        self.solution = arr.copy()

    def search(self) -> tuple[list,int]:
        q2 = np.random.random()
        if q2 <= 0.3:
            self.interchange()
        elif 0.3< q2 <= 0.7:
            self.shift()
        else:
            self.inverse()
        scheduler = PhaseBaseSchedule(self.solution)
        return scheduler.run()

    def interchange(self):
        """Has 2 random behaviour and randomly run one of the 2 ():
            @ (1): exchange 2 random part in side the operation string
            @ (2): slice the longer end into smaller part
        """
        series_1 = node_encode(self.solution[0])
        series_2 = node_encode(self.solution[1])
        inter_type = np.random.randint(0,2)
        if inter_type >= 1:
            # Exchange in between
            x = np.random.choice(range(len(series_1)))
            y = np.random.choice(range(len(series_2)))
            series_1[x], series_2[y] = series_2[y],series_1[x]
        else:
            # Extend one with part of other diff
            l1, l2 = sum([_[1] for _ in series_1]), sum(_[1] for _ in series_2) 
            if l1 > l2:
                snd ,rcv = series_1, series_2
            else:
                rcv ,snd = series_1, series_2
            end_node= snd.pop()
            split  = int(np.random.randint(range(end_node[1])))
            rcv.append((end_node[0], split))
            snd.append((end_node[0], end_node[1]- split))

        self.solution[0] = node_decode(series_1)
        self.solution[1] = node_decode(series_2)
        return

    def inverse(self):
        """Get a piece of a random set of node \n
        Inverse that and re-insert
        """
        line = np.random.randint(0,2)
        series = node_encode(self.solution[line])
        start_index = np.random.choice(range(len(series)-1))  # Ensure that there will always be 2 node if possible
        end_index = np.random.choice(range(start_index+2, len(series)+1))
        hold = series[start_index: end_index]
        hold.reverse()
        series[start_index: end_index] = hold
        self.solution[line] = node_decode(series)
        return

    def shift(self):
        """Choose a sequence and randomly move it to other place in the sequence
        """
        line = np.random.randint(0,2)
        series = node_encode(self.solution[line])
        seq = series.pop(np.random.choice(range(len(series))))
        mod_rate = [4 if _[0] == seq[0] else 1 for _ in series]  # typical off-banner rate_up
        mod_rate.append(1)
        mod_rate = np.array(mod_rate)
        series.insert(np.random.choice(range(len(series)), p= mod_rate), seq)
        self.solution[line] = node_decode(series)
        return


class Scout:
    def __init__(self) -> None:
        pass
    pass

class BeeColony:
    def __init__(self, weeks: int) -> None:
        self.population = 400
        self.best_site_No = 10
        self.number_of_elite_site = 6
        self.recruited_for_best = 10
        self.recruitedfor_elite = 10
        self.neighboor_size = 10
        self.path, self.fitness = get_initial_fitness(weeks)
