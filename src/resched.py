from utilities import *

def time_variant(weeks : int):
    rate = np.array([0.05, 0.9,0.05])

    generator = np.random.choice([-1,0,1], p=rate, size=(4,120))
    generator =generator.tolist()

    og_sched = get_output_sched(weeks)


og_sched = get_output_sched(0)
print(og_sched)