from reschedule import *
from data import Data
# # # import json

make_dir()
ProductionDisturbance()
MaintenanceDisturbance()
# from utilities import glob
# week = 0
# _directory = f"./resched/week_{week}"

# list_file = glob.glob(_directory + "./operation*.json")
# for file in list_file:
#     _directory = f"./resched/week_{week}"
#     list_file = glob.glob(_directory + "./operation*.json")
#     for file in list_file:
# print(Data.DataByWeek(0).get_data())

data_for_ml = Data()
print(data_for_ml.data)
