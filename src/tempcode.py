from ultilities import *

test1 = [1,2,2,3,1,3,3,1,2,4,1,3,4,2,1]
test2 = [1,2,2,3,1,3,3,1,2,4,1,3,4,2,1]
test2.reverse()
for _ in range(100):
    block_a= sorted(np.random.choice(range(len(test1)//2), size=2, replace=False).tolist())
    block_b= sorted(np.random.choice(range(len(test2)//2), size=2, replace=False).tolist())
    if block_a[0]==block_a[1] or block_b[0]==block_b[1]:
        print(f"Dup at {_}")
# block_b= sorted(np.random.choice(range(len(test2)//2), size=2).tolist())

# print(block_a)
# print(block_b)
