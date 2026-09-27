with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<div class="text-2xl sm:text-3xl font-extrabold font-mono text-cyan-400">25</div>', '<div class="text-2xl sm:text-3xl font-extrabold font-mono text-cyan-400">7</div>')
text = text.replace('<div class="text-2xl sm:text-3xl font-extrabold font-mono text-purple-400">55</div>', '<div class="text-2xl sm:text-3xl font-extrabold font-mono text-purple-400">12+</div>')

text = text.replace('Medium to Hard &bull; 20 Questions', 'Basic to Medium &bull; 5 Questions')
text = text.replace('Max: 100 Marks', 'Max: 50 Marks')

text = text.replace('<i class="fa-brands fa-java text-3xl text-red-400"></i>', '<div class="flex gap-1"><i class="fa-brands fa-java text-3xl text-red-400"></i><i class="fa-brands fa-python text-3xl text-blue-400"></i></div>')
text = text.replace('Java Debugging', 'Multi-Track Debugging')
text = text.replace('Hard &bull; 5 Complex Systems', 'Medium &bull; 2 Complex Systems')
text = text.replace('Each program contains <strong class="text-rose-400 font-semibold">exactly 7 intentional errors</strong>. Fix OOP flaws, typing errors, concurrency traps, loop boundaries, and Java API exceptions.', 'Choose your preferred language (Java or Python). Each program contains <strong class="text-rose-400 font-semibold">multiple intentional errors</strong> (syntax and logic).')
text = text.replace('Max: 70 Marks', 'Max: 50 Marks')
text = text.replace('Scoring: <strong>{{ comp.r2_points_per_error if comp else 2 }} pts / error</strong>', 'Scoring: <strong>25 pts / question</strong>')
text = text.replace('Scoring: <strong>{{ comp.r1_points_per_question if comp else 5 }} pts / question</strong>', 'Scoring: <strong>10 pts / question</strong>')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
