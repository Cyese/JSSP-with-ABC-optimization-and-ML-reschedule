import pandas as pd
import numpy as np

def check(arr: list):
    No_More_Operation = True
    for operation in arr:
        No_More_Operation = No_More_Operation and operation == 0
    return No_More_Operation
