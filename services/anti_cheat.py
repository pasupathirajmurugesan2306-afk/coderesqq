from datetime import datetime
from models import db, SuspiciousActivity, Participant, Competition

def log_suspicious_activity(participant_id, event, details=None):
    """Logs an anti-cheat event to the database."""
    try:
        activity = SuspiciousActivity(
            participant_id=participant_id,
            event=event,
            details=details,
            timestamp=datetime.utcnow()
        )
        db.session.add(activity)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

def validate_round_timer(participant, round_num):
    """
    Validates server-side that participant is within allowed timer limit for the round.
    Returns (is_valid, remaining_seconds).
    """
    comp = Competition.query.first()
    if not comp:
        return True, 1800
        
    duration_mins = comp.r1_duration_minutes if round_num == 1 else comp.r2_duration_minutes
    start_time = participant.r1_started_at if round_num == 1 else participant.r2_started_at
    
    if not start_time:
        return True, duration_mins * 60
        
    elapsed = (datetime.utcnow() - start_time).total_seconds()
    allowed = duration_mins * 60
    # 30-second grace period for network latency
    remaining = max(0, int(allowed - elapsed))
    is_valid = elapsed <= (allowed + 30)
    
    return is_valid, remaining
