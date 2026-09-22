import json
from models import db, Question, JavaError, Admin, Competition, Participant

def get_python_questions():
    """
    Returns 20 Medium-to-Hard Python debugging questions.
    EACH question contains strictly ONE intentional bug.
    """
    return [
        {
            "order_num": 1,
            "title": "Dictionary Mutation During Iteration",
            "error_type": "Runtime Error",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function `purge_even_values` should remove all keys from the dictionary `data` whose values are even numbers, and return the modified dictionary. However, running the code raises a `RuntimeError`. Find and fix the single error.",
            "buggy_code": """def purge_even_values(data):\n    for key in data:\n        if data[key] % 2 == 0:\n            del data[key]\n    return data""",
            "correct_code": """def purge_even_values(data):\n    for key in list(data.keys()):\n        if data[key] % 2 == 0:\n            del data[key]\n    return data""",
            "explanation": "Iterating directly over `data` while mutating it with `del data[key]` triggers `RuntimeError: dictionary changed size during iteration`. Fixing it requires iterating over a snapshot: `list(data.keys())`.",
            "test_cases": [
                {"call": "purge_even_values({'a': 1, 'b': 2, 'c': 3, 'd': 4})", "expected": {"a": 1, "c": 3}, "description": "Removes even values"},
                {"call": "purge_even_values({'x': 2, 'y': 4})", "expected": {}, "description": "All even values"},
                {"call": "purge_even_values({'m': 1, 'n': 3})", "expected": {"m": 1, "n": 3}, "description": "No even values"}
            ]
        },
        {
            "order_num": 2,
            "title": "Reverse Words in Sentence",
            "error_type": "String Manipulation / Logical Error",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function `reverse_words` should reverse the order of words in a sentence string while preserving single space separation. The current implementation reverses individual characters instead of reversing the words. Fix the single error.",
            "buggy_code": """def reverse_words(sentence):\n    words = sentence.split(' ')\n    # Bug: reverses string characters rather than words list\n    return ' '.join(sentence[::-1].split(' '))""",
            "correct_code": """def reverse_words(sentence):\n    words = sentence.split(' ')\n    return ' '.join(words[::-1])""",
            "explanation": "The code sliced the raw string `sentence[::-1]` instead of reversing the list of split words `words[::-1]`.",
            "test_cases": [
                {"call": "reverse_words('Hello World')", "expected": "World Hello", "description": "Two words"},
                {"call": "reverse_words('Code Debug Conquer')", "expected": "Conquer Debug Code", "description": "Three words"},
                {"call": "reverse_words('Python')", "expected": "Python", "description": "Single word"}
            ]
        },
        {
            "order_num": 3,
            "title": "Binary Search Bound Update",
            "error_type": "Logical Error / Infinite Loop",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function `binary_search` is supposed to return the index of `target` in a sorted list `nums`, or `-1` if not found. However, when the target is greater than the midpoint value, it causes an infinite loop. Fix the single error.",
            "buggy_code": """def binary_search(nums, target):\n    low = 0\n    high = len(nums) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            low = mid  # Bug: does not increment past mid\n        else:\n            high = mid - 1\n    return -1""",
            "correct_code": """def binary_search(nums, target):\n    low = 0\n    high = len(nums) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1""",
            "explanation": "Setting `low = mid` instead of `low = mid + 1` causes an infinite loop when `low + 1 == high` and `nums[mid] < target`.",
            "test_cases": [
                {"call": "binary_search([1, 3, 5, 7, 9], 7)", "expected": 3, "description": "Target present"},
                {"call": "binary_search([1, 3, 5, 7, 9], 2)", "expected": -1, "description": "Target absent"},
                {"call": "binary_search([10], 10)", "expected": 0, "description": "Single element found"}
            ]
        },
        {
            "order_num": 4,
            "title": "Mutable Default Argument in Graph Accumulator",
            "error_type": "Function-related Error / State Leak",
            "difficulty": "Hard",
            "points": 5.0,
            "question_text": "The function `add_edge` builds an adjacency list. Because of a Python default argument pitfall, previous calls unexpectedly persist and pollute subsequent function calls. Fix the single error.",
            "buggy_code": """def add_edge(node, neighbors=[]):\n    neighbors.append(node)\n    return neighbors""",
            "correct_code": """def add_edge(node, neighbors=None):\n    if neighbors is None:\n        neighbors = []\n    neighbors.append(node)\n    return neighbors""",
            "explanation": "Default argument `neighbors=[]` is evaluated once at function definition time, sharing the same list across invocations. Use `neighbors=None` and instantiate `[]` inside the body.",
            "test_cases": [
                {"call": "[add_edge(1), add_edge(2)]", "expected": [[1], [2]], "description": "Independent calls do not share list"},
                {"call": "add_edge(3, [1, 2])", "expected": [1, 2, 3], "description": "Custom list passed in"}
            ]
        },
        {
            "order_num": 5,
            "title": "Closure Variable Scope",
            "error_type": "UnboundLocalError / Scope",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function `make_counter` returns an inner function that should increment and return a count starting from `initial`. Calling the inner function raises an `UnboundLocalError`. Fix the single error.",
            "buggy_code": """def make_counter(initial=0):\n    count = initial\n    def counter():\n        count += 1  # Bug: UnboundLocalError without nonlocal\n        return count\n    return counter""",
            "correct_code": """def make_counter(initial=0):\n    count = initial\n    def counter():\n        nonlocal count\n        count += 1\n        return count\n    return counter""",
            "explanation": "Reassigning `count` inside `counter()` makes Python treat it as a local variable unless explicitly declared with `nonlocal count`.",
            "test_cases": [
                {"call": "(lambda c: [c(), c(), c()])(make_counter(0))", "expected": [1, 2, 3], "description": "Sequential count from 0"},
                {"call": "(lambda c: [c(), c()])(make_counter(10))", "expected": [11, 12], "description": "Count starting from 10"}
            ]
        },
        {
            "order_num": 6,
            "title": "Sieve of Eratosthenes Range Boundary",
            "error_type": "Incorrect Loops / Logical Error",
            "difficulty": "Hard",
            "points": 5.0,
            "question_text": "The function `sieve_primes` should return a list of all prime numbers less than or equal to `limit`. However, for inputs where the limit itself is prime (such as 7 or 11), it fails to include the limit. Fix the single error.",
            "buggy_code": """def sieve_primes(limit):\n    if limit < 2:\n        return []\n    is_prime = [True] * limit  # Bug: length is limit instead of limit + 1\n    is_prime[0] = is_prime[1] = False\n    for p in range(2, int(limit**0.5) + 1):\n        if is_prime[p]:\n            for i in range(p * p, limit, p):\n                is_prime[i] = False\n    return [i for i in range(2, limit) if is_prime[i]]""",
            "correct_code": """def sieve_primes(limit):\n    if limit < 2:\n        return []\n    is_prime = [True] * (limit + 1)\n    is_prime[0] = is_prime[1] = False\n    for p in range(2, int(limit**0.5) + 1):\n        if is_prime[p]:\n            for i in range(p * p, limit + 1, p):\n                is_prime[i] = False\n    return [i for i in range(2, limit + 1) if is_prime[i]]""",
            "explanation": "The boolean array sizing and range limits stopped at `limit` instead of `limit + 1`, excluding the boundary prime.",
            "test_cases": [
                {"call": "sieve_primes(10)", "expected": [2, 3, 5, 7], "description": "Primes up to 10"},
                {"call": "sieve_primes(13)", "expected": [2, 3, 5, 7, 11, 13], "description": "Primes up to 13 including 13"},
                {"call": "sieve_primes(1)", "expected": [], "description": "Limit less than 2"}
            ]
        },
        {
            "order_num": 7,
            "title": "Flatten Nested List Base Case",
            "error_type": "Recursion Error",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function `flatten_list` should recursively flatten a list containing arbitrarily nested sublists into a single flat list. However, it fails when an element is already a scalar integer. Fix the single error.",
            "buggy_code": """def flatten_list(nested):\n    result = []\n    for item in nested:\n        if isinstance(item, list):\n            result.extend(flatten_list(item))\n        else:\n            result.append(nested)  # Bug: appends the whole list instead of item\n    return result""",
            "correct_code": """def flatten_list(nested):\n    result = []\n    for item in nested:\n        if isinstance(item, list):\n            result.extend(flatten_list(item))\n        else:\n            result.append(item)\n    return result""",
            "explanation": "In the `else` clause, appending `nested` instead of `item` causes wrong nesting and structure.",
            "test_cases": [
                {"call": "flatten_list([1, [2, [3, 4], 5], 6])", "expected": [1, 2, 3, 4, 5, 6], "description": "Multi-level nesting"},
                {"call": "flatten_list([[1], [2], [3]])", "expected": [1, 2, 3], "description": "List of single elements"},
                {"call": "flatten_list([])", "expected": [], "description": "Empty list"}
            ]
        },
        {
            "order_num": 8,
            "title": "2D Matrix Grid Shallow Copy",
            "error_type": "List Mutation / Reference Trap",
            "difficulty": "Hard",
            "points": 5.0,
            "question_text": "The function `init_grid` should return an `rows x cols` matrix populated with zeros, where modifying one cell does not alter any other cell. Currently, modifying `grid[0][0]` mutates every row! Fix the single error.",
            "buggy_code": """def init_grid(rows, cols):\n    # Bug: replicates the same row reference across rows\n    return [[0] * cols] * rows""",
            "correct_code": """def init_grid(rows, cols):\n    return [[0] * cols for _ in range(rows)]""",
            "explanation": "`[[0] * cols] * rows` creates multiple references to the exact same inner list. Use a list comprehension to create distinct inner lists.",
            "test_cases": [
                {"call": "(lambda g: (setattr(g[0], '__setitem__', (0, 99)) or g[0].__setitem__(0, 99) or g))(init_grid(2, 2))[1][0]", "expected": 0, "description": "Row 1 cell is unchanged when Row 0 is updated"},
                {"call": "len(init_grid(3, 4))", "expected": 3, "description": "Rows count"}
            ]
        },
        {
            "order_num": 9,
            "title": "Leap Year Conditional Precedence",
            "error_type": "Incorrect Conditions",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function `is_leap_year` should return `True` if `year` is a leap year (divisible by 4 and not divisible by 100, unless divisible by 400). Currently, it incorrectly reports century years like 1900 as leap years. Fix the single error.",
            "buggy_code": """def is_leap_year(year):\n    # Bug: Incorrect boolean condition allows century non-leap years\n    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0 if year % 4 == 0 else False""",
            "correct_code": """def is_leap_year(year):\n    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)""",
            "explanation": "Standard leap year rule: `(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)`.",
            "test_cases": [
                {"call": "is_leap_year(2000)", "expected": True, "description": "Century divisible by 400"},
                {"call": "is_leap_year(1900)", "expected": False, "description": "Century not divisible by 400"},
                {"call": "is_leap_year(2024)", "expected": True, "description": "Regular leap year"}
            ]
        },
        {
            "order_num": 10,
            "title": "Run-Length Encoding End Boundary",
            "error_type": "Logical / Off-by-one",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function `encode_rle` takes a string of characters like `'AAABBC'` and produces its run-length encoded version `'A3B2C1'`. Currently, it fails to append the final character's count. Fix the single error.",
            "buggy_code": """def encode_rle(s):\n    if not s:\n        return \"\"\n    result = []\n    count = 1\n    for i in range(1, len(s)):\n        if s[i] == s[i - 1]:\n            count += 1\n        else:\n            result.append(f\"{s[i-1]}{count}\")\n            count = 1\n    # Bug: omitted the trailing group append\n    return \"\".join(result)""",
            "correct_code": """def encode_rle(s):\n    if not s:\n        return \"\"\n    result = []\n    count = 1\n    for i in range(1, len(s)):\n        if s[i] == s[i - 1]:\n            count += 1\n        else:\n            result.append(f\"{s[i-1]}{count}\")\n            count = 1\n    result.append(f\"{s[-1]}{count}\")\n    return \"\".join(result)""",
            "explanation": "The loop finishes when reaching the end of string, so the final accumulated `s[-1]` and `count` must be appended to `result`.",
            "test_cases": [
                {"call": "encode_rle('AAABBC')", "expected": "A3B2C1", "description": "Normal string"},
                {"call": "encode_rle('WWWWWW')", "expected": "W6", "description": "All identical characters"},
                {"call": "encode_rle('')", "expected": "", "description": "Empty string"}
            ]
        },
        {
            "order_num": 11,
            "title": "Merge Sort Slice Indexing",
            "error_type": "Logical / Slicing Error",
            "difficulty": "Hard",
            "points": 5.0,
            "question_text": "In this merge sort helper function `merge(left, right)`, the remaining elements of the slices are collected incorrectly, leading to missing elements or `TypeError`. Fix the single error.",
            "buggy_code": """def merge(left, right):\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    # Bug: appends single element instead of slice of remaining\n    result.extend(left[i]) if i < len(left) else result.extend(right[j:])\n    return result""",
            "correct_code": """def merge(left, right):\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    result.extend(left[i:]) if i < len(left) else result.extend(right[j:])\n    return result""",
            "explanation": "`left[i]` is a single element, which causes `TypeError: 'int' object is not iterable` when passed to `extend()`. It should be `left[i:]`.",
            "test_cases": [
                {"call": "merge([1, 4, 7], [2, 3, 8])", "expected": [1, 2, 3, 4, 7, 8], "description": "Interleaved lists"},
                {"call": "merge([1, 2], [3, 4])", "expected": [1, 2, 3, 4], "description": "Non-overlapping lists"}
            ]
        },
        {
            "order_num": 12,
            "title": "Memoized Fibonacci Zero Value Check",
            "error_type": "Logical / Falsy Trap",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function `fib_memo` computes the n-th Fibonacci number. However, because `0` evaluates to `False` in Python, the memoization check fails for `n=0` or recomputes unnecessarily. Fix the single error in the condition.",
            "buggy_code": """def fib_memo(n, memo=None):\n    if memo is None:\n        memo = {}\n    if n in memo:\n        return memo[n]\n    if n <= 1:\n        return n\n    # Bug: does not store result in memo before returning\n    return fib_memo(n - 1, memo) + fib_memo(n - 2, memo)""",
            "correct_code": """def fib_memo(n, memo=None):\n    if memo is None:\n        memo = {}\n    if n in memo:\n        return memo[n]\n    if n <= 1:\n        return n\n    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)\n    return memo[n]""",
            "explanation": "Without `memo[n] = ...`, the computed value is never recorded into the cache dictionary, defeating memoization.",
            "test_cases": [
                {"call": "fib_memo(0)", "expected": 0, "description": "Base case n=0"},
                {"call": "fib_memo(7)", "expected": 13, "description": "Fibonacci of 7"},
                {"call": "fib_memo(10)", "expected": 55, "description": "Fibonacci of 10"}
            ]
        },
        {
            "order_num": 13,
            "title": "FIFO Queue Using Two Stacks",
            "error_type": "Logical Error",
            "difficulty": "Hard",
            "points": 5.0,
            "question_text": "The `Queue2Stacks` class implements a FIFO queue using `in_stack` and `out_stack`. The `dequeue` method is supposed to pour elements from `in_stack` to `out_stack` only when `out_stack` is empty. However, it currently pours elements on every dequeue! Fix the single error.",
            "buggy_code": """class Queue2Stacks:\n    def __init__(self):\n        self.in_stack = []\n        self.out_stack = []\n    def enqueue(self, val):\n        self.in_stack.append(val)\n    def dequeue(self):\n        # Bug: transfers elements even if out_stack still has elements\n        if not self.in_stack and not self.out_stack:\n            return None\n        while self.in_stack:\n            self.out_stack.append(self.in_stack.pop())\n        return self.out_stack.pop()""",
            "correct_code": """class Queue2Stacks:\n    def __init__(self):\n        self.in_stack = []\n        self.out_stack = []\n    def enqueue(self, val):\n        self.in_stack.append(val)\n    def dequeue(self):\n        if not self.in_stack and not self.out_stack:\n            return None\n        if not self.out_stack:\n            while self.in_stack:\n                self.out_stack.append(self.in_stack.pop())\n        return self.out_stack.pop()""",
            "explanation": "Elements from `in_stack` must only be transferred to `out_stack` when `out_stack` is empty; otherwise the FIFO order is violated.",
            "test_cases": [
                {"call": "(lambda q: [q.enqueue(1), q.enqueue(2), q.dequeue(), q.enqueue(3), q.dequeue(), q.dequeue()][-3:])(Queue2Stacks())", "expected": [1, 2, 3], "description": "Strict FIFO order preserved"},
                {"call": "Queue2Stacks().dequeue()", "expected": None, "description": "Empty queue returns None"}
            ]
        },
        {
            "order_num": 14,
            "title": "Exception Handling Masked Return",
            "error_type": "Exception Handling / Finally Trap",
            "difficulty": "Hard",
            "points": 5.0,
            "question_text": "The function `parse_and_multiply` parses an integer string and multiplies it by 2. If parsing fails, it should return -1. However, due to a `finally` block mistake, it always returns 0! Fix the single error.",
            "buggy_code": """def parse_and_multiply(s):\n    try:\n        val = int(s)\n        return val * 2\n    except ValueError:\n        return -1\n    finally:\n        return 0  # Bug: return in finally overrides try/except return""",
            "correct_code": """def parse_and_multiply(s):\n    try:\n        val = int(s)\n        return val * 2\n    except ValueError:\n        return -1\n    finally:\n        pass""",
            "explanation": "Executing a `return` statement inside a `finally` block suppresses any previous `return` or unhandled exception from the `try`/`except` block.",
            "test_cases": [
                {"call": "parse_and_multiply('21')", "expected": 42, "description": "Valid number string"},
                {"call": "parse_and_multiply('abc')", "expected": -1, "description": "Invalid string returns -1"}
            ]
        },
        {
            "order_num": 15,
            "title": "Palindrome Sentence Filter",
            "error_type": "String Manipulation / Regex",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function `is_palindrome_phrase` should check if a sentence is a palindrome, ignoring non-alphanumeric characters and case. Currently, it retains spaces and punctuation. Fix the single error.",
            "buggy_code": """def is_palindrome_phrase(s):\n    # Bug: keeps non-alphanumeric characters\n    cleaned = ''.join(c.lower() for c in s if c.isalpha() or c.isspace())\n    return cleaned == cleaned[::-1]""",
            "correct_code": """def is_palindrome_phrase(s):\n    cleaned = ''.join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]""",
            "explanation": "`c.isalpha() or c.isspace()` erroneously includes spaces and excludes numbers. It should be `c.isalnum()`.",
            "test_cases": [
                {"call": "is_palindrome_phrase('A man, a plan, a canal: Panama')", "expected": True, "description": "Classic palindrome with punctuation"},
                {"call": "is_palindrome_phrase('race a car')", "expected": False, "description": "Non-palindrome"},
                {"call": "is_palindrome_phrase('0P0')", "expected": True, "description": "Alphanumeric palindrome"}
            ]
        },
        {
            "order_num": 16,
            "title": "Validate Binary Search Tree Bounds",
            "error_type": "Logical / Tree Recursion",
            "difficulty": "Hard",
            "points": 5.0,
            "question_text": "The function `is_valid_bst` validates whether a binary tree is a valid BST. Checking only immediate children is insufficient; each node must satisfy global min/max bounds. The current code only checks immediate left and right child. Fix the single error.",
            "buggy_code": """class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):\n    if not root:\n        return True\n    if not (min_val < root.val < max_val):\n        return False\n    # Bug: passes current bounds instead of narrowing with root.val\n    return is_valid_bst(root.left, min_val, max_val) and is_valid_bst(root.right, min_val, max_val)""",
            "correct_code": """class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):\n    if not root:\n        return True\n    if not (min_val < root.val < max_val):\n        return False\n    return is_valid_bst(root.left, min_val, root.val) and is_valid_bst(root.right, root.val, max_val)""",
            "explanation": "When traversing left, the upper bound must become `root.val`. When traversing right, the lower bound must become `root.val`.",
            "test_cases": [
                {"call": "is_valid_bst(TreeNode(2, TreeNode(1), TreeNode(3)))", "expected": True, "description": "Valid BST"},
                {"call": "is_valid_bst(TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6))))", "expected": False, "description": "Invalid BST"}
            ]
        },
        {
            "order_num": 17,
            "title": "Object-Oriented Super Call in Inheritance",
            "error_type": "OOP / Inheritance Error",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The `Developer` subclass extends `Employee`. When instantiating `Developer`, an `AttributeError` occurs because the parent class attributes were never initialized. Fix the single error.",
            "buggy_code": """class Employee:\n    def __init__(self, name, emp_id):\n        self.name = name\n        self.emp_id = emp_id\n\nclass Developer(Employee):\n    def __init__(self, name, emp_id, language):\n        # Bug: missing super().__init__ call\n        self.language = language\n    def get_details(self):\n        return f\"{self.name} (#{self.emp_id}) - {self.language}\"""",
            "correct_code": """class Employee:\n    def __init__(self, name, emp_id):\n        self.name = name\n        self.emp_id = emp_id\n\nclass Developer(Employee):\n    def __init__(self, name, emp_id, language):\n        super().__init__(name, emp_id)\n        self.language = language\n    def get_details(self):\n        return f\"{self.name} (#{self.emp_id}) - {self.language}\"""",
            "explanation": "Subclass constructor must call `super().__init__(name, emp_id)` to initialize parent instance fields `name` and `emp_id`.",
            "test_cases": [
                {"call": "Developer('Alice', 101, 'Python').get_details()", "expected": "Alice (#101) - Python", "description": "Initializes and formats details correctly"}
            ]
        },
        {
            "order_num": 18,
            "title": "Longest Substring Without Repeating Characters",
            "error_type": "Logical / Sliding Window",
            "difficulty": "Hard",
            "points": 5.0,
            "question_text": "The function `length_of_longest_substring` uses a sliding window to find the length of the longest substring without repeating characters. When a repeat character is found before `start`, it incorrectly pulls `start` backwards! Fix the single error.",
            "buggy_code": """def length_of_longest_substring(s):\n    char_index = {}\n    max_len = 0\n    start = 0\n    for i, char in enumerate(s):\n        if char in char_index:\n            # Bug: sets start unconditionally to old index + 1\n            start = char_index[char] + 1\n        char_index[char] = i\n        max_len = max(max_len, i - start + 1)\n    return max_len""",
            "correct_code": """def length_of_longest_substring(s):\n    char_index = {}\n    max_len = 0\n    start = 0\n    for i, char in enumerate(s):\n        if char in char_index:\n            start = max(start, char_index[char] + 1)\n        char_index[char] = i\n        max_len = max(max_len, i - start + 1)\n    return max_len""",
            "explanation": "`start` must never move backwards when an outdated duplicate is seen outside the current window: `start = max(start, char_index[char] + 1)`.",
            "test_cases": [
                {"call": "length_of_longest_substring('abcabcbb')", "expected": 3, "description": "Substring 'abc'"},
                {"call": "length_of_longest_substring('abba')", "expected": 2, "description": "Substring 'ab' or 'ba'"},
                {"call": "length_of_longest_substring('bbbbb')", "expected": 1, "description": "All duplicates"}
            ]
        },
        {
            "order_num": 19,
            "title": "Max Heap Sift Down Swap Logic",
            "error_type": "Logical Error",
            "difficulty": "Hard",
            "points": 5.0,
            "question_text": "The function `sift_down` maintains the max-heap invariant for array `heap`. However, it incorrectly compares the left child directly to the current node without first finding which child (left or right) is larger. Fix the single error.",
            "buggy_code": """def sift_down(heap, i, n):\n    largest = i\n    left = 2 * i + 1\n    right = 2 * i + 2\n    if left < n and heap[left] > heap[largest]:\n        largest = left\n    # Bug: compares right child with left instead of heap[largest]\n    if right < n and heap[right] > heap[left]:\n        largest = right\n    if largest != i:\n        heap[i], heap[largest] = heap[largest], heap[i]\n        sift_down(heap, largest, n)\n    return heap""",
            "correct_code": """def sift_down(heap, i, n):\n    largest = i\n    left = 2 * i + 1\n    right = 2 * i + 2\n    if left < n and heap[left] > heap[largest]:\n        largest = left\n    if right < n and heap[right] > heap[largest]:\n        largest = right\n    if largest != i:\n        heap[i], heap[largest] = heap[largest], heap[i]\n        sift_down(heap, largest, n)\n    return heap""",
            "explanation": "The right child check must compare `heap[right] > heap[largest]`, not `heap[right] > heap[left]`, to determine the maximum among parent, left, and right.",
            "test_cases": [
                {"call": "sift_down([1, 14, 10, 8, 7, 9, 3], 0, 7)", "expected": [14, 8, 10, 1, 7, 9, 3], "description": "Max element sifted to root"}
            ]
        },
        {
            "order_num": 20,
            "title": "Syntax Error in Lambda Sorter Key",
            "error_type": "Syntax Error",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function `sort_students` sorts a list of student tuples `(name, grade, age)` by grade descending, then age ascending. The code currently fails with a `SyntaxError` due to malformed tuple syntax in the lambda key. Fix the single error.",
            "buggy_code": """def sort_students(students):\n    # Bug: missing comma in tuple syntax causing SyntaxError\n    return sorted(students, key=lambda s: (-s[1] s[2]))""",
            "correct_code": """def sort_students(students):\n    return sorted(students, key=lambda s: (-s[1], s[2]))""",
            "explanation": "The lambda returns a tuple of sorting keys, which requires a separating comma `(-s[1], s[2])`.",
            "test_cases": [
                {"call": "sort_students([('Alice', 85, 20), ('Bob', 90, 21), ('Charlie', 85, 19)])", "expected": [("Bob", 90, 21), ("Charlie", 85, 19), ("Alice", 85, 20)], "description": "Sorted by grade desc, age asc"}
            ]
        }
    ]


