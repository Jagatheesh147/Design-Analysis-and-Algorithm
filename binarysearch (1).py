def binary_search(arr, target):
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid  # found it
        elif arr[mid] < target:
            low = mid + 1  # search right half
        else:
            high = mid - 1  # search left half

    return -1  # not found

# Example usage
numbers = [1, 2, 3, 4, 7, 9, 11, 15]
result = binary_search(numbers, 7)

if result != -1:
    print(f"Element found at index {result}")
else:
    print("Element not found")