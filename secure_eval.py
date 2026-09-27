with open('services/code_evaluator.py', 'r', encoding='utf-8') as f:
    text = f.read()

sanitizer = """        stderr = proc.stderr
        
        if stderr:
            lines = stderr.strip().split('\\n')
            final_err = lines[-1] if lines else 'Unknown Python Error'
            stderr = f"Execution Error System Output:\\n{final_err}\\n\\n(Line numbers & locations are hidden for the debugging challenge)"
"""

text = text.replace('        stderr = proc.stderr', sanitizer)

with open('services/code_evaluator.py', 'w', encoding='utf-8') as f:
    f.write(text)
