"""
AI Service - Mock AI service for personalized recommendations
In production, this would integrate with actual ML models
"""

class AIService:
    """Service for AI-powered recommendations"""

    @staticmethod
    def generate_savings_tips(expenses_summary):
        """Generate personalized savings tips based on spending"""
        tips = []
        categories = expenses_summary.get('categories', {})
        total_spent = expenses_summary.get('total_spent', 0)
        
        # Tip 1: High spending category
        if categories:
            highest_category = max(categories.items(), key=lambda x: x[1])
            category_name = highest_category[0]
            amount = highest_category[1]
            percentage = (amount / total_spent * 100) if total_spent > 0 else 0
            
            if percentage > 30:
                tips.append({
                    'priority': 'High',
                    'category': category_name,
                    'message': f'You spent {percentage:.1f}% on {category_name}. Try reducing by 20% to save ₹{amount * 0.2:.0f}/month',
                    'emoji': '💡'
                })
        
        # Tip 2: Daily average
        if total_spent > 0:
            daily_avg = total_spent / 30
            if daily_avg > 500:
                tips.append({
                    'priority': 'Medium',
                    'message': f'Your daily spending average is ₹{daily_avg:.0f}. Target ₹{daily_avg * 0.8:.0f}/day',
                    'emoji': '📊'
                })
        
        # Tip 3: Round-up potential
        tips.append({
            'priority': 'Low',
            'message': 'Keep using round-up savings - small amounts add up to big sums!',
            'emoji': '🚀'
        })
        
        return tips

    @staticmethod
    def suggest_spending_cuts(expenses_summary, target_cut_percentage=10):
        """Suggest specific spending cuts to reach target"""
        categories = expenses_summary.get('categories', {})
        total_spent = expenses_summary.get('total_spent', 0)
        
        target_savings = total_spent * (target_cut_percentage / 100)
        suggestions = []
        
        # Sort categories by spending
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        
        remaining_target = target_savings
        for category, amount in sorted_categories:
            if remaining_target <= 0:
                break
            
            cut_amount = min(amount * 0.3, remaining_target)  # Cut up to 30% of category
            suggestions.append({
                'category': category,
                'current_spending': round(amount, 2),
                'suggested_cut': round(cut_amount, 2),
                'new_spending': round(amount - cut_amount, 2),
                'percentage_reduction': round((cut_amount / amount * 100), 1)
            })
            
            remaining_target -= cut_amount
        
        total_savings = sum(s['suggested_cut'] for s in suggestions)
        
        return {
            'target_monthly_savings': round(target_savings, 2),
            'achievable_savings': round(total_savings, 2),
            'suggestions': suggestions
        }

    @staticmethod
    def predict_spending_trend(expenses_list):
        """Predict next month's spending based on trend"""
        if len(expenses_list) < 2:
            return {'prediction': 'Not enough data', 'confidence': 0}
        
        # Simple moving average
        recent_spending = sum(e['amount'] for e in expenses_list[-30:])
        previous_spending = sum(e['amount'] for e in expenses_list[-60:-30])
        
        if previous_spending == 0:
            trend = 'increasing'
            percentage = 100
        else:
            change = (recent_spending - previous_spending) / previous_spending
            trend = 'increasing' if change > 0 else 'decreasing'
            percentage = abs(change) * 100
        
        return {
            'next_month_prediction': round(recent_spending, 2),
            'trend': trend,
            'change_percentage': round(percentage, 1),
            'confidence': 0.7
        }

    @staticmethod
    def match_side_hustle(skills=None, time_available=5, risk_tolerance='medium'):
        """Match users with suitable side hustles"""
        all_hustles = [
            {
                'title': 'Freelance Web Development',
                'earnings': '₹1,000 - ₹5,000/project',
                'time': '4-6 hours/week',
                'skills_match': ['coding', 'web-development', 'technical'],
                'difficulty': 'intermediate',
                'ai_score': 95
            },
            {
                'title': 'Content Writing',
                'earnings': '₹500 - ₹2,000/article',
                'time': '5-10 hours/week',
                'skills_match': ['writing', 'communication', 'research'],
                'difficulty': 'beginner',
                'ai_score': 88
            },
            {
                'title': 'Freelance Design',
                'earnings': '₹2,000 - ₹8,000/project',
                'time': '3-5 hours/week',
                'skills_match': ['design', 'creative', 'ui-ux'],
                'difficulty': 'intermediate',
                'ai_score': 92
            },
            {
                'title': 'Online Tutoring',
                'earnings': '₹300 - ₹1,500/hour',
                'time': '10-15 hours/week',
                'skills_match': ['teaching', 'communication', 'patience'],
                'difficulty': 'beginner',
                'ai_score': 85
            },
            {
                'title': 'Stock Photography',
                'earnings': '₹100 - ₹1,000/month/image',
                'time': 'Flexible',
                'skills_match': ['photography', 'visual', 'creative'],
                'difficulty': 'beginner',
                'ai_score': 80
            },
            {
                'title': 'Virtual Assistant',
                'earnings': '₹8,000 - ₹15,000/month',
                'time': '5-10 hours/week',
                'skills_match': ['organization', 'communication', 'admin'],
                'difficulty': 'beginner',
                'ai_score': 82
            }
        ]
        
        # Simple matching algorithm
        recommendations = []
        for hustle in all_hustles:
            score = hustle['ai_score']
            
            # Adjust based on time availability
            if time_available == 'flexible' or time_available >= 10:
                score += 5
            elif time_available < 3:
                score -= 10
            
            recommendations.append({
                **hustle,
                'match_score': score
            })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return recommendations[:5]  # Top 5
