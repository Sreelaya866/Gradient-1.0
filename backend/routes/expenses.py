"""
Expense Routes - Expense tracking and management endpoints
"""

from flask import Blueprint, request, jsonify
from backend.services.expense_service import ExpenseService
from backend.database.csv_handler import CSVHandler

bp = Blueprint('expenses', __name__, url_prefix='/api/expenses')

@bp.route('/', methods=['GET'])
def get_expenses():
    """Get all expenses for a user"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        expenses = ExpenseService.get_user_expenses(user_id)
        
        return jsonify({
            'success': True,
            'expenses': expenses,
            'count': len(expenses)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/add', methods=['POST'])
def add_expense():
    """Add new expense"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'date', 'category', 'merchant', 'amount']
        if not all(data.get(f) for f in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        expense = ExpenseService.add_expense(
            data['user_id'],
            data['date'],
            data['category'],
            data['merchant'],
            data['amount']
        )
        
        if not expense:
            return jsonify({'success': False, 'error': 'Failed to add expense'}), 500
        
        return jsonify({
            'success': True,
            'message': 'Expense added successfully',
            'expense': expense
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/summary', methods=['GET'])
def get_summary():
    """Get expense summary for user"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        summary = ExpenseService.get_expense_summary(user_id)
        
        return jsonify({
            'success': True,
            'summary': summary
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/by-category', methods=['GET'])
def get_by_category():
    """Get expense breakdown by category"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        breakdown = ExpenseService.get_category_breakdown(user_id)
        
        return jsonify({
            'success': True,
            'breakdown': breakdown
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/top-days', methods=['GET'])
def get_top_days():
    """Get top spending days"""
    try:
        user_id = request.args.get('user_id', type=int)
        limit = request.args.get('limit', default=10, type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        days = ExpenseService.get_top_spending_days(user_id, limit)
        
        return jsonify({
            'success': True,
            'top_days': days
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/budget', methods=['GET'])
def get_budget():
    """Get daily budget analysis"""
    try:
        user_id = request.args.get('user_id', type=int)
        monthly_limit = request.args.get('limit', default=50000, type=float)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        budget = ExpenseService.calculate_daily_budget(user_id, monthly_limit)
        
        return jsonify({
            'success': True,
            'budget': budget
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/date-range', methods=['GET'])
def get_by_date_range():
    """Get expenses within date range"""
    try:
        user_id = request.args.get('user_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not all([user_id, start_date, end_date]):
            return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
        
        from datetime import datetime
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        expenses = ExpenseService.get_expenses_by_date_range(user_id, start, end)
        
        return jsonify({
            'success': True,
            'expenses': expenses,
            'count': len(expenses)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/export', methods=['GET'])
def export_csv():
    """Export expenses to CSV"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        expenses = ExpenseService.get_user_expenses(user_id)
        
        # Create CSV content
        csv_content = "date,category,merchant,amount,roundup\n"
        for exp in expenses:
            csv_content += f"{exp['date']},{exp['category']},{exp['merchant']},{exp['amount']},{exp['roundup']}\n"
        
        return {
            'success': True,
            'csv': csv_content,
            'filename': f'expenses_user_{user_id}.csv'
        }, 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
