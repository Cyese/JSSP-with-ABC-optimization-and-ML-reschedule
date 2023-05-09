import pandas as pd
import numpy as np
from machine import *


def check(arr: list):
    """Check if all operation is empty ( $==0 )
        @param arr: list of demand/pending task
        @return : all empty -> true
    """
    No_More_Operation = True
    for operation in arr:
        No_More_Operation = No_More_Operation and operation == 0
    return No_More_Operation


def make_operation_node(arr: list[MachinePhase1|MachinePhase2]) -> list[int]:
    """
        @param arr :2-D operating
        @return : list of operations
    """
    result = [0 for i in range(4)]
    for i in range(4):
        result[i] = arr[i].get_config()
        if result[i] ==-1:
            result[i] = 8
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


def get_max(table: list, task: list[bool]) -> int:
    _max = 0
    for i in range(len(task)):
        if _max <= table[1][i] and not task[i]:
            _max = table[1][i]
    if _max == 0:
        return -1
    return table[1].index(_max)


def unassigned(arr: list[list[int]]) -> bool:
    for x in range(len(arr)):
        if arr[x][0] == -1:
            return True
    return False
