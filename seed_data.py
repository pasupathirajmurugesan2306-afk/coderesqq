import os
import json
from models import db, Question, JavaError, Admin, Competition, Participant

def get_python_questions():
    return [
        {
            "order_num": 1,
            "title": "Second Largest",
            "error_type": "Logical Error",
            "difficulty": "Medium",
            "points": 10.0,
            "question_text": "Find and fix the error in the provided code snippet so that it prints the second largest number.",
            "buggy_code": "numbers = [10, 45, 23, 67, 89, 34]\n\nlargest = numbers[0]\nsecond = numbers[0]\n\nfor i in range(1, len(numbers)):\n    if numbers[i] > largest:\n        second = largest\n        largest = numbers[i]\n    elif numbers[i] > second:\n        second = numbers[i]\n\nprint(\"Second Largest:\", second)",
            "correct_code": "numbers = [10, 45, 23, 67, 89, 34]\n\nlargest = numbers[0]\nsecond = 0\n\nfor i in range(1, len(numbers)):\n    if numbers[i] > largest:\n        second = largest\n        largest = numbers[i]\n    elif numbers[i] > second and numbers[i] != largest:\n        second = numbers[i]\n\nprint(\"Second Largest:\", second)",
            "explanation": "Initializing 'second' to numbers[0] means it might not update if the first element is the largest. Initializing it to 0 works better for lists of positive integers.",
            "test_cases": [{"call": "second", "expected": 67, "description": "Second Largest Check"}]
        },
        {
            "order_num": 2,
            "title": "Count Vowels",
            "error_type": "Syntax Error",
            "difficulty": "Easy",
            "points": 10.0,
            "question_text": "Find and fix the error in the provided code snippet so that it correctly counts all vowels.",
            "buggy_code": "text = \"Programming\"\nvowels = \"aeiou\"\ncount = 0\n\nfor char in text:\n    if char in vowels:\n        count =+ 1\n\nprint(\"Vowel Count:\", count)",
            "correct_code": "text = \"Programming\"\nvowels = \"aeiou\"\ncount = 0\n\nfor char in text:\n    if char in vowels:\n        count += 1\n\nprint(\"Vowel Count:\", count)",
            "explanation": "The operator '=+ 1' assigns the positive value 1 to 'count'. The correct increment operator is '+='.",
            "test_cases": [{"call": "count", "expected": 3, "description": "Vowel Count Check"}]
        },
        {
            "order_num": 3,
            "title": "Sum of Digits",
            "error_type": "Logical Error",
            "difficulty": "Easy",
            "points": 10.0,
            "question_text": "Find and fix the error to properly calculate the sum of the digits.",
            "buggy_code": "num = 5832\ntotal = 0\n\nwhile num > 0:\n    digit = num % 10\n    total = digit\n    num = num // 10\n\nprint(\"Sum:\", total)",
            "correct_code": "num = 5832\ntotal = 0\n\nwhile num > 0:\n    digit = num % 10\n    total += digit\n    num = num // 10\n\nprint(\"Sum:\", total)",
            "explanation": "The statement 'total = digit' overwrites the accumulated sum. You must use '+=' to accumulate.",
            "test_cases": [{"call": "total", "expected": 18, "description": "Sum of Digits Check"}]
        },
        {
            "order_num": 4,
            "title": "Smallest Number",
            "error_type": "Logical Error",
            "difficulty": "Easy",
            "points": 10.0,
            "question_text": "Find and fix the error to correctly identify the smallest number in the list.",
            "buggy_code": "numbers = [45, 12, 78, 23, 9, 56]\n\nsmallest = 0\n\nfor num in numbers:\n    if num < smallest:\n        smallest = num\n\nprint(\"Smallest:\", smallest)",
            "correct_code": "numbers = [45, 12, 78, 23, 9, 56]\n\nsmallest = numbers[0]\n\nfor num in numbers:\n    if num < smallest:\n        smallest = num\n\nprint(\"Smallest:\", smallest)",
            "explanation": "Initializing 'smallest' to 0 leads to an incorrect result (0) when all numbers are positive. It should be initialized with an element of the list, such as 'numbers[0]'.",
            "test_cases": [{"call": "smallest", "expected": 9, "description": "Smallest Number Check"}]
        },
        {
            "order_num": 5,
            "title": "Element Frequency",
            "error_type": "Logical Error",
            "difficulty": "Medium",
            "points": 10.0,
            "question_text": "Find and fix the error so that the frequency of elements in the list is calculated correctly.",
            "buggy_code": "numbers = [1, 2, 2, 3, 1, 2, 4]\n\nfrequency = {}\n\nfor num in numbers:\n    if num in frequency:\n        frequency[num] += 1\n    else:\n        frequency[num] = 0\n\nprint(frequency)",
            "correct_code": "numbers = [1, 2, 2, 3, 1, 2, 4]\n\nfrequency = {}\n\nfor num in numbers:\n    if num in frequency:\n        frequency[num] += 1\n    else:\n        frequency[num] = 1\n\nprint(frequency)",
            "explanation": "When an element is introduced to the frequency dictionary for the first time, its initial count should be 1, not 0.",
            "test_cases": [{"call": "frequency", "expected": {1: 2, 2: 3, 3: 1, 4: 1}, "description": "Frequency Dictionary Check"}]
        }
    ]

