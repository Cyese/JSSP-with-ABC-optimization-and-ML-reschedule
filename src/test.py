# from optimize import BeeColony
from graph import *
# from utilities import *
# from reschedule import *
# from shutil import rmtree

from reschedule import ProductionDisturbance, generate_all_disturbance, NewOrder
from data import DataProduct, DataNewOrder

# generate_all_disturbance()

# ProductionDisturbance()
# DataProduct.make_disturbance_sheet()
from machine_learning import *


data_src = 0 #int(input(">>>"))

meh = "order" if data_src else "product"
# NewOrder()
# DataNewOrder()
# run_DecisionTree(meh)
# balance_data(meh)
# plot_decesion_tree(meh)
# plot_correlation("order")
for x in [True, False]:
    meh = "order" if x else "product"
    for x in range(2,7):
        split_sample_test(meh, x)
