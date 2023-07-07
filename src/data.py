from utilities import pd, json, glob


def export_make_spans() -> None:
    schedule_spans: list[int] = []
    for week in range(0, 311):
        info = json.load(open(f"sched/week_{week}/info.json", 'r'))
        schedule_spans.append(int(info["span"]))
    exported = pd.Series(schedule_spans)
    exported.to_excel("data/make_span.xlsx", index=False)


def calculate_RSDU(Util_list: list[float], MU: float) -> float:
    result: float = 0.0
    for i in Util_list:
        result += (i - MU) ** 2
    result /= 3.0
    result **= 1 / 2
    result /= MU
    return result


def calculate_RBM(_max: float, MU: float) -> float:
    result: float = _max / MU
    return result


class DataProduct:
    class DataByWeek:
        def __init__(self, weeks: int) -> None:
            self.data: list = []
            read = json.load(open("sched/week_{}/info.json".format(weeks), "r"))
            self.span = int(read["span"])
            self.working = [int(_) for _ in read["working"]]
            utilization = [_ / self.span for _ in self.working]
            mean = sum(utilization) / len(utilization)
            RBM = calculate_RBM(max(utilization), mean)
            RSDU = calculate_RSDU(utilization, mean)
            org: list = [weeks, -1]
            org.extend([_ for _ in utilization])
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
                working = [int(_) / span for _ in data["working"]]
                mean = sum(working) / 4
                RBM = calculate_RBM(max(working), mean)
                RSDU = calculate_RSDU(working, mean)
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
        self.data: pd.DataFrame
        self.make_data_product()
        pass

    def make_data_product(self) -> None:
        holder = []
        for week in range(311):
            holder.extend(DataProduct.DataByWeek(week).get_data())
        self.data = pd.DataFrame(holder)
        self.data.columns = ["Week", "Timestep", "U1", "U2", "U3", "U4", "MU", "RBM", "RSDU", "Total extended time",
                             "Stage", "Rescheduling"]
        self.data.to_csv("data/feature_product.csv", index=False)
        self.data.to_excel("data/feature_product.xlsx", index=False)


class DataNewOrder:
    count = 0
    class DataByWeek:
        def __init__(self, weeks: int) -> None:
            self.data: list = []
            read = json.load(open("sched/week_{}/info.json".format(weeks), "r"))
            self.span = int(read["span"])
            self.working = [int(_) for _ in read["working"]]
            self.run(weeks)
            pass

        def run(self, week: int) -> None:
            _directory = f"./resched/week_{week}"
            list_file = glob.glob(_directory + "/order*.json")
            for file in list_file:
                data = json.load(open(file, "r"))
                span = int(data["span"])
                timestep = int(data["timestep"])
                working = [int(_) / span for _ in data["working"]]
                mean = sum(working) / 4
                RBM = calculate_RBM(max(working), mean)
                RSDU = calculate_RSDU(working, mean)
                extended = int(data["extended"])
                # timestep = int(data["timestep"])
                reschedule = bool(data["reschedule"])
                key: list = [week, timestep]
                key.extend(working)
                key.extend([mean, RBM, RSDU, extended, reschedule])
                self.data.append(key)

        def get_data(self) -> list:
            return self.data

    def __init__(self) -> None:
        self.data: pd.DataFrame
        self.make_data_order()
        _true = (self.data["Rescheduling"] == True).sum()
        total = self.data.shape[0]
        print(f"True/False ratio = {_true/total}")
        pass

    def make_data_order(self) -> None:
        holder = []
        for week in range(311):
            holder.extend(DataNewOrder.DataByWeek(week).get_data())
        self.data = pd.DataFrame(holder)
        self.data.columns = ["Week", "timestep","U1", "U2", "U3", "U4", "MU", "RBM", "RSDU", "Total extended time", "Rescheduling"]
        self.data.to_csv("data/feature_order.csv", index=False)
        self.data.to_excel("data/feature_order.xlsx", index=False)

    @staticmethod
    def make_disturbance_sheet() -> None:
        disturbance_set = []
        for week in range(311):
            with open(f"disturbance/week_{week}/order.json") as file:
                data = json.load(file)
                for x in data:
                    disturbance_set.append([week, int(x), data[x][0], data[x][1]])
        data = pd.DataFrame(disturbance_set)
        data.columns = ['Weeks', 'Timestep', 'Type', 'Quantity']
        data.to_excel("data/new_order_disturbance.xlsx", index=False)