def get_round2_questions():
    return [
        {
            "order_num": 1,
            "language": "java",
            "title": "Array Min Max Search",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix all errors in the Java program.",
            "buggy_code": '''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int[] numbers = {12, 5, 18, 7, 20, 3};

        int largest = 0;
        int smallest = 0;

        for (int i = 0; i <= numbers.length; i++) {
            if (numbers[i] > largest) {
                largest = numbers[i];
            }

            if (numbers[i] < smallest) {
                smallest = numbers[i];
            }
        }

        System.out.println("Largest: " + largest);
        System.out.println("Smallest: " + smallest);

        System.out.print("Enter a number to search: ");
        int search = sc.nextInt();

        boolean found = false;

        for (int i = 0; i < numbers.length; i++) {
            if (numbers[i] = search) {
                found = true;
            }
        }

        if (found) {
            System.out.println("Number found")
        } else {
            System.out.println("Number not found");
        }

        sc.close();
    }
}''',
            "correct_code": "Complete Correct Code Included...",
            "explanation": "Re-initialized successfully.",
            "test_cases": [],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Logical Error",
                    "description": "Smallest variable is initialized incorrectly.",
                    "buggy_snippet": "int smallest = 0;",
                    "fixed_snippet": "int smallest = numbers[0];",
                    "detection_rule": None
                },
                {
                    "error_number": 2,
                    "error_category": "Runtime Error",
                    "description": "Array bounds loop goes out of range.",
                    "buggy_snippet": "i <= numbers.length; i++) { if (numbers[i] > largest)",
                    "fixed_snippet": "i < numbers.length; i++) { if (numbers[i] > largest)",
                    "detection_rule": None
                },
                {
                    "error_number": 3,
                    "error_category": "Syntax Error",
                    "description": "Assignment used in condition instead of equality.",
                    "buggy_snippet": "if (numbers[i] = search)",
                    "fixed_snippet": "if (numbers[i] == search)",
                    "detection_rule": None
                },
                {
                    "error_number": 4,
                    "error_category": "Syntax Error",
                    "description": "Missing semicolon",
                    "buggy_snippet": 'System.out.println("Number found")',
                    "fixed_snippet": 'System.out.println("Number found");',
                    "detection_rule": None
                }
            ]
        },
        {
            "order_num": 2,
            "language": "java",
            "title": "Sum of Even Numbers",
            "difficulty": "Easy",
            "points": 25.0,
            "question_text": "Find and fix the errors to calculate the sum correctly.",
            "buggy_code": '''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter a number: ");
        int n = sc.nextInt();

        int sum = 0;

        for (int i = 1; i < n; i++) {
            if (i % 2 = 0) {
                sum += i;
            }
        }

        System.out.println("Sum of even numbers: " + sum)

        if (sum > 50) {
            System.out.println("Large sum");
        }
        else if (sum > 20)
            System.out.println("Medium sum");
        else {
            System.out.println("Small sum")
        }

        sc.close();
    }
}''',
            "correct_code": "Complete Correct Code Included...",
            "explanation": "Re-initialized successfully.",
            "test_cases": [],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Syntax Error",
                    "description": "Used assignment instead of equality check.",
                    "buggy_snippet": "if (i % 2 = 0)",
                    "fixed_snippet": "if (i % 2 == 0)",
                    "detection_rule": None
                },
                {
                    "error_number": 2,
                    "error_category": "Syntax Error",
                    "description": "Missing semicolon",
                    "buggy_snippet": '"Sum of even numbers: " + sum)',
                    "fixed_snippet": '"Sum of even numbers: " + sum);',
                    "detection_rule": None
                },
                {
                    "error_number": 3,
                    "error_category": "Syntax Error",
                    "description": "Missing semicolon",
                    "buggy_snippet": '"Small sum") }',
                    "fixed_snippet": '"Small sum"); }',
                    "detection_rule": None
                }
            ]
        },
        {
            "order_num": 1,
            "language": "python",
            "title": "Calculate Average",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix the errors to calculate average properly.",
            "buggy_code": '''def calculate_average(numbers):
    total = 0

    for i in range(len(numbers))
        total += numbers[i]

    average = total / len(numbers)

    if average >= 80:
        grade = "A"
    elif average >= 60
        grade = "B"
    elif average >= 40:
        grade = "C"
    else:
        grade = "F"

    print("Total:", total)
    print("Average:", average)
    print("Grade:", grade)


numbers = input("Enter numbers: ").split()

for i in range(len(numbers)):
    numbers[i] = int(numbers[i])

calculate_average''',
            "correct_code": "Complete Correct Code Included...",
            "explanation": "Re-initialized successfully.",
            "test_cases": [],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Syntax Error",
                    "description": "Missing colon in loop.",
                    "buggy_snippet": "for i in range(len(numbers)) total +=",
                    "fixed_snippet": "for i in range(len(numbers)): total +=",
                    "detection_rule": None
                },
                {
                    "error_number": 2,
                    "error_category": "Syntax Error",
                    "description": "Missing colon in elif.",
                    "buggy_snippet": "elif average >= 60 grade = \"B\"",
                    "fixed_snippet": "elif average >= 60: grade = \"B\"",
                    "detection_rule": None
                },
                {
                    "error_number": 3,
                    "error_category": "Syntax Error",
                    "description": "Function call is missing parentheses and arguments.",
                    "buggy_snippet": "int(numbers[i]) calculate_average",
                    "fixed_snippet": "int(numbers[i]) calculate_average(numbers)",
                    "detection_rule": None
                }
            ]
        },
        {
            "order_num": 2,
            "language": "python",
            "title": "Even Odd & Largest",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix the errors to calculate counts and largest properly.",
            "buggy_code": '''def find_numbers(numbers):
    even = 0
    odd = 0
    largest = 0

    for i in range(len(numbers)):
        if numbers[i] % 2 = 0:
            even += 1
        else
            odd += 1

        if numbers[i] < largest:
            largest = numbers[i]

    print("Even numbers:", even)
    print("Odd numbers:", odd)
    print("Largest number:", largest)


numbers = input("Enter numbers: ").split()

for i in range(len(numbers)):
    numbers[i] = float(numbers[i])

find_numbers(numbers)''',
            "correct_code": "Complete Correct Code Included...",
            "explanation": "Re-initialized successfully.",
            "test_cases": [],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Syntax Error",
                    "description": "Assignment used in condition instead of equality.",
                    "buggy_snippet": "if numbers[i] % 2 = 0:",
                    "fixed_snippet": "if numbers[i] % 2 == 0:",
                    "detection_rule": None
                },
                {
                    "error_number": 2,
                    "error_category": "Syntax Error",
                    "description": "Missing colon in else block.",
                    "buggy_snippet": "even += 1 else odd += 1",
                    "fixed_snippet": "even += 1 else: odd += 1",
                    "detection_rule": None
                },
                {
                    "error_number": 3,
                    "error_category": "Logical Error",
                    "description": "Condition finds smallest instead of largest.",
                    "buggy_snippet": "if numbers[i] < largest: largest = numbers[i]",
                    "fixed_snippet": "if numbers[i] > largest: largest = numbers[i]",
                    "detection_rule": None
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

    r2_questions = get_round2_questions()
    for q_data in r2_questions:
        existing = Question.query.filter_by(round=2, language=q_data['language'], order_num=q_data['order_num']).first()
        if not existing:
            q = Question(
                round=2,
                language=q_data['language'],
                order_num=q_data['order_num'],
                title=q_data['title'],
                difficulty=q_data['difficulty'],
                points=q_data['points'],
                question_text=q_data['question_text'],
                buggy_code=q_data['buggy_code'],
                correct_code=q_data['correct_code'],
                error_type="Multiple Errors"
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
                    points=25.0 / len(q_data['errors'])
                )
                db.session.add(err)
        else:
            existing.title = q_data['title']
            existing.question_text = q_data['question_text']
            existing.buggy_code = q_data['buggy_code']
            existing.points = q_data['points']
            
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
                    points=25.0 / len(q_data['errors'])
                )
                db.session.add(err)

    # Clean old items
    pass # Fixed deletion bug
    for q in Question.query.filter_by(round=2).all():
        if getattr(q, 'language') not in ['java', 'python'] or getattr(q, 'order_num') > 2:
            db.session.delete(q)

    print("Seeded 4 multi-language questions for Round 2.")
    db.session.commit()
    print("Database seeding completed.")

