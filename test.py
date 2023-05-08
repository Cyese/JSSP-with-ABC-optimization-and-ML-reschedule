from schedule import *
# import matplotlib


path = r"D:/Project/SisThesis/"
data = pd.read_excel(path+"data.xlsx", sheet_name=2, usecols="B:G")

Demand1 = [int(data.loc[0][_]) for _ in range(6)]
Demand2 = [int(data.loc[1][_]) for _ in range(6)]
for index in range(3, 6):
    Demand1[index] //= 3

schedule = Schedule(Demand1)
schedule.add(Demand2)
result, cycle = schedule.run()
for timestamp in result:
    print(timestamp)
print(cycle)
