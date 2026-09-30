from models import db, Participant, Submission, Question
from sqlalchemy import func, desc, asc

def get_leaderboard(college=None, department=None, round_filter=None):
    """
    Returns ranked participants list.
    Primary sort: total_score DESC (or round score if filtered)
    Secondary sort: total_time_seconds ASC
    """
    query = Participant.query
    
    if college and college != 'all':
        query = query.filter(Participant.college == college)
    if department and department != 'all':
        query = query.filter(Participant.department == department)
        
    participants = query.all()
    
    # Recalculate totals for consistency
    for p in participants:
        p.update_totals()
        
    if round_filter == 'round1':
        sorted_p = sorted(participants, key=lambda x: (-x.r1_score, x.total_time_seconds))
    elif round_filter == 'round2':
        sorted_p = sorted(participants, key=lambda x: (-x.r2_score, x.total_time_seconds))
    else:
        sorted_p = sorted(participants, key=lambda x: (-x.total_score, x.total_time_seconds))
        
    ranked = []
    for rank, p in enumerate(sorted_p, start=1):
        ranked.append({
            'rank': rank,
            'id': p.id,
            'name': p.name,
            'participant_id': p.participant_id,
            'college': p.college,
            'department': p.department,
            'year': p.year,
            'team_name': p.team_name,
            'r1_score': p.r1_score,
            'r2_score': p.r2_score,
            'total_score': p.total_score,
            'formatted_time': p.formatted_time,
            'status': p.status
        })
        
    return ranked

def get_admin_dashboard_metrics():
    """Calculates comprehensive statistics for the Admin Dashboard."""
    total_participants = Participant.query.count()
    r1_participants = Participant.query.filter(Participant.r1_started_at.isnot(None)).count()
    r2_participants = Participant.query.filter(Participant.r2_started_at.isnot(None)).count()
    completed_count = Participant.query.filter(Participant.status == 'completed').count()
    
    avg_score = db.session.query(func.avg(Participant.total_score)).scalar() or 0.0
    highest_score = db.session.query(func.max(Participant.total_score)).scalar() or 0.0
    avg_r1_score = db.session.query(func.avg(Participant.r1_score)).scalar() or 0.0
    avg_r2_score = db.session.query(func.avg(Participant.r2_score)).scalar() or 0.0

    # Score Distribution buckets
    # 0-20, 21-40, 41-60, 61-80, 81-100
    all_scores = [p.total_score for p in Participant.query.all()]
    buckets = {'0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0}
    for s in all_scores:
        if s <= 20:
            buckets['0-20'] += 1
        elif s <= 40:
            buckets['21-40'] += 1
        elif s <= 60:
            buckets['41-60'] += 1
        elif s <= 80:
            buckets['61-80'] += 1
        else:
            buckets['81-100'] += 1

    # College breakdown
    college_counts = db.session.query(Participant.college, func.count(Participant.id))\
        .group_by(Participant.college)\
        .order_by(func.count(Participant.id).desc())\
        .limit(6).all()
        
    colleges_data = {
        'labels': [c[0] for c in college_counts],
        'counts': [c[1] for c in college_counts]
    }

    return {
        'total_participants': total_participants,
        'r1_participants': r1_participants,
        'r2_participants': r2_participants,
        'completed_count': completed_count,
        'avg_score': round(avg_score, 1),
        'highest_score': round(highest_score, 1),
        'avg_r1_score': round(avg_r1_score, 1),
        'avg_r2_score': round(avg_r2_score, 1),
        'score_distribution': buckets,
        'college_distribution': colleges_data
    }
