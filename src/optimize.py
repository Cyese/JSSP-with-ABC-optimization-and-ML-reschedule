from ultilities import * 

population = 100
scout_number = 20
follower = 10

class Bee:
    @staticmethod
    def fitness_evalutation(makespan: int) -> float:  # Suppose to change to match the matrix that used this thing
        return 1/(1+ makespan)
    def __init__(self, solution: list[list[int]]) -> None:
        self.sol = solution


class ScoutBee(Bee):
    def __init__(self, solution: list[list[int]]) -> None:
        super().__init__(solution)
        