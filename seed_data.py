import os
import json
from models import db, Question, JavaError, Admin, Competition, Participant

def get_python_questions():
    return [
        {
            "order_num": 1,
            "title": "Multiplication",
            "error_type": "Syntax Error",
            "difficulty": "Easy",
            "points": 5.0,
            "question_text": "The function multiply(a, b) should return the product of a and b. Find and fix the error.",
            "buggy_code": "def multiply(a, b):\n    result = a x b\n    return result",
            "correct_code": "def multiply(a, b):\n    result = a * b\n    return result",
            "explanation": "The multiplication operator in Python is '*' not 'x'.",
            "test_cases": [{"call": "multiply(5, 4)", "expected": 20}]
        },
        {
            "order_num": 2,
            "title": "While loop execution",
            "error_type": "Syntax Error",
            "difficulty": "Easy",
            "points": 5.0,
            "question_text": "The function print_1_to_5() should return a list of numbers from 1 to 5. Find and fix the error.",
            "buggy_code": "def print_1_to_5():\n    result = []\n    i = 1\n    while i <= 5\n        result.append(i)\n        i += 1\n    return result",
            "correct_code": "def print_1_to_5():\n    result = []\n    i = 1\n    while i <= 5:\n        result.append(i)\n        i += 1\n    return result",
            "explanation": "A colon ':' is required at the end of the while loop statement.",
            "test_cases": [{"call": "print_1_to_5()", "expected": [1, 2, 3, 4, 5]}]
        },
        {
            "order_num": 3,
            "title": "Length of a string",
            "error_type": "Name Error",
            "difficulty": "Easy",
            "points": 5.0,
            "question_text": "The function get_length(name) should return the length of the string. Find and fix the error.",
            "buggy_code": "def get_length(name):\n    return lenght(name)",
            "correct_code": "def get_length(name):\n    return len(name)",
            "explanation": "The correct function to get the length of an object is 'len()', not 'lenght()'.",
            "test_cases": [{"call": "get_length(\"Python\")", "expected": 6}]
        },
        {
            "order_num": 4,
            "title": "Sum of even numbers",
            "error_type": "Syntax Error",
            "difficulty": "Easy",
            "points": 5.0,
            "question_text": "The function sum_even(numbers) should return the sum of all even numbers in the list. However, it contains a syntax error.",
            "buggy_code": "def sum_even(numbers):\n    total = 0\n    for n in numbers:\n        if n % 2 = 0:\n            total += n\n    return total",
            "correct_code": "def sum_even(numbers):\n    total = 0\n    for n in numbers:\n        if n % 2 == 0:\n            total += n\n    return total",
            "explanation": "Equality comparison is done using '==', not '=' (which is assignment).",
            "test_cases": [{"call": "sum_even([2, 5, 8, 11, 14])", "expected": 24}]
        },
        {
            "order_num": 5,
            "title": "Reverse a number",
            "error_type": "Logical Error",
            "difficulty": "Medium",
            "points": 5.0,
            "question_text": "The function should reverse a given integer, however, the division operator used causes an infinite loop or float conversion. Fix it.",
            "buggy_code": "def reverse_number(num):\n    rev = 0\n    while num > 0:\n        digit = num % 10\n        rev = rev * 10 + digit\n        num = num / 10\n    return rev",
            "correct_code": "def reverse_number(num):\n    rev = 0\n    while num > 0:\n        digit = num % 10\n        rev = rev * 10 + digit\n        num = num // 10\n    return rev",
            "explanation": "In Python 3, '/' creates a float. For integer division, you should use '//'.",
            "test_cases": [{"call": "reverse_number(1234)", "expected": 4321}]
        },
        {
            "order_num": 6,
            "title": "Array average",
            "error_type": "Logical Error",
            "difficulty": "Easy",
            "points": 5.0,
            "question_text": "Calculate the average of the given numbers. The logic has an unnecessary subtraction. Fix it.",
            "buggy_code": "def array_average(numbers):\n    total = 0\n    for n in numbers:\n        total += n\n    average = total / len(numbers) - 1\n    return average",
            "correct_code": "def array_average(numbers):\n    total = 0\n    for n in numbers:\n        total += n\n    average = total / len(numbers)\n    return average",
            "explanation": "The '- 1' at the end of the average calculation gives an incorrect result.",
            "test_cases": [{"call": "array_average([10, 20, 30, 40])", "expected": 25.0}]
        },
        {
            "order_num": 7,
            "title": "Count positive numbers",
            "error_type": "Logical Error",
            "difficulty": "Easy",
            "points": 5.0,
            "question_text": "The function should count positive numbers in an array, but it has the wrong condition.",
            "buggy_code": "def count_positives(numbers):\n    count = 0\n    for n in numbers:\n        if n < 0:\n            count += 1\n    return count",
            "correct_code": "def count_positives(numbers):\n    count = 0\n    for n in numbers:\n        if n > 0:\n            count += 1\n    return count",
            "explanation": "Positive numbers are strictly greater than 0, so the condition should be `n > 0`.",
            "test_cases": [{"call": "count_positives([-2, 5, 8, -1, 10])", "expected": 3}]
        },
        {
            "order_num": 8,
            "title": "Factorial",
            "error_type": "Logical Error / Boundary",
            "difficulty": "Easy",
            "points": 5.0,
            "question_text": "The function should compute the factorial of a number, but the loop range is off by one.",
            "buggy_code": "def factorial(n):\n    fact = 1\n    for i in range(1, n):\n        fact *= i\n    return fact",
            "correct_code": "def factorial(n):\n    fact = 1\n    for i in range(1, n + 1):\n        fact *= i\n    return fact",
            "explanation": "The `range` function is exclusive of the upper bound, so to include `n`, it must be `n + 1`.",
            "test_cases": [{"call": "factorial(5)", "expected": 120}]
        },
        {
            "order_num": 9,
            "title": "Sum of odd numbers",
            "error_type": "Logical Error",
            "difficulty": "Easy",
            "points": 5.0,
            "question_text": "The function should return the total sum of all odd numbers, but it overwrites the total instead.",
            "buggy_code": "def sum_odds(numbers):\n    total = 0\n    for n in numbers:\n        if n % 2 == 1:\n            total = n\n    return total",
            "correct_code": "def sum_odds(numbers):\n    total = 0\n    for n in numbers:\n        if n % 2 == 1:\n            total += n\n    return total",
            "explanation": "Instead of overwriting `total = n`, we should add to it `total += n`.",
            "test_cases": [{"call": "sum_odds([3, 8, 11, 14, 17])", "expected": 35}]
        },
        {
            "order_num": 10,
            "title": "Count digits",
            "error_type": "Logical Error",
            "difficulty": "Easy",
            "points": 5.0,
            "question_text": "The function should count the digits of a number, but it returns the wrong variable at the end.",
            "buggy_code": "def count_digits(num):\n    count = 0\n    while num > 0:\n        num = num // 10\n        count += 1\n    return num",
            "correct_code": "def count_digits(num):\n    count = 0\n    while num > 0:\n        num = num // 10\n        count += 1\n    return count",
            "explanation": "The function was returning the depleted `num` (which is 0) instead of the accumulated `count`.",
            "test_cases": [{"call": "count_digits(54321)", "expected": 5}]
        }
    ]

