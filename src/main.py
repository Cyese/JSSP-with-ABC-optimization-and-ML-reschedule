from optimize import BeeColony
from graph import draw_chart, draw_sample, display
from utilities import make_dir
from resched import gen_variants


make_dir()

weeks = 13  # int(input("Enter a weeks for optimization: "))
bee = BeeColony(weeks)
limit = bee.optimize()
draw_chart(weeks, limit)
draw_sample(weeks)
display(weeks)

gen_variants(weeks)
