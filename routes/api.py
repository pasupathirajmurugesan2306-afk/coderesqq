from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models import db, Participant, SuspiciousActivity, Competition
from services.anti_cheat import log_suspicious_activity, validate_round_timer

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/anti_cheat/log', methods=['POST'])
def log_cheat_activity():
    data = request.get_json() or {}
    event = data.get('event', 'Unknown Suspicious Activity')
    details = data.get('details', '')
    
    pid = session.get('participant_id')
    if not pid:
        return jsonify({'logged': False, 'message': 'No session'}), 200

    participant = Participant.query.filter_by(participant_id=pid).first()
    if not participant:
        return jsonify({'logged': False, 'message': 'Participant not found'}), 200

    log_suspicious_activity(participant.id, event, details)
    return jsonify({'logged': True, 'event': event})

@api_bp.route('/api/timer/sync', methods=['GET'])
def sync_timer():
    pid = session.get('participant_id')
    round_num = request.args.get('round', 1, type=int)
    
    if not pid:
        return jsonify({'remaining_seconds': 0, 'is_valid': False})
        
    participant = Participant.query.filter_by(participant_id=pid).first()
    if not participant:
        return jsonify({'remaining_seconds': 0, 'is_valid': False})

    is_valid, remaining_seconds = validate_round_timer(participant, round_num)
    return jsonify({
        'is_valid': is_valid,
        'remaining_seconds': remaining_seconds
    })
