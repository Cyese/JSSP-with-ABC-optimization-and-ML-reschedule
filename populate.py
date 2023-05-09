from schedule import *

path = r"D:/Project/SisThesis/"
write_out_path = path + "population/"


def populated(weeks: int):
    """Create and population base on the data in week and weeks+1 
        Args:
            weeks (int): number represent a weeks, in range [0,311]
        Returns:
            A collection of text file in .\\population\\week_{weeks}
    """
    write_Path = write_out_path + "week_{}/".format(weeks)
    if not os.path.exists(write_Path):
        os.mkdir(write_Path)
    data = pd.read_excel(path+"data.xlsx", sheet_name=2, usecols="B:G")

    Demand1 = [int(data.loc[weeks][_]) for _ in range(6)]
    Demand2 = [int(data.loc[weeks+1][_]) for _ in range(6)]
    Total = [Demand2[_] + Demand1[_] for _ in range(6)]
    for index in range(3, 6):
        Total[index] //= 3
    for invidual in range(100):
        schedule = Schedule(Total)
        result, cycle, output = schedule.run()
        file = open(write_Path + "invi_{}.txt".format(invidual), "w+")
        for machine in result:
            file.writelines(' '.join(str(ele) for ele in machine) + '\n')
        file.write(str(cycle))
        
    # file = open("sample_init_sched.txt", "w+")
    # for timestamp in result:
    #     file.writelines(' '.join(str(ele) for ele in timestamp) + '\n') 
    # print(cycle)
    # print(output)
    # print(Total)

populated(200)