from machine import *
from ultilities import *

Total_time = 16*5*2


class Schedule:
    def __init__(self, task_list: list[int | float]) -> None:
        # 2 Line of production
        self.Line1 = [
            MachinePhase1(12000,2),
            MachinePhase2(3000)
        ]
        self.Line2 = [
            MachinePhase1(6000,2),
            MachinePhase2(2800)
        ]
        # Task for storing all pending task
        # Task1 & 2 represent task for each line
        # Each slot represent [Demand left, Phase 1 out, Phase 2 out]
        self.Tasks = [task for task in task_list]
        self.task1 = [[int,int,int] for _ in range(3)]
        self.task2 = [[int,int,int] for _ in range(3)]
        self.limit = Total_time
        self.Operate1 = [[-1,8] for _ in range(3)]
        self.Operate2 = [[-1,8] for _ in range(3)]
    
