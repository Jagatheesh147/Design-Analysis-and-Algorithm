"""
Improving Quick Sort Efficiency using Randomized Algorithm
------------------------------------------------------------
Deterministic Quick Sort (always picks the last/first element as
pivot) degrades to O(n^2) on already-sorted or reverse-sorted input.

Randomized Quick Sort picks the pivot uniformly at random, which
makes the O(n^2) worst case extremely unlikely regardless of input
order, giving expected O(n log n) performance on ANY input.
"""

import random
import time
import sys

sys.setrecursionlimit(20000)


# ---------------------------------------------------------------
# 1. Deterministic Quick Sort (pivot = last element)
# Worst Case: O(n^2)  -- e.g. already sorted / reverse sorted input
# Best/Average Case: O(n log n)
# ---------------------------------------------------------------
def deterministic_quick_sort(arr):
    a = arr[:]  # avoid mutating caller's list
    comparisons = [0]
    _deterministic_sort(a, 0, len(a) - 1, comparisons)
    return a, comparisons[0]


def _deterministic_sort(a, low, high, comparisons):
    if low < high:
        pivot_index = _partition(a, low, high, high, comparisons)
        _deterministic_sort(a, low, pivot_index - 1, comparisons)
        _deterministic_sort(a, pivot_index + 1, high, comparisons)


# ---------------------------------------------------------------
# 2. Randomized Quick Sort (pivot chosen uniformly at random)
# Worst Case: O(n^2)  -- but probability is negligible
# Expected Case: O(n log n) on ANY input, regardless of order
# ---------------------------------------------------------------
def randomized_quick_sort(arr):
    a = arr[:]
    comparisons = [0]
    _randomized_sort(a, 0, len(a) - 1, comparisons)
    return a, comparisons[0]


def _randomized_sort(a, low, high, comparisons):
    if low < high:
        random_index = random.randint(low, high)
        a[random_index], a[high] = a[high], a[random_index]  # move random pivot to end
        pivot_index = _partition(a, low, high, high, comparisons)
        _randomized_sort(a, low, pivot_index - 1, comparisons)
        _randomized_sort(a, pivot_index + 1, high, comparisons)


# ---------------------------------------------------------------
# Shared Lomuto partition scheme
# ---------------------------------------------------------------
def _partition(a, low, high, pivot_pos, comparisons):
    pivot = a[pivot_pos]
    i = low - 1

    for j in range(low, high):
        comparisons[0] += 1
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]

    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1


# ---------------------------------------------------------------
# Bonus: Randomized Quick Sort with median-of-three-random
# further reduces variance in pivot quality
# ---------------------------------------------------------------
def randomized_median_of_three_quick_sort(arr):
    a = arr[:]
    comparisons = [0]
    _median_of_three_sort(a, 0, len(a) - 1, comparisons)
    return a, comparisons[0]


def _median_of_three_sort(a, low, high, comparisons):
    if low < high:
        if high - low >= 2:
            candidates = random.sample(range(low, high + 1), 3)
            candidates.sort(key=lambda idx: a[idx])
            median_index = candidates[1]
            a[median_index], a[high] = a[high], a[median_index]
        pivot_index = _partition(a, low, high, high, comparisons)
        _median_of_three_sort(a, low, pivot_index - 1, comparisons)
        _median_of_three_sort(a, pivot_index + 1, high, comparisons)


# ---------------------------------------------------------------
# Benchmarking / Comparison Utility
# ---------------------------------------------------------------
def benchmark(arr, label=""):
    algorithms = {
        "Deterministic QS":      deterministic_quick_sort,
        "Randomized QS":         randomized_quick_sort,
        "Randomized Median-of-3": randomized_median_of_three_quick_sort,
    }

    print(f"--- {label} (n={len(arr)}) ---")
    print(f"{'Algorithm':<26}{'Comparisons':<14}{'Time (s)':<12}{'Sorted OK':<10}")
    print("-" * 62)

    for name, func in algorithms.items():
        start = time.perf_counter()
        result, comparisons = func(arr)
        elapsed = time.perf_counter() - start
        is_sorted = result == sorted(arr)
        print(f"{name:<26}{comparisons:<14}{elapsed:<12.6f}{str(is_sorted):<10}")

    print()


if __name__ == "__main__":
    # --- Case 1: Random input (all algorithms perform well) ---
    random.seed(42)
    random_arr = [random.randint(1, 10000) for _ in range(2000)]
    benchmark(random_arr, "Random input")

    # --- Case 2: Already sorted input (worst case for deterministic) ---
    sorted_arr = list(range(1, 2001))
    benchmark(sorted_arr, "Already sorted input")

    # --- Case 3: Reverse sorted input (also worst case for deterministic) ---
    reverse_arr = list(range(2000, 0, -1))
    benchmark(reverse_arr, "Reverse sorted input")

    # --- Case 4: Many duplicate values ---
    duplicate_arr = [random.choice([1, 2, 3]) for _ in range(2000)]
    benchmark(duplicate_arr, "Many duplicates")