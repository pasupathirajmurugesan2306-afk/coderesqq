with open("templates/rules.html", "r", encoding="utf-8") as f:
    text = f.read()

import re

r1_bullets = """                    <li><strong class="text-white">Basic to Medium difficulty</strong> covering Python fundamentals and standard logic.</li>
                    <li><strong class="text-amber-400">Identify and resolve the bugs</strong> in the provided Python code snippets.</li>
                    <li>Time limit: <strong class="text-indigo-300 font-mono">{{ comp.r1_duration_minutes if comp else 30 }} Minutes</strong>. The countdown begins upon entering.</li>
                    <li>Scoring: <strong class="text-emerald-400 font-mono">10 marks per question</strong> (Total: 50 Marks).</li>
                    <li>Test your code with the <strong>Run Code</strong> button before official submission.</li>"""
text = re.sub(r'                    <li><strong class="text-white">Medium to Hard difficulty.*?</strong> button before official submission.</li>', r1_bullets, text, flags=re.DOTALL)


r2_bullets = """                    <li><strong class="text-white">Medium difficulty</strong> involving arrays and string manipulation (e.g., Finding Second Largest, Counting Vowels).</li>
                    <li>Each program contains <strong class="text-rose-400 font-semibold">multiple intentional errors</strong> (missing syntax, incorrect logic, wrong bounds).</li>
                    <li>Track Selection: You must select either the <strong class="text-white">Java or Python</strong> track. Both tracks face identical challenges for fairness.</li>
                    <li>Time limit: <strong class="text-purple-300 font-mono">{{ comp.r2_duration_minutes if comp else 30 }} Minutes</strong>.</li>
                    <li>Scoring: <strong class="text-emerald-400 font-mono">25 marks per question</strong>. Partial points are awarded dynamically based on how many bugs you resolve! (Total: 50 Marks).</li>"""
text = re.sub(r'                    <li><strong class="text-white">Hard difficulty.*?Total: 50 Marks\).</li>', r2_bullets, text, flags=re.DOTALL)


with open("templates/rules.html", "w", encoding="utf-8") as f:
    f.write(text)
