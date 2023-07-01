from schedule import *


def populated(weeks: int):
    """Create and sample base on the data in week and weeks+1 
        Args:
            weeks (int): number represent a weeks, in range [0,311]
        Returns:
            A collection of text file in .\\sample\\week_{weeks}
    """
    write_Path = write_out_path + "week_{}/".format(weeks)
    if not os.path.exists(write_Path):
        os.mkdir(write_Path)
    data = pd.read_excel("data/data1.xlsx", sheet_name=2, usecols="B:G")

    Demand1 = [int(data.loc[weeks][_]) for _ in range(6)]
    Demand2 = [int(data.loc[weeks + 1][_]) for _ in range(6)]
    Total = [Demand2[_] + Demand1[_] for _ in range(6)]
    make_span = [0 for _ in range(100)]
    for index in range(3, 6):
        Total[index] //= 3
    for route in range(100):
        schedule = Schedule(Total)
        result, cycle = schedule.run()
        file = open(write_Path + "path_{}.txt".format(route), "w+")
        for machine in result:
            file.writelines(' '.join(str(ele) for ele in machine) + '\n')
        make_span[route] = cycle
    with open(write_Path + "span.txt", "w+") as fitness_file:
        fitness_file.writelines(str(ele) + '\n' for ele in make_span)
