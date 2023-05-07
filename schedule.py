from machine import *
from ultilities import *

Total_time = 16 * 5 * 2


class Scheduler:
    def __init__(self, task_list: list[int]):
        # Rewrite this a bit
        # self.MList = [Machine(machine["job"], machine["capacity"]) for machine in machine_list]
        self.MList = [
            MixingMachine(12000, 2),
            MixingMachine(6000, 2),
            BottlingMachine(3000),
            BottlingMachine(2800)
        ]

        self.numberOfTask = len(task_list)
        self.numberOfMachine = 4
        self.Phase0 = [demand for demand in task_list]  # Demand
        self.Phase1 = [0 for _ in range(self.numberOfTask)]  # Mixed
        self.Phase2 = [0 for _ in range(self.numberOfTask)]  # Bottled / Finished
        # self.Schedule = []
        self.Time_limit = Total_time
        # Task on machine _ time on task
        self.Operating = [[-1, 8] for _ in range(self.numberOfMachine)]

    # Use for assigning new task to a machine
    def dispatcher(self, machine_id: int, phase: int, rate_decision: int = 0):
        task: list
        if phase == 0:
            task = self.Phase0
        elif phase == 1:
            task = self.Phase1
        # Just ignore this ~ ~ that branch is never reached
        else:
            task = self.Phase2
        rate = []
        for index in range(self.numberOfTask):
            ref_value = task[index] / self.MList[machine_id].capacity
            if index != self.MList[machine_id].type_config:
                ref_value += 2
            rate.append(ref_value)
        rate = np.array(rate)
        prate = None
        if rate.sum() == 0:
            return -1
        if rate_decision == 0:
            prate = rate / rate.sum()
        elif rate_decision == 1:
            rate = rate.sum() / rate
            prate = rate / rate.sum()
        choice = np.random.choice(range(self.numberOfTask), p=prate)
        self.MList[machine_id].assign(choice)
        self.Operating[machine_id] = [choice, 0]

    def arrange_phase_1(self, machine_id: int):
        current_task = self.MList[machine_id].type_config
        # Limit cycle = 8h (8 quantum time/time slot)
        # If exceed cycle || no more demand -> choose another process to assign
        if self.Operating[machine_id][0] == -1 and sum(self.Phase0) == 0:
            pass
        if self.Operating[machine_id][1] == 8:
            self.dispatcher(machine_id, machine_id % 2)
        output = self.MList[machine_id].process()
        self.Operating[machine_id][1] += 1
        self.Phase0[current_task] -= output
        if self.Phase0[current_task] <= 0:
            self.Phase0[current_task] = 0
            self.dispatcher(machine_id, machine_id % 2)
        self.Phase1[current_task] += output

    def arrange_phase_2(self, machine_id: int):
        current_task = self.MList[machine_id].type_config
        # Wait for dependence if producing
        # Else assign a new task
        # Not enough requirement for producing
        if current_task == -1 and sum(self.Phase1) > 0:
            self.dispatcher(machine_id, machine_id % 2)
        elif self.Phase1[current_task] <= 0:
            # If another machine is producing its dependence then wait for it
            if self.Operating[0][0] == current_task or self.Operating[1][0] == current_task:
                pass
                # Else assign a new task for the machine
                # else:
                self.dispatcher(machine_id, machine_id % 2)
        # Produce like normal
        else:
            output = self.MList[machine_id].process(self.Phase1[current_task])
            self.Phase1[current_task] -= output
            self.Phase2[current_task] += output

    # Scheduling for each quantum time this is for
    def arrange(self):
        for machine_id in range(len(self.MList)):
            if machine_id < 2:
                self.arrange_phase_1(machine_id)
            else:
                self.arrange_phase_2(machine_id)
        return check(self.Phase0) and check(self.Phase1)

    # Add optimizer that loop through all quantum time and run scheduler for each quantum time
    def run(self):
        counter = 0
        result = []
        while counter < self.Time_limit:
            stopped = self.arrange()
            result.append(operation_node(self.Operating))
            if stopped:
                return True, result
        return False, result

    # If needed to add a new week to current schedule
    def append(self, arr: list[int]):
        """Add weekly demand to current schedule:
            @param arr: list of demand
            @return: None
        """
        for i in range(self.numberOfTask):
            self.Phase0[i] += arr[i]
