from ultilities import *

Total_time = 16 * 5 * 2


class Schedule:
    def __init__(self, task_list: list[int]) -> None:
        # 2 Line of production
        self.MachineLine: list[MachinePhase1 | MachinePhase2]

        self.MachineLine = [
            MachinePhase1(12000, 2),
            MachinePhase1(6000, 2),
            MachinePhase2(3000),
            MachinePhase2(2800)
        ]
        # Task for storing all pending task
        # Table[x -> Phase][y -> Task]
        # self.Tasks = [task for task in task_list]
        self.TaskByPhase1 = [False for _ in range(6)]  # Mark which task is currently distrubuted
        self.TaskByPhase2 = [False for _ in range(6)]  # Same from above
        self.Table = [[task for task in task_list],
                      [0 for _ in range(6)],
                      [0 for _ in range(6)]
                      ]
        self.limit = Total_time
        # self.arrange_task()
        # Operate[x -> Line][y -> Phase][z : 0 | 1 -> task | cycle_time]
        self.Operate = [[-1, 8] for _ in range(4)]
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
        self.TaskByPhase1[choice] = True
        self.Operate[machine_id][0] = choice
        self.Operate[machine_id][1] = 0
        return

    def dispatch_P2(self, machine_id: int) -> None:
        if (self.Operate[machine_id][0] == -1 and sum(self.Table[1]) != 0) \
                or self.Table[1][self.Operate[machine_id][0]] <= 0:
            # No more to produce
            choice = get_max(self.Table, self.TaskByPhase2)
            current = self.Operate[machine_id][0]
            if current != -1:
                self.TaskByPhase2[current] = False
            if choice == -1:
                self.Operate[machine_id][0] = choice
                # self.Operate[id][1] = 0
                return
            current = self.Operate[machine_id][0]
            self.MachineLine[machine_id].assign(choice)
            self.Operate[machine_id][0] = choice
            self.Operate[machine_id][1] = 0
            self.TaskByPhase2[choice] = True

    def arrange_P1(self, machine_id: int):
        if self.Operate[machine_id][0] == -1 and sum(self.Table[0]) == 0:
            return
        if self.Operate[machine_id][1] == 8:
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
            # if line == 0:
            #     self.TaskByLine1.pop(self.TaskByLine1.index(current_task))
            # else:
            #     self.TaskByLine2.pop(self.TaskByLine2.index(current_task))
            self.dispatch_P1(machine_id, machine_id)
        return

    def arrange_P2(self, machine_id: int) -> None:
        current_task = self.MachineLine[machine_id].config
        if current_task == -1:
            self.dispatch_P2(machine_id)
            current_task = self.MachineLine[machine_id].config
            self.MachineLine[machine_id].process(self.Table[1][current_task])
        elif self.Table[1][current_task] <= 0:
            self.dispatch_P2(machine_id)
        else:
            output = self.MachineLine[machine_id].process(self.Table[1][current_task])
            self.Table[2][current_task] += output
            self.Table[1][current_task] -= output
        return

    def arrange(self) -> bool:
        """Invoke a cycle in all machine
            Returns: is done with all process
        """
        for machine_id in range(4):
            if machine_id // 2 == 0:
                self.arrange_P1(machine_id)
            else:
                self.arrange_P2(machine_id)
        if unassigned(self.Operate):
            for machine_id in range(4):
                if machine_id // 2 == 0 and self.Operate[machine_id][0] == -1:
                    self.arrange_P1(machine_id)
                elif self.Operate[machine_id][0] == -1:
                    self.arrange_P2(machine_id)
        return sum(self.Table[0]) == 0 and sum(self.Table[1]) == 0

    def run(self) -> tuple[list, int, list]:
        result = [[] for _ in range(4)]
        cycle = 0
        while cycle <= self.limit:
            Is_done = self.arrange()
            for i in range(4):
                result[i].append(self.MachineLine[i].get_config())
            if Is_done:
                break
            else:
                cycle += 1
        return result, cycle, self.Table[2]

    def add(self, task: list[int]):
        for i in range(6):
            self.Table[0][i] += task[i]
