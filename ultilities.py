import pandas as pd
import numpy as np

def check(arr: list):
    """Check if all opertaion is empty ( $==0 )
        @param arr: list of demand/pending task
        @return : all empty -> true
    """
    No_More_Operation = True
    for operation in arr:
        No_More_Operation = No_More_Operation and operation == 0
    return No_More_Operation

def operation_node(arr :list[list]):
    """Return opertaion list
        @param arr :2-D operating list
        @return : list of opertaion
    """
    result = [int for _ in range(len(arr))]
    for i in range(len(arr)):
        result[i] = arr[i][0]
    return result
