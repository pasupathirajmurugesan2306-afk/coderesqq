with open('templates/admin/add_question.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Enforce exactly 1 bug for Python (Round 1) or exactly 7 bugs for Java (Round 2)', 'Enforce exactly 1 bug for Python (Round 1) or multiple mapped bugs for Round 2')
text = text.replace('Round 2 (Java - Exactly 7 Bugs)', 'Round 2 (Multi-track - Flexible Bugs)')

html_inj = """                <div id="language-select-container" class="hidden">
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Language Track *</label>
                    <select name="language" class="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-100 focus:outline-none focus:border-indigo-500">
                        <option value="java">Java</option>
                        <option value="python">Python</option>
                    </select>
                </div>"""
                
text = text.replace('                <div>\n                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Difficulty *</label>', html_inj + '\n\n                <div>\n                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Difficulty *</label>')

text = text.replace('Specification for Exactly 7 Java Errors', 'Specification for Multiple Bugs (Round 2)')
text = text.replace('All 7 Required', 'Map up to 10 bugs (Leave blank to skip)')
text = text.replace('range(1, 8)', 'range(1, 11)')

script_inj = """        if (roundSelect.value === '2') {
            javaSec.classList.remove('hidden');
            pySec.classList.add('hidden');
            document.getElementById('language-select-container').classList.remove('hidden');
            pointsInput.value = '25.0';
        } else {
            javaSec.classList.add('hidden');
            pySec.classList.remove('hidden');
            document.getElementById('language-select-container').classList.add('hidden');
            pointsInput.value = '10.0';
        }"""
        
import re
text = re.sub(r'        if \(roundSelect.value === \'2\'\) \{.*?        \}', script_inj, text, flags=re.DOTALL)

with open('templates/admin/add_question.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Also fix Edit Question
with open('templates/admin/edit_question.html', 'r', encoding='utf-8') as f:
    eval_text = f.read()

html_edit_inj = """            {% if question.round == 2 %}
            <div>
                <label class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Language Track</label>
                <select name="language" class="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-100 focus:outline-none focus:border-indigo-500">
                    <option value="java" {% if question.language == 'java' %}selected{% endif %}>Java</option>
                    <option value="python" {% if question.language == 'python' %}selected{% endif %}>Python</option>
                </select>
            </div>
            {% endif %}"""
eval_text = eval_text.replace('            <div>\n                <label class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Points / Marks *</label>', html_edit_inj + '\n\n            <div>\n                <label class="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1">Points / Marks *</label>')
eval_text = eval_text.replace('Specification for Exactly 7 Java Errors', 'Specification for Multiple Bugs (Round 2)')

with open('templates/admin/edit_question.html', 'w', encoding='utf-8') as f:
    f.write(eval_text)