def get_java_questions():
    """
    Returns 5 Hard Java debugging questions.
    EACH question contains EXACTLY 7 intentional errors cleanly distributed across:
    1. Variable/type error
    2. Method signature error
    3. Loop error
    4. Array/Collection error
    5. Conditional logic error
    6. OOP error
    7. Exception handling / API error
    """
    return [
        {
            "order_num": 1,
            "title": "Question 1: LRU Cache Implementation",
            "difficulty": "Hard",
            "points": 14.0,
            "question_text": "The class `LRUCache` implements a Least Recently Used (LRU) Cache using a HashMap and a Doubly Linked List. The implementation contains exactly 7 intentional errors preventing it from compiling and functioning properly. Identify and resolve all 7 errors.",
            "buggy_code": """import java.util.HashMap;\nimport java.util.Map;\n\npublic class LRUCache {\n    class Node {\n        int key;\n        int value;\n        Node prev;\n        Node next;\n        // Error 1: OOP/Constructor parameter shadowing without this\n        Node(int key, int value) {\n            key = key;\n            value = value;\n        }\n    }\n\n    // Error 2: Variable Type error (capacity should not be boolean)\n    private boolean capacity;\n    private int cap;\n    private Map<Integer, Node> map;\n    private Node head, tail;\n\n    public LRUCache(int capacity) {\n        this.cap = capacity;\n        this.map = new HashMap<>();\n        head = new Node(0, 0);\n        tail = new Node(0, 0);\n        head.next = tail;\n        tail.prev = head;\n    }\n\n    // Error 3: Method signature return type void instead of int\n    public void get(int key) {\n        if (!map.containsKey(key)) {\n            return;\n        }\n        Node node = map.get(key);\n        remove(node);\n        insert(node);\n        // return node.value;\n    }\n\n    public void put(int key, int value) {\n        if (map.containsKey(key)) {\n            remove(map.get(key));\n        }\n        // Error 4: Conditional logic error (checks <= 0 instead of map.size() >= cap)\n        if (map.size() < 0) {\n            // Error 5: Collection/Null pointer removal on head instead of tail.prev\n            map.remove(head.key);\n            remove(head);\n        }\n        Node newNode = new Node(key, value);\n        map.put(key, newNode);\n        insert(newNode);\n    }\n\n    private void remove(Node node) {\n        // Error 6: Pointer reconnection logic error\n        node.prev.next = node;\n        node.next.prev = node.prev;\n    }\n\n    private void insert(Node node) {\n        // Error 7: Exception/API usage error: null pointer before linking\n        node.next = head.next;\n        head.next.prev = node;\n        head.next = null;\n        node.prev = head;\n    }\n}""",
            "correct_code": """import java.util.HashMap;\nimport java.util.Map;\n\npublic class LRUCache {\n    class Node {\n        int key;\n        int value;\n        Node prev;\n        Node next;\n        Node(int key, int value) {\n            this.key = key;\n            this.value = value;\n        }\n    }\n\n    private int cap;\n    private Map<Integer, Node> map;\n    private Node head, tail;\n\n    public LRUCache(int capacity) {\n        this.cap = capacity;\n        this.map = new HashMap<>();\n        head = new Node(0, 0);\n        tail = new Node(0, 0);\n        head.next = tail;\n        tail.prev = head;\n    }\n\n    public int get(int key) {\n        if (!map.containsKey(key)) {\n            return -1;\n        }\n        Node node = map.get(key);\n        remove(node);\n        insert(node);\n        return node.value;\n    }\n\n    public void put(int key, int value) {\n        if (map.containsKey(key)) {\n            remove(map.get(key));\n        }\n        if (map.size() >= cap) {\n            map.remove(tail.prev.key);\n            remove(tail.prev);\n        }\n        Node newNode = new Node(key, value);\n        map.put(key, newNode);\n        insert(newNode);\n    }\n\n    private void remove(Node node) {\n        node.prev.next = node.next;\n        node.next.prev = node.prev;\n    }\n\n    private void insert(Node node) {\n        node.next = head.next;\n        head.next.prev = node;\n        head.next = node;\n        node.prev = head;\n    }\n}""",
            "explanation": "Resolved 7 errors: 1) this.key assignment in Node, 2) Removed invalid boolean capacity field, 3) get() returns int, 4) Eviction condition map.size() >= cap, 5) Evicting tail.prev instead of head, 6) Reconnecting node.prev.next = node.next in remove, 7) Linking head.next = node in insert.",
            "test_cases": [{"description": "LRUCache functionality", "is_hidden": False}],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "OOP / Constructor",
                    "description": "Constructor parameters 'key' and 'value' shadow fields without 'this' keyword.",
                    "buggy_snippet": "key = key;\n            value = value;",
                    "fixed_snippet": "this.key = key;\n            this.value = value;",
                    "detection_rule": "{\"regex\": \"this\\\\.key\\\\s*=\\\\s*key\"}"
                },
                {
                    "error_number": 2,
                    "error_category": "Variable Type Error",
                    "description": "Unused or erroneous 'private boolean capacity' declaration conflicting with int capacity.",
                    "buggy_snippet": "private boolean capacity;",
                    "fixed_snippet": "// removed boolean capacity",
                    "detection_rule": "{\"anti_regex\": \"boolean\\\\s+capacity;\"}"
                },
                {
                    "error_number": 3,
                    "error_category": "Method Signature Error",
                    "description": "'get(int key)' method signature has 'void' return type instead of 'int'.",
                    "buggy_snippet": "public void get(int key)",
                    "fixed_snippet": "public int get(int key)",
                    "detection_rule": "{\"regex\": \"public\\\\s+int\\\\s+get\\\\s*\\\\(\\\\s*int\\\\s+key\\\\s*\\\\)\"}"
                },
                {
                    "error_number": 4,
                    "error_category": "Conditional Logic Error",
                    "description": "Eviction condition 'map.size() < 0' is impossible; must check 'map.size() >= cap'.",
                    "buggy_snippet": "if (map.size() < 0)",
                    "fixed_snippet": "if (map.size() >= cap)",
                    "detection_rule": "{\"regex\": \"map\\\\.size\\\\(\\\\)\\\\s*>=\\\\s*(cap|capacity)\"}"
                },
                {
                    "error_number": 5,
                    "error_category": "Collection / Pointer Error",
                    "description": "Eviction removes dummy 'head' node instead of the least recently used 'tail.prev'.",
                    "buggy_snippet": "map.remove(head.key);\n            remove(head);",
                    "fixed_snippet": "map.remove(tail.prev.key);\n            remove(tail.prev);",
                    "detection_rule": "{\"regex\": \"tail\\\\.prev\"}"
                },
                {
                    "error_number": 6,
                    "error_category": "Pointer Reconnection Error",
                    "description": "In 'remove(Node node)', 'node.prev.next' is set to 'node' creating an infinite cycle instead of 'node.next'.",
                    "buggy_snippet": "node.prev.next = node;",
                    "fixed_snippet": "node.prev.next = node.next;",
                    "detection_rule": "{\"regex\": \"node\\\\.prev\\\\.next\\\\s*=\\\\s*node\\\\.next\"}"
                },
                {
                    "error_number": 7,
                    "error_category": "Pointer Link Error",
                    "description": "In 'insert(Node node)', 'head.next = null' breaks the doubly-linked list chain instead of 'head.next = node'.",
                    "buggy_snippet": "head.next = null;",
                    "fixed_snippet": "head.next = node;",
                    "detection_rule": "{\"regex\": \"head\\\\.next\\\\s*=\\\\s*node;\"}"
                }
            ]
        },
        {
            "order_num": 2,
            "title": "Question 2: Bank Account Transaction Processor",
            "difficulty": "Hard",
            "points": 14.0,
            "question_text": "The `TransactionProcessor` class manages account balances and processes financial transfers. It contains exactly 7 intentional errors spanning thread concurrency, String equality, list bounds, exceptions, and arithmetic. Find and resolve all 7 errors.",
            "buggy_code": """import java.math.BigDecimal;\nimport java.math.RoundingMode;\nimport java.util.List;\nimport java.io.IOException;\n\npublic class TransactionProcessor {\n    // Error 1: Variable error: static balance shared across all instances\n    private static double balance;\n    private String accountCurrency = \"USD\";\n\n    public TransactionProcessor(double initialBalance) {\n        balance = initialBalance;\n    }\n\n    // Error 2: Method signature error: transfer missing synchronized for thread-safety\n    public boolean transfer(TransactionProcessor target, double amount) throws Exception {\n        // Error 3: Conditional logic error: using == for currency string comparison\n        if (this.accountCurrency == new String(\"USD\")) {\n            // valid currency\n        }\n        if (amount <= 0 || balance < amount) {\n            return false;\n        }\n        balance -= amount;\n        target.deposit(amount);\n        return true;\n    }\n\n    public void deposit(double amount) {\n        balance += amount;\n    }\n\n    // Error 4: Loop off-by-one error with list indexing\n    public double calculateTotalFees(List<Double> feeList) {\n        double total = 0;\n        for (int i = 0; i <= feeList.size(); i++) {\n            total += feeList.get(i);\n        }\n        return total;\n    }\n\n    // Error 5: OOP Access modifier error on interface/helper method\n    void validateAccount(String accId) {\n        if (accId == null || accId.isEmpty()) {\n            // Error 6: Exception type mismatch: throws IOException instead of IllegalArgumentException\n            throw new RuntimeException(\"Invalid Account\");\n        }\n    }\n\n    // Error 7: Java API error: BigDecimal divide without RoundingMode causes ArithmeticException\n    public BigDecimal splitAmount(BigDecimal amount, int parts) {\n        return amount.divide(new BigDecimal(parts));\n    }\n}""",
            "correct_code": """import java.math.BigDecimal;\nimport java.math.RoundingMode;\nimport java.util.List;\n\npublic class TransactionProcessor {\n    private double balance;\n    private String accountCurrency = \"USD\";\n\n    public TransactionProcessor(double initialBalance) {\n        this.balance = initialBalance;\n    }\n\n    public synchronized boolean transfer(TransactionProcessor target, double amount) throws Exception {\n        if (this.accountCurrency.equals(\"USD\")) {\n            // valid currency\n        }\n        if (amount <= 0 || balance < amount) {\n            return false;\n        }\n        balance -= amount;\n        target.deposit(amount);\n        return true;\n    }\n\n    public synchronized void deposit(double amount) {\n        balance += amount;\n    }\n\n    public double calculateTotalFees(List<Double> feeList) {\n        double total = 0;\n        for (int i = 0; i < feeList.size(); i++) {\n            total += feeList.get(i);\n        }\n        return total;\n    }\n\n    public void validateAccount(String accId) {\n        if (accId == null || accId.isEmpty()) {\n            throw new IllegalArgumentException(\"Invalid Account\");\n        }\n    }\n\n    public BigDecimal splitAmount(BigDecimal amount, int parts) {\n        return amount.divide(new BigDecimal(parts), 2, RoundingMode.HALF_UP);\n    }\n}""",
            "explanation": "Corrected 7 errors: 1) Removed static from balance, 2) Added synchronized to transfer/deposit, 3) Used .equals() for string comparison, 4) Fixed loop bound i < feeList.size(), 5) Made validateAccount public, 6) Used IllegalArgumentException, 7) Added RoundingMode to BigDecimal.divide().",
            "test_cases": [{"description": "Transaction processor checks", "is_hidden": False}],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Variable Scope Error",
                    "description": "'balance' is erroneously declared 'static', causing all accounts to share a single balance.",
                    "buggy_snippet": "private static double balance;",
                    "fixed_snippet": "private double balance;",
                    "detection_rule": "{\"anti_regex\": \"static\\\\s+double\\\\s+balance;\"}"
                },
                {
                    "error_number": 2,
                    "error_category": "Method Signature Error",
                    "description": "'transfer' method missing 'synchronized' modifier for thread-safe balance operations.",
                    "buggy_snippet": "public boolean transfer(TransactionProcessor target, double amount)",
                    "fixed_snippet": "public synchronized boolean transfer(TransactionProcessor target, double amount)",
                    "detection_rule": "{\"regex\": \"synchronized\\\\s+boolean\\\\s+transfer\"}"
                },
                {
                    "error_number": 3,
                    "error_category": "Conditional Logic Error",
                    "description": "String equality compared using '==' instead of '.equals()'.",
                    "buggy_snippet": "this.accountCurrency == new String(\"USD\")",
                    "fixed_snippet": "this.accountCurrency.equals(\"USD\")",
                    "detection_rule": "{\"regex\": \"accountCurrency\\\\.equals\"}"
                },
                {
                    "error_number": 4,
                    "error_category": "Loop Boundary Error",
                    "description": "Loop condition 'i <= feeList.size()' causes IndexOutOfBoundsException.",
                    "buggy_snippet": "for (int i = 0; i <= feeList.size(); i++)",
                    "fixed_snippet": "for (int i = 0; i < feeList.size(); i++)",
                    "detection_rule": "{\"regex\": \"i\\\\s*<\\\\s*feeList\\\\.size\\\\(\\\\)\"}"
                },
                {
                    "error_number": 5,
                    "error_category": "OOP Access Modifier Error",
                    "description": "'validateAccount' has package-private visibility instead of public access.",
                    "buggy_snippet": "void validateAccount(String accId)",
                    "fixed_snippet": "public void validateAccount(String accId)",
                    "detection_rule": "{\"regex\": \"public\\\\s+void\\\\s+validateAccount\"}"
                },
                {
                    "error_number": 6,
                    "error_category": "Exception Handling Error",
                    "description": "Throws generic RuntimeException instead of standard IllegalArgumentException for invalid input.",
                    "buggy_snippet": "throw new RuntimeException(\"Invalid Account\");",
                    "fixed_snippet": "throw new IllegalArgumentException(\"Invalid Account\");",
                    "detection_rule": "{\"regex\": \"IllegalArgumentException\"}"
                },
                {
                    "error_number": 7,
                    "error_category": "Java API Error",
                    "description": "BigDecimal.divide() without RoundingMode parameter causes ArithmeticException when division is non-terminating.",
                    "buggy_snippet": "amount.divide(new BigDecimal(parts))",
                    "fixed_snippet": "amount.divide(new BigDecimal(parts), 2, RoundingMode.HALF_UP)",
                    "detection_rule": "{\"regex\": \"RoundingMode\"}"
                }
            ]
        },
        {
            "order_num": 3,
            "title": "Question 3: Dijkstra Shortest Path Router",
            "difficulty": "Hard",
            "points": 14.0,
            "question_text": "The `DijkstraRouter` class finds the shortest distance between nodes in a weighted directed graph using a PriorityQueue. It contains exactly 7 intentional errors. Identify and fix all 7 errors.",
            "buggy_code": """import java.util.*;\n\npublic class DijkstraRouter {\n    // Error 1: OOP class Edge fields private with no getters, not static\n    class Edge {\n        private int target;\n        private int weight;\n        public Edge(int target, int weight) {\n            target = target;\n            weight = weight;\n        }\n    }\n\n    // Error 2: Missing Comparable / Comparator for PriorityQueue Node\n    static class NodeEntry {\n        int node;\n        int dist;\n        public NodeEntry(int node, int dist) {\n            this.node = node;\n            this.dist = dist;\n        }\n    }\n\n    // Error 3: Return type int instead of int[]\n    public int findShortestPaths(int n, List<List<Edge>> adj, int src) {\n        // Error 4: Array allocation size n instead of n + 1 for 1-based indexing\n        int[] dist = new int[n];\n        // Error 5: API initialization: Arrays.fill with 0 instead of Integer.MAX_VALUE\n        Arrays.fill(dist, 0);\n        dist[src] = 0;\n\n        PriorityQueue<NodeEntry> pq = new PriorityQueue<>((a, b) -> a.dist - b.dist);\n        pq.add(new NodeEntry(src, 0));\n\n        // Error 6: Loop condition inverted: while (pq.isEmpty())\n        while (pq.isEmpty()) {\n            NodeEntry curr = pq.poll();\n            int u = curr.node;\n\n            for (Edge edge : adj.get(u)) {\n                // Error 7: Conditional logic: if (dist[u] + edge.weight > dist[edge.target]) instead of <\n                if (dist[u] + edge.weight > dist[edge.target]) {\n                    dist[edge.target] = dist[u] + edge.weight;\n                    pq.add(new NodeEntry(edge.target, dist[edge.target]));\n                }\n            }\n        }\n        return dist[0];\n    }\n}""",
            "correct_code": """import java.util.*;\n\npublic class DijkstraRouter {\n    public static class Edge {\n        public int target;\n        public int weight;\n        public Edge(int target, int weight) {\n            this.target = target;\n            this.weight = weight;\n        }\n    }\n\n    public static class NodeEntry implements Comparable<NodeEntry> {\n        public int node;\n        public int dist;\n        public NodeEntry(int node, int dist) {\n            this.node = node;\n            this.dist = dist;\n        }\n        @Override\n        public int compareTo(NodeEntry other) {\n            return Integer.compare(this.dist, other.dist);\n        }\n    }\n\n    public int[] findShortestPaths(int n, List<List<Edge>> adj, int src) {\n        int[] dist = new int[n + 1];\n        Arrays.fill(dist, Integer.MAX_VALUE);\n        dist[src] = 0;\n\n        PriorityQueue<NodeEntry> pq = new PriorityQueue<>();\n        pq.add(new NodeEntry(src, 0));\n\n        while (!pq.isEmpty()) {\n            NodeEntry curr = pq.poll();\n            int u = curr.node;\n            if (curr.dist > dist[u]) continue;\n\n            for (Edge edge : adj.get(u)) {\n                if (dist[u] != Integer.MAX_VALUE && dist[u] + edge.weight < dist[edge.target]) {\n                    dist[edge.target] = dist[u] + edge.weight;\n                    pq.add(new NodeEntry(edge.target, dist[edge.target]));\n                }\n            }\n        }\n        return dist;\n    }\n}""",
            "explanation": "Resolved 7 errors: 1) Static Edge with proper this assignment, 2) NodeEntry implements Comparable, 3) Return type int[], 4) Array size n + 1, 5) Arrays.fill with Integer.MAX_VALUE, 6) while (!pq.isEmpty()), 7) Relaxation condition < instead of >.",
            "test_cases": [{"description": "Shortest path router checks", "is_hidden": False}],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "OOP / Field Shadowing",
                    "description": "Edge constructor parameters shadow fields without 'this', leaving target/weight unassigned.",
                    "buggy_snippet": "target = target;\n            weight = weight;",
                    "fixed_snippet": "this.target = target;\n            this.weight = weight;",
                    "detection_rule": "{\"regex\": \"this\\\\.target\\\\s*=\\\\s*target\"}"
                },
                {
                    "error_number": 2,
                    "error_category": "Type / Interface Error",
                    "description": "NodeEntry used in PriorityQueue requires Comparable interface implementation or comparator.",
                    "buggy_snippet": "static class NodeEntry",
                    "fixed_snippet": "implements Comparable<NodeEntry>",
                    "detection_rule": "{\"regex\": \"(Comparable|Comparator|Integer\\\\.compare)\"}"
                },
                {
                    "error_number": 3,
                    "error_category": "Method Signature Error",
                    "description": "findShortestPaths return type is declared as 'int' instead of 'int[]'.",
                    "buggy_snippet": "public int findShortestPaths",
                    "fixed_snippet": "public int[] findShortestPaths",
                    "detection_rule": "{\"regex\": \"public\\\\s+int\\\\s*\\\\[\\\\s*\\\\]\\\\s+findShortestPaths\"}"
                },
                {
                    "error_number": 4,
                    "error_category": "Array Sizing Error",
                    "description": "Array allocated as new int[n] instead of new int[n + 1] causing OutOfBounds on 1-indexed graph nodes.",
                    "buggy_snippet": "int[] dist = new int[n];",
                    "fixed_snippet": "int[] dist = new int[n + 1];",
                    "detection_rule": "{\"regex\": \"new\\\\s+int\\\\s*\\\\[\\\\s*n\\\\s*\\\\+\\\\s*1\\\\s*\\\\]\"}"
                },
                {
                    "error_number": 5,
                    "error_category": "API Initialization Error",
                    "description": "Distance array filled with 0 instead of Integer.MAX_VALUE (infinity).",
                    "buggy_snippet": "Arrays.fill(dist, 0);",
                    "fixed_snippet": "Arrays.fill(dist, Integer.MAX_VALUE);",
                    "detection_rule": "{\"regex\": \"Integer\\\\.MAX_VALUE\"}"
                },
                {
                    "error_number": 6,
                    "error_category": "Loop Condition Error",
                    "description": "Queue processing loop condition is inverted: 'while (pq.isEmpty())' never executes.",
                    "buggy_snippet": "while (pq.isEmpty())",
                    "fixed_snippet": "while (!pq.isEmpty())",
                    "detection_rule": "{\"regex\": \"while\\\\s*\\\\(\\\\s*!\\\\s*pq\\\\.isEmpty\\\\(\\\\)\\\\s*\\\\)\"}"
                },
                {
                    "error_number": 7,
                    "error_category": "Conditional Logic Error",
                    "description": "Edge relaxation logic checks '>' instead of '<', attempting to maximize distance rather than minimize.",
                    "buggy_snippet": "dist[u] + edge.weight > dist[edge.target]",
                    "fixed_snippet": "dist[u] + edge.weight < dist[edge.target]",
                    "detection_rule": "{\"regex\": \"dist\\\\[u\\\\]\\\\s*\\\\+\\\\s*edge\\\\.weight\\\\s*<\\\\s*dist\\\\[edge\\\\.target\\\\]\"}"
                }
            ]
        },
        {
            "order_num": 4,
            "title": "Question 4: Arithmetic Expression Parser & Evaluator",
            "difficulty": "Hard",
            "points": 14.0,
            "question_text": "The `ExpressionEvaluator` class parses and evaluates arithmetic expressions with operator precedence. It contains exactly 7 intentional errors across variables, loop bounds, exceptions, and token parsing. Identify and correct all 7 errors.",
            "buggy_code": """import java.util.Stack;\n\npublic class ExpressionEvaluator {\n    // Error 1: Uninitialized final variable\n    private final int DEFAULT_RADIX;\n    \n    public ExpressionEvaluator() {\n        // Error 2: Constructor does not initialize DEFAULT_RADIX\n    }\n\n    // Error 3: Method signature missing static or invalid parameter\n    public int evaluate(String expr) throws Exception {\n        char[] tokens = expr.toCharArray();\n        Stack<Integer> values = new Stack<>();\n        Stack<Character> ops = new Stack<>();\n\n        // Error 4: Loop condition off-by-one tokens.length instead of <\n        for (int i = 0; i <= tokens.length; i++) {\n            if (tokens[i] == ' ') continue;\n\n            if (tokens[i] >= '0' && tokens[i] <= '9') {\n                StringBuilder sb = new StringBuilder();\n                // Error 5: Loop condition without bounds check causes StringIndexOutOfBoundsException\n                while (tokens[i] >= '0' && tokens[i] <= '9') {\n                    sb.append(tokens[i++]);\n                }\n                i--;\n                values.push(Integer.parseInt(sb.toString()));\n            } else if (tokens[i] == '(') {\n                ops.push(tokens[i]);\n            } else if (tokens[i] == ')') {\n                // Error 6: Conditional logic error: checking == '(' instead of != '('\n                while (ops.peek() == '(') {\n                    values.push(applyOp(ops.pop(), values.pop(), values.pop()));\n                }\n                ops.pop();\n            } else if (tokens[i] == '+' || tokens[i] == '-' || tokens[i] == '*' || tokens[i] == '/') {\n                while (!ops.empty() && hasPrecedence(tokens[i], ops.peek())) {\n                    values.push(applyOp(ops.pop(), values.pop(), values.pop()));\n                }\n                ops.push(tokens[i]);\n            }\n        }\n\n        while (!ops.empty()) {\n            values.push(applyOp(ops.pop(), values.pop(), values.pop()));\n        }\n        return values.pop();\n    }\n\n    private boolean hasPrecedence(char op1, char op2) {\n        if (op2 == '(' || op2 == ')') return false;\n        if ((op1 == '*' || op1 == '/') && (op2 == '+' || op2 == '-')) return false;\n        return true;\n    }\n\n    // Error 7: Parameter order reversed when dividing or subtracting (b / a vs a / b)\n    private int applyOp(char op, int b, int a) {\n        switch (op) {\n            case '+': return a + b;\n            case '-': return b - a; // Bug: should be a - b\n            case '*': return a * b;\n            case '/': if (b == 0) throw new UnsupportedOperationException(\"Cannot divide by zero\"); return a / b;\n        }\n        return 0;\n    }\n}""",
            "correct_code": """import java.util.Stack;\n\npublic class ExpressionEvaluator {\n    private final int DEFAULT_RADIX = 10;\n    \n    public ExpressionEvaluator() {\n    }\n\n    public int evaluate(String expr) throws Exception {\n        char[] tokens = expr.toCharArray();\n        Stack<Integer> values = new Stack<>();\n        Stack<Character> ops = new Stack<>();\n\n        for (int i = 0; i < tokens.length; i++) {\n            if (tokens[i] == ' ') continue;\n\n            if (tokens[i] >= '0' && tokens[i] <= '9') {\n                StringBuilder sb = new StringBuilder();\n                while (i < tokens.length && tokens[i] >= '0' && tokens[i] <= '9') {\n                    sb.append(tokens[i++]);\n                }\n                i--;\n                values.push(Integer.parseInt(sb.toString()));\n            } else if (tokens[i] == '(') {\n                ops.push(tokens[i]);\n            } else if (tokens[i] == ')') {\n                while (!ops.empty() && ops.peek() != '(') {\n                    values.push(applyOp(ops.pop(), values.pop(), values.pop()));\n                }\n                if (!ops.empty()) ops.pop();\n            } else if (tokens[i] == '+' || tokens[i] == '-' || tokens[i] == '*' || tokens[i] == '/') {\n                while (!ops.empty() && hasPrecedence(tokens[i], ops.peek())) {\n                    values.push(applyOp(ops.pop(), values.pop(), values.pop()));\n                }\n                ops.push(tokens[i]);\n            }\n        }\n\n        while (!ops.empty()) {\n            values.push(applyOp(ops.pop(), values.pop(), values.pop()));\n        }\n        return values.pop();\n    }\n\n    private boolean hasPrecedence(char op1, char op2) {\n        if (op2 == '(' || op2 == ')') return false;\n        if ((op1 == '*' || op1 == '/') && (op2 == '+' || op2 == '-')) return false;\n        return true;\n    }\n\n    private int applyOp(char op, int b, int a) {\n        switch (op) {\n            case '+': return a + b;\n            case '-': return a - b;\n            case '*': return a * b;\n            case '/': if (b == 0) throw new ArithmeticException(\"Cannot divide by zero\"); return a / b;\n        }\n        return 0;\n    }\n}""",
            "explanation": "Corrected 7 errors: 1) Initialized final DEFAULT_RADIX = 10, 2) Constructor safety, 3) Correct evaluate signature, 4) Loop bound i < tokens.length, 5) Inner bound i < tokens.length, 6) ops.peek() != '(', 7) Return a - b for subtraction.",
            "test_cases": [{"description": "Expression evaluator tests", "is_hidden": False}],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Variable Initialization",
                    "description": "Uninitialized 'final int DEFAULT_RADIX' causes compilation error.",
                    "buggy_snippet": "private final int DEFAULT_RADIX;",
                    "fixed_snippet": "private final int DEFAULT_RADIX = 10;",
                    "detection_rule": "{\"regex\": \"DEFAULT_RADIX\\\\s*=\\\\s*10\"}"
                },
                {
                    "error_number": 2,
                    "error_category": "Constructor Error",
                    "description": "Constructor must handle instance setup without leaving blank final state.",
                    "buggy_snippet": "// Error 2: Constructor does not initialize DEFAULT_RADIX",
                    "fixed_snippet": "// resolved",
                    "detection_rule": "{\"regex\": \"public\\\\s+ExpressionEvaluator\\\\(\\\\)\"}"
                },
                {
                    "error_number": 3,
                    "error_category": "Method Signature Error",
                    "description": "evaluate() method signature requires clean declaration matching caller specification.",
                    "buggy_snippet": "public int evaluate(String expr) throws Exception",
                    "fixed_snippet": "public int evaluate(String expr) throws Exception",
                    "detection_rule": "{\"regex\": \"public\\\\s+int\\\\s+evaluate\"}"
                },
                {
                    "error_number": 4,
                    "error_category": "Loop Boundary Error",
                    "description": "Main token loop 'i <= tokens.length' throws ArrayIndexOutOfBoundsException.",
                    "buggy_snippet": "for (int i = 0; i <= tokens.length; i++)",
                    "fixed_snippet": "for (int i = 0; i < tokens.length; i++)",
                    "detection_rule": "{\"regex\": \"i\\\\s*<\\\\s*tokens\\\\.length\"}"
                },
                {
                    "error_number": 5,
                    "error_category": "Inner Loop Bounds Error",
                    "description": "Multi-digit number scanner while loop missing boundary check 'i < tokens.length'.",
                    "buggy_snippet": "while (tokens[i] >= '0' && tokens[i] <= '9')",
                    "fixed_snippet": "while (i < tokens.length && tokens[i] >= '0' && tokens[i] <= '9')",
                    "detection_rule": "{\"regex\": \"while\\\\s*\\\\(\\\\s*i\\\\s*<\\\\s*tokens\\\\.length\"}"
                },
                {
                    "error_number": 6,
                    "error_category": "Conditional Logic Error",
                    "description": "Closing parenthesis handler checks 'ops.peek() == '('' instead of '!= '(''.",
                    "buggy_snippet": "while (ops.peek() == '(')",
                    "fixed_snippet": "while (!ops.empty() && ops.peek() != '(')",
                    "detection_rule": "{\"regex\": \"ops\\\\.peek\\\\(\\\\)\\\\s*!=\\\\s*'\\\\('\"}"
                },
                {
                    "error_number": 7,
                    "error_category": "Arithmetic Logic Error",
                    "description": "Subtraction case computes 'b - a' instead of 'a - b' due to stack pop order.",
                    "buggy_snippet": "case '-': return b - a;",
                    "fixed_snippet": "case '-': return a - b;",
                    "detection_rule": "{\"regex\": \"return\\\\s+a\\\\s*-\\\\s*b;\"}"
                }
            ]
        },
        {
            "order_num": 5,
            "title": "Question 5: Hospital Patient Priority Registry",
            "difficulty": "Hard",
            "points": 14.0,
            "question_text": "The `HospitalRegistry` class maintains patient priority queues using a custom Binary Search Tree. It contains exactly 7 intentional errors across type casting, method overriding, loop modification, and OOP access. Correct all 7 errors.",
            "buggy_code": """import java.util.ArrayList;\nimport java.util.List;\n\npublic class HospitalRegistry {\n    public static class Patient {\n        // Error 1: OOP private encapsulation prevents subclass/nested access\n        private String name;\n        private int severity;\n        \n        public Patient(String name, int severity) {\n            this.name = name;\n            this.severity = severity;\n        }\n\n        // Error 2: Method signature error: compareTo with wrong parameter Object instead of Patient\n        public int compareTo(Object other) {\n            // Error 3: Type casting missing on Object\n            return this.severity - other.severity;\n        }\n    }\n\n    static class TreeNode {\n        Patient patient;\n        TreeNode left, right;\n        TreeNode(Patient p) {\n            this.patient = p;\n        }\n    }\n\n    private TreeNode root;\n    private List<Patient> admitList = new ArrayList<>();\n\n    // Error 4: Method signature return type void instead of Patient\n    public void insert(Patient p) {\n        root = insertRec(root, p);\n    }\n\n    private TreeNode insertRec(TreeNode current, Patient p) {\n        if (current == null) return new TreeNode(p);\n        // Error 5: Conditional logic error: <= instead of > for high priority placement\n        if (p.severity <= current.patient.severity) {\n            current.left = insertRec(current.left, p);\n        } else {\n            current.right = insertRec(current.right, p);\n        }\n        return current;\n    }\n\n    // Error 6: Modifying list during forward iteration causes ConcurrentModification / Index shift\n    public void dischargePatients(int threshold) {\n        for (int i = 0; i < admitList.size(); i++) {\n            if (admitList.get(i).severity < threshold) {\n                admitList.remove(i);\n                // missing i-- index compensation\n            }\n        }\n    }\n\n    // Error 7: Exception/Return logic error: returns null without checking root\n    public Patient getHighestPriority() {\n        TreeNode curr = root;\n        while (curr.right != null) {\n            curr = curr.right;\n        }\n        return curr.patient;\n    }\n}""",
            "correct_code": """import java.util.ArrayList;\nimport java.util.List;\n\npublic class HospitalRegistry {\n    public static class Patient implements Comparable<Patient> {\n        public String name;\n        public int severity;\n        \n        public Patient(String name, int severity) {\n            this.name = name;\n            this.severity = severity;\n        }\n\n        @Override\n        public int compareTo(Patient other) {\n            return Integer.compare(this.severity, other.severity);\n        }\n    }\n\n    static class TreeNode {\n        Patient patient;\n        TreeNode left, right;\n        TreeNode(Patient p) {\n            this.patient = p;\n        }\n    }\n\n    private TreeNode root;\n    private List<Patient> admitList = new ArrayList<>();\n\n    public void insert(Patient p) {\n        root = insertRec(root, p);\n    }\n\n    private TreeNode insertRec(TreeNode current, Patient p) {\n        if (current == null) return new TreeNode(p);\n        if (p.severity > current.patient.severity) {\n            current.right = insertRec(current.right, p);\n        } else {\n            current.left = insertRec(current.left, p);\n        }\n        return current;\n    }\n\n    public void dischargePatients(int threshold) {\n        for (int i = admitList.size() - 1; i >= 0; i--) {\n            if (admitList.get(i).severity < threshold) {\n                admitList.remove(i);\n            }\n        }\n    }\n\n    public Patient getHighestPriority() {\n        if (root == null) return null;\n        TreeNode curr = root;\n        while (curr.right != null) {\n            curr = curr.right;\n        }\n        return curr.patient;\n    }\n}""",
            "explanation": "Corrected 7 errors: 1) Public or accessible Patient fields, 2) compareTo(Patient other) signature, 3) Severity comparison with Patient casting, 4) Method structure, 5) Proper BST insertion direction, 6) Backward loop iteration for removal, 7) Null root guard in getHighestPriority().",
            "test_cases": [{"description": "Hospital registry checks", "is_hidden": False}],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "OOP Encapsulation Access",
                    "description": "Patient fields 'name' and 'severity' require public access or getters for registry access.",
                    "buggy_snippet": "private String name;\n        private int severity;",
                    "fixed_snippet": "public String name;\n        public int severity;",
                    "detection_rule": "{\"regex\": \"public\\\\s+int\\\\s+severity;\"}"
                },
                {
                    "error_number": 2,
                    "error_category": "Method Signature Error",
                    "description": "compareTo() declared with Object parameter instead of Patient, failing Comparable contract.",
                    "buggy_snippet": "public int compareTo(Object other)",
                    "fixed_snippet": "public int compareTo(Patient other)",
                    "detection_rule": "{\"regex\": \"compareTo\\\\s*\\\\(\\\\s*Patient\\\\s+other\\\\s*\\\\)\"}"
                },
                {
                    "error_number": 3,
                    "error_category": "Type Error / Comparison",
                    "description": "Accessing other.severity directly on Object without casting causes compilation error.",
                    "buggy_snippet": "return this.severity - other.severity;",
                    "fixed_snippet": "return Integer.compare(this.severity, other.severity);",
                    "detection_rule": "{\"regex\": \"Integer\\\\.compare\"}"
                },
                {
                    "error_number": 4,
                    "error_category": "Comparable Interface",
                    "description": "Patient class missing 'implements Comparable<Patient>'.",
                    "buggy_snippet": "public static class Patient {",
                    "fixed_snippet": "public static class Patient implements Comparable<Patient> {",
                    "detection_rule": "{\"regex\": \"implements\\\\s+Comparable<Patient>\"}"
                },
                {
                    "error_number": 5,
                    "error_category": "BST Direction Logic",
                    "description": "Severity insertion logic places higher severity on left instead of right.",
                    "buggy_snippet": "if (p.severity <= current.patient.severity)",
                    "fixed_snippet": "if (p.severity > current.patient.severity)",
                    "detection_rule": "{\"regex\": \"p\\\\.severity\\\\s*>\\\\s*current\\\\.patient\\\\.severity\"}"
                },
                {
                    "error_number": 6,
                    "error_category": "Collection Mutation in Loop",
                    "description": "Removing elements during forward iteration skips adjacent elements.",
                    "buggy_snippet": "for (int i = 0; i < admitList.size(); i++)",
                    "fixed_snippet": "for (int i = admitList.size() - 1; i >= 0; i--)",
                    "detection_rule": "{\"regex\": \"for\\\\s*\\\\(\\\\s*int\\\\s+i\\\\s*=\\\\s*admitList\\\\.size\\\\(\\\\)\\\\s*-\\\\s*1\"}"
                },
                {
                    "error_number": 7,
                    "error_category": "Null Pointer Guard",
                    "description": "getHighestPriority() dereferences 'root.right' without checking if root is null.",
                    "buggy_snippet": "TreeNode curr = root;\n        while (curr.right != null)",
                    "fixed_snippet": "if (root == null) return null;\n        TreeNode curr = root;",
                    "detection_rule": "{\"regex\": \"if\\\\s*\\\\(\\\\s*root\\\\s*==\\\\s*null\\\\s*\\\\)\\\\s*return\\\\s+null;\"}"
                }
            ]
        }
    ]


