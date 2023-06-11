from utilities import pd, json, glob


class Data:
    @staticmethod
    def calculate_RBM(_max: float, MU: float) -> float:
        result: float = _max / MU
        return result

    @staticmethod
    def calculate_RSDU(Util_list: list[float], MU: float) -> float:
        result: float = 0.0
        for i in Util_list:
            result += (i - MU) ** 2
        result /= 3.0
        result **= 1 / 2
        result /= MU
        return result

    class DataByWeek:
        def __init__(self, weeks: int) -> None:
            self.data: list
            read = json.load(open("sched/week_{}/info.json".format(weeks), "r"))
            self.span = int(read["span"])
            self.working = [int(_) for _ in read["working"]]
            utilization = [_ / self.span for _ in self.working]
            mean = sum(utilization) / len(utilization)
            RBM = Data.calculate_RBM(max(utilization), mean)
            RSDU = Data.calculate_RSDU(utilization, mean)
            self.data = [_ for _ in utilization]
            self.data.extend([mean, RBM, RSDU])
            self.run(weeks)
            pass

        def run(self, week: int) -> None:
            _directory = f"./resched/week_{week}"
            maintain = glob.glob(_directory + "/maintain_info.json")
            multi: bool
            if len(maintain) != 0:
                multi = True
            else:
                multi = False
            No_Operation: int = 0
            Total_extended_time: int = 0
            list_file = glob.glob(_directory + "/operation*.json")
            for file in list_file:
                data = json.load(open(file, "r"))
                working = [int(_) for _ in data["working"]]
                for x in working:
                    Total_extended_time += x
                No_Operation += data["remake"]
            self.data.extend([multi, No_Operation, Total_extended_time])

        def get_data(self) -> list:
            return self.data

    def __init__(self) -> None:
        self.data = None
        self.make_data()
        pass

    def make_data(self) -> None:
        holder = [Data.DataByWeek(x).get_data() for x in range(311)]
        self.data = pd.DataFrame(holder)
