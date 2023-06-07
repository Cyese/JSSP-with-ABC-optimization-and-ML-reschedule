from utilities import *

Total_time = 16 * 5 * 2


class Schedule:
    def __init__(self, task_list: list[int]) -> None:
        # 2 Line of production
        self.MachineLine: list[MachinePhase1 | MachinePhase2]

        self.MachineLine = [
            MachinePhase1(9000, 2),
            MachinePhase1(9000, 2),
            MachinePhase2(4500),
            MachinePhase2(4500)
        ]
        self.TaskByPhase1 = [False for _ in range(6)]  # Mark which task is currently distributed
        self.TaskByPhase2 = [False for _ in range(6)]  # Same from above
        self.Table = [[task for task in task_list],
                      [0 for _ in range(6)],
                      [0 for _ in range(6)]
                      ]
        self.limit = Total_time
        self.Operate = [[-1, 4] for _ in range(4)]
        self.PenaltyTime = [4, 3, 8, 16]
        return

    def dispatch_P1(self, machine_id: int, rate_decision: int = 0) -> None:
        rate = []
        choice_list = []
        current = self.Operate[machine_id][0]
        self.TaskByPhase1[current] = self.Table[0][current] == 0
        for i in range(6):
            if self.Table[0][i] == 0 or self.TaskByPhase1[i]:
                pass
            else:
                value = self.Table[0][i] / self.MachineLine[machine_id].capacity
                rate.append(value)
                choice_list.append(i)
        rate = np.array(rate)
        if rate.sum() == 0:
            choice = -1
        else:
            if rate_decision:
                rate = rate.sum() / rate
                prate = rate / rate.sum()
            else:
                prate = rate / rate.sum()
            choice = np.random.choice(choice_list, p=prate)
        self.MachineLine[machine_id].assign(choice)
        if choice != -1:
            self.TaskByPhase1[choice] = True
        self.Operate[machine_id][0] = choice
        self.Operate[machine_id][1] = 0
        return

    def dispatch_P2(self, machine_id: int) -> None:
        if (self.Operate[machine_id][0] == -1 and sum(self.Table[1]) != 0) \
                or self.Table[1][self.Operate[machine_id][0]] <= 0:
            # No more to produce
            choice = get_max(self.Table[1], self.TaskByPhase2)
            current = self.Operate[machine_id][0]
            if current != -1:
                self.TaskByPhase2[current] = False
            if choice == -1:
                self.Operate[machine_id][0] = choice
                self.MachineLine[machine_id].assign(choice)
                return
            # current = self.Operate[machine_id][0]
            self.MachineLine[machine_id].assign(choice)
            self.Operate[machine_id][0] = choice
            self.Operate[machine_id][1] = 0
            self.TaskByPhase2[choice] = True

    def arrange_P1(self, machine_id: int):
        if self.Operate[machine_id][0] == -1 and sum(self.Table[0]) == 0:
            self.MachineLine[machine_id].assign(-1)
        current_task = self.MachineLine[machine_id].config
        if self.Operate[machine_id][1] == 4 or self.Table[0][current_task] <= 0:
            self.dispatch_P1(machine_id, machine_id)
        current_task = self.MachineLine[machine_id].config
        if current_task == -1:
            return
        output = self.MachineLine[machine_id].process()
        self.Operate[machine_id][1] += 1  # increase time
        self.Table[0][current_task] -= output
        self.Table[1][current_task] += output
        if self.Table[0][current_task] <= 0:
            self.Table[0][current_task] = 0
        return

    def arrange_P2(self, machine_id: int) -> None:
        current_task = self.MachineLine[machine_id].config
        if current_task == -1:
            self.dispatch_P2(machine_id)
            self.MachineLine[machine_id].process()
        elif self.Table[1][current_task] <= 0:
            self.dispatch_P2(machine_id)
            current_task = self.MachineLine[machine_id].config
            if current_task == -1:
                return
            self.MachineLine[machine_id].process()
        else:
            output = self.MachineLine[machine_id].process()
            self.Table[2][current_task] += output
            self.Table[1][current_task] -= output
        return

    def arrange(self) -> bool:
        """Invoke a cycle in all machine
            Returns: is done with all process
        """
        for machine_id in [3, 2, 1, 0]:  # range(4):
            if self.PenaltyTime[machine_id] > 0:
                self.PenaltyTime[machine_id] -= 1
            elif machine_id // 2 == 0:
                self.arrange_P1(machine_id)
            else:
                self.arrange_P2(machine_id)
        return sum(self.Table[0]) == 0 and sum(self.Table[1]) == 0

    def run(self) -> tuple[list, int, list]:
        result = [[] for _ in range(4)]
        cycle = 0
        while True:
            Is_done = self.arrange()
            for i in range(4):
                result[i].append(self.MachineLine[i].get_config())
            if Is_done:
                break
            else:
                cycle += 1
        for y in range(4):
            for x in range(cycle + 1):
                if result[y][x] == -1:
                    result[y][x] = 8
        return result, cycle, self.Table[2]

    def add(self, task: list[int]):
        for i in range(6):
            self.Table[0][i] += task[i]


