"""
    Module use for testing code
"""


from utilities import node_encode, node_decode
import numpy as np
# import random

test1 = [1,1,1,1,2,2,3,3]
test2 = [4,4,4,4,5,5,5,0,0,0,0,00,5,5,5,5,5,5,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0]

# print(test1)
# print(test2)

series = node_encode(test2)
print(series)
# series_2 = node_encode(test2)
# x = np.random.choice(range(len(series_1)))
# y = np.random.choice(range(len(series_2)))
# series_1[x], series_2[y] = series_2[y],series_1[x]
# # l1, l2 = sum(_[1] for _ in series_1), sum(_[1] for _ in series_2) 
# # print(f"1: {l1}, 2:{l2}")

start_index = np.random.choice(range(len(series)-1))  # Ensure that there will always be 2 node if possible
end_index = np.random.choice(range(start_index+2, len(series)+1))
hold = series[start_index: end_index]
print(hold)
hold.reverse()
series[start_index: end_index] = hold
print(start_index, end_index)
print(series)

# test1 = node_decode(series_1)
# test2 = node_decode(series_2)

# print(test1)
# print(test2)
