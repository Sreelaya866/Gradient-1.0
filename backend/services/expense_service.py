"""
Expense Service - Business logic for expense management
"""

from backend.database.csv_handler import CSVHandler
from datetime import datetime, timedelta

class ExpenseService:
    """Service for handling expense-related operations"""

    @staticmethod
    def add_expense(user_id, date, category, merchant, amount):
        """Add expense and calculate round-up"""
        expense = CSVHandler.add_expense(user_id, date, category, merchant, amount)
        if expense:
            expense['roundup'] = round(amount) - amount
        return expense

    @staticmethod
    def get_user_expenses(user_id):
        """Get all expenses with round-up calculation"""
        expenses = CSVHandler.get_user_expenses(user_id)
        for exp in expenses:
            exp['roundup'] = round(exp['amount']) - exp['amount']
        return expenses

    @staticmethod
    def get_expense_summary(user_id):
        """Get comprehensive expense summary"""
        summary = CSVHandler.get_user_expense_summary(user_id)
        expenses = CSVHandler.get_user_expenses(user_id)
        
        # Calculate roundup total
        total_roundup = sum(round(e['amount']) - e['amount'] for e in expenses)
        
        summary['total_roundup'] = total_roundup
        summary['monthly_average'] = summary.get('average_expense', 0)
        
        return summary

    @staticmethod
    def get_expenses_by_date_range(user_id, start_date, end_date):
        """Get expenses within a date range"""
        expenses = CSVHandler.get_user_expenses(user_id)
        
        filtered = []
        for exp in expenses:
            try:
                exp_date = datetime.strptime(exp['date'], '%Y-%m-%d')
                if start_date <= exp_date <= end_date:
                    exp['roundup'] = round(exp['amount']) - exp['amount']
                    filtered.append(exp)
            except:
                continue
        
        return filtered

    @staticmethod
    def get_category_breakdown(user_id):
        """Get spending breakdown by category"""
        summary = CSVHandler.get_user_expense_summary(user_id)
        categories = summary.get('categories', {})
        
        total = sum(categories.values())
        breakdown = {}
        
        for category, amount in categories.items():
            percentage = (amount / total * 100) if total > 0 else 0
            breakdown[category] = {
                'amount': amount,
                'percentage': round(percentage, 2)
            }
        
        return breakdown

    @staticmethod
    def get_top_spending_days(user_id, limit=10):
        """Get top spending days"""
        expenses = CSVHandler.get_user_expenses(user_id)
        
        daily = {}
        for exp in expenses:
            date = exp['date']
            daily[date] = daily.get(date, 0) + exp['amount']
        
        sorted_days = sorted(daily.items(), key=lambda x: x[1], reverse=True)
        return [{'date': day[0], 'amount': day[1]} for day in sorted_days[:limit]]

    @staticmethod
    def calculate_daily_budget(user_id, monthly_limit=50000):
        """Calculate if user is within daily budget"""
        expenses = CSVHandler.get_user_expenses(user_id)
        
        # Get expenses from this month
        today = datetime.now()
        month_start = today.replace(day=1)
        
        month_total = 0
        for exp in expenses:
            try:
                exp_date = datetime.strptime(exp['date'], '%Y-%m-%d')
                if exp_date >= month_start:
                    month_total += exp['amount']
            except:
                continue
        
        days_in_month = (today.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1)).day
        daily_budget = monthly_limit / days_in_month
        days_remaining = days_in_month - today.day
        daily_remaining = (monthly_limit - month_total) / days_remaining if days_remaining > 0 else 0
        
        return {
            'monthly_limit': monthly_limit,
            'spent_this_month': month_total,
            'remaining': monthly_limit - month_total,
            'daily_budget': round(daily_budget, 2),
            'daily_remaining': round(daily_remaining, 2),
            'on_budget': month_total <= monthly_limit * (today.day / days_in_month)
        }
