import os
import json
from models import db, Question, JavaError, Admin, Competition, Participant

def get_python_questions():
    return [
        {
            "order_num": 1,
            "title": "First Missing Positive",
            "error_type": "Logical Error",
            "difficulty": "Medium",
            "points": 10.0,
            "question_text": "Find and fix the error in the provided code snippet so that it correctly identifies the first missing positive integer.",
            "buggy_code": "numbers = [3, 4, -1, 1, 2]\n\nmissing = 1\n\nfor num in numbers:\n    if num == missing:\n        missing += 1\n\nprint(\"First Missing Positive:\", missing)",
            "correct_code": "numbers = [3, 4, -1, 1, 2]\n\nnumbers.sort()\n\nmissing = 1\n\nfor num in numbers:\n    if num == missing:\n        missing += 1\n\nprint(\"First Missing Positive:\", missing)",
            "explanation": "The algorithm works by checking the numbers in ascending order. Without sorting the list first (numbers.sort()), it fails to identify sequence gaps correctly.",
            "test_cases": [{"call": "missing", "expected": 5, "description": "First Missing Positive Check"}]
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
            "title": "Unique Elements",
            "error_type": "Logical Error",
            "difficulty": "Easy",
            "points": 10.0,
            "question_text": "Find and fix the error so that the script accurately extracts only the unique elements from the list.",
            "buggy_code": "numbers = [10, 20, 10, 30, 20, 40, 30]\n\nunique = []\n\nfor num in numbers:\n    if num not in unique:\n        unique.append(numbers)\n\nprint(unique)",
            "correct_code": "numbers = [10, 20, 10, 30, 20, 40, 30]\n\nunique = []\n\nfor num in numbers:\n    if num not in unique:\n        unique.append(num)\n\nprint(unique)",
            "explanation": "The statement 'unique.append(numbers)' incorrectly appends the entire original list instead of the individual numerical element 'num'.",
            "test_cases": [{"call": "unique", "expected": [10, 20, 30, 40], "description": "Unique Elements List Check"}]
        }
    ]

