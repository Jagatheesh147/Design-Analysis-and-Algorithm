def find_min_max(arr, low, high):
    """
    Recursively finds the minimum and maximum values in arr[low..high]
    using Divide and Conquer.
    Returns a tuple (min_value, max_value).
    """
    # Base case: only one element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        else:
            return arr[high], arr[low]

    # Divide: split the array into two halves
    mid = (low + high) // 2

    # Conquer: recursively find min/max of each half
    left_min, left_max = find_min_max(arr, low, mid)
    right_min, right_max = find_min_max(arr, mid + 1, high)

    # Combine: compare results of both halves
    overall_min = min(left_min, right_min)
    overall_max = max(left_max, right_max)

    return overall_min, overall_max


# Driver code
if __name__ == "__main__":
    arr = [22, 4, 45, 65, 1, 30, 99, 7, 12, 3]

    n = len(arr)
    minimum, maximum = find_min_max(arr, 0, n - 1)

    print("Array:", arr)
    print("Minimum value:", minimum)
    print("Maximum value:", maximum)