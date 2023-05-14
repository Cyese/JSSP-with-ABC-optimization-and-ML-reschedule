"""
    Module use for testing code
"""

# import numpy as np
from schedule import PhaseBaseSchedule as PBSchedule

# import random
test1 = [1, 1, 1, 1, 2, 2, 3, 3]
test2 = [4, 4, 4, 4, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0]
P1 = [test1, test2]
scheduler = PBSchedule(P1)
result, cycle = scheduler.run()
for item in result:
    print(item)
print(cycle)
