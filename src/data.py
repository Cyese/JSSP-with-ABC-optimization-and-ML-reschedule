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
            self.data: list = []
            read = json.load(open("sched/week_{}/info.json".format(weeks), "r"))
            self.span = int(read["span"])
            self.working = [int(_) for _ in read["working"]]
            utilization = [_ / self.span for _ in self.working]
            mean = sum(utilization) / len(utilization)
            RBM = Data.calculate_RBM(max(utilization), mean)
            RSDU = Data.calculate_RSDU(utilization, mean)
            org : list =  [weeks, -1]
            org.extend([ _ for _ in utilization])
            org.extend([mean, RBM, RSDU, 0, 0, False])
            self.data.append(org)
            self.run(weeks)
            pass

        def run(self, week: int) -> None:
            _directory = f"./resched/week_{week}"
            list_file = glob.glob(_directory + "/operation*.json")
            for file in list_file:
                data = json.load(open(file, "r"))
                span = int(data["span"])
                working = [int(_)/span for _ in data["working"]]
                mean = sum(working)/4
                RBM = Data.calculate_RBM(max(working), mean)
                RSDU = Data.calculate_RSDU(working, mean)
                extended = int(data["extended"])
                stage = int(data["stage"])
                timestep = int(data["timestep"])
                reschedule = bool(data["reschedule"])
                key: list = [week, timestep]
                key.extend(working)
                key.extend([mean, RBM, RSDU, extended, stage, reschedule])
                self.data.append(key)


        def get_data(self) -> list:
            return self.data

    def __init__(self) -> None:
        self.data : pd.DataFrame
        self.make_data()
        pass

    def make_data(self) -> None:
        holder = []
        for week in range(311):
            holder.extend(Data.DataByWeek(week).get_data())
        self.data = pd.DataFrame(holder)
        self.data.columns = ["Week", "Timestep", "U1", "U2", "U3", "U4", "MU", "RBM", "RSDU", "Total extended time","Stage", "Rescheduling"]
        self.data.to_csv("data/feature.csv", index= False)
