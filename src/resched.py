from utilities import *


def time_variant(weeks: int):
    og_sched = get_output_sched(weeks)
    span: int
    with open(f"./sched/week_{weeks}/span.txt", "r") as file:
        span = int(file.read())
    rate = np.array([0.05, 0.9, 0.05])
    generator = np.random.choice([-1, 0, 1], p=rate, size=(4, span))
    generator = generator.tolist()
    variant = {int : tuple}
    for x in len(generator):


time_variant(0)
