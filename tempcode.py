test = [1,2,2,3,1,3,3,1,2,4,1,3,4,2,1]

def multi_index(arr: list[int], value: int) -> list[int]:
    result = []
    for index in range(len(arr)):
        if arr[index] == value:
            result.append(index)
    return result


print(multi_index(test, 1))
