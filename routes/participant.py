import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from models import db, Participant, Competition, Question, Submission
from services.stats_service import get_leaderboard

participant_bp = Blueprint('participant', __name__)

@participant_bp.route('/')
def index():
    comp = Competition.query.first()
    total_participants = Participant.query.count()
    return render_template('index.html', comp=comp, total_participants=total_participants)

@participant_bp.route('/register', methods=['GET', 'POST'])
def register():
    # If participant is already registered in session, offer to continue or re-register
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        participant_id = request.form.get('participant_id', '').strip().upper()
        email = request.form.get('email', '').strip().lower()
        college = request.form.get('college', '').strip()
        department = request.form.get('department', '').strip()
        year = request.form.get('year', '').strip()
        team_name = request.form.get('team_name', '').strip()

        # Validation
        if not all([name, participant_id, email, college, department, year]):
            flash('All required fields must be filled.', 'error')
            return render_template('register.html', form=request.form)

        # Check existing participant ID or email
        existing_pid = Participant.query.filter_by(participant_id=participant_id).first()
        if existing_pid:
            # Login as existing participant if matching
            if existing_pid.email == email:
                session['participant_id'] = existing_pid.participant_id
                session['session_token'] = existing_pid.session_token
                flash(f'Welcome back, {existing_pid.name}! Resuming your session.', 'info')
                if existing_pid.status == 'completed':
                    return redirect(url_for('participant.result'))
                elif existing_pid.status in ['round2_active', 'round1_completed']:
                    return redirect(url_for('competition.round2'))
                else:
                    return redirect(url_for('participant.rules'))
            else:
                flash('Participant ID / Register Number already in use with another email.', 'error')
                return render_template('register.html', form=request.form)

        # Create new participant
        token = str(uuid.uuid4())
        participant = Participant(
            name=name,
            participant_id=participant_id,
            email=email,
            college=college,
            department=department,
            year=year,
            team_name=team_name if team_name else None,
            session_token=token,
            status='registered'
        )
        db.session.add(participant)
        db.session.commit()

        session['participant_id'] = participant.participant_id
        session['session_token'] = token
        flash('Registration successful! Please review the competition rules.', 'success')
        return redirect(url_for('participant.rules'))

    return render_template('register.html', form={})

@participant_bp.route('/rules')
def rules():
    pid = session.get('participant_id')
    if not pid:
        flash('Please register before accessing competition rules.', 'warning')
        return redirect(url_for('participant.register'))

    participant = Participant.query.filter_by(participant_id=pid).first()
    comp = Competition.query.first()
    return render_template('rules.html', participant=participant, comp=comp)

@participant_bp.route('/result')
def result():
    pid = session.get('participant_id')
    participant = None
    # Allow admin or participant lookup via query param as well
    query_pid = request.args.get('pid')
    if query_pid:
        participant = Participant.query.filter_by(participant_id=query_pid).first()
    elif pid:
        participant = Participant.query.filter_by(participant_id=pid).first()

    if not participant:
        flash('No participant session found.', 'warning')
        return redirect(url_for('participant.register'))

    participant.update_totals()
    comp = Competition.query.first()
    
    # Calculate performance rating and percentage
    max_score = 170.0 # 100 R1 + 70 R2
    if comp:
        max_score = (comp.r1_points_per_question * 20) + (comp.r2_points_per_question * 5)
        
    pct = round((participant.total_score / max_score * 100), 2) if max_score > 0 else 0.0
    
    if pct >= 85:
        performance = "Outstanding (Grandmaster Debugger)"
        badge_color = "emerald"
    elif pct >= 70:
        performance = "Excellent (Expert Debugger)"
        badge_color = "indigo"
    elif pct >= 50:
        performance = "Proficient (Skilled Solver)"
        badge_color = "blue"
    elif pct >= 30:
        performance = "Promising (Developing Solver)"
        badge_color = "amber"
    else:
        performance = "Participant (Good Effort)"
        badge_color = "slate"

    # Submissions breakdown
    submissions = Submission.query.filter_by(participant_id=participant.id).all()
    sub_map = {s.question_id: s for s in submissions}

    return render_template('result.html',
                           participant=participant,
                           comp=comp,
                           pct=pct,
                           max_score=max_score,
                           performance=performance,
                           badge_color=badge_color,
                           sub_map=sub_map,
                           allow_review=comp.allow_answer_review if comp else False)

@participant_bp.route('/leaderboard')
def leaderboard():
    college = request.args.get('college', 'all')
    department = request.args.get('department', 'all')
    round_filter = request.args.get('round', 'total')
    
    ranked_participants = get_leaderboard(college=college, department=department, round_filter=round_filter)
    
    # Distinct colleges and departments for filter dropdowns
    colleges = [c[0] for c in db.session.query(Participant.college).distinct().all() if c[0]]
    departments = [d[0] for d in db.session.query(Participant.department).distinct().all() if d[0]]
    
    return render_template('leaderboard.html',
                           participants=ranked_participants,
                           colleges=colleges,
                           departments=departments,
                           active_college=college,
                           active_dept=department,
                           active_round=round_filter)
