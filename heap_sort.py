"""
DSA Implementations - Data Structures & Algorithms Component
Includes: Heap Sort, Binary Search, and Kth Largest Element Finder
Used for sorting, searching, and analyzing price predictions
"""

def heapify(arr, n, i):
    """
    Heapify subtree rooted at index i
    n is size of heap
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # Check if right child exists and is greater than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # Change root if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    """
    Main heap sort function
    Time Complexity: O(n log n)
    Space Complexity: O(1)
    """
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    
    return arr


# ============================================
# BINARY SEARCH - O(log n)
# ============================================

def binary_search(arr, target):
    """
    Binary search for finding a specific price in sorted array
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Args:
        arr: Sorted array of prices
        target: Price to search for
    
    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


# ============================================
# KTH LARGEST ELEMENT - O(n log n)
# ============================================

def find_kth_largest(arr, k):
    """
    Find kth largest price using heap sort
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        arr: Array of prices
        k: Position (1 = largest, 2 = second largest, etc.)
    
    Returns:
        Kth largest price, or None if k is invalid
    
    Example:
        prices = [100, 50, 200, 75, 150]
        find_kth_largest(prices, 1)  # Returns 200 (largest)
        find_kth_largest(prices, 2)  # Returns 150 (2nd largest)
    """
    if k > len(arr) or k < 1:
        return None
    
    sorted_arr = heap_sort(arr.copy())
    return sorted_arr[-k]
