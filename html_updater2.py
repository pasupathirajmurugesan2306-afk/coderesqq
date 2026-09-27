with open('templates/rules.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Python Debugging (20 Questions)', 'Python Debugging (5 Questions)')
text = text.replace('Total: 100 Marks', 'Total: 50 Marks')
text = text.replace('Java Debugging (5 Complex Systems)', 'Multi-Language Debugging (2 Complex Problems)')
text = text.replace('Each Java program contains <strong class="text-rose-400 font-semibold">exactly 7 intentional errors</strong>.', 'Each program contains multiple intentional errors (syntax and logic).')
text = text.replace('Errors cover: Variable declarations, method signatures, loops, collections, conditional logic, OOP, and Java exceptions.', 'You can select either Java or Python track. Solve the problems in your chosen language.')
text = text.replace('(14 marks/question &bull; Total: 70 Marks)', '(25 marks/question &bull; Total: 50 Marks)')

with open('templates/rules.html', 'w', encoding='utf-8') as f:
    f.write(text)