def seed_database():
    """Seeds the database with initial Admin, Competition settings, and all 25 questions."""
    # 1. Seed Admin
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin')
        admin.set_password('CoderesQ@Admin2026')
        db.session.add(admin)
        print("Created default admin user: 'admin'")

    # 2. Seed Competition Settings
    comp = Competition.query.first()
    if not comp:
        comp = Competition(
            r1_duration_minutes=30,
            r2_duration_minutes=30,
            r1_enabled=True,
            r2_enabled=True,
            r1_points_per_question=5.0,
            r2_points_per_question=14.0,
            r2_points_per_error=2.0,
            allow_answer_review=False,
            anti_cheat_enabled=True
        )
        db.session.add(comp)
        print("Created competition default settings.")

    # 3. Seed Python Questions (Round 1)
    py_questions = get_python_questions()
    for q_data in py_questions:
        existing = Question.query.filter_by(round=1, order_num=q_data['order_num']).first()
        if not existing:
            q = Question(
                round=1,
                language='python',
                order_num=q_data['order_num'],
                title=q_data['title'],
                difficulty=q_data['difficulty'],
                points=q_data['points'],
                question_text=q_data['question_text'],
                buggy_code=q_data['buggy_code'],
                correct_code=q_data['correct_code'],
                error_type=q_data['error_type'],
                explanation=q_data['explanation']
            )
            q.test_cases = q_data['test_cases']
            db.session.add(q)
    print(f"Seeded {len(py_questions)} Python questions for Round 1.")

    # 4. Seed Java Questions (Round 2)
    java_questions = get_java_questions()
    for q_data in java_questions:
        existing = Question.query.filter_by(round=2, order_num=q_data['order_num']).first()
        if not existing:
            q = Question(
                round=2,
                language='java',
                order_num=q_data['order_num'],
                title=q_data['title'],
                difficulty=q_data['difficulty'],
                points=q_data['points'],
                question_text=q_data['question_text'],
                buggy_code=q_data['buggy_code'],
                correct_code=q_data['correct_code'],
                error_type="Multiple Intentional Errors (7)",
                explanation=q_data['explanation']
            )
            q.test_cases = q_data['test_cases']
            db.session.add(q)
            db.session.flush() # Ensure q.id is populated

            for err_data in q_data['errors']:
                err = JavaError(
                    question_id=q.id,
                    error_number=err_data['error_number'],
                    error_category=err_data['error_category'],
                    description=err_data['description'],
                    buggy_snippet=err_data['buggy_snippet'],
                    fixed_snippet=err_data['fixed_snippet'],
                    detection_rule=err_data.get('detection_rule'),
                    points=2.0
                )
                db.session.add(err)
    print(f"Seeded {len(java_questions)} Java questions with 35 error checkpoints for Round 2.")

    db.session.commit()
    print("Database seeding completed successfully!")
