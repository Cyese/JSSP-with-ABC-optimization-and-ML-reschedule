from utilities import *

datas = json.load(open(f'disturbance/week_7/order.json'))
for data in datas:
    for fragment in datas[data]:
        print(type(fragment))