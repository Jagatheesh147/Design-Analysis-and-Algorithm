def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i  # index of the found element
    return -1  # not found

# Example usage
numbers = [4, 2, 7, 1, 9, 3]
result = linear_search(numbers, 7)

if result != -1:
    print(f"Element found at index {result}")
else:
    print("Element not found")