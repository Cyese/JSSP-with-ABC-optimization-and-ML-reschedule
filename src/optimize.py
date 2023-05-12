from ultilities import * 

"""Parameter:
    population = 400
    best_site_No = 10
    number_of_elite_site = 6
    recruited_for_best = 10
    recruitedfor_elite = 10
    neighboor_size = 10
    q1 = 0.7

"""


class Bee:
    def __init__(self, arr: list[list[int]]) -> None:
        self.solution = arr.copy()

    def search(self) -> list:
        q2 = np.random.random()
        if q2 <= 0.3:
            self.interchange()
        elif 0.3< q2 <= 0.7:
            self.shift()
        else:
            self.inverse()
        return self.solution

    def interchange(self):
        # block_a= sorted(np.random.choice(range(len(self.solution[0])), size=2, replace=False).tolist())
        # block_b= sorted(np.random.choice(range(len(self.solution[1])), size=2, replace =False).tolist())
        # new_upper = [self.solution[0][_] if a <= block_a[0] or a > block_a[2] for _ in range(len(sel.solution[0]))]
        inter_type = np.random.random()
        if inter_type >= 0.5:
            # Exchange in between
            pass
        else:
            # Extend one with part of other diff
            pass    
        
        pass


    def inverse(self):
        # Get a piece of a random set
        # Inverse that and re-insert
        pass

    def shift(self):
        # Choose a sequence of a same job if available the shift it together
        pass


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
