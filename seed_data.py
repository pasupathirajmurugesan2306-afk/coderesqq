import os
import json
from models import db, Question, JavaError, Admin, Competition, Participant

def get_python_questions():
    return [
        {
            "order_num": 1,
            "title": "Number Threshold",
            "error_type": "Syntax Error",
            "difficulty": "Easy",
            "points": 10.0,
            "question_text": "Find and fix the error in the provided code snippet.",
            "buggy_code": "numbers = [10, 20, 30, 40, 50]\n\nfor i in range(len(numbers)):\n    if numbers[i] > 25:\n        print(numbers[i])\n    else\n        print(\"Small\")",
            "correct_code": "numbers = [10, 20, 30, 40, 50]\n\nfor i in range(len(numbers)):\n    if numbers[i] > 25:\n        print(numbers[i])\n    else:\n        print(\"Small\")",
            "explanation": "A colon is required at the end of the else keyword.",
            "test_cases": [{"call": "numbers[-1]", "expected": 50, "description": "Logic Check"}]
        },
        {
            "order_num": 2,
            "title": "Find the Largest",
            "error_type": "Name Error",
            "difficulty": "Easy",
            "points": 10.0,
            "question_text": "Find and fix the error in the provided code snippet.",
            "buggy_code": "x = 10\ny = 20\nz = 30\n\nif x > y and x > z:\n    largest = x\nelif y > x and y > z:\n    largest = y\nelse:\n    largest = z\n\nprint(\"Largest:\", larges)",
            "correct_code": "x = 10\ny = 20\nz = 30\n\nif x > y and x > z:\n    largest = x\nelif y > x and y > z:\n    largest = y\nelse:\n    largest = z\n\nprint(\"Largest:\", largest)",
            "explanation": "The variable is correctly named largest, not larges.",
            "test_cases": [{"call": "largest", "expected": 30, "description": "Variable Check"}]
        },
        {
            "order_num": 3,
            "title": "Count Vowels",
            "error_type": "Logical Error",
            "difficulty": "Medium",
            "points": 10.0,
            "question_text": "Find and fix the error in the provided code snippet.",
            "buggy_code": "text = \"Python\"\ncount = 0\n\nfor char in text:\n    if char == \"a\" or \"e\" or \"i\" or \"o\" or \"u\":\n        count += 1\n\nprint(count)",
            "correct_code": "text = \"Python\"\ncount = 0\n\nfor char in text:\n    if char in \"aeiou\":\n        count += 1\n\nprint(count)",
            "explanation": "In Python, combining strings with OR will evaluate truthiness of strings. Check each condition explicitly, or use 'in'.",
            "test_cases": [{"call": "count", "expected": 1, "description": "Count Logic Check"}]
        },
        {
            "order_num": 4,
            "title": "Reverse Number",
            "error_type": "Name Error",
            "difficulty": "Medium",
            "points": 10.0,
            "question_text": "Find and fix the error in the provided code snippet.",
            "buggy_code": "num = 123\nreverse = 0\n\nwhile num > 0:\n    digit = num % 10\n    reverse = reverse * 10 + digit\n    num = num // 10\n\nprint(revers)",
            "correct_code": "num = 123\nreverse = 0\n\nwhile num > 0:\n    digit = num % 10\n    reverse = reverse * 10 + digit\n    num = num // 10\n\nprint(reverse)",
            "explanation": "Misspelled variable in the final print statement.",
            "test_cases": [{"call": "reverse", "expected": 321, "description": "Reverse Logic Check"}]
        },
        {
            "order_num": 5,
            "title": "Extract Even Numbers",
            "error_type": "Syntax Error",
            "difficulty": "Easy",
            "points": 10.0,
            "question_text": "Find and fix the error in the provided code snippet.",
            "buggy_code": "numbers = [1, 2, 3, 4, 5]\nresult = []\n\nfor num in numbers:\n    if num % 2 = 0:\n        result.append(num)\n\nprint(result)",
            "correct_code": "numbers = [1, 2, 3, 4, 5]\nresult = []\n\nfor num in numbers:\n    if num % 2 == 0:\n        result.append(num)\n\nprint(result)",
            "explanation": "To check for equality, use '==' instead of '='.",
            "test_cases": [{"call": "result", "expected": [2, 4], "description": "Even Logic Check"}]
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
            existing.error_type = q_data['error_type']
            existing.points = q_data['points']
            existing.explanation = q_data['explanation']
    # Delete excess python questions
    Question.query.filter_by(round=1).filter(Question.order_num > len(py_questions)).delete()
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
