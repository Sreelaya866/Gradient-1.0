"""
Insights Routes - AI-powered insights and recommendations
"""

from flask import Blueprint, request, jsonify
from backend.services.ai_service import AIService
from backend.services.investment_service import InvestmentService
from backend.database.csv_handler import CSVHandler
from backend.services.expense_service import ExpenseService

bp = Blueprint('insights', __name__, url_prefix='/api/insights')

@bp.route('/savings-tips', methods=['GET'])
def get_savings_tips():
    """Get personalized savings tips"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        summary = ExpenseService.get_expense_summary(user_id)
        tips = AIService.generate_savings_tips(summary)
        
        return jsonify({
            'success': True,
            'tips': tips
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/spending-cuts', methods=['GET'])
def get_spending_cuts():
    """Get personalized spending cut suggestions"""
    try:
        user_id = request.args.get('user_id', type=int)
        target_cut = request.args.get('cut_percentage', default=10, type=float)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        summary = ExpenseService.get_expense_summary(user_id)
        suggestions = AIService.suggest_spending_cuts(summary, target_cut)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/spending-trend', methods=['GET'])
def get_spending_trend():
    """Predict spending trend"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        expenses = CSVHandler.get_user_expenses(user_id)
        prediction = AIService.predict_spending_trend(expenses)
        
        return jsonify({
            'success': True,
            'prediction': prediction
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/investment-recommendations', methods=['GET'])
def get_investment_recommendations():
    """Get investment recommendations"""
    try:
        user_id = request.args.get('user_id', type=int)
        risk_profile = request.args.get('risk_profile', default='Medium')
        budget = request.args.get('budget', default=5000, type=float)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        recommendations = InvestmentService.recommend_investments(user_id, risk_profile, budget)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/portfolio-analysis', methods=['GET'])
def get_portfolio_analysis():
    """Analyze investment portfolio"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        portfolio = InvestmentService.get_portfolio(user_id)
        returns = InvestmentService.calculate_investment_returns(user_id)
        diversification = InvestmentService.get_diversification_analysis(user_id)
        
        return jsonify({
            'success': True,
            'portfolio': portfolio,
            'returns': returns,
            'diversification': diversification
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/investment-plan', methods=['POST'])
def create_investment_plan():
    """Create long-term investment plan"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        monthly_savings = data.get('monthly_savings', 1000)
        duration_months = data.get('duration_months', 12)
        risk_profile = data.get('risk_profile', 'Medium')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        plan = InvestmentService.create_investment_plan(
            user_id, monthly_savings, duration_months, risk_profile
        )
        
        return jsonify({
            'success': True,
            'plan': plan
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/dashboard-summary', methods=['GET'])
def get_dashboard_summary():
    """Get comprehensive dashboard summary"""
    try:
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id required'}), 400
        
        # Get all data
        expense_summary = ExpenseService.get_expense_summary(user_id)
        goal_progress = CSVHandler.get_goal_progress(user_id)
        portfolio = InvestmentService.get_portfolio(user_id)
        roundup_savings = CSVHandler.calculate_roundup_savings(user_id)
        
        return jsonify({
            'success': True,
            'summary': {
                'expenses': expense_summary,
                'goals': goal_progress,
                'investments': portfolio,
                'roundup_savings': roundup_savings
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
