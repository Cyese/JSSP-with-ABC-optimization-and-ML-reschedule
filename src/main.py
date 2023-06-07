from optimize import BeeColony
from graph import draw_chart, draw_sample, display
from utilities import make_dir
from resched import gen_variant_and_reschedule


make_dir()
# make_disturbance()
weeks = int(input("Enter a weeks for optimization: "))
bee = BeeColony(weeks)
limit = bee.optimize()
draw_chart(weeks, limit)
draw_sample(weeks)
display(weeks)
gen_variant_and_reschedule(weeks)
