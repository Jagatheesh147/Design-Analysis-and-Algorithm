"""
Efficient Bin Packing using Approximation Algorithms
-----------------------------------------------------
Implements First Fit, First Fit Decreasing, Best Fit, and
Best Fit Decreasing heuristics for the Bin Packing Problem.

Bin Packing is NP-hard, so these are polynomial-time approximation
algorithms that give near-optimal solutions in practice.
"""

import random


# ---------------------------------------------------------------
# 1. Next Fit (NF)
# Time Complexity: O(n)
# Approximation ratio: 2 * OPT
# ---------------------------------------------------------------
def next_fit(items, capacity):
    bins = [0]  # remaining space tracked implicitly via fill level
    fill = [0]

    for item in items:
        if fill[-1] + item <= capacity:
            fill[-1] += item
        else:
            fill.append(item)

    return _fill_to_bins(items, fill, capacity, strategy="next")


def _fill_to_bins(items, fill_levels, capacity, strategy):
    # Helper not used directly for packing correctness display;
    # kept minimal — actual bin contents are tracked in each function below.
    return fill_levels


# ---------------------------------------------------------------
# 2. First Fit (FF)
# Time Complexity: O(n^2) naive, O(n log n) with balanced BST
# Approximation ratio: ~1.7 * OPT
# ---------------------------------------------------------------
def first_fit(items, capacity):
    bins = []  # each element = remaining capacity of that bin
    bin_contents = []

    for item in items:
        placed = False
        for i in range(len(bins)):
            if bins[i] >= item:
                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break
        if not placed:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ---------------------------------------------------------------
# 3. First Fit Decreasing (FFD)
# Sort items descending, then apply First Fit.
# Approximation ratio: 11/9 * OPT + 6/9
# ---------------------------------------------------------------
def first_fit_decreasing(items, capacity):
    sorted_items = sorted(items, reverse=True)
    return first_fit(sorted_items, capacity)


# ---------------------------------------------------------------
# 4. Best Fit (BF)
# Places item in the bin that leaves the least remaining space.
# Approximation ratio: ~1.7 * OPT
# ---------------------------------------------------------------
def best_fit(items, capacity):
    bins = []
    bin_contents = []

    for item in items:
        best_index = -1
        min_space_left = capacity + 1

        for i in range(len(bins)):
            if bins[i] >= item and (bins[i] - item) < min_space_left:
                min_space_left = bins[i] - item
                best_index = i

        if best_index != -1:
            bins[best_index] -= item
            bin_contents[best_index].append(item)
        else:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ---------------------------------------------------------------
# 5. Best Fit Decreasing (BFD)
# Sort items descending, then apply Best Fit.
# Approximation ratio: 11/9 * OPT + 6/9 (matches FFD in practice, often better)
# ---------------------------------------------------------------
def best_fit_decreasing(items, capacity):
    sorted_items = sorted(items, reverse=True)
    return best_fit(sorted_items, capacity)


# ---------------------------------------------------------------
# Utility: compute stats for a packing result
# ---------------------------------------------------------------
def packing_stats(bin_contents, capacity):
    num_bins = len(bin_contents)
    fill_levels = [sum(b) for b in bin_contents]
    avg_utilization = sum(fill_levels) / (num_bins * capacity) * 100 if num_bins else 0
    return num_bins, fill_levels, avg_utilization


# ---------------------------------------------------------------
# Benchmarking / Comparison
# ---------------------------------------------------------------
def benchmark(items, capacity):
    algorithms = {
        "First Fit":            first_fit,
        "First Fit Decreasing": first_fit_decreasing,
        "Best Fit":             best_fit,
        "Best Fit Decreasing":  best_fit_decreasing,
    }

    print(f"Items: {items}")
    print(f"Bin capacity: {capacity}\n")
    print(f"{'Algorithm':<22}{'Bins used':<12}{'Avg Utilization %':<20}")
    print("-" * 54)

    for name, func in algorithms.items():
        result = func(items, capacity)
        num_bins, fill_levels, avg_util = packing_stats(result, capacity)
        print(f"{name:<22}{num_bins:<12}{avg_util:<20.2f}")

    print()
    for name, func in algorithms.items():
        result = func(items, capacity)
        print(f"{name}: {result}")


if __name__ == "__main__":
    # --- Example 1: Small illustrative example ---
    print("=== Example 1: Small item set ===")
    items = [4, 8, 1, 4, 2, 1]
    capacity = 10
    benchmark(items, capacity)

    # --- Example 2: Larger randomized item set ---
    print("\n=== Example 2: Larger random item set ===")
    random.seed(42)
    capacity = 50
    large_items = [random.randint(1, capacity) for _ in range(30)]
    benchmark(large_items, capacity)