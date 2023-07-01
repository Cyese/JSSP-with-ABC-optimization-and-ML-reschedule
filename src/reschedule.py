from machine import MachinePhase1, MachinePhase2
from utilities import *


def generate_production(weeks: int) -> None:
    """ Use to generate the disturbance for production
    """
    ProductionDisturbance.clean(weeks)
    span: int
    with open(f"sched/week_{weeks}/info.json", "r") as file:
        data = json.loads(file.read())
        span = data["span"]
    if not os.path.exists(f"disturbance/week_{weeks}"):
        os.mkdir(f"disturbance/week_{weeks}")
    ProductionDisturbance.make_disturbance(weeks, span)
    return


def generate_maintenance() -> None:
    number_of_week = 300
    number_of_stage = 2
    generator = [np.random.choice([True, False], size=number_of_week, p=[0.25, 0.75]).tolist() for _ in range(2)]
    sth = 0
    j: int = 0
    result = [[] for _ in range(4)]
    for f, stage in enumerate(generator):
        print(f"Maintain by stage {f + 1}: {stage.count(True)}")
        sth += stage.count(True)
        k = 0
        for i, value in enumerate(stage):
            if value:
                result[j + (k % 2)].append(i)
                k += 1
        j += 2
    for k, gen in enumerate(result):
        avgDiff = 0
        for i in range(0, len(gen) - 1):
            avgDiff += (gen[i + 1] - gen[i])
        avgDiff /= len(gen) - 1
        print(f"{k} : {avgDiff}")
    maintain: dict[int, int] = {}
    for i, gen in enumerate(result):
        for j in gen:
            maintain.__setitem__(j, i)
    sorted_key = sorted([i for i in maintain])
    sorted_maintain = {i: maintain[i] for i in sorted_key}
    data = json.dumps(sorted_maintain)
    with open("disturbance/maintain.json", "w+") as file:
        file.write(data)
    print(f"Ratio: {sth / (number_of_stage * number_of_week)}")


def interpret_maintenance() -> None:
    maintain = json.load(open("disturbance/maintain.json", "r"))
    new_maintain: dict[int, list[int]] = {}
    for x in maintain:
        week = int(x)
        info = json.load(open("sched/week_{}/info.json".format(week), 'r'))["span"]
        time = np.random.randint(0, info)
        machine = maintain[x]
        new_maintain.__setitem__(week, [machine, time])
    json.dump(new_maintain, open("disturbance/maintain.json", "w+"))


def generate_newOrder(week : int) -> None:
    """New order requirements:  time step, type, quantity"""
    randint = np.random.randint
    _quantity = [1, 2, 3, 4]
    cycle = 100
    rates = [0.4, 0.3, 0.2 , 0.1] # mean = 2
    no_of_orders = randint(low=4, high= 7)
    # for order in range(no_of_orders):
    order_quantity = np.random.choice(_quantity,size=(no_of_orders), p= rates).tolist()
    result = {}
    for index, order in enumerate(order_quantity):
        _type = randint(6)
        _timestep = randint(cycle)
        result.update({index : [_type, _timestep, order]})
    json.dump(result, open(f"./disturbance/week_{week}/order.json", "w+"))


# May change to more DYNAMIC way to get prob (lot more gacha)
class StaticProb:
    def __init__(self, span: int) -> None:
        self.size = span
        self.chance = np.random.choice([False, True], p=np.array([0.95, 0.05]),
                                       size=(4, span)).tolist()  # Predawn sample size at runtime
        self.y = -1
        self.x = 0

    def randomize(self) -> bool:
        self.y += 1
        if self.y == self.size:
            self.x += 1
            self.y = 0
        if self.x == 4:
            self.x = 0
        return self.chance[self.x][self.y]


