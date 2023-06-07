import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import os
from machine import *
from PIL import Image
import glob
import json

write_out_path = r"./sample/"


def make_dir():
    path_list = [
        r"./sample/",
        r"./sched",
        r"./resched",
        r"./resched/",
        r"./disturbance"
    ]
    for _directory in path_list:
        if not os.path.exists(_directory):
            os.mkdir(_directory)


def check(arr: list):
    """Check if all operation is empty ( $==0 )
        @param arr: list of demand/pending task
        @return : all empty -> true
    """
    No_More_Operation = True
    for operation in arr:
        No_More_Operation = No_More_Operation and operation == 0
    return No_More_Operation


def make_operation_node(arr: list[MachinePhase1 | MachinePhase2]) -> list[int]:
    """
        @param arr :2-D operating
        @return : list of operations
    """
    result = [0 for _ in range(4)]
    for i in range(4):
        result[i] = arr[i].get_config()
        if result[i] == -1:
            result[i] = 8
    return result


# def split_task(arr: list) -> tuple:
#     arr2 = list(arr)
#     first = []
#     second = []
#     for _ in range(3):
#         first.append(arr.index(arr2.pop(arr2.index(max(arr2)))))
#     for i in arr2:
#         second.append(arr.index(i))
#     return first, second


def get_max(table: list, task: list[bool]) -> int:
    _max = 0
    for i in range(len(task)):
        if _max <= table[i] and not task[i]:
            _max = table[i]
    if _max == 0:
        return -1
    return table.index(_max)


def unassigned(arr: list[list[int]]) -> bool:
    for x in range(len(arr)):
        if arr[x][0] == -1:
            return True
    return False


def ORead(weeks: int, _path: int) -> list[list[int]]:
    result = []
    with open(r"./sample/week_{}/path_{}.txt".format(weeks, _path), "r") as file:
        lines = file.readlines()
    for line in lines:
        result.append([int(_) for _ in line.split() if _ != '7' and _ != '8'])
    result = result[0:2]
    return compress(result)  # value
    # return result


def OutputCompress(weeks: int) -> list[list[int]]:
    result: list[list[int]] = []
    with open(r"./sched/week_{}/raw.txt".format(weeks), "r") as file:
        lines = file.readlines()
    for line in lines:
        result.append([int(_) for _ in line.split() if _ != '7' and _ != '8'])
    result = result[0:2]
    return compress(result)


def skip(arr: list[list[int]]) -> list:
    result = [[x for x in y if x != 7 and x != 8] for y in arr]
    return result


# OpenAI code, quite useful
def get_sequences(lst: list[int]):
    # Initialize variables to track the current sequence
    start_index = 0
    current_value = lst[0]
    current_length = 1

    # Iterate over the list starting from the second element
    for i in range(1, len(lst)):
        if lst[i] == current_value:
            # If the current element is the same as the previous element,
            # increment the current sequence length
            current_length += 1
        else:
            # If the current element is different from the previous element,
            # yield the current sequence and start a new one
            yield lst[start_index], start_index, current_length
            start_index = i
            current_value = lst[i]
            current_length = 1

    # Yield the final sequence
    yield lst[start_index], start_index, current_length


def compress(arr: list[list[int]]) -> list:
    result = [[], []]
    for x in range(2):
        # a : int = -1
        compressed = get_sequences(arr[x])
        for item in compressed:
            result[x].extend([item[0] for _ in range(item[2] // 2)])
    return result


def get_initial_fitness(weeks: int, quantity: int) -> tuple[list[int], list[int]]:
    result: list[int]
    fitness_value: list[int]
    with open("./sample/week_{}/span.txt".format(weeks), "r") as file:
        lines = file.readlines()
        result = [int(line.strip()) for line in lines]
    # rate = np.array(result)
    # rate = rate.sum() / rate
    # rate = rate / rate.sum()
    choice = sorted(np.random.choice(len(result), size=quantity).tolist())  # , p=rate
    fitness_value = [result[_] for _ in choice]
    return choice, fitness_value


def node_encode(arr: list[int]) -> list[tuple[int, int]]:
    operating_string = []
    start_index = 0
    ref = arr[0]
    for i in range(1, len(arr)):
        if arr[i] != ref:
            operating_string.append((ref, i - start_index))
            start_index = i
            ref = arr[i]
    operating_string.append((ref, len(arr) - start_index))
    return operating_string


def node_decode(arr: list[tuple]) -> list[int]:
    result = []
    for item in arr:
        result.extend([item[0] for _ in range(item[1])])
    return result


def get_output_sched(weeks: int) -> list[list[int]]:
    result: list[list[int]]
    result = [[] for _ in range(4)]
    with open("./sched/week_{}/raw.txt".format(weeks), "r") as file:
        lines = file.readlines()
        for x, line in enumerate(lines):
            result[x].extend([int(_) for _ in line.split()])
    return result


def end_before(arr: list[list[int]], para: int) -> int:
    iter_range = range(len(arr[para]))
    reversed(iter_range)
    count1, count2 = 0, 0
    stop = [False for _ in range(2)]
    for _ in iter_range:
        if arr[para + 0][_] != 8:
            stop[0] = True
        else:
            count1 += 1
        if arr[para + 1][_] != 8:
            stop[1] = True
        else:
            count2 += 1
        if stop[0] and stop[1]:
            break
    return para if count1 > count2 else (para + 1)
    # return sth: int =0
