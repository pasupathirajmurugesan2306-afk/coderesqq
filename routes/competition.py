from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Participant, Question, JavaError, Submission, Competition
from services.code_evaluator import run_python_code, evaluate_java_code
from services.anti_cheat import validate_round_timer

competition_bp = Blueprint('competition', __name__)

@competition_bp.route('/round1')
def round1():
    pid = session.get('participant_id')
    if not pid:
        flash('Please register before starting the challenge.', 'warning')
        return redirect(url_for('participant.register'))
        
    participant = Participant.query.filter_by(participant_id=pid).first()
    if not participant:
        flash('Participant not found.', 'error')
        return redirect(url_for('participant.register'))

    comp = Competition.query.first()
    if comp and not comp.r1_enabled:
        flash('Round 1 is currently disabled by the competition administrator.', 'warning')
        return redirect(url_for('participant.rules'))

    # Start timer if not already started
    if not participant.r1_started_at:
        participant.r1_started_at = datetime.utcnow()
        participant.status = 'round1_active'
        db.session.commit()

    # Check remaining time
    is_valid, remaining_seconds = validate_round_timer(participant, 1)
    if remaining_seconds <= 0 and participant.status == 'round1_active':
        # Auto-complete round 1
        participant.r1_completed_at = datetime.utcnow()
        participant.status = 'round1_completed'
        db.session.commit()
        flash('Round 1 time limit has expired.', 'info')
        return redirect(url_for('competition.round2'))

    questions = Question.query.filter_by(round=1).order_by(Question.order_num).all()
    submissions = Submission.query.filter_by(participant_id=participant.id, round=1).all()
    sub_map = {s.question_id: s for s in submissions}

    # Prepare questions data for JavaScript Monaco editor
    q_data_list = []
    for q in questions:
        sub = sub_map.get(q.id)
        current_code = sub.submitted_code if sub else q.buggy_code
        is_solved = (sub.status == 'passed') if sub else False
        score = sub.score if sub else 0.0
        
        q_data_list.append({
            'id': q.id,
            'order_num': q.order_num,
            'title': q.title,
            'difficulty': q.difficulty,
            'error_type': q.error_type,
            'question_text': q.question_text,
            'buggy_code': q.buggy_code,
            'current_code': current_code,
            'is_solved': is_solved,
            'score': score,
            'points': q.points,
            'test_cases': [tc for tc in q.test_cases if not tc.get('is_hidden', False)]
        })

    return render_template('round1.html',
                           participant=participant,
                           comp=comp,
                           questions=questions,
                           q_data_json=q_data_list,
                           remaining_seconds=remaining_seconds)


@competition_bp.route('/round1/finish', methods=['POST'])
def finish_round1():
    pid = session.get('participant_id')
    if not pid:
        return redirect(url_for('participant.register'))
        
    participant = Participant.query.filter_by(participant_id=pid).first()
    if participant:
        if not participant.r1_completed_at:
            participant.r1_completed_at = datetime.utcnow()
        participant.status = 'round1_completed'
        
        # Calculate R1 total score
        r1_subs = Submission.query.filter_by(participant_id=participant.id, round=1).all()
        participant.r1_score = sum(s.score for s in r1_subs)
        participant.update_totals()
        db.session.commit()
        
        flash('Round 1 submitted successfully! You are now entering Round 2.', 'success')
        
    comp = Competition.query.first()
    if comp and comp.r2_enabled:
        return redirect(url_for('competition.round2'))
    return redirect(url_for('participant.result'))


@competition_bp.route('/round2')
def round2():
    pid = session.get('participant_id')
    if not pid:
        flash('Please register before accessing Round 2.', 'warning')
        return redirect(url_for('participant.register'))
        
    participant = Participant.query.filter_by(participant_id=pid).first()
    if not participant:
        return redirect(url_for('participant.register'))

    comp = Competition.query.first()
    if comp and not comp.r2_enabled:
        flash('Round 2 is currently disabled by the competition administrator.', 'warning')
        return redirect(url_for('participant.result'))

    # Start timer if not already started
    if not participant.r2_started_at:
        participant.r2_started_at = datetime.utcnow()
        participant.status = 'round2_active'
        db.session.commit()

    # Check remaining time
    is_valid, remaining_seconds = validate_round_timer(participant, 2)
    if remaining_seconds <= 0 and participant.status == 'round2_active':
        participant.r2_completed_at = datetime.utcnow()
        participant.status = 'completed'
        participant.update_totals()
        db.session.commit()
        flash('Round 2 time limit has expired.', 'info')
        return redirect(url_for('participant.result'))

    questions = Question.query.filter_by(round=2).order_by(Question.order_num).all()
    submissions = Submission.query.filter_by(participant_id=participant.id, round=2).all()
    sub_map = {s.question_id: s for s in submissions}

    q_data_list = []
    for q in questions:
        sub = sub_map.get(q.id)
        current_code = sub.submitted_code if sub else q.buggy_code
        fixed_count = sub.errors_fixed_count if sub else 0
        score = sub.score if sub else 0.0
        
        q_data_list.append({
            'id': q.id,
            'order_num': q.order_num,
            'title': q.title,
            'difficulty': q.difficulty,
            'question_text': q.question_text,
            'buggy_code': q.buggy_code,
            'current_code': current_code,
            'errors_fixed_count': fixed_count,
            'total_errors': 7,
            'score': score,
            'points': q.points
        })

    return render_template('round2.html',
                           participant=participant,
                           comp=comp,
                           questions=questions,
                           q_data_json=q_data_list,
                           remaining_seconds=remaining_seconds)


