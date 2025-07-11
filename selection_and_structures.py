# Part 1: Selection Algorithms

import random
import time
import statistics

# Deterministic Selection Algorithm: Median of Medians
def median_of_medians(arr, k):
    """
    Finds the k-th smallest element in an array using the Median of Medians algorithm.
    
    This algorithm guarantees O(n) worst-case time complexity by selecting a good pivot
    (the median of medians) that ensures a balanced partition.
    
    Parameters:
    - arr: List of integers
    - k: The order statistic to find (1-based index)
    
    Returns:
    - The k-th smallest element in arr
    """
    if len(arr) <= 5:
        # For small arrays, sorting is efficient enough
        return sorted(arr)[k - 1]
    
    # Divide the array into groups of 5 and find the median of each group
    medians = []
    for i in range(0, len(arr), 5):
        group = arr[i:i + 5]
        medians.append(sorted(group)[len(group) // 2])
    
    # Recursively find the median of the medians to use as the pivot
    pivot = median_of_medians(medians, len(medians) // 2 + 1)
    
    # Partition the array around the pivot
    left, right = [], []
    pivot_count = 0
    for x in arr:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            pivot_count += 1  # Count occurrences of the pivot for accurate positioning
    
    # Determine which partition contains the k-th element and recurse accordingly
    if k <= len(left):
        return median_of_medians(left, k)
    elif k > len(left) + pivot_count:
        return median_of_medians(right, k - len(left) - pivot_count)
    else:
        return pivot  # k falls within the pivot's position

# Randomized Selection Algorithm: Quickselect
def randomized_quickselect(arr, k):
    """
    Finds the k-th smallest element in an array using Randomized Quickselect.
    
    This algorithm has an expected O(n) time complexity due to random pivot selection,
    which on average leads to balanced partitions.
    
    Parameters:
    - arr: List of integers
    - k: The order statistic to find (1-based index)
    
    Returns:
    - The k-th smallest element in arr
    """
    if len(arr) == 1:
        return arr[0]  # Base case: single element
    
    # Select a random pivot to partition the array
    pivot_idx = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_idx]
    
    # Partition the array into elements less than, equal to, and greater than the pivot
    left, right = [], []
    pivot_count = 0
    for x in arr:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            pivot_count += 1  # Count occurrences of the pivot
    
    # Recurse into the appropriate partition based on k
    if k <= len(left):
        return randomized_quickselect(left, k)
    elif k > len(left) + pivot_count:
        return randomized_quickselect(right, k - len(left) - pivot_count)
    else:
        return pivot  # k falls within the pivot's position

# Empirical Testing Function
def test_selection_algorithms():
    """
    Tests the performance of both selection algorithms on various input sizes and distributions.
    
    This function generates arrays of different sizes and distributions, measures the average
    running time of each algorithm over multiple runs, and stores the results for analysis.
    
    Returns:
    - A dictionary containing average running times for each algorithm and input type
    """
    sizes = [100, 1000, 10000]  # Array sizes to test
    distributions = {
        "random": lambda n: [random.randint(0, 1000) for _ in range(n)],  # Random integers
        "sorted": lambda n: list(range(n)),  # Already sorted array
        "reverse_sorted": lambda n: list(range(n - 1, -1, -1)),  # Reverse sorted array
        "duplicates": lambda n: [random.randint(0, 10) for _ in range(n)]  # Array with many duplicates
    }
    
    results = {"MoM": {}, "Quickselect": {}}  # Dictionary to store results
    for size in sizes:
        for dist_name, dist_func in distributions.items():
            arr = dist_func(size)  # Generate array based on distribution
            k = size // 2  # Find the median (k = n/2)
            times = {"MoM": [], "Quickselect": []}  # Lists to store running times
            
            for _ in range(5):  # Run each test 5 times to average out variations
                arr_copy = arr.copy()  # Copy to avoid modifying the original array
                start = time.time()
                median_of_medians(arr_copy, k)
                times["MoM"].append(time.time() - start)
                
                arr_copy = arr.copy()
                start = time.time()
                randomized_quickselect(arr_copy, k)
                times["Quickselect"].append(time.time() - start)
            
            # Calculate and store the average time for each algorithm and input type
            results["MoM"][f"{dist_name}_{size}"] = statistics.mean(times["MoM"])
            results["Quickselect"][f"{dist_name}_{size}"] = statistics.mean(times["Quickselect"])
    
    return results

# Part 2: Elementary Data Structures

# Stack Implementation
class Stack:
    """
    A simple stack implementation using a Python list.
    
    Stacks follow the Last In, First Out (LIFO) principle.
    """
    def __init__(self):
        self.items = []  # Internal list to store stack elements
    
    def push(self, item):
        """Adds an item to the top of the stack."""
        self.items.append(item)
    
    def pop(self):
        """Removes and returns the top item from the stack. Raises IndexError if empty."""
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Stack is empty")
    
    def peek(self):
        """Returns the top item without removing it. Raises IndexError if empty."""
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("Stack is empty")
    
    def is_empty(self):
        """Checks if the stack is empty."""
        return len(self.items) == 0

# Queue Implementation
class Queue:
    """
    A simple queue implementation using a Python list.
    
    Queues follow the First In, First Out (FIFO) principle.
    Note: This implementation uses list.append() for enqueue (O(1)) and list.pop(0) for dequeue (O(n)).
    """
    def __init__(self):
        self.items = []  # Internal list to store queue elements
    
    def enqueue(self, item):
        """Adds an item to the end of the queue."""
        self.items.append(item)
    
    def dequeue(self):
        """Removes and returns the front item from the queue. Raises IndexError if empty."""
        if not self.is_empty():
            return self.items.pop(0)  # O(n) operation due to shifting elements
        raise IndexError("Queue is empty")
    
    def peek(self):
        """Returns the front item without removing it. Raises IndexError if empty."""
        if not self.is_empty():
            return self.items[0]
        raise IndexError("Queue is empty")
    
    def is_empty(self):
        """Checks if the queue is empty."""
        return len(self.items) == 0

# Linked List Implementation
class Node:
    """
    A node class for the singly linked list.
    
    Each node contains data and a reference to the next node.
    """
    def __init__(self, data):
        self.data = data
        self.next = None  # Reference to the next node

class LinkedList:
    """
    A singly linked list implementation.
    
    Supports insertion at the head, deletion by value, and traversal.
    """
    def __init__(self):
        self.head = None  # Head of the linked list
    
    def insert_head(self, data):
        """Inserts a new node with the given data at the head of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    
    def delete(self, data):
        """Deletes the first node with the given data value."""
        if not self.head:
            return  # List is empty
        if self.head.data == data:
            self.head = self.head.next  # Remove head if it matches
            return
        current = self.head
        while current.next and current.next.data != data:
            current = current.next
        if current.next:
            current.next = current.next.next  # Skip the node to delete it
    
    def traverse(self):
        """Returns a list of all elements in the linked list."""
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

# Main execution for testing
if __name__ == "__main__":
    # Test Selection Algorithms
    results = test_selection_algorithms()
    print("Empirical Results:")
    for algo, data in results.items():
        print(f"{algo}:")
        for key, value in data.items():
            print(f"  {key}: {value:.6f} seconds")
    
    # Test Data Structures
    stack = Stack()
    stack.push(1)
    stack.push(2)
    print("Stack peek:", stack.peek())  # Should print 2
    
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    print("Queue peek:", queue.peek())  # Should print 1
    
    ll = LinkedList()
    ll.insert_head(1)
    ll.insert_head(2)
    print("Linked List:", ll.traverse())  # Should print [2, 1]