def get_round2_questions():
    return [
        {
            "order_num": 1,
            "language": "python",
            "title": "Student Result",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix the 7 errors in the Python program.",
            "buggy_code": """def student_result(marks):
    total = 0
    highest = mark[0]
    passed = 0

    for i in range(len(marks)):
        total += marks[i]

        if marks[i] >= 40
            passed += 1

        if marks[i] < highest:
            highest = marks[i]

    average = total / len(mark)

    print("Total:" total)
    print("Average:", average)
    print("Highest:", highest)
    print("Passed:", passed)


values = input("Enter marks: ").split()

marks = []
for value in values:
    marks.append(float(value))

if len(marks) = 0:
    print("No marks entered")
else:
    student_results(marks)""",
            "correct_code": "",
            "explanation": "",
            "test_cases": [],
            "errors": [
                {"error_number": 1, "error_category": "Name Error", "description": "Variable mark instead of marks", "buggy_snippet": "highest = mark[0]", "fixed_snippet": "highest = marks[0]", "detection_rule": None},
                {"error_number": 2, "error_category": "Syntax Error", "description": "Missing colon in if statement", "buggy_snippet": "if marks[i] >= 40 passed +=", "fixed_snippet": "if marks[i] >= 40: passed +=", "detection_rule": None},
                {"error_number": 3, "error_category": "Logical Error", "description": "Finding lowest instead of highest", "buggy_snippet": "if marks[i] < highest:", "fixed_snippet": "if marks[i] > highest:", "detection_rule": None},
                {"error_number": 4, "error_category": "Name Error", "description": "Variable mark instead of marks in length", "buggy_snippet": "len(mark)", "fixed_snippet": "len(marks)", "detection_rule": None},
                {"error_number": 5, "error_category": "Syntax Error", "description": "Missing comma in print", "buggy_snippet": '"Total:" total)', "fixed_snippet": '"Total:", total)', "detection_rule": None},
                {"error_number": 6, "error_category": "Syntax Error", "description": "Assignment instead of equality", "buggy_snippet": "if len(marks) = 0:", "fixed_snippet": "if len(marks) == 0:", "detection_rule": None},
                {"error_number": 7, "error_category": "Name Error", "description": "Wrong function name called", "buggy_snippet": "student_results(marks)", "fixed_snippet": "student_result(marks)", "detection_rule": None}
            ]
        },
        {
            "order_num": 2,
            "language": "python",
            "title": "Analyze List",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix the 7 errors in the Python program.",
            "buggy_code": """def analyze_list(numbers):
    even_sum = 0
    odd_sum = 0
    smallest = numbers[0]

    for number in numbers
        if number % 2 = 0:
            evensum += number
        else:
            odd_sum += number

        if number > smallest:
            smallest = number

    difference = even_sum - odd_sum

    print("Even sum:", even_sum)
    print("Odd sum:", odd_sum)
    print("Difference:" difference)
    print("Smallest:", smallest)


data = input("Enter numbers: ")
numbers = data.split()

for i in range(len(numbers)):
    numbers[i] = int(numbers[i])

if len(numbers) == 0
    print("List is empty")
else:
    analyze_numbers(numbers)

print("Program completed")""",
            "correct_code": "",
            "explanation": "",
            "test_cases": [],
            "errors": [
                {"error_number": 1, "error_category": "Syntax Error", "description": "Missing colon in for loop", "buggy_snippet": "for number in numbers if", "fixed_snippet": "for number in numbers: if", "detection_rule": None},
                {"error_number": 2, "error_category": "Syntax Error", "description": "Assignment instead of equality", "buggy_snippet": "if number % 2 = 0:", "fixed_snippet": "if number % 2 == 0:", "detection_rule": None},
                {"error_number": 3, "error_category": "Name Error", "description": "Wrong variable name", "buggy_snippet": "evensum += number", "fixed_snippet": "even_sum += number", "detection_rule": None},
                {"error_number": 4, "error_category": "Logical Error", "description": "Finding largest instead of smallest", "buggy_snippet": "if number > smallest:", "fixed_snippet": "if number < smallest:", "detection_rule": None},
                {"error_number": 5, "error_category": "Syntax Error", "description": "Missing comma in print", "buggy_snippet": '"Difference:" difference)', "fixed_snippet": '"Difference:", difference)', "detection_rule": None},
                {"error_number": 6, "error_category": "Syntax Error", "description": "Missing colon in if statement", "buggy_snippet": "if len(numbers) == 0 print", "fixed_snippet": "if len(numbers) == 0: print", "detection_rule": None},
                {"error_number": 7, "error_category": "Name Error", "description": "Wrong function name called", "buggy_snippet": "analyze_numbers(numbers)", "fixed_snippet": "analyze_list(numbers)", "detection_rule": None}
            ]
        },
        {
            "order_num": 1,
            "language": "java",
            "title": "Sum Average",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix the 6 errors in the Java program.",
            "buggy_code": """import java.util.Scanner;

class SumAverage {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of elements: ");
        int n = sc.nextInt();

        int[] arr = new int[n];

        System.out.println("Enter " + n + " numbers:");

        for (int i = 0; i <= n; i++) {
            arr[i] = sc.nextInt();
        }

        int sum = 0;

        for (int i = 0; i < n; i++) {
            sum =+ arr[i];
        }

        double average = sum / n;

        System.out.println("Sum = " + sum)
        System.out.println("Average = " + average);

        sc.close
    }
}""",
            "correct_code": "",
            "explanation": "",
            "test_cases": [],
            "errors": [
                {"error_number": 1, "error_category": "Syntax Error", "description": "Class name should be Main (usually requires public class Main)", "buggy_snippet": "class SumAverage {", "fixed_snippet": "public class Main {", "detection_rule": None},
                {"error_number": 2, "error_category": "Runtime Error", "description": "Array bounds loop goes out of range", "buggy_snippet": "i <= n; i++) {\n            arr[i]", "fixed_snippet": "i < n; i++) {\n            arr[i]", "detection_rule": None},
                {"error_number": 3, "error_category": "Syntax Error", "description": "Assignment instead of addition assignment", "buggy_snippet": "sum =+ arr[i];", "fixed_snippet": "sum += arr[i];", "detection_rule": None},
                {"error_number": 4, "error_category": "Logical Error", "description": "Integer division", "buggy_snippet": "sum / n;", "fixed_snippet": "(double) sum / n;", "detection_rule": None},
                {"error_number": 5, "error_category": "Syntax Error", "description": "Missing semicolon", "buggy_snippet": "\"Sum = \" + sum)", "fixed_snippet": "\"Sum = \" + sum);", "detection_rule": None},
                {"error_number": 6, "error_category": "Syntax Error", "description": "Missing method call parenthesis and semicolon", "buggy_snippet": "sc.close\n    }", "fixed_snippet": "sc.close();\n    }", "detection_rule": None}
            ]
        },
        {
            "order_num": 2,
            "language": "java",
            "title": "Array Min Max Search",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix the 7 errors in the Java program.",
            "buggy_code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int[] numbers = {15, 8, 23, 4, 17, 10};

        int largest = 0;
        int smallest = 0;
        int sum = 0;

        for (int i = 0; i <= numbers.length; i++) {
            sum += numbers[i];

            if (numbers[i] > largest) {
                largest = numbers[i];
            }

            if (numbers[i] > smallest) {
                smallest = numbers[i];
            }
        }

        double average = sum / numbers.length;

        System.out.println("Largest: " + largest);
        System.out.println("Smallest: " + smallest);
        System.out.println("Average: " + average);

        System.out.print("Enter number to search: ");
        int search = sc.nextInt();

        boolean found = false

        for (int i = 0; i < numbers.length; i++) {
            if (numbers[i] = search) {
                found = true;
            }
        }

        if (found = true) {
            System.out.println("Number found");
        } else {
            System.out.println("Number not found");
        }

        sc.close();
    }
}""",
            "correct_code": "",
            "explanation": "",
            "test_cases": [],
            "errors": [
                {"error_number": 1, "error_category": "Logical Error", "description": "Smallest variable is initialized incorrectly", "buggy_snippet": "int smallest = 0;", "fixed_snippet": "int smallest = numbers[0];", "detection_rule": None},
                {"error_number": 2, "error_category": "Runtime Error", "description": "Array bounds loop goes out of range", "buggy_snippet": "i <= numbers.length; i++) { sum +=", "fixed_snippet": "i < numbers.length; i++) { sum +=", "detection_rule": None},
                {"error_number": 3, "error_category": "Logical Error", "description": "Finding largest instead of smallest", "buggy_snippet": "if (numbers[i] > smallest)", "fixed_snippet": "if (numbers[i] < smallest)", "detection_rule": None},
                {"error_number": 4, "error_category": "Logical Error", "description": "Integer division", "buggy_snippet": "sum / numbers.length;", "fixed_snippet": "(double) sum / numbers.length;", "detection_rule": None},
                {"error_number": 5, "error_category": "Syntax Error", "description": "Missing semicolon", "buggy_snippet": "boolean found = false for", "fixed_snippet": "boolean found = false; for", "detection_rule": None},
                {"error_number": 6, "error_category": "Syntax Error", "description": "Assignment instead of equality", "buggy_snippet": "if (numbers[i] = search)", "fixed_snippet": "if (numbers[i] == search)", "detection_rule": None},
                {"error_number": 7, "error_category": "Syntax Error", "description": "Assignment instead of equality", "buggy_snippet": "if (found = true)", "fixed_snippet": "if (found == true)", "detection_rule": None}
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

