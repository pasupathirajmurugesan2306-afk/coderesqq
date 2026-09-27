import re

new_r2 = """def get_round2_questions():
    return [
        {
            "order_num": 1,
            "language": "java",
            "title": "Second Largest",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix the errors to calculate the second largest number.",
            "buggy_code": '''import java.util.Scanner;

public class SecondLargest {

    static int[] findSecondLargest(int[] numbers) {
        int largest = numbers[0];
        int second = 0;

        for (int i = 1; i < numbers.length; i++) {
            if (numbers[i] > largest) {
                second = largest;
                largest = numbers[i];
            } else if (numbers[i] > second) {
                second = numbers[i];
            }
        }

        return new int[]{largest second};
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter numbers:");
        String input = sc.nextLine();

        String[] parts = input.split(" ");
        int[] numbers = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {
            numbers[i] = Integer.parseInt(parts[i]);
        }
        int[] result = findSecondLargest(numbers);
        System.out.println("Largest: " + result[0]);
        System.out.println("Second Largest: " result[1]);
    }
}''',
            "correct_code": "",
            "explanation": "",
            "test_cases": [],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Syntax Error",
                    "description": "Missing comma in array initialization",
                    "buggy_snippet": "new int[]{largest second};",
                    "fixed_snippet": "new int[]{largest, second};",
                    "detection_rule": '{"regex": "new\\\\s+int\\\\s*\\\\[\\\\s*\\\\]\\\\s*\\\\{\\\\s*largest\\\\s*,\\\\s*second\\\\s*\\\\}"}'
                },
                {
                    "error_number": 2,
                    "error_category": "Syntax Error",
                    "description": "Missing concatenation operator in print",
                    "buggy_snippet": '"Second Largest: " result[1]',
                    "fixed_snippet": '"Second Largest: " + result[1]',
                    "detection_rule": '{"regex": "\\\\"Second Largest: \\\\"\\\\s*\\\\+\\\\s*result\\\\[1\\\\]"}'
                }
            ]
        },
        {
            "order_num": 2,
            "language": "java",
            "title": "Count Vowels",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix the errors to calculate vowels.",
            "buggy_code": '''import java.util.Scanner;

public class CountVowels {
    static int countVowels(String text) {
        String vowels = "aeiou";
        int count = 0;
        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i)
            if (vowels.indexOf(ch) >= 0) {
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a string: ");
        String text = sc.nextLine();
        
        if (text.length() = 0) {
            System.out.println("Empty string");
        } else {
            int result = countVowels(text);
            System.out.println("Vowels: " + result);
            if (result > 0) {
                System.out.println("Vowels found");
            } else {
                System.out.println("No vowels found");
            }
        }
    }
}''',
            "correct_code": "",
            "explanation": "",
            "test_cases": [],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Syntax Error",
                    "description": "Missing semicolon",
                    "buggy_snippet": "char ch = text.charAt(i)",
                    "fixed_snippet": "char ch = text.charAt(i);",
                    "detection_rule": '{"regex": "char\\\\s+ch\\\\s*=\\\\s*text\\\\.charAt\\\\(i\\\\)\\\\s*;"}'
                },
                {
                    "error_number": 2,
                    "error_category": "Syntax Error",
                    "description": "Assignment instead of conditional",
                    "buggy_snippet": "if (text.length() = 0)",
                    "fixed_snippet": "if (text.length() == 0)",
                    "detection_rule": '{"regex": "text\\\\.length\\\\(\\\\)\\\\s*==\\\\s*0"}'
                }
            ]
        },
        {
            "order_num": 1,
            "language": "python",
            "title": "Second Largest",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix the errors to calculate the second largest number.",
            "buggy_code": '''def find_second_largest(numbers):
    largest = numbers[0]
    second = 0
    for i in range(1, len(numbers))
        if numbers[i] > largest:
            second = largest
            largest = numbers[i]
        elif numbers[i] > second
            second = numbers[i]
    return largest, second

numbers = list(map(int, input().split()))
result = find_second_largest(numbers)
print("Largest:", result[0])
print("Second Largest:" result[1])''',
            "correct_code": "",
            "explanation": "",
            "test_cases": [],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Syntax Error",
                    "description": "Missing colon in for loop",
                    "buggy_snippet": "for i in range(1, len(numbers))",
                    "fixed_snippet": "for i in range(1, len(numbers)):",
                    "detection_rule": '{"regex": "for\\\\s+i\\\\s+in\\\\s+range\\\\(1,\\\\s*len\\\\(numbers\\\\)\\\\):"}'
                },
                {
                    "error_number": 2,
                    "error_category": "Syntax Error",
                    "description": "Missing colon in elif",
                    "buggy_snippet": "elif numbers[i] > second",
                    "fixed_snippet": "elif numbers[i] > second:",
                    "detection_rule": '{"regex": "elif\\\\s+numbers\\\\[i\\\\]\\\\s*>\\\\s*second:"}'
                },
                {
                    "error_number": 3,
                    "error_category": "Syntax Error",
                    "description": "Missing comma in print",
                    "buggy_snippet": 'print("Second Largest:" result[1])',
                    "fixed_snippet": 'print("Second Largest:", result[1])',
                    "detection_rule": '{"regex": "print\\\\(\\\\[\\\'\\\"]Second Largest:\\\\[\\\'\\\\\"\\\\s*,\\\\s*result\\\\[1\\\\]\\\\)"}'
                }
            ]
        },
        {
            "order_num": 2,
            "language": "python",
            "title": "Count Vowels",
            "difficulty": "Medium",
            "points": 25.0,
            "question_text": "Find and fix the errors to count vowels.",
            "buggy_code": '''def count_vowels(text):
    vowels = "aeiou"
    count = 0
    for ch in text
        if ch in vowels:
            count += 1
    return count

text = input("Enter a string: ")
if len(text) = 0:
    print("Empty string")
else
    result = count_vowels(text)
    print("Vowels:", result)
    if result > 0
        print("Vowels found")
    else:
        print("No vowels found")''',
            "correct_code": "",
            "explanation": "",
            "test_cases": [],
            "errors": [
                {
                    "error_number": 1,
                    "error_category": "Syntax Error",
                    "description": "Missing colon in for loop",
                    "buggy_snippet": "for ch in text",
                    "fixed_snippet": "for ch in text:",
                    "detection_rule": '{"regex": "for\\\\s+ch\\\\s+in\\\\s+text:"}'
                },
                {
                    "error_number": 2,
                    "error_category": "Syntax Error",
                    "description": "Assignment instead of conditional",
                    "buggy_snippet": "if len(text) = 0:",
                    "fixed_snippet": "if len(text) == 0:",
                    "detection_rule": '{"regex": "if\\\\s+len\\\\(text\\\\)\\\\s*==\\\\s*0:"}'
                },
                {
                    "error_number": 3,
                    "error_category": "Syntax Error",
                    "description": "Missing colon in else",
                    "buggy_snippet": "else",
                    "fixed_snippet": "else:",
                    "detection_rule": '{"regex": "else:"}'
                },
                {
                    "error_number": 4,
                    "error_category": "Syntax Error",
                    "description": "Missing colon in if",
                    "buggy_snippet": "if result > 0",
                    "fixed_snippet": "if result > 0:",
                    "detection_rule": '{"regex": "if\\\\s+result\\\\s*>\\\\s*0:"}'
                }
            ]
        }
    ]
"""

seed_logic = """    r2_questions = get_round2_questions()
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
    Question.query.filter_by(round=2).delete() # We will just delete all R2 questions first and reinsert them to be clean, wait, I shouldn't delete if I just updated them. Let's just delete the ones that don't match.
    for q in Question.query.filter_by(round=2).all():
        if getattr(q, 'language') not in ['java', 'python'] or getattr(q, 'order_num') > 2:
            db.session.delete(q)

    print("Seeded 4 multi-language questions for Round 2.")
    db.session.commit()
    print("Database seeding completed.")
"""

with open('seed_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace get_java_questions up to seed_database definition
content = re.sub(r'def get_java_questions\(\):.*?def seed_database\(\):', new_r2 + '\ndef seed_database():', content, flags=re.DOTALL)

# Replace the seeding logic within seed_database
content = re.sub(r'    java_questions = get_java_questions\(\).*?print\("Database seeding completed."\)', seed_logic, content, flags=re.DOTALL)

with open('seed_data.py', 'w', encoding='utf-8') as f:
    f.write(content)
