with open('templates/admin/questions.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Configure 1-error Python problems and 7-error Java challenge programs', 'Configure all Round 1 & Round 2 tracking and problems')
text = text.replace('Round 2 (Java)', 'Round 2 (Multi-track)')
text = text.replace('<i class="fa-brands fa-java"></i> Round 2', '<i class="fa-brands fa-java"></i><i class="fa-brands fa-python"></i> Round 2')
text = text.replace('<i class="fa-brands fa-java text-red-400 mr-1"></i> Round 2 (Multi-track)', '<i class="fa-solid fa-code text-indigo-400 mr-1"></i> Round 2 (Multi-track)')

with open('templates/admin/questions.html', 'w', encoding='utf-8') as f:
    f.write(text)