def get_java_questions():
    return [
        {
            "order_num": 1,
            "title": "Second largest element",
            "difficulty": "Medium",
            "points": 14.0,
            "question_text": "The method secondLargest contains multiple errors including array bounds and incorrect assignment logic. Fix them to return the second largest element.",
            "buggy_code": "public class Main {\n    public static int secondLargest(int[] arr) {\n        int largest = 0;\n        int second = 0;\n        for (int i = 0; i <= arr.length; i++) {\n            if (arr[i] < largest) {\n                second = largest;\n                largest = arr[i];\n            } else if (arr[i] > second) {\n                largest = arr[i];\n            }\n        }\n        return largest;\n    }\n}",
            "correct_code": "public class Main {\n    public static int secondLargest(int[] arr) {\n        int largest = 0;\n        int second = 0;\n        for (int i = 0; i < arr.length; i++) {\n            if (arr[i] > largest) {\n                second = largest;\n                largest = arr[i];\n            } else if (arr[i] > second && arr[i] != largest) {\n                second = arr[i];\n            }\n        }\n        return second;\n    }\n}",
            "explanation": "Fixed array bounds, comparison direction, logic assignment, and the return value.",
            "test_cases": [{"description": "Check if second largest element logic works", "is_hidden": False}],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Array Bounds",
                    "description": "Loop condition accesses out of bounds.",
                    "buggy_snippet": "i <= arr.length",
                    "fixed_snippet": "i < arr.length",
                    "detection_rule": '{"regex": "i\\\\s*<\\\\s*arr\\\\.length"}'
                },
                {
                    "error_number": 2,
                    "error_category": "Logic",
                    "description": "Incorrect comparison for largest element.",
                    "buggy_snippet": "arr[i] < largest",
                    "fixed_snippet": "arr[i] > largest",
                    "detection_rule": '{"regex": "arr\\\\[i\\\\]\\\\s*>\\\\s*largest"}'
                },
                {
                    "error_number": 3,
                    "error_category": "Return Value",
                    "description": "Returning largest instead of second largest.",
                    "buggy_snippet": "return largest;",
                    "fixed_snippet": "return second;",
                    "detection_rule": '{"regex": "return\\\\s+second;"}'
                }
            ]
        },
        {
            "order_num": 2,
            "title": "Palindrome number",
            "difficulty": "Medium",
            "points": 14.0,
            "question_text": "Determine if a number is a palindrome by reversing it.",
            "buggy_code": "public class Main {\n    public static boolean isPalindrome(int num) {\n        int original = 0;\n        int reverse = 0;\n        while (num >= 0) {\n            int digit = num / 10;\n            reverse = reverse * 10 + digit;\n            num = num % 10;\n        }\n        if (original == reverse)\n            return true;\n        else\n            return false;\n    }\n}",
            "correct_code": "public class Main {\n    public static boolean isPalindrome(int num) {\n        int original = num;\n        int reverse = 0;\n        while (num > 0) {\n            int digit = num % 10;\n            reverse = reverse * 10 + digit;\n            num = num / 10;\n        }\n        if (original == reverse)\n            return true;\n        else\n            return false;\n    }\n}",
            "explanation": "Fixed math operators and loop logic. original should track num, and extracting digits uses '%' while reducing uses '/'.",
            "test_cases": [{"description": "Palindrome number tests", "is_hidden": False}],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Assignment",
                    "description": "original does not store the incoming number.",
                    "buggy_snippet": "int original = 0;",
                    "fixed_snippet": "int original = num;",
                    "detection_rule": '{"regex": "int\\\\s+original\\\\s*=\\\\s*num;"}'
                },
                {
                    "error_number": 2,
                    "error_category": "Math",
                    "description": "Incorrect operators for extraction and reduction.",
                    "buggy_snippet": "digit = num / 10;",
                    "fixed_snippet": "digit = num % 10;",
                    "detection_rule": '{"regex": "num\\\\s*%\\\\s*10"}'
                }
            ]
        },
        {
            "order_num": 3,
            "title": "Missing number",
            "difficulty": "Easy",
            "points": 14.0,
            "question_text": "Find the missing number in an array containing elements from 1 to N.",
            "buggy_code": "public class Main {\n    public static int missingNumber(int[] arr) {\n        int n = arr.length + 1;\n        int expected = n * (n + 1) / 2;\n        int actual = 0;\n        for (int i = 0; i <= arr.length; i++) {\n            actual += arr[i];\n        }\n        int missing = actual - expected;\n        return actual;\n    }\n}",
            "correct_code": "public class Main {\n    public static int missingNumber(int[] arr) {\n        int n = arr.length + 1;\n        int expected = n * (n + 1) / 2;\n        int actual = 0;\n        for (int i = 0; i < arr.length; i++) {\n            actual += arr[i];\n        }\n        int missing = expected - actual;\n        return missing;\n    }\n}",
            "explanation": "Fixed array bounds and logic for returning missing number.",
            "test_cases": [{"description": "Missing number check", "is_hidden": False}],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Bounds",
                    "description": "Loop goes out of bounds.",
                    "buggy_snippet": "i <= arr.length",
                    "fixed_snippet": "i < arr.length",
                    "detection_rule": '{"regex": "i\\\\s*<\\\\s*arr\\\\.length"}'
                },
                {
                    "error_number": 2,
                    "error_category": "Logic",
                    "description": "Returns the actual sum instead of the missing element.",
                    "buggy_snippet": "return actual;",
                    "fixed_snippet": "return missing;",
                    "detection_rule": '{"regex": "return\\\\s+missing;"}'
                }
            ]
        },
        {
            "order_num": 4,
            "title": "Duplicate elements",
            "difficulty": "Easy",
            "points": 14.0,
            "question_text": "Print the duplicate elements in an array. Currently, the conditionals and loop variables are wrong.",
            "buggy_code": "public class Main {\n    public static int findDuplicate(int[] arr) {\n        for (int i = 0; i < arr.length; i++) {\n            for (int j = i; j < arr.length; j++) {\n                if (arr[i] != arr[j]) {\n                    return arr[i];\n                }\n            }\n        }\n        return -1;\n    }\n}",
            "correct_code": "public class Main {\n    public static int findDuplicate(int[] arr) {\n        for (int i = 0; i < arr.length; i++) {\n            for (int j = i + 1; j < arr.length; j++) {\n                if (arr[i] == arr[j]) {\n                    return arr[i];\n                }\n            }\n        }\n        return -1;\n    }\n}",
            "explanation": "To check for duplicates, j should start from i+1, and testing equality uses ==.",
            "test_cases": [{"description": "Check duplicate finding", "is_hidden": False}],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Loop Start",
                    "description": "Inner loop compares element with itself.",
                    "buggy_snippet": "int j = i;",
                    "fixed_snippet": "int j = i + 1;",
                    "detection_rule": '{"regex": "int\\\\s+j\\\\s*=\\\\s*i\\\\s*\\\\+\\\\s*1"}'
                },
                {
                    "error_number": 2,
                    "error_category": "Comparator",
                    "description": "Finds different elements rather than equal ones.",
                    "buggy_snippet": "arr[i] != arr[j]",
                    "fixed_snippet": "arr[i] == arr[j]",
                    "detection_rule": '{"regex": "arr\\\\[i\\\\]\\\\s*==\\\\s*arr\\\\[j\\\\]"}'
                }
            ]
        },
        {
            "order_num": 5,
            "title": "Target sum pair",
            "difficulty": "Medium",
            "points": 14.0,
            "question_text": "Find if there exists a pair that sums to target.",
            "buggy_code": "public class Main {\n    public static boolean hasTargetSum(int[] arr, int target) {\n        for (int i = 0; i <= arr.length; i++) {\n            for (int j = i; j < arr.length; j++) {\n                if (arr[i] + arr[j] = target) {\n                    return true;\n                }\n            }\n        }\n        return false;\n    }\n}",
            "correct_code": "public class Main {\n    public static boolean hasTargetSum(int[] arr, int target) {\n        for (int i = 0; i < arr.length; i++) {\n            for (int j = i + 1; j < arr.length; j++) {\n                if (arr[i] + arr[j] == target) {\n                    return true;\n                }\n            }\n        }\n        return false;\n    }\n}",
            "explanation": "Fixed array bounds, assignment in conditional, and self-pairing (j=i).",
            "test_cases": [{"description": "Target sum check", "is_hidden": False}],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Syntax Error",
                    "description": "Assignment instead of equality in if condition.",
                    "buggy_snippet": "= target",
                    "fixed_snippet": "== target",
                    "detection_rule": '{"regex": "==\\\\s*target"}'
                },
                {
                    "error_number": 2,
                    "error_category": "Array Bounds",
                    "description": "Outer loop goes out of bounds.",
                    "buggy_snippet": "i <= arr.length",
                    "fixed_snippet": "i < arr.length",
                    "detection_rule": '{"regex": "i\\\\s*<\\\\s*arr\\\\.length"}'
                }
            ]
        }
    ]

