from optimize import BeeColony
import threading
from graph import draw_chart, draw_sample
from utilities import make_dir

make_dir()

weeks = int(input("Enter a weeks for optimization: "))
bee = BeeColony(weeks)
limit = bee.optimize()
draw_chart(weeks, limit)
draw_sample(weeks)

# draw_1 = threading.Thread(target=draw_chart, args=[weeks, limit])
# draw_2 = threading.Thread(target=draw_sample, args=[weeks])

# draw_1.start()
# draw_2.start()

# draw_1.join()
# draw_2.join()