"""
Investment Service - Business logic for investment recommendations and portfolio management
"""

from backend.database.csv_handler import CSVHandler

class InvestmentService:
    """Service for handling investment operations"""

    # Investment templates by risk level
    INVESTMENT_OPTIONS = {
        'Low': [
            {'name': 'Fixed Deposit', 'type': 'Fixed Deposit', 'return': 7, 'description': 'Safe, guaranteed returns'},
            {'name': 'Govt Bonds', 'type': 'Bonds', 'return': 6, 'description': 'Government-backed securities'},
            {'name': 'Index ETF', 'type': 'ETF', 'return': 9, 'description': 'Market-linked low-cost investing'}
        ],
        'Medium': [
            {'name': 'Balanced Mutual Fund', 'type': 'Mutual Fund', 'return': 12, 'description': '50-50 equity-debt'},
            {'name': 'Digital Gold', 'type': 'Gold', 'return': 8, 'description': 'Tangible asset with value'},
            {'name': 'Corporate Bonds', 'type': 'Bonds', 'return': 10, 'description': 'Higher returns, moderate risk'}
        ],
        'High': [
            {'name': 'Growth Mutual Fund', 'type': 'Mutual Fund', 'return': 15, 'description': 'High growth potential'},
            {'name': 'Stock Portfolio', 'type': 'Stocks', 'return': 18, 'description': 'Individual company stocks'},
            {'name': 'Cryptocurrency', 'type': 'Crypto', 'return': 20, 'description': 'High volatility, high potential'}
        ]
    }

    @staticmethod
    def get_portfolio(user_id):
        """Get user's investment portfolio"""
        portfolio = CSVHandler.get_investment_portfolio(user_id)
        return portfolio

    @staticmethod
    def recommend_investments(user_id, risk_profile='Medium', budget=5000):
        """Get investment recommendations based on risk profile"""
        options = InvestmentService.INVESTMENT_OPTIONS.get(risk_profile, 
                                                           InvestmentService.INVESTMENT_OPTIONS['Medium'])
        
        recommendations = []
        per_investment = budget / len(options)
        
        for i, option in enumerate(options):
            recommendations.append({
                'rank': i + 1,
                'name': option['name'],
                'type': option['type'],
                'suggested_amount': round(per_investment, 2),
                'expected_return': option['return'],
                'expected_annual_return': round(per_investment * (option['return'] / 100), 2),
                'description': option['description'],
                'risk_level': risk_profile
            })
        
        return {
            'risk_profile': risk_profile,
            'total_budget': budget,
            'recommendations': recommendations
        }

    @staticmethod
    def calculate_investment_returns(user_id):
        """Calculate potential returns from investments"""
        investments = CSVHandler.get_user_investments(user_id)
        
        if not investments:
            return {
                'total_invested': 0,
                'estimated_returns': 0,
                'annual_dividend': 0,
                'roi_percentage': 0
            }
        
        total_invested = sum(inv['amount_invested'] for inv in investments)
        
        # Parse return percentages
        estimated_returns = 0
        for inv in investments:
            try:
                return_pct = float(inv['avg_return'].rstrip('%')) / 100
                estimated_returns += inv['amount_invested'] * return_pct
            except:
                continue
        
        return {
            'total_invested': round(total_invested, 2),
            'estimated_annual_returns': round(estimated_returns, 2),
            'roi_percentage': round((estimated_returns / total_invested * 100), 2) if total_invested > 0 else 0,
            'investment_count': len(investments)
        }

    @staticmethod
    def create_investment_plan(user_id, monthly_savings=1000, duration_months=12, risk_profile='Medium'):
        """Create a long-term investment plan"""
        recommendations = InvestmentService.recommend_investments(user_id, risk_profile, monthly_savings)
        
        total_investment = monthly_savings * duration_months
        
        # Calculate projected returns based on risk profile
        return_rates = {
            'Low': 0.08,
            'Medium': 0.12,
            'High': 0.18
        }
        
        annual_return = return_rates.get(risk_profile, 0.12)
        projected_value = total_investment * (1 + annual_return) ** (duration_months / 12)
        projected_gains = projected_value - total_investment
        
        return {
            'plan_duration': f'{duration_months} months',
            'monthly_investment': monthly_savings,
            'total_investment': total_investment,
            'risk_profile': risk_profile,
            'expected_annual_return': f'{annual_return * 100}%',
            'projected_final_value': round(projected_value, 2),
            'projected_gains': round(projected_gains, 2),
            'recommendations': recommendations['recommendations']
        }

    @staticmethod
    def get_diversification_analysis(user_id):
        """Analyze portfolio diversification"""
        portfolio = CSVHandler.get_investment_portfolio(user_id)
        by_type = portfolio.get('by_type', {})
        total_invested = portfolio.get('total_invested', 0)
        
        if total_invested == 0:
            return {
                'total_invested': 0,
                'diversification': {},
                'recommendation': 'Start investing to build a diversified portfolio'
            }
        
        diversification = {}
        for inv_type, data in by_type.items():
            percentage = (data['amount'] / total_invested * 100)
            diversification[inv_type] = {
                'amount': round(data['amount'], 2),
                'percentage': round(percentage, 2),
                'count': data['count']
            }
        
        # Check if well-diversified (no single type > 50%)
        max_percentage = max([d['percentage'] for d in diversification.values()])
        is_diversified = max_percentage <= 50 and len(diversification) >= 3
        
        return {
            'total_invested': round(total_invested, 2),
            'diversification': diversification,
            'diversification_score': round(100 - max_percentage, 2),
            'is_well_diversified': is_diversified,
            'recommendation': 'Your portfolio is well-diversified' if is_diversified else 'Consider diversifying across more investment types'
        }
