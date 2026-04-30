"""
Savings Routes - Savings goals and round-up savings management
"""

from flask import Blueprint, request, jsonify
from backend.services.savings_service import SavingsService
from backend.database.csv_handler import CSVHandler

bp = Blueprint('savings', __name__, url_prefix='/api/savings')

@bp.route('/roundup-total', methods=['GET'])
def get_roundup_total():
    """Get total round-up savings"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        data = SavingsService.get_total_roundup_savings(user_id)
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/savings-potential', methods=['GET'])
def get_savings_potential():
    """Get savings potential analysis"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        potential = SavingsService.get_savings_potential(user_id)
        
        return jsonify({
            'success': True,
            'potential': potential
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/emergency-fund-plan', methods=['GET'])
def get_emergency_fund():
    """Get emergency fund building plan"""
    try:
        user_id = request.args.get('user_id', type=int)
        monthly_income = request.args.get('monthly_income', default=50000, type=float)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        plan = SavingsService.build_emergency_fund_plan(user_id, monthly_income)
        
        return jsonify({
            'success': True,
            'plan': plan
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/monthly-comparison', methods=['GET'])
def get_monthly_comparison():
    """Get month-over-month savings comparison"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        comparison = SavingsService.get_monthly_comparison(user_id)
        
        return jsonify({
            'success': True,
            'comparison': comparison
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/auto-savings-targets', methods=['GET'])
def get_auto_savings():
    """Get automatic savings distribution suggestions"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        suggestions = SavingsService.suggest_auto_savings_targets(user_id)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/goals', methods=['GET'])
def get_goals():
    """Get all savings goals for user"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        goals = CSVHandler.get_user_goals(user_id)
        progress = CSVHandler.get_goal_progress(user_id)
        
        return jsonify({
            'success': True,
            'goals': goals,
            'progress': progress
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/goals/add', methods=['POST'])
def add_goal():
    """Add new savings goal"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'goal_name', 'target_amount', 'deadline']
        if not all(data.get(f) for f in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        goal = CSVHandler.add_goal(
            data['user_id'],
            data['goal_name'],
            data['target_amount'],
            data['deadline']
        )
        
        if not goal:
            return jsonify({'success': False, 'error': 'Failed to add goal'}), 500
        
        return jsonify({
            'success': True,
            'message': 'Goal created successfully',
            'goal': goal
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/goals/progress', methods=['GET'])
def get_goal_progress():
    """Get overall goal progress"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        progress = CSVHandler.get_goal_progress(user_id)
        
        return jsonify({
            'success': True,
            'progress': progress
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
