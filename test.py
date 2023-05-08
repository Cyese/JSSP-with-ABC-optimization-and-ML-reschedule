from schedu import *
# import matplotlib


path = r"D:/Project/SisThesis/"
data = pd.read_excel(path+"data.xlsx", sheet_name=2, usecols="B:G")
x = 206
Demand1 = [int(data.loc[x][_]) for _ in range(6)]
Demand2 = [int(data.loc[x+1][_]) for _ in range(6)]
Total = [Demand2[_] + Demand1[_] for _ in range(6)]
for index in range(3, 6):
    Total[index] //= 3
    # Demand2[index] //= 3

schedule = Schedule(Total)
# schedule.add(Demand2)
result, cycle, output = schedule.run()

file = open("sample_init_sched.txt", "w+")
for timestamp in result:
    file.writelines(' '.join(str(ele) for ele in timestamp) + '\n') 
print(cycle)
print(output)
print(Total)
