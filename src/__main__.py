from optimize import BeeColony
from graph import draw_chart, draw_sample, display
from utilities import make_dir, os
from reschedule import ProductionDisturbance, generate_production
from data import Data
from machine_learning import run_DecisionTree
from shutil import rmtree

exited = False 

def cls():
    os.system('cls')

def display_schedule(weeks: int):
    print(f"Displaying schedule of week: {weeks}")
    display(weeks)

def runDS():
    print("Fletching data from data/feature.csv")
    print("Result for sample size of 5%")
    run_DecisionTree()

def rerun_everything():
    make_dir()
    sched = "sched/week_{}"
    resched = "resched/week_{}"
    disturb =  "disturbance/week_{}"
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
        Bee =BeeColony(weeks)
        limit = Bee.optimize()
        draw_chart(weeks, limit)
        draw_sample(weeks)
    print("Generated new schedule")
    print("Generating disturbance")
    for weeks in range(311):
        generate_production(weeks)
    print("Generated disturbanced")
    print("Rescheduling")
    ProductionDisturbance()
    print("Rescheduled")
    print("Collecting data for model training")
    _ = Data().make_data()
    print("Data collected and stored")

def continual_prompt():
    input("Press <<Enter>> to continue\n")
    cls()

cls()
while not exited:
    try:
        print("Choose what to run: ")
        print("press (1) for displaying a schedule")
        print("press (2) for running decision tree")
        print("press (3) for re-running every thing <<Note: it take very long>>")
        print("press (4) for exiting")
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
            print("Please type <<Y>> to continue:")
            confirm = input(">>> ")
            if confirm == "Y":
                rerun_everything()
                continual_prompt()
            else:
                print("Canceled")
        elif choice == 4: 
            exited = True
            Data().make_data()
            print("Exiting")
        else:
            print("Unknown option")
    except:
        print("Something went wrong, please try again!")

