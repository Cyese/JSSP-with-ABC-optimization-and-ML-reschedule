from optimize import BeeColony
from graph import draw_chart

weeks = int(input("Enter a weeks for optimization: "))

bee = BeeColony(weeks)
limit = bee.optimize()
draw_chart(weeks, limit)
