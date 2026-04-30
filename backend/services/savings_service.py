"""
Savings Service - Business logic for savings and round-up operations
"""

from backend.database.csv_handler import CSVHandler

class SavingsService:
    """Service for handling savings-related operations"""

    @staticmethod
    def get_total_roundup_savings(user_id):
        """Get total savings from round-ups"""
        roundup_data = CSVHandler.calculate_roundup_savings(user_id)
        return roundup_data

    @staticmethod
    def get_savings_potential(user_id):
        """Calculate savings potential based on spending"""
        expenses = CSVHandler.get_user_expenses(user_id)
        
        if not expenses:
            return {
                'total_roundup': 0,
                'savings_rate': 0,
                'potential_monthly': 0
            }
        
        total_roundup = sum(round(e['amount']) - e['amount'] for e in expenses)
        total_spent = sum(e['amount'] for e in expenses)
        savings_rate = (total_roundup / total_spent * 100) if total_spent > 0 else 0
        
        # Estimate monthly potential if consistent
        avg_expense = total_spent / len(expenses) if expenses else 0
        potential_monthly = (round(avg_expense) - avg_expense) * 30
        
        return {
            'total_roundup': round(total_roundup, 2),
            'savings_rate': round(savings_rate, 2),
            'potential_monthly': round(potential_monthly, 2),
            'expense_count': len(expenses)
        }

    @staticmethod
    def build_emergency_fund_plan(user_id, monthly_income=50000):
        """Build emergency fund strategy (3-6 months of expenses)"""
        expenses = CSVHandler.get_user_expenses(user_id)
        goals = CSVHandler.get_user_goals(user_id)
        
        # Calculate average monthly expense
        if not expenses:
            avg_monthly = monthly_income * 0.7  # Assume 70% spending
        else:
            total_spent = sum(e['amount'] for e in expenses)
            avg_monthly = total_spent / max(1, len(set(e['date'][:7] for e in expenses)))
        
        # Emergency fund targets
        three_month = avg_monthly * 3
        six_month = avg_monthly * 6
        
        # Get current emergency fund goal if exists
        current_emergency = 0
        for goal in goals:
            if 'Emergency' in goal.get('goal_name', ''):
                current_emergency = goal.get('saved_amount', 0)
        
        roundup_savings = CSVHandler.calculate_roundup_savings(user_id)
        monthly_roundup = roundup_savings['total_roundup'] / max(1, roundup_savings['expense_count'])
        
        return {
            'average_monthly_expense': round(avg_monthly, 2),
            'three_month_target': round(three_month, 2),
            'six_month_target': round(six_month, 2),
            'current_emergency_fund': current_emergency,
            'monthly_roundup_contribution': round(monthly_roundup, 2),
            'months_to_three_month': round((three_month - current_emergency) / monthly_roundup) if monthly_roundup > 0 else 0,
            'recommendation': 'Start with 3-month emergency fund, then build to 6 months'
        }

    @staticmethod
    def get_monthly_comparison(user_id):
        """Compare savings month over month"""
        expenses = CSVHandler.get_user_expenses(user_id)
        
        monthly_data = {}
        for exp in expenses:
            month = exp['date'][:7]  # YYYY-MM
            if month not in monthly_data:
                monthly_data[month] = {
                    'total_spent': 0,
                    'total_roundup': 0,
                    'count': 0
                }
            
            amount = exp['amount']
            roundup = round(amount) - amount
            
            monthly_data[month]['total_spent'] += amount
            monthly_data[month]['total_roundup'] += roundup
            monthly_data[month]['count'] += 1
        
        # Sort by month
        sorted_months = sorted(monthly_data.items())
        
        return {
            'months': {month: {
                'total_spent': round(data['total_spent'], 2),
                'total_roundup': round(data['total_roundup'], 2),
                'savings_rate': round(data['total_roundup'] / data['total_spent'] * 100, 2) if data['total_spent'] > 0 else 0
            } for month, data in sorted_months},
            'trend': 'improving' if len(sorted_months) > 1 and sorted_months[-1][1]['total_roundup'] > sorted_months[-2][1]['total_roundup'] else 'stable'
        }

    @staticmethod
    def suggest_auto_savings_targets(user_id):
        """Suggest automatic savings targets"""
        savings_potential = SavingsService.get_savings_potential(user_id)
        emergency_plan = SavingsService.build_emergency_fund_plan(user_id)
        
        monthly_roundup = savings_potential['potential_monthly']
        
        suggestions = {
            'auto_savings': {
                'enabled': True,
                'monthly_target': round(monthly_roundup, 2),
                'annual_savings': round(monthly_roundup * 12, 2)
            },
            'distribution': {
                'emergency_fund': '40%',
                'investments': '40%',
                'personal_goals': '20%'
            },
            'monthly_breakdown': {
                'to_emergency': round(monthly_roundup * 0.4, 2),
                'to_investments': round(monthly_roundup * 0.4, 2),
                'to_goals': round(monthly_roundup * 0.2, 2)
            }
        }
        
        return suggestions