class ProductionDisturbance:
    """This is a wrapper class since every thing is a mess
    """
    count = 0
    class RescheduleProduction:
        def __init__(self, phase1: list[list[int]]) -> None:
            self.MachineLine: list[MachinePhase1 | MachinePhase2]
            self.MachineLine = [
                MachinePhase1(2, 2),
                MachinePhase1(2, 2),
                MachinePhase2(1),
                MachinePhase2(1)
            ]
            self.disturb: list[int]
            self.Dispatch = [True, True]
            self.Operate = [[-1, 8] for _ in range(4)]
            self.PenaltyTime = [4, 3, 8, 16]
            self.Phase1Schedule = phase1.copy()
            self.Task = [False for _ in range(6)]
            self.Table = [0 for _ in range(6)]
            self.count = ProductionDisturbance.count
            ProductionDisturbance.count += 1

        def add_disturbance(self, disturb: list[int]) -> None:
            self.disturb = disturb
            # self.run(disturb= 1)

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

        def arrange_P1(self, machine_id: int, disturb: int = 0) -> None:
            if self.MachineLine[machine_id].config == -1 or self.Dispatch[machine_id]:
                self.dispatch_P1(machine_id)
                self.Dispatch[machine_id] = False
            output = self.MachineLine[machine_id].process()
            if output != 0:
                self.Dispatch[machine_id] = True
                cur = self.MachineLine[machine_id].config
                if cur == -1:
                    pass
                else:
                    self.Table[cur] += output
                    if disturb == 2:
                        # 2 stand for broken batch
                        self.Table[cur] -= output
                        self.Phase1Schedule[machine_id].insert(0, cur)
            else:
                pass
            return

        def arrange_P2(self, machine_id: int, disturb: int = 0):
            current_task = self.MachineLine[machine_id].config
            if current_task == -1:
                self.dispatch_P2(machine_id)
            elif self.Table[current_task] <= 0:
                self.dispatch_P2(machine_id)
            current_task = self.MachineLine[machine_id].config
            if current_task == -1:
                return
            output = self.MachineLine[machine_id].process()
            if disturb == 0:
                self.Table[current_task] -= output
            elif disturb == -1:
                self.arrange_P2(machine_id)
            elif disturb == 1:
                pass
            elif disturb == 2:
                self.insert_batch(current_task)

        def is_Done(self) -> bool:
            value: bool = True
            for enum, _ in enumerate(self.Table):
                value &= _ == 0 and self.Task[enum] is False
            value &= len(self.Phase1Schedule[0]) == 0 and len(self.Phase1Schedule[1]) == 0
            return value

        def arrange(self, machine: int = 5, _type: int = 0):
            for machine_id in [0, 1, 2, 3]:  # range(4):
                if self.PenaltyTime[machine_id] > 0:
                    self.PenaltyTime[machine_id] -= 1
                elif machine_id // 2 == 0:
                    if machine_id == machine:
                        self.arrange_P1(machine_id, _type)
                    else:
                        self.arrange_P1(machine_id)
                else:
                    if machine_id == machine:
                        self.arrange_P2(machine_id, _type)
                    else:
                        self.arrange_P2(machine_id)
            return self.is_Done()

        def insert_batch(self, _id: int):
            added = False
            for machine in self.Phase1Schedule:
                for i, item in enumerate(machine):
                    if item == _id:
                        machine.insert(i, _id)
                        added = True
                        break
            if not added:
                self.Phase1Schedule[0].append(_id)

        def append_batch(self, _id: int):
            if len(self.Phase1Schedule[0])  <- len(self.Phase1Schedule[1]):
                self.Phase1Schedule[0].append(_id)
            else: self.Phase1Schedule[1].append(_id)

        def run_with_disturbance(self) -> tuple[list[list[int]], int, list[int], int]:
            result = [[] for _ in range(4)]
            cycle = 0
            machine, time, _type = self.disturb
            total_working_time: list[int] = [0, 0, 0, 0]
            if machine >= 2:
                stage = 2
            else:
                stage = 1
            while True:
                if time <= cycle <= time + 1:
                    Is_done = self.arrange(machine, _type)
                else:
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
                    if result[y][x] != 8:
                        total_working_time[y] += 1
            return result, cycle, total_working_time, stage

        def bruteforce_P1(self, machine_id: int, disturb: int = 0) -> None:
            if self.MachineLine[machine_id].config == -1 or self.Dispatch[machine_id]:
                self.dispatch_P1(machine_id)
                self.Dispatch[machine_id] = False
            output = self.MachineLine[machine_id].process()
            if output != 0:
                self.Dispatch[machine_id] = True
                cur = self.MachineLine[machine_id].config
                if cur == -1:
                    pass
                else:
                    self.Table[cur] += output
                    if disturb == 2:
                        # 2 stand for broken batch
                        self.Table[cur] -= output
                        self.append_batch(cur)
            else:
                pass
            return            

        def bruteforce_P2(self, machine_id: int, disturb: int = 0) -> None:
            current_task = self.MachineLine[machine_id].config
            if current_task == -1:
                self.dispatch_P2(machine_id)
            elif self.Table[current_task] <= 0:
                self.dispatch_P2(machine_id)
            current_task = self.MachineLine[machine_id].config
            if current_task == -1:
                return
            output = self.MachineLine[machine_id].process()
            if disturb == 0:
                self.Table[current_task] -= output
            elif disturb == -1:
                self.arrange_P2(machine_id)
            elif disturb == 1:
                pass
            elif disturb == 2:
                self.append_batch(current_task)

        def bruteforce(self, machine: int = 5, _type: int = 0):
            for machine_id in [0, 1, 2, 3]:  # range(4):
                if self.PenaltyTime[machine_id] > 0:
                    self.PenaltyTime[machine_id] -= 1
                elif machine_id // 2 == 0:
                    if machine_id == machine:
                        self.bruteforce_P1(machine_id, _type)
                    else:
                        self.bruteforce_P1(machine_id)
                else:
                    if machine_id == machine:
                        self.bruteforce_P2(machine_id, _type)
                    else:
                        self.bruteforce_P2(machine_id)
            return self.is_Done()           

        def run_with_bruteforce(self) -> tuple[list[list[int]], int, list[int], int]:
            result = [[] for _ in range(4)]
            cycle = 0
            machine, time, _type = self.disturb
            total_working_time: list[int] = [0, 0, 0, 0]
            if machine >= 2:
                stage = 2
            else:
                stage = 1
            while True:
                if time <= cycle <= time + 1:
                    Is_done = self.bruteforce(machine, _type)
                else:
                    Is_done = self.bruteforce()
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
                    if result[y][x] != 8:
                        total_working_time[y] += 1
            return result, cycle, total_working_time, stage


    @staticmethod
    def clean(weeks: int) -> None:
        """Utility function: clear space for rescheduling data
            @param: weeks (int): week ot clear
        """
        _dir = f"./resched/week_{weeks}"
        file_list = glob.glob(_dir + "/*.json")
        for file in file_list:
            os.remove(file)
        file_list = glob.glob(_dir + "/*.txt")
        for file in file_list:
            os.remove(file)

    # ---Space for creating disturbance--- #

    @staticmethod
    def make_disturbance(weeks: int, size: int) -> None:
        time = ProductionDisturbance.time_variant(size)
        time_data = json.dumps(time)
        operation = ProductionDisturbance.operate_variant(size)
        operation_data = json.dumps(operation)
        with open(f"disturbance/week_{weeks}/time.json", "w+") as time_file:
            time_file.write(time_data)
        with open(f"disturbance/week_{weeks}/operation.json", "w+") as operation_file:
            operation_file.write(operation_data)

    @staticmethod
    def time_variant(size: int) -> dict[int, tuple[int, int, int]]:
        span: int = size
        rate = np.array([0.05, 0.9, 0.05])
        generator = np.random.choice([-1, 0, 1], p=rate, size=(4, span))
        generator = generator.tolist()
        variants: dict[int, tuple[int, int, int]]
        variants = {}  # Matching timestep with variant
        counter = 0
        for x, machine in enumerate(generator):
            for y, changes in enumerate(machine):
                if changes != 0:
                    variants.__setitem__(counter, (x, y, int(changes)))
                    counter += 1
        return variants

    @staticmethod
    def operate_variant(size: int) -> dict[int, tuple[int, int, int]]:
        prob = StaticProb(size)
        variants: dict[int, tuple[int, int, int]] = {}
        counter = 0
        for x in range(4):
            for y in range(120):
                if prob.randomize():
                    variants.__setitem__(counter, (x, y, 2))  # 2 represent broken batch
                    counter += 1
        return variants

    # ---End of space for creating disturbance--- #

    @staticmethod
    def generate_schedule(weeks: int, span: int) -> None:
        variants: dict
        with open(f"disturbance/week_{weeks}/time.json", "r") as time:
            data = time.read()
            variants = json.loads(data)
        for variant in variants:
            ProductionDisturbance.make_reschedule_PDisturbance(weeks, variants[variant], "time")
        ProductionDisturbance.count = 0
        with open(f"disturbance/week_{weeks}/operation.json", "r") as operation:
            data = operation.read()
            variants = json.loads(data)
        for variant in variants:
            ProductionDisturbance.make_reschedule_PDisturbance(weeks, variants[variant], "operation")

    @staticmethod
    def make_reschedule_PDisturbance(weeks: int, variants: list[int], filename: str) -> None:
        solution : list[list[int]]
        _span: int
        working_time: list[int]
        stage: int
        changes: list[int] = variants
        sched = get_output_sched(weeks)
        rescheduler = ProductionDisturbance.RescheduleProduction(sched)
        rescheduler.add_disturbance(changes)
        resched = rescheduler.run_with_disturbance()
        sched = get_output_sched(weeks)
        rescheduler = ProductionDisturbance.RescheduleProduction(sched)
        rescheduler.add_disturbance(changes)
        non_resched = rescheduler.run_with_bruteforce()
        rescheded : bool = resched[1] <= 0.95 * non_resched[1]
        if rescheded:
            solution, _span, working_time, stage = resched
        
        else:
            solution, _span, working_time, stage = non_resched
        original = json.load(open(f"sched/week_{weeks}/info.json", "r"))
        extended = sum([working_time[i] - int(_) for i, _ in enumerate(original["working"])])
        if extended == 0:
            ProductionDisturbance.count -= 1
            return
        with open(f'resched/week_{weeks}/{filename}_{rescheduler.count}.txt', "w+") as file:
            for x in solution:
                file.writelines(' '.join(str(_) for _ in x) + '\n')
        data = {"span": _span, "working": working_time, "extended": extended, "stage": stage, "reschedule" : rescheded, "timestep" : variants[1]}  # Remake: number of batch have to be make again
        write_data = json.dumps(data)
        with open(f'resched/week_{weeks}/{filename}_{rescheduler.count}.json', "w+") as file:
            file.write(write_data)

    def __init__(self) -> None:
        """Call me if u dare!"""
        for week in range(311):
            if not os.path.exists(f"resched/week_{week}"):
                os.mkdir(f"resched/week_{week}")
            span = read_span(week)
            ProductionDisturbance.generate_schedule(week, span)
            ProductionDisturbance.count = 0
        pass


