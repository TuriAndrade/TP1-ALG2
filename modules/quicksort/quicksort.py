from random import randrange
from typing import Any, List


def partition(arr: List[Any], start: int, stop: int, pivotIndex: int, compare: Any):
    arr[start], arr[pivotIndex] = \
        arr[pivotIndex], arr[start]

    pivot: int = start

    i: int = start + 1

    for j in range(start + 1, stop + 1):

        if (compare(arr[j], arr[pivot])):
            arr[i], arr[j] = arr[j], arr[i]
            i = i + 1

    arr[pivot], arr[i - 1] =\
        arr[i - 1], arr[pivot]

    pivot = i - 1
    return i - 1


def quicksort(arr: Any, start: int, stop: int, compare: Any) -> None:
    if (start < stop):

        randPivot: int = randrange(start, stop)

        pivotIndex: int = partition(
            arr, start, stop, randPivot, compare)

        quicksort(arr, start, pivotIndex-1, compare)
        quicksort(arr, pivotIndex + 1, stop, compare)
