from schedule import *
# import matplotlib


path = r"D:/Project/SisThesis/"
data = pd.read_excel(path+"data.xlsx", sheet_name=2, usecols="B:G")

Demand1 = [data.loc[0][_] for _ in range(6)]

schedule = Scheduler(Demand1)

result = schedule.run()
print(result)
