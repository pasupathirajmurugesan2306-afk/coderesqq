import re

with open('seed_data.py', 'r') as f:
    text = f.read()

replacement = '''def get_round2_questions():
    return [
        {
            "order_num": 1,
            "language": "python",
            "title": "Student Result",
            "difficulty": "Medium",
            "points": 35.0,
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
            "points": 35.0,
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
            "title": "Sum and Average",
            "difficulty": "Medium",
            "points": 35.0,
            "question_text": "Find and fix the 7 errors in the Java program.",
            "buggy_code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in)

        System.out.print("Enter a number: ");
        int n = sc.nextInt();

        int sum = 0
        int evenCount = 0;

        for (int i = 1; i <= n; i++) {
            if (i % 2 = 0) {
                sum += i;
                evenCount++
            }
        }

        double average = sum / evenCount;

        System.out.println("Even sum: " + sum);
        System.out.println("Even count: " + evenCount);
        System.out.println("Average: " + average)

        if (average > 10) {
            System.out.println("Average is high")
        } else {
            System.out.println("Average is low");
        }

        sc.close();
    }
}""",
            "correct_code": "",
            "explanation": "",
            "test_cases": [],
            "errors": [
                {"error_number": 1, "error_category": "Syntax Error", "description": "Missing semicolon", "buggy_snippet": "Scanner sc = new Scanner(System.in)", "fixed_snippet": "Scanner sc = new Scanner(System.in);", "detection_rule": None},
                {"error_number": 2, "error_category": "Syntax Error", "description": "Missing semicolon", "buggy_snippet": "int sum = 0 int evenCount", "fixed_snippet": "int sum = 0; int evenCount", "detection_rule": None},
                {"error_number": 3, "error_category": "Syntax Error", "description": "Assignment instead of equality", "buggy_snippet": "if (i % 2 = 0)", "fixed_snippet": "if (i % 2 == 0)", "detection_rule": None},
                {"error_number": 4, "error_category": "Syntax Error", "description": "Missing semicolon", "buggy_snippet": "evenCount++ }", "fixed_snippet": "evenCount++; }", "detection_rule": None},
                {"error_number": 5, "error_category": "Logical Error", "description": "Integer division", "buggy_snippet": "sum / evenCount;", "fixed_snippet": "(double) sum / evenCount;", "detection_rule": None},
                {"error_number": 6, "error_category": "Syntax Error", "description": "Missing semicolon", "buggy_snippet": '"Average: " + average)', "fixed_snippet": '"Average: " + average);', "detection_rule": None},
                {"error_number": 7, "error_category": "Syntax Error", "description": "Missing semicolon", "buggy_snippet": '"Average is high") }', "fixed_snippet": '"Average is high"); }', "detection_rule": None}
            ]
        },
        {
            "order_num": 2,
            "language": "java",
            "title": "Array Min Max Search",
            "difficulty": "Medium",
            "points": 35.0,
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
'''

text = re.sub(r'def get_round2_questions\(\).*?(?=def seed_database\(\):)', replacement + '\n', text, flags=re.DOTALL)

with open('seed_data.py', 'w') as f:
    f.write(text)
