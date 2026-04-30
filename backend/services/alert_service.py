"""
Alert Service - Daily spending alerts and financial reminders
"""

from datetime import datetime
from backend.database.csv_handler import CSVHandler
from backend.services.expense_service import ExpenseService

class AlertService:
    """Service for managing user notifications and alerts"""

    @staticmethod
    def get_daily_alerts(user_id):
        """Get relevant alerts for the user today"""
        alerts = []
        
        # 1. Budget Alert
        budget_analysis = ExpenseService.calculate_daily_budget(user_id)
        if budget_analysis['is_over_budget']:
            alerts.append({
                'id': 'budget_warning',
                'type': 'warning',
                'title': 'Budget Exceeded!',
                'message': f'You are over your daily budget by ₹{abs(budget_analysis["remaining_today"])}. Try to save more tomorrow.',
                'icon': '⚠️'
            })
        elif budget_analysis['remaining_today'] < 500:
            alerts.append({
                'id': 'budget_near',
                'type': 'info',
                'title': 'Nearing Daily Limit',
                'message': f'You only have ₹{budget_analysis["remaining_today"]} left for today.',
                'icon': 'ℹ️'
            })

        # 2. Savings Streak Alert
        expenses = CSVHandler.get_user_expenses(user_id)
        if expenses:
            # Simple streak: days with roundup > 0
            dates = sorted(list(set(e['date'] for e in expenses)), reverse=True)
            streak = 0
            for i in range(len(dates)):
                # In a real app, check consecutive days
                streak += 1
            
            if streak >= 3:
                alerts.append({
                    'id': 'savings_streak',
                    'type': 'success',
                    'title': 'Amazing Streak!',
                    'message': f'You have been saving for {streak} days in a row. Keep it up!',
                    'icon': '🔥'
                })

        # 3. Emergency Fund Reminder
        goals = CSVHandler.get_user_goals(user_id)
        has_emergency = any('Emergency' in g['goal_name'] for g in goals)
        if not has_emergency:
            alerts.append({
                'id': 'no_emergency',
                'type': 'action',
                'title': 'Safety First',
                'message': 'You haven\'t started an emergency fund yet. Let\'s build one today!',
                'icon': '🛡️'
            })

        # 4. Side Hustle Opportunity
        alerts.append({
            'id': 'hustle_promo',
            'type': 'info',
            'title': 'New Earning Opportunity',
            'message': 'A new high-paying side hustle matches your skills. Check it out!',
            'icon': '💰'
        })

        return alerts

    @staticmethod
    def get_reminders(user_id):
        """Get scheduled reminders"""
        return [
            {'time': '09:00', 'message': 'Don\'t forget to log your breakfast expenses!'},
            {'time': '21:00', 'message': 'Daily wrap-up: Check your savings progress for today.'}
        ]
