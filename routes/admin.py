import io
import csv
import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, Response, jsonify
from models import db, Admin, Participant, Question, JavaError, Submission, Competition, SuspiciousActivity
from routes.auth import admin_required
from services.stats_service import get_admin_dashboard_metrics, get_leaderboard

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@admin_required
def require_admin():
    pass

@admin_bp.route('/admin/dashboard')
def dashboard():
    metrics = get_admin_dashboard_metrics()
    recent_submissions = Submission.query.order_by(Submission.submitted_at.desc()).limit(8).all()
    recent_suspicious = SuspiciousActivity.query.order_by(SuspiciousActivity.timestamp.desc()).limit(8).all()
    comp = Competition.query.first()
    return render_template('admin/dashboard.html',
                           metrics=metrics,
                           recent_submissions=recent_submissions,
                           recent_suspicious=recent_suspicious,
                           comp=comp)

@admin_bp.route('/admin/questions')
def questions():
    round_filter = request.args.get('round', 'all')
    query = Question.query
    if round_filter in ['1', '2']:
        query = query.filter_by(round=int(round_filter))
    questions_list = query.order_by(Question.round, Question.order_num).all()
    return render_template('admin/questions.html', questions=questions_list, active_round=round_filter)

@admin_bp.route('/admin/questions/add', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        round_num = int(request.form.get('round', 1))
        language = 'python' if round_num == 1 else 'java'
        title = request.form.get('title', '').strip()
        difficulty = request.form.get('difficulty', 'Medium')
        points = float(request.form.get('points', 5.0 if round_num == 1 else 14.0))
        question_text = request.form.get('question_text', '').strip()
        buggy_code = request.form.get('buggy_code', '')
        correct_code = request.form.get('correct_code', '')
        explanation = request.form.get('explanation', '').strip()
        error_type = request.form.get('error_type', 'Debugging Error')

        # Validation
        if not all([title, question_text, buggy_code, correct_code]):
            flash('All required question fields must be filled.', 'error')
            return redirect(url_for('admin.add_question'))

        # Count max order_num
        max_order = db.session.query(db.func.max(Question.order_num)).filter_by(round=round_num).scalar() or 0
        
        q = Question(
            round=round_num,
            language=language,
            order_num=max_order + 1,
            title=title,
            difficulty=difficulty,
            points=points,
            question_text=question_text,
            buggy_code=buggy_code,
            correct_code=correct_code,
            error_type=error_type,
            explanation=explanation
        )

        # Parse test cases if provided
        test_cases_raw = request.form.get('test_cases', '')
        if test_cases_raw:
            try:
                q.test_cases = json.loads(test_cases_raw)
            except Exception:
                q.test_cases = []

        db.session.add(q)
        db.session.flush()

        if round_num == 2:
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
                db.session.add(err)

        db.session.commit()
        flash(f'Question "{title}" created successfully!', 'success')
        return redirect(url_for('admin.questions'))

    return render_template('admin/add_question.html')

@admin_bp.route('/admin/questions/edit/<int:q_id>', methods=['GET', 'POST'])
def edit_question(q_id):
    q = db.get_or_404(Question, q_id)
    if request.method == 'POST':
        q.title = request.form.get('title', '').strip()
        q.difficulty = request.form.get('difficulty', 'Medium')
        q.points = float(request.form.get('points', q.points))
        q.question_text = request.form.get('question_text', '').strip()
        q.buggy_code = request.form.get('buggy_code', '')
        q.correct_code = request.form.get('correct_code', '')
        q.explanation = request.form.get('explanation', '').strip()
        q.error_type = request.form.get('error_type', q.error_type)

        test_cases_raw = request.form.get('test_cases', '')
        if test_cases_raw:
            try:
                q.test_cases = json.loads(test_cases_raw)
            except Exception:
                pass

        if q.round == 2:
            for err in q.java_errors:
                i = err.error_number
                cat = request.form.get(f'error_{i}_category')
                desc = request.form.get(f'error_{i}_desc')
                buggy_snip = request.form.get(f'error_{i}_buggy')
                fixed_snip = request.form.get(f'error_{i}_fixed')
                if cat: err.error_category = cat
                if desc: err.description = desc
                if buggy_snip: err.buggy_snippet = buggy_snip
                if fixed_snip: err.fixed_snippet = fixed_snip

        db.session.commit()
        flash(f'Question "{q.title}" updated successfully!', 'success')
        return redirect(url_for('admin.questions'))

    return render_template('admin/edit_question.html', question=q)

@admin_bp.route('/admin/questions/delete/<int:q_id>', methods=['POST'])
def delete_question(q_id):
    q = db.get_or_404(Question, q_id)
    db.session.delete(q)
    db.session.commit()
    flash(f'Question #{q_id} deleted.', 'info')
    return redirect(url_for('admin.questions'))

@admin_bp.route('/admin/participants')
def participants():
    college = request.args.get('college', 'all')
    dept = request.args.get('department', 'all')
    participants_list = get_leaderboard(college=college, department=dept)
    
    colleges = [c[0] for c in db.session.query(Participant.college).distinct().all() if c[0]]
    departments = [d[0] for d in db.session.query(Participant.department).distinct().all() if d[0]]
    
    return render_template('admin/participants.html',
                           participants=participants_list,
                           colleges=colleges,
                           departments=departments,
                           active_college=college,
                           active_dept=dept)

@admin_bp.route('/admin/participants/export')
def export_participants():
    participants = Participant.query.all()
    for p in participants:
        p.update_totals()
    sorted_p = sorted(participants, key=lambda x: (-x.total_score, x.total_time_seconds))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Rank', 'Participant ID', 'Name', 'Email', 'College', 'Department', 'Year', 'Team Name', 'Round 1 Score', 'Round 2 Score', 'Total Score', 'Time (mm:ss)', 'Status', 'Registered At'])

    for rank, p in enumerate(sorted_p, start=1):
        writer.writerow([
            rank,
            p.participant_id,
            p.name,
            p.email,
            p.college,
            p.department,
            p.year,
            p.team_name or 'N/A',
            p.r1_score,
            p.r2_score,
            p.total_score,
            p.formatted_time,
            p.status,
            p.registered_at.strftime('%Y-%m-%d %H:%M:%S') if p.registered_at else ''
        ])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename=coderesq_leaderboard_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    return response

@admin_bp.route('/admin/submissions')
def submissions():
    round_filter = request.args.get('round', 'all')
    status_filter = request.args.get('status', 'all')
    
    query = Submission.query
    if round_filter in ['1', '2']:
        query = query.filter_by(round=int(round_filter))
    if status_filter in ['passed', 'failed', 'partial']:
        query = query.filter_by(status=status_filter)
        
    subs = query.order_by(Submission.submitted_at.desc()).limit(100).all()
    return render_template('admin/submissions.html',
                           submissions=subs,
                           active_round=round_filter,
                           active_status=status_filter)

@admin_bp.route('/admin/settings', methods=['GET', 'POST'])
def settings():
    comp = Competition.query.first()
    if not comp:
        comp = Competition()
        db.session.add(comp)
        db.session.commit()

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'save_config':
            comp.r1_duration_minutes = int(request.form.get('r1_duration_minutes', 30))
            comp.r2_duration_minutes = int(request.form.get('r2_duration_minutes', 30))
            comp.r1_enabled = bool(request.form.get('r1_enabled'))
            comp.r2_enabled = bool(request.form.get('r2_enabled'))
            comp.r1_points_per_question = float(request.form.get('r1_points_per_question', 5.0))
            comp.r2_points_per_question = float(request.form.get('r2_points_per_question', 14.0))
            comp.r2_points_per_error = float(request.form.get('r2_points_per_error', 2.0))
            comp.allow_answer_review = bool(request.form.get('allow_answer_review'))
            comp.anti_cheat_enabled = bool(request.form.get('anti_cheat_enabled'))
            db.session.commit()
            flash('Competition settings updated successfully.', 'success')

        elif action == 'reset_competition':
            confirm = request.form.get('confirm_reset')
            if confirm == 'RESET':
                Submission.query.delete()
                SuspiciousActivity.query.delete()
                Participant.query.delete()
                db.session.commit()
                flash('All participants, submissions, and logs have been reset!', 'warning')
            else:
                flash('Reset confirmation code incorrect. Type RESET to confirm.', 'error')

        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html', comp=comp)

@admin_bp.route('/admin/anti-cheat')
def anti_cheat_logs():
    logs = SuspiciousActivity.query.order_by(SuspiciousActivity.timestamp.desc()).limit(150).all()
    return render_template('admin/logs.html', logs=logs)
