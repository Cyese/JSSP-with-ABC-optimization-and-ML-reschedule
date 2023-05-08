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


def make_operation_node(arr: list[list[list[int]]]) -> list[int]:
    """
        @param arr :2-D operating
        @return : list of operations
    """
    result = [0 for i in range(4)]
    for i in range(4):
        result[i] = arr[i//2][i%2][1]
    return result


def split_task(arr: list) -> tuple:
    arr2 = list(arr)
    first = []
    second = []
    for _ in range(3):
        first.append(arr.index(arr2.pop(arr2.index(max(arr2)))))
    for i in arr2:
        second.append(arr.index(i))
    return first, second

def get_max(table : list, task: list) -> int:
    _max = 0
    for i in task:
        _max = max(_max, table[1][i])
    if _max == 0:
        return -1 
    return table[1].index(_max)