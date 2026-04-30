"""
CSV Data Handler - Database abstraction layer for CSV files
Handles all CSV read/write operations for users, expenses, goals, and investments
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from pathlib import Path
from config.settings import USERS_CSV, EXPENSES_CSV, GOALS_CSV, INVESTMENTS_CSV

class CSVHandler:
    """Handles all CSV file operations"""

    @staticmethod
    def ensure_data_dir():
        """Ensure data directory exists"""
        data_dir = os.path.dirname(USERS_CSV)
        Path(data_dir).mkdir(parents=True, exist_ok=True)

    # ========================================
    # USER OPERATIONS
    # ========================================

    @staticmethod
    def get_all_users():
        """Get all users"""
        try:
            if not os.path.exists(USERS_CSV):
                return []
            df = pd.read_csv(USERS_CSV)
            return df.replace({pd.NA: None}).to_dict('records')
        except Exception as e:
            print(f"Error reading users: {e}")
            return []

    @staticmethod
    def get_user(user_id):
        """Get user by ID"""
        try:
            if not os.path.exists(USERS_CSV):
                return None
            df = pd.read_csv(USERS_CSV)
            user = df[df['id'] == int(user_id)]
            if user.empty:
                return None
            return user.replace({pd.NA: None}).to_dict('records')[0]
        except Exception as e:
            print(f"Error reading user: {e}")
            return None

    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        try:
            if not os.path.exists(USERS_CSV):
                return None
            df = pd.read_csv(USERS_CSV)
            user = df[df['email'] == email]
            if user.empty:
                return None
            return user.replace({pd.NA: None}).to_dict('records')[0]
        except Exception as e:
            print(f"Error reading user: {e}")
            return None

    @staticmethod
    def add_user(name, email, password):
        """Add new user"""
        try:
            CSVHandler.ensure_data_dir()
            
            if os.path.exists(USERS_CSV):
                df = pd.read_csv(USERS_CSV)
                if not df.empty:
                    new_id = int(df['id'].max()) + 1
                else:
                    new_id = 1
            else:
                df = pd.DataFrame(columns=['id', 'name', 'email', 'password'])
                new_id = 1

            new_user = pd.DataFrame({
                'id': [new_id],
                'name': [name],
                'email': [email],
                'password': [password]
            })

            df = pd.concat([df, new_user], ignore_index=True)
            df.to_csv(USERS_CSV, index=False)
            return {'id': int(new_id), 'name': name, 'email': email}
        except Exception as e:
            print(f"Error adding user: {e}")
            return None

    # ========================================
    # EXPENSE OPERATIONS
    # ========================================

    @staticmethod
    def get_user_expenses(user_id):
        """Get all expenses for a user"""
        try:
            if not os.path.exists(EXPENSES_CSV):
                return []
            df = pd.read_csv(EXPENSES_CSV)
            user_expenses = df[df['user_id'] == int(user_id)]
            return user_expenses.replace({pd.NA: None}).to_dict('records')
        except Exception as e:
            print(f"Error reading expenses: {e}")
            return []

    @staticmethod
    def add_expense(user_id, date, category, merchant, amount):
        """Add new expense"""
        try:
            CSVHandler.ensure_data_dir()

            if os.path.exists(EXPENSES_CSV):
                df = pd.read_csv(EXPENSES_CSV)
                if not df.empty and 'expense_id' in df.columns:
                    new_id = int(df['expense_id'].max()) + 1
                else:
                    new_id = 1
            else:
                df = pd.DataFrame(columns=['expense_id', 'user_id', 'date', 'category', 'merchant', 'amount'])
                new_id = 1

            new_expense = pd.DataFrame({
                'expense_id': [new_id],
                'user_id': [int(user_id)],
                'date': [date],
                'category': [category],
                'merchant': [merchant],
                'amount': [float(amount)]
            })

            df = pd.concat([df, new_expense], ignore_index=True)
            df.to_csv(EXPENSES_CSV, index=False)
            
            round_up = float(round(amount) - amount)
            return {
                'expense_id': int(new_id),
                'user_id': int(user_id),
                'amount': float(amount),
                'roundup': round_up
            }
        except Exception as e:
            print(f"Error adding expense: {e}")
            return None

    @staticmethod
    def get_user_expense_summary(user_id):
        """Get expense summary for a user"""
        try:
            expenses = CSVHandler.get_user_expenses(user_id)
            if not expenses:
                return {'total_spent': 0, 'categories': {}, 'expense_count': 0, 'average_expense': 0}

            total_spent = float(sum(e['amount'] for e in expenses))
            
            # Group by category
            categories = {}
            for expense in expenses:
                cat = expense['category']
                categories[cat] = float(categories.get(cat, 0) + expense['amount'])

            return {
                'total_spent': total_spent,
                'categories': categories,
                'expense_count': len(expenses),
                'average_expense': float(total_spent / len(expenses)) if expenses else 0
            }
        except Exception as e:
            print(f"Error calculating summary: {e}")
            return None

    # ========================================
    # SAVINGS OPERATIONS
    # ========================================

    @staticmethod
    def calculate_roundup_savings(user_id):
        """Calculate total round-up savings"""
        try:
            expenses = CSVHandler.get_user_expenses(user_id)
            total_roundup = float(sum(round(e['amount']) - e['amount'] for e in expenses))
            return {'total_roundup': total_roundup, 'expense_count': len(expenses)}
        except Exception as e:
            print(f"Error calculating roundup: {e}")
            return None

    # ========================================
    # GOALS OPERATIONS
    # ========================================

    @staticmethod
    def get_user_goals(user_id):
        """Get all goals for a user"""
        try:
            if not os.path.exists(GOALS_CSV):
                return []
            df = pd.read_csv(GOALS_CSV)
            user_goals = df[df['user_id'] == int(user_id)]
            return user_goals.replace({pd.NA: None}).to_dict('records')
        except Exception as e:
            print(f"Error reading goals: {e}")
            return []

    @staticmethod
    def add_goal(user_id, goal_name, target_amount, deadline):
        """Add new savings goal"""
        try:
            CSVHandler.ensure_data_dir()

            if os.path.exists(GOALS_CSV):
                df = pd.read_csv(GOALS_CSV)
                if not df.empty and 'goal_id' in df.columns:
                    new_id = int(df['goal_id'].max()) + 1
                else:
                    new_id = 1
            else:
                df = pd.DataFrame(columns=['goal_id', 'user_id', 'goal_name', 'target_amount', 'saved_amount', 'deadline'])
                new_id = 1

            new_goal = pd.DataFrame({
                'goal_id': [new_id],
                'user_id': [int(user_id)],
                'goal_name': [goal_name],
                'target_amount': [float(target_amount)],
                'saved_amount': [0.0],
                'deadline': [deadline]
            })

            df = pd.concat([df, new_goal], ignore_index=True)
            df.to_csv(GOALS_CSV, index=False)
            
            return {
                'goal_id': int(new_id),
                'user_id': int(user_id),
                'goal_name': goal_name,
                'target_amount': float(target_amount),
                'saved_amount': 0.0
            }
        except Exception as e:
            print(f"Error adding goal: {e}")
            return None

    @staticmethod
    def get_goal_progress(user_id):
        """Get overall goal progress"""
        try:
            goals = CSVHandler.get_user_goals(user_id)
            if not goals:
                return {'total_goals': 0, 'total_saved': 0, 'total_target': 0, 'overall_progress': 0}

            total_saved = float(sum(g['saved_amount'] for g in goals))
            total_target = float(sum(g['target_amount'] for g in goals))
            progress = (total_saved / total_target * 100) if total_target > 0 else 0

            return {
                'total_goals': len(goals),
                'total_saved': total_saved,
                'total_target': total_target,
                'overall_progress': round(float(progress), 2)
            }
        except Exception as e:
            print(f"Error calculating progress: {e}")
            return None

    # ========================================
    # INVESTMENT OPERATIONS
    # ========================================

    @staticmethod
    def get_user_investments(user_id):
        """Get all investments for a user"""
        try:
            if not os.path.exists(INVESTMENTS_CSV):
                return []
            df = pd.read_csv(INVESTMENTS_CSV)
            user_investments = df[df['user_id'] == int(user_id)]
            return user_investments.replace({pd.NA: None}).to_dict('records')
        except Exception as e:
            print(f"Error reading investments: {e}")
            return []

    @staticmethod
    def get_investment_portfolio(user_id):
        """Get investment portfolio summary"""
        try:
            investments = CSVHandler.get_user_investments(user_id)
            if not investments:
                return {
                    'total_invested': 0.0,
                    'by_type': {},
                    'potential_returns': 0.0
                }

            total_invested = float(sum(inv['amount_invested'] for inv in investments))
            
            # Group by type
            by_type = {}
            for inv in investments:
                inv_type = inv['type']
                if inv_type not in by_type:
                    by_type[inv_type] = {'amount': 0.0, 'count': 0}
                by_type[inv_type]['amount'] = float(by_type[inv_type]['amount'] + inv['amount_invested'])
                by_type[inv_type]['count'] += 1

            # Calculate potential returns
            potential_returns = 0.0
            for inv in investments:
                try:
                    ret_str = str(inv['avg_return']).rstrip('%')
                    potential_returns += float(inv['amount_invested']) * (float(ret_str) / 100)
                except:
                    continue

            return {
                'total_invested': total_invested,
                'by_type': by_type,
                'potential_returns': float(potential_returns),
                'investment_count': len(investments)
            }
        except Exception as e:
            print(f"Error calculating portfolio: {e}")
            return None

    @staticmethod
    def recommend_investment(user_id, type_, name, risk_level, amount):
        """Recommend or add investment"""
        try:
            CSVHandler.ensure_data_dir()

            if os.path.exists(INVESTMENTS_CSV):
                df = pd.read_csv(INVESTMENTS_CSV)
                if not df.empty and 'investment_id' in df.columns:
                    new_id = int(df['investment_id'].max()) + 1
                else:
                    new_id = 1
            else:
                df = pd.DataFrame(columns=['investment_id', 'user_id', 'type', 'name', 'risk_level', 'amount_invested', 'avg_return'])
                new_id = 1

            return_map = {'Low': 9, 'Medium': 12, 'High': 15}
            avg_return = return_map.get(risk_level, 10)

            new_investment = pd.DataFrame({
                'investment_id': [new_id],
                'user_id': [int(user_id)],
                'type': [type_],
                'name': [name],
                'risk_level': [risk_level],
                'amount_invested': [float(amount)],
                'avg_return': [f'{avg_return}%']
            })

            df = pd.concat([df, new_investment], ignore_index=True)
            df.to_csv(INVESTMENTS_CSV, index=False)
            
            return {
                'investment_id': int(new_id),
                'type': type_,
                'name': name,
                'amount': float(amount),
                'avg_return': f'{avg_return}%'
            }
        except Exception as e:
            print(f"Error recommending investment: {e}")
            return None
