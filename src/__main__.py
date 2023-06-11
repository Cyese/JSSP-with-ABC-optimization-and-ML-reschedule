from optimize import BeeColony
from graph import draw_chart, draw_sample, display
from utilities import make_dir
from reschedule import ProductionDisturbance, MaintenanceDisturbance
from data import Data


# make_dir()

# for week in range(311):
#     # week = int(input("Enter a weeks for optimization: "))
#     bee = BeeColony(week)
#     limit = bee.optimize()
#     draw_chart(week, limit)
#     draw_sample(week)
#     generate_production(week)

# ProductionDisturbance()
# MaintenanceDisturbance()
# display(8)

Data()