def seed_database():
    """Seeds the database with initial Admin, Competition settings, and all questions."""
    admin = Admin.query.filter_by(username='admin').first()

    if not admin:
        admin = Admin(username='admin')
        admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
        admin.set_password(admin_password)
        db.session.add(admin)

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
        else:
            existing.title = q_data['title']
            existing.question_text = q_data['question_text']
            existing.buggy_code = q_data['buggy_code']
            existing.correct_code = q_data['correct_code']
            existing.test_cases = q_data['test_cases']
            
    # Delete excess python questions if there were 20 before
    Question.query.filter_by(round=1).filter(Question.order_num > 10).delete()
    print(f"Seeded {len(py_questions)} Python questions for Round 1.")

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
                error_type="Multiple Intentional Errors",
                explanation=q_data['explanation']
            )
            q.test_cases = q_data['test_cases']
            db.session.add(q)
            db.session.flush()

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
        else:
            existing.title = q_data['title']
            existing.question_text = q_data['question_text']
            existing.buggy_code = q_data['buggy_code']
            existing.correct_code = q_data['correct_code']
            existing.test_cases = q_data['test_cases']
            JavaError.query.filter_by(question_id=existing.id).delete()
            for err_data in q_data['errors']:
                err = JavaError(
                    question_id=existing.id,
                    error_number=err_data['error_number'],
                    error_category=err_data['error_category'],
                    description=err_data['description'],
                    buggy_snippet=err_data['buggy_snippet'],
                    fixed_snippet=err_data['fixed_snippet'],
                    detection_rule=err_data.get('detection_rule'),
                    points=2.0
                )
                db.session.add(err)

    print(f"Seeded {len(java_questions)} Java questions for Round 2.")

    db.session.commit()
    print("Database seeding completed.")
