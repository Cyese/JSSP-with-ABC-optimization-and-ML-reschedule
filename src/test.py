from utilities import *

randint = np.random.randint

week =  7
_quantity = [1, 2, 3, 4]
cycle = 100
rates = [0.4, 0.3, 0.2 , 0.1] # mean = 2
no_of_orders = randint(low=4, high= 7)
# for order in range(no_of_orders):
order_quantity = np.random.choice(_quantity,size=(no_of_orders), p= rates).tolist()
result = {}
for index, order in enumerate(order_quantity):
    _type = randint(6)
    _timestep = randint(cycle)
    result.update({index : [_type, _timestep, order]})
json.dump(result, open(f"./disturbance/week_{week}/order.json", "w+"))