@competition_bp.route('/round2/finish', methods=['POST'])
def finish_round2():
    pid = session.get('participant_id')
    if not pid:
        return redirect(url_for('participant.register'))
        
    participant = Participant.query.filter_by(participant_id=pid).first()
    if participant:
        if not participant.r2_completed_at:
            participant.r2_completed_at = datetime.utcnow()
        participant.status = 'completed'
        
        # Calculate R2 total score
        r2_subs = Submission.query.filter_by(participant_id=participant.id, round=2).all()
        participant.r2_score = sum(s.score for s in r2_subs)
        participant.update_totals()
        db.session.commit()
        
        flash('Challenge successfully completed! Here is your final scorecard.', 'success')
        
    return redirect(url_for('participant.result'))


# API: Run Code (Trial Run without submitting for score)
@competition_bp.route('/api/run_code', methods=['POST'])
def api_run_code():
    data = request.get_json() or {}
    question_id = data.get('question_id')
    user_code = data.get('code', '')
    
    question = db.session.get(Question, question_id)
    if not question:
        return jsonify({'success': False, 'error': 'Question not found'}), 404
        
    if question.language == 'python':
        # Run visible test cases
        visible_tests = [tc for tc in question.test_cases if not tc.get('is_hidden', False)]
        eval_res = run_python_code(user_code, visible_tests)
        return jsonify({
            'success': eval_res['success'],
            'results': eval_res['results'],
            'stdout': eval_res['stdout'],
            'stderr': eval_res['stderr'],
            'fatal_error': eval_res.get('fatal_error')
        })
    else: # Java
        eval_res = evaluate_java_code(user_code, question.java_errors, question.test_cases, question)
        return jsonify({
            'success': eval_res['success'],
            'errors_fixed_count': eval_res['errors_fixed_count'],
            'total_errors': eval_res['total_errors'],
            'fixed_status_list': eval_res['fixed_status_list'],
            'stdout': eval_res['stdout']
        })


# API: Submit Code (Official Submission & Scoring)
@competition_bp.route('/api/submit_code', methods=['POST'])
def api_submit_code():
    pid = session.get('participant_id')
    if not pid:
        return jsonify({'success': False, 'error': 'Unauthorized session'}), 401
        
    participant = Participant.query.filter_by(participant_id=pid).first()
    if not participant:
        return jsonify({'success': False, 'error': 'Participant not found'}), 404
        
    data = request.get_json() or {}
    question_id = data.get('question_id')
    user_code = data.get('code', '')
    
    question = db.session.get(Question, question_id)
    if not question:
        return jsonify({'success': False, 'error': 'Question not found'}), 404

    comp = Competition.query.first()
    pts_per_q1 = comp.r1_points_per_question if comp else 5.0
    pts_per_error2 = comp.r2_points_per_error if comp else 2.0

    score = 0.0
    status = 'failed'
    errors_fixed_count = 0
    eval_details = {}

    if question.language == 'python':
        # Evaluate against ALL test cases (visible + hidden)
        eval_res = run_python_code(user_code, question.test_cases)
        eval_details = eval_res
        if eval_res['success']:
            score = question.points or pts_per_q1
            status = 'passed'
        else:
            score = 0.0
            status = 'failed'
    else: # Java
        eval_res = evaluate_java_code(user_code, question.java_errors, question.test_cases, question)
        eval_details = eval_res
        errors_fixed_count = eval_res['errors_fixed_count']
        score = round(errors_fixed_count * pts_per_error2, 2)
        if errors_fixed_count == len(question.java_errors):
            status = 'passed'
            score = question.points # full marks
        elif errors_fixed_count > 0:
            status = 'partial'
        else:
            status = 'failed'

    # Save or update submission
    submission = Submission.query.filter_by(participant_id=participant.id, question_id=question.id).first()
    if not submission:
        submission = Submission(
            participant_id=participant.id,
            question_id=question.id,
            round=question.round,
            submitted_code=user_code,
            score=score,
            errors_fixed_count=errors_fixed_count,
            status=status
        )
        db.session.add(submission)
    else:
        # Keep highest score
        if score >= submission.score:
            submission.submitted_code = user_code
            submission.score = score
            submission.errors_fixed_count = errors_fixed_count
            submission.status = status
            submission.submitted_at = datetime.utcnow()

    submission.test_results = eval_details

    # Update participant round score
    if question.round == 1:
        r1_subs = Submission.query.filter_by(participant_id=participant.id, round=1).all()
        participant.r1_score = sum(s.score for s in r1_subs)
    else:
        r2_subs = Submission.query.filter_by(participant_id=participant.id, round=2).all()
        participant.r2_score = sum(s.score for s in r2_subs)

    participant.update_totals()
    db.session.commit()

    return jsonify({
        'success': True,
        'status': status,
        'score': score,
        'errors_fixed_count': errors_fixed_count,
        'total_errors': 7 if question.language == 'java' else 1,
        'r1_score': participant.r1_score,
        'r2_score': participant.r2_score,
        'total_score': participant.total_score,
        'eval_details': eval_details
    })
