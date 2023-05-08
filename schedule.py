from machine import *
from ultilities import *
# from queue import Queue

Total_time = 16*5*2


class Schedule:
    def __init__(self, task_list: list[int|float]) -> None:
        # 2 Line of production
        self.MachineLine : list[list[MachinePhase1 | MachinePhase2]]
        
        
        self.MachineLine = [[
            MachinePhase1(12000,2),
            MachinePhase2(3000)
        ],[
            MachinePhase1(6000,2),
            MachinePhase2(2800)
        ]]
        # Task for storing all pending task
        # Table[x -> Phase][y -> Task]
        # self.Tasks = [task for task in task_list]
        self.TaskByLine1 : list[int]
        self.TaskByLine2 : list[int]
        self.Table = [[task for task in task_list],
                        [0 for _ in range(6)],
                        [0 for _ in range(6)]
                    ]
        self.limit = Total_time
        self.arange_task()
        # Operate[x -> Line][y -> Phase][z : 0 | 1 -> task | cycle_tim 
        self.Operate = [[[-1,8] for _ in range(2)],[[-1,8] for _ in range(2)]]
        self.Queue1 = []
        self.Queue2 = []
        return

    def arange_task(self) -> None:
        self.TaskByLine1, self.TaskByLine2 = split_task(self.Table[0])
        return

    def dispatch_P1(self, line: int, rate_decision : int = 0) -> None:
        task : list[int]
        if line ==1:
            task = self.TaskByLine1
        else:
            task = self.TaskByLine2
        rate = []
        for i in range(3):
            value = self.Table[0][task[i]]/ self.MachineLine[line][1].capacity
            rate.append(value)
        rate = np.array(rate)
        if rate.sum() == 0:
            choice = -1 
        else:
            if rate_decision ==1: 
                rate = rate.sum()/ rate
                prate = rate/ rate.sum()
            else:
                prate = rate /rate.sum()
            choice = np.random.choice(task, p=prate)
        self.MachineLine[line][0].assign(choice)
        self.Operate[line][0] = [choice, 0]
        return
    
    def dispatch_P2(self, line: int) -> None:
        task : list[int]
        # choice : int
        if line ==1:
            task = self.TaskByLine1
        else:
            task = self.TaskByLine2
        
        if sum(self.Table[self.MachineLine[line][1].get_config()]) <= 0: # No more to produce
            choice = get_max(self.Table, task)
            if choice == -1:
                pass
            else: 
                self.MachineLine[line][1].assign(choice)

    def arrange_P1(self, line:int):
        if self.Operate[line][0][0] == -1 and sum(self.Table[0]) == 0:
            return
        if self.Operate[line][0][1] == 8:
            self.dispatch_P1(line,line)
        current_task = self.MachineLine[line][0].get_config()
        if current_task ==-1:
            return
        ouput = self.MachineLine[line][0].process()
        self.Operate[line][0][1] += 1
        self.Table[0][current_task] -= ouput
        self.Table[1][current_task] += ouput
        if self.Table[0][current_task]==0:
            self.dispatch_P1(line,line)
        return

    def arrange_P2(self, line : int) -> None:
        task : list[int]
        # choice : int
        if line ==1:
            task = self.TaskByLine1
        else:
            task = self.TaskByLine2
        current_task = self.MachineLine[line][1].get_config()
        if self.Table[1][current_task] <= 0:
            if self.MachineLine[line][0].get_config() == current_task:
                return
            else: self.dispatch_P2(line)
        else:
            output = self.MachineLine[line][1].process(self.Table[1][current_task])
            self.Table[2][current_task] += output
            self.Table[1][current_task] -= output
        return
    
    def arrrange(self) -> bool:
        """Invoke a cycle in all machine
            Returns: is done with all process
        """
        for line in range(2):
            self.arrange_P1(line)
            self.arrange_P2(line)
        return sum(self.Table[0])==0 and sum(self.Table[1])==0

    def run(self) -> list:
        result = []
        cycle = 0
        while cycle <= self.limit:
            Is_done = self.arrrange()
            result.append(make_operation_node(self.Operate))
        
        return result 
    
    def append(self, task: list[int]):
        for i in range(6):
            self.Table[0][i] += task[i]