class PhaseBaseSchedule:
    def __init__(self, phase1: list[list[int]]) -> None:
        self.MachineLine: list[MachinePhase1 | MachinePhase2]
        self.MachineLine = [
            MachinePhase1(2, 2),
            MachinePhase1(2, 2),
            MachinePhase2(1),
            MachinePhase2(1)
        ]
        self.Dispatch = [True, True]
        self.Operate = [[-1, 8] for _ in range(4)]
        self.PenaltyTime = [4, 3, 8, 16]
        self.Phase1Schedule = phase1
        self.Task = [False for _ in range(6)]
        self.Table = [0 for _ in range(6)]
        # temp = [True for _ in range(6)]
        # for x in phase1:
        #     for ope in x:
        #         temp[ope] &= False
        # for x, item in enumerate(temp):
        #     if item:
        #         print(f"Missing a key: {x}") 

    def dispatch_P1(self, machine_id: int) -> None:
        if len(self.Phase1Schedule[machine_id]) == 0:
            self.MachineLine[machine_id].assign(-1)
        else:
            choice = self.Phase1Schedule[machine_id].pop(0)
            self.MachineLine[machine_id].assign(choice)
            self.Operate[machine_id][0] = choice
            self.Operate[machine_id][1] = 0
        return

    def dispatch_P2(self, machine_id: int) -> None:
        if (self.Operate[machine_id][0] == -1 and sum(self.Table) != 0) \
                or self.Table[self.Operate[machine_id][0]] <= 0:
            # No more to produce
            choice = get_max(self.Table, self.Task)
            current = self.Operate[machine_id][0]
            if current != -1:
                self.Task[current] = False
            if choice == -1:
                self.Operate[machine_id][0] = choice
                self.MachineLine[machine_id].assign(choice)
                return
            # current = self.Operate[machine_id][0]
            self.MachineLine[machine_id].assign(choice)
            self.Operate[machine_id][0] = choice
            self.Operate[machine_id][1] = 0
            self.Task[choice] = True

    def arrange_P1(self, machine_id: int) -> None:
        if self.MachineLine[machine_id].config == -1 or self.Dispatch[machine_id]:
            self.dispatch_P1(machine_id)
            self.Dispatch[machine_id] = False
        # output = self.MachineLine[machine_id].process()
        output = self.MachineLine[machine_id].process()
        if output != 0:
            self.Dispatch[machine_id] = True
            # What's below here is black magic, don't question/ask about it, it just works (maybe)
            # (and no im not racist the black, is just a Yugioh ref)
            cur = self.MachineLine[machine_id].config
            if cur == -1:
                pass
            else:
                self.Table[cur] += output
            # End of black magic
        else:
            pass
        return

    def arrange_P2(self, machine_id: int):
        current_task = self.MachineLine[machine_id].config
        if current_task == -1:
            self.dispatch_P2(machine_id)
        elif self.Table[current_task] <= 0:
            self.dispatch_P2(machine_id)
        current_task = self.MachineLine[machine_id].config
        if current_task == -1:
            return
        output = self.MachineLine[machine_id].process()
        self.Table[current_task] -= output

    def is_Done(self) -> bool:
        value: bool = True
        for enum, _ in enumerate(self.Table):
            value &= _ == 0 and self.Task[enum] is False
        value &= len(self.Phase1Schedule[0]) == 0 and len(self.Phase1Schedule[1]) == 0
        return value

    def arrange(self):
        for machine_id in [0, 1, 2, 3]:  # range(4):
            if self.PenaltyTime[machine_id] > 0:
                self.PenaltyTime[machine_id] -= 1
            elif machine_id // 2 == 0:
                self.arrange_P1(machine_id)
            else:
                self.arrange_P2(machine_id)
        return self.is_Done()

    def run(self) -> tuple[list[list[int]], int]:
        result = [[] for _ in range(4)]
        cycle = 0
        while True:
            Is_done = self.arrange()
            for i in range(4):
                result[i].append(self.MachineLine[i].get_config())
            if Is_done:
                break
            else:
                cycle += 1
        for y in range(4):
            for x in range(cycle + 1):
                if result[y][x] == -1:
                    result[y][x] = 8
        return result, cycle

    # def runToStage(self, data, checkpoint: int):
    #     result = [[] for _ in range(4)]
    #     cycle = 0
    #     while cycle < checkpoint:
    #         Is_done = self.arrange()
    #         for i in range(4):
    #             result[i].append(self.MachineLine[i].get_config())
    #         if Is_done:
    #             break
    #         else:
    #             cycle += 1
    #     """
    #         Add code to modify as the demand changes (inplace removal/ of the patch then continue)
    #         What need to be done: branching,

    #     """
    #     return result, cycle
