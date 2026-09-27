with open('routes/admin.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "language = 'python' if round_num == 1 else 'java'",
    "language = request.form.get('language', 'python' if round_num == 1 else 'java')"
)

old_add = """        if round_num == 2:
            # Java question: Validate exactly 7 errors submitted
            errors_data = []
            for i in range(1, 8):
                cat = request.form.get(f'error_{i}_category', f'Category {i}').strip()
                desc = request.form.get(f'error_{i}_desc', '').strip()
                buggy_snip = request.form.get(f'error_{i}_buggy', '').strip()
                fixed_snip = request.form.get(f'error_{i}_fixed', '').strip()
                if not desc or not buggy_snip or not fixed_snip:
                    db.session.rollback()
                    flash('Java questions must have all 7 error descriptions and code snippets completed.', 'error')
                    return redirect(url_for('admin.add_question'))
                errors_data.append((i, cat, desc, buggy_snip, fixed_snip))

            for (err_idx, cat, desc, buggy_snip, fixed_snip) in errors_data:
                err = JavaError(
                    question_id=q.id,
                    error_number=err_idx,
                    error_category=cat,
                    description=desc,
                    buggy_snippet=buggy_snip,
                    fixed_snippet=fixed_snip,
                    points=points / 7.0
                )
                db.session.add(err)"""

new_add = """        if round_num == 2:
            errors_data = []
            for i in range(1, 11): # Up to 10 errors
                cat = request.form.get(f'error_{i}_category', '').strip()
                desc = request.form.get(f'error_{i}_desc', '').strip()
                buggy_snip = request.form.get(f'error_{i}_buggy', '').strip()
                fixed_snip = request.form.get(f'error_{i}_fixed', '').strip()
                if not desc or not buggy_snip:
                    continue
                errors_data.append((len(errors_data)+1, cat, desc, buggy_snip, fixed_snip))

            if not errors_data:
                db.session.rollback()
                flash('Round 2 questions must have at least 1 error mapped.', 'error')
                return redirect(url_for('admin.add_question'))

            for (err_idx, cat, desc, buggy_snip, fixed_snip) in errors_data:
                err = JavaError(
                    question_id=q.id,
                    error_number=err_idx,
                    error_category=cat,
                    description=desc,
                    buggy_snippet=buggy_snip,
                    fixed_snippet=fixed_snip,
                    points=points / len(errors_data)
                )
                db.session.add(err)"""

text = text.replace(old_add, new_add)

old_edit = """        if q.round == 2:
            for err in q.java_errors:
                i = err.error_number
                cat = request.form.get(f'error_{i}_category')
                desc = request.form.get(f'error_{i}_desc')
                buggy_snip = request.form.get(f'error_{i}_buggy')
                fixed_snip = request.form.get(f'error_{i}_fixed')
                if cat: err.error_category = cat
                if desc: err.description = desc
                if buggy_snip: err.buggy_snippet = buggy_snip
                if fixed_snip: err.fixed_snippet = fixed_snip"""

new_edit = """        if q.round == 2:
            q.language = request.form.get('language', q.language)
            for err in q.java_errors:
                i = err.error_number
                cat = request.form.get(f'error_{i}_category')
                desc = request.form.get(f'error_{i}_desc')
                buggy_snip = request.form.get(f'error_{i}_buggy')
                fixed_snip = request.form.get(f'error_{i}_fixed')
                if cat is not None: err.error_category = cat
                if desc is not None: err.description = desc
                if buggy_snip is not None: err.buggy_snippet = buggy_snip
                if fixed_snip is not None: err.fixed_snippet = fixed_snip"""

text = text.replace(old_edit, new_edit)

with open('routes/admin.py', 'w', encoding='utf-8') as f:
    f.write(text)
