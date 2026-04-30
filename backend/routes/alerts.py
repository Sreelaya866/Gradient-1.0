"""
Alert Routes - Daily alerts and reminders endpoints
"""

from flask import Blueprint, request, jsonify
from backend.services.alert_service import AlertService

bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

@bp.route('/', methods=['GET'])
def get_alerts():
    """Get daily alerts for user"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
            
        alerts = AlertService.get_daily_alerts(user_id)
        reminders = AlertService.get_reminders(user_id)
        
        return jsonify({
            'success': True,
            'alerts': alerts,
            'reminders': reminders
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
