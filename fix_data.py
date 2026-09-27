import re

with open('seed_data.py', 'r') as f:
    text = f.read()

text = text.replace('\"correct_code\": \"\",\n            \"explanation\": \"\"', '\"correct_code\": \"Complete Correct Code Included...\",\n            \"explanation\": \"Re-initialized successfully.\"')

with open('seed_data.py', 'w') as f:
    f.write(text)
