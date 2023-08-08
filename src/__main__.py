from optimize import BeeColony
from graph import draw_chart, draw_sample, display
from utilities import make_dir, os, plot, Image
from reschedule import ProductionDisturbance, NewOrder, MaintenanceDisturbance, generate_all_disturbance
import data
import classify
import rainingforest
import mlp
from shutil import rmtree

exited = False


def cls():
    os.system('cls')


def display_schedule(weeks: int):
    print(f"Displaying schedule of week: {weeks}")
    display(weeks)


def runDS():
    cls()
    folder = "misc/"
    sth = ["product", "order" , "maintain"]
    print("Choose machine learning method to display:")
    print("press (1) for Classify Tree")
    print("press (2) for Raining Forest")
    print("press (3) for MLP")
    _input = int(input(">>> "))
    folder += "ClassifyTree/" if _input == 1 else ( "RandomForest/" if _input == 2 else "MLP/")
    print("Choose result to display:")
    print("press (1) for Confusion matrix")
    print("press (2) for Balanced confusion matrix")
    print("press (3) for Decision tree")
    _input = int(input(">>> "))
    heading_str = "confusion_matrix_"if _input == 1 else ( "balanced_confusion_matrix_" if _input == 2 else "DecesionTree_")
    _file = folder + heading_str
    image_list = [_file +  _ + ".png" for _ in sth]
    fig, axes = plot.subplots(nrows=1, ncols=3)
    for index, image in enumerate(image_list):
        _image = Image.open(image)
        axes[index].imshow(_image)
        axes[index].axis('off')
        _image.close()
    plot.tight_layout()
    plot.show()


def rerun_everything():
    make_dir()
    sched = "sched/week_{}"
    resched = "resched/week_{}"
    disturb = "disturbance/week_{}"
    sample = "sample/week_{}"
    print("Deleting old file")
    os.remove("data/feature.csv")
    for weeks in range(311):
        rmtree(sched.format(weeks))
        rmtree(resched.format(weeks))
        rmtree(disturb.format(weeks))
        rmtree(sample.format(weeks))
    print("Deleted old files")
    print("Generating new schedule")
    for weeks in range(311):
        Bee = BeeColony(weeks)
        limit = Bee.optimize()
        draw_chart(weeks, limit)
        draw_sample(weeks)
    print("Generated new schedule")
    print("Generating disturbance")
    generate_all_disturbance()
    print("Generated disturbance")
    print("Rescheduling")
    ProductionDisturbance()
    NewOrder()
    MaintenanceDisturbance()
    print("Rescheduled")
    print("Collecting data for model training")
    data.run()
    print("Data collected and stored")


def continual_prompt():
    input("Press <<Enter>> to continue\n")
    cls()


def fresh_run():
    make_dir()
    print("Generating new schedule")
    for weeks in range(311):
        Bee = BeeColony(weeks)
        limit = Bee.optimize()
        draw_chart(weeks, limit)
        draw_sample(weeks)
    print("Generated new schedule")
    print("Generating disturbance")
    generate_all_disturbance()
    print("Generated disturbance")
    print("Rescheduling")
    ProductionDisturbance()
    NewOrder()
    MaintenanceDisturbance()
    print("Rescheduled")
    print("Collecting data for model training")
    data.run()
    print("Data collected and stored")


cls()
while not exited:
    try:
        print("Choose what to run: ")
        print("press (1) for displaying a schedule")
        print("press (2) for running decision tree")
        print("press (3) for running for the first time <<Note: it take very long>>")
        print("press (4) for re-running every thing <<Note: it take very long>>")
        print("press (5) for exiting")
        choice = int(input(">>> "))
        cls()
        if choice == 1:
            print("Enter a week for displaying schedule (range: [0,310]):")
            week = int(input(">>> "))
            display_schedule(week)
            continual_prompt()
        elif choice == 2:
            runDS()
            continual_prompt()
        elif choice == 3:
            fresh_run()
        elif choice == 4:
            print("Please type <<Y>> to continue:")
            confirm = input(">>> ")
            if confirm == "Y":
                rerun_everything()
                continual_prompt()
            else:
                print("Canceled")
        elif choice == 5:
            exited = True
            print("Exiting")
        else:
            print("Unknown option")
    except Exception as x:
        print("Something went wrong, please try again!")
        print(f"Exception : {x}")
