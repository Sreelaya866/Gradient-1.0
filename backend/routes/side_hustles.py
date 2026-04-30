"""
Side Hustles Routes - Side hustle recommendations and opportunities
"""

from flask import Blueprint, request, jsonify
from backend.services.hustle_service import HustleService
from backend.services.ai_service import AIService

bp = Blueprint('side_hustles', __name__, url_prefix='/api/side-hustles')

@bp.route('/', methods=['GET'])
def get_all_hustles():
    """Get all available side hustles"""
    try:
        hustles = HustleService.get_all_hustles()
        
        return jsonify({
            'success': True,
            'hustles': hustles,
            'count': len(hustles)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/top', methods=['GET'])
def get_top_hustles():
    """Get top rated hustles"""
    try:
        limit = request.args.get('limit', default=5, type=int)
        hustles = HustleService.get_top_hustles(limit)
        
        return jsonify({
            'success': True,
            'hustles': hustles,
            'count': len(hustles)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/search', methods=['GET'])
def search_hustles():
    """Search hustles by keyword"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query required'}), 400
        
        results = HustleService.search_hustles(query)
        
        return jsonify({
            'success': True,
            'hustles': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/filter', methods=['GET'])
def filter_hustles():
    """Filter hustles by criteria"""
    try:
        difficulty = request.args.get('difficulty')
        max_time = request.args.get('max_time', type=int)
        min_earnings = request.args.get('min_earnings', type=float)
        
        results = HustleService.filter_hustles(difficulty, max_time, min_earnings)
        
        return jsonify({
            'success': True,
            'hustles': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """Get AI-personalized hustle recommendations"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        recommendations = HustleService.get_hustle_recommendations(user_id)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<int:hustle_id>', methods=['GET'])
def get_hustle_details(hustle_id):
    """Get details for specific hustle"""
    try:
        hustle = HustleService.get_hustle_by_id(hustle_id)
        
        if not hustle:
            return jsonify({'success': False, 'error': 'Hustle not found'}), 404
        
        return jsonify({
            'success': True,
            'hustle': hustle
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<int:hustle_id>/guide', methods=['GET'])
def get_success_guide(hustle_id):
    """Get success guide for specific hustle"""
    try:
        guide = HustleService.get_hustle_success_guide(hustle_id)
        
        if not guide:
            return jsonify({'success': False, 'error': 'Guide not found'}), 404
        
        return jsonify({
            'success': True,
            'guide': guide
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/earning-potential', methods=['GET'])
def get_earning_potential():
    """Calculate earning potential based on time"""
    try:
        hours_per_week = request.args.get('hours_per_week', default=10, type=float)
        
        potential = HustleService.get_earning_potential_by_time(hours_per_week)
        
        return jsonify({
            'success': True,
            'potential': potential
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/ai-match', methods=['POST'])
def get_ai_match():
    """Get AI-matched hustles based on user profile"""
    try:
        data = request.get_json()
        
        skills = data.get('skills', [])
        time_available = data.get('time_available', 5)
        risk_tolerance = data.get('risk_tolerance', 'medium')
        
        matches = AIService.match_side_hustle(skills, time_available, risk_tolerance)
        
        return jsonify({
            'success': True,
            'matches': matches,
            'count': len(matches)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