class MaintenanceDisturbance:
    class RescheduleMaintenance:
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
            self.maintenance: list[int]

        def add_maintenance(self, maintenance: list[int]) -> None:
            self.maintenance = maintenance

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
                self.MachineLine[machine_id].assign(choice)
                self.Operate[machine_id][0] = choice
                self.Operate[machine_id][1] = 0
                self.Task[choice] = True

        def arrange_P1(self, machine_id: int) -> None:
            if self.MachineLine[machine_id].config == -1 or self.Dispatch[machine_id]:
                self.dispatch_P1(machine_id)
                self.Dispatch[machine_id] = False
            output = self.MachineLine[machine_id].process()
            if output != 0:
                self.Dispatch[machine_id] = True
                cur = self.MachineLine[machine_id].config
                if cur == -1:
                    pass
                else:
                    self.Table[cur] += output
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

        def arrange(self, machine: int = 5):
            for machine_id in [0, 1, 2, 3]:  # range(4):
                if machine_id == machine:
                    continue
                elif self.PenaltyTime[machine_id] > 0:
                    self.PenaltyTime[machine_id] -= 1
                elif machine_id // 2 == 0:
                    self.arrange_P1(machine_id)
                else:
                    self.arrange_P2(machine_id)
            return self.is_Done()

        def run_with_maintenance(self) -> tuple[list[list[int]], int, list[int]]:
            result = [[] for _ in range(4)]
            cycle = 0
            total_working_time: list[int] = [0, 0, 0, 0]
            machine, time = self.maintenance
            while True:
                if time <= cycle < time + 3:
                    Is_done = self.arrange(machine)
                else:
                    Is_done = self.arrange()
                for i in range(4):
                    result[i].append(self.MachineLine[i].get_config())
                if Is_done:
                    break
                else:
                    cycle += 1
            if cycle <= time:
                pass
            elif time < cycle < time + 3:
                result[machine][time: cycle] = [9 for _ in range(cycle - time)]
            else:
                result[machine][time: time + 3] = [9 for _ in range(3)]
            for y in range(4):
                for x in range(cycle + 1):
                    if result[y][x] == -1:
                        result[y][x] = 8
                    if result[y][x] != 8:
                        total_working_time[y] += 1
            return result, cycle, total_working_time

    @staticmethod
    def generate_schedule() -> None:
        maintain = json.load(open("disturbance/maintain.json", "r"))
        for item in maintain:
            week = int(item)
            sched = get_output_sched(week)
            maintain_info = maintain[item]
            rescheduler = MaintenanceDisturbance.RescheduleMaintenance(sched)
            rescheduler.add_maintenance(maintain_info)
            solution, _span, working_time = rescheduler.run_with_maintenance()
            with open(f'resched/week_{week}/maintain.txt', "w+") as file:
                for x in solution:
                    file.writelines(' '.join(str(_) for _ in x) + '\n')
            data = {"span": _span, "working": working_time}
            write_data = json.dumps(data)
            with open(f'resched/week_{week}/maintain_info.json', "w+") as file:
                file.write(write_data)

    def __init__(self) -> None:
        MaintenanceDisturbance.generate_schedule()
        pass


# class NewOrder: