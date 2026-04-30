"""
Hustle Service - Business logic for side hustle recommendations
"""

from backend.services.ai_service import AIService

class HustleService:
    """Service for side hustle operations"""

    HUSTLES = [
        {
            'id': 1,
            'title': 'Freelance Web Development',
            'description': 'Build websites and apps for clients on platforms like Upwork, Fiverr, or Toptal.',
            'earnings': '₹1,000 - ₹5,000/project',
            'time_commitment': '4-6 hours/week',
            'difficulty': 'intermediate',
            'skills': ['HTML/CSS', 'JavaScript', 'React', 'Python'],
            'platforms': ['Fiverr', 'Upwork', 'Toptal'],
            'ai_match': 95
        },
        {
            'id': 2,
            'title': 'Content Writing & Blogging',
            'description': 'Write articles, blog posts, and web content for websites and publications.',
            'earnings': '₹500 - ₹2,000/article',
            'time_commitment': '5-10 hours/week',
            'difficulty': 'beginner',
            'skills': ['Writing', 'SEO', 'Research', 'Communication'],
            'platforms': ['Medium', 'Hacker News', 'LinkedIn'],
            'ai_match': 88
        },
        {
            'id': 3,
            'title': 'Graphic Design & UI/UX',
            'description': 'Create designs for brands on Fiverr, 99designs, or design-specific platforms.',
            'earnings': '₹2,000 - ₹8,000/project',
            'time_commitment': '3-5 hours/week',
            'difficulty': 'intermediate',
            'skills': ['Adobe CC', 'Figma', 'UI Design', 'Branding'],
            'platforms': ['Fiverr', '99designs', 'Dribbble'],
            'ai_match': 92
        },
        {
            'id': 4,
            'title': 'Online Tutoring & Teaching',
            'description': 'Teach languages, academics, or skills on platforms like Chegg Tutors or VIPKid.',
            'earnings': '₹300 - ₹1,500/hour',
            'time_commitment': '10-15 hours/week',
            'difficulty': 'beginner',
            'skills': ['Teaching', 'English', 'Math', 'Subject Knowledge'],
            'platforms': ['Chegg', 'VIPKid', 'Tutor.com'],
            'ai_match': 85
        },
        {
            'id': 5,
            'title': 'Stock Photography & Videos',
            'description': 'Sell your photos and videos on Shutterstock, Getty Images, or Adobe Stock.',
            'earnings': '₹100 - ₹1,000/month/image',
            'time_commitment': 'Flexible',
            'difficulty': 'beginner',
            'skills': ['Photography', 'Videography', 'Creative Eye'],
            'platforms': ['Shutterstock', 'Getty Images', 'Adobe Stock'],
            'ai_match': 80
        },
        {
            'id': 6,
            'title': 'Virtual Assistant / Admin',
            'description': 'Help entrepreneurs with administrative tasks and travel planning.',
            'earnings': '₹8,000 - ₹15,000/month',
            'time_commitment': '5-10 hours/week',
            'difficulty': 'beginner',
            'skills': ['Organization', 'Communication', 'Admin', 'Time Management'],
            'platforms': ['Belay', 'Time Etc', 'Fancy Hands'],
            'ai_match': 82
        },
        {
            'id': 7,
            'title': 'E-commerce & Dropshipping',
            'description': 'Set up online stores and sell products without holding inventory.',
            'earnings': '₹5,000 - ₹50,000/month',
            'time_commitment': '8-12 hours/week',
            'difficulty': 'advanced',
            'skills': ['Marketing', 'Sales', 'Business Acumen', 'Customer Service'],
            'platforms': ['Shopify', 'Amazon', 'Etsy'],
            'ai_match': 75
        },
        {
            'id': 8,
            'title': 'Podcast & YouTube Content',
            'description': 'Create content and earn through ads, sponsorships, and memberships.',
            'earnings': '₹500 - ₹10,000/month',
            'time_commitment': '10-15 hours/week',
            'difficulty': 'intermediate',
            'skills': ['Audio Production', 'Video Editing', 'Content Creation', 'Editing'],
            'platforms': ['YouTube', 'Spotify', 'Anchor'],
            'ai_match': 78
        }
    ]

    @staticmethod
    def get_all_hustles():
        """Get all available hustles"""
        return HustleService.HUSTLES

    @staticmethod
    def get_hustle_by_id(hustle_id):
        """Get specific hustle details"""
        for hustle in HustleService.HUSTLES:
            if hustle['id'] == hustle_id:
                return hustle
        return None

    @staticmethod
    def get_top_hustles(limit=5):
        """Get top rated hustles"""
        sorted_hustles = sorted(HustleService.HUSTLES, key=lambda x: x['ai_match'], reverse=True)
        return sorted_hustles[:limit]

    @staticmethod
    def search_hustles(query):
        """Search hustles by title or skills"""
        query = query.lower()
        results = []
        
        for hustle in HustleService.HUSTLES:
            if (query in hustle['title'].lower() or
                query in hustle['description'].lower() or
                any(query in skill.lower() for skill in hustle['skills'])):
                results.append(hustle)
        
        return results

    @staticmethod
    def filter_hustles(difficulty=None, max_time=None, min_earnings=None):
        """Filter hustles by criteria"""
        results = HustleService.HUSTLES.copy()
        
        if difficulty:
            results = [h for h in results if h['difficulty'] == difficulty]
        
        if max_time:
            time_map = {'flexible': 999, '3-5': 5, '4-6': 6, '5-10': 10, '10-15': 15, '8-12': 12}
            results = [h for h in results if any(
                time_map.get(t.split('-')[0], 999) <= max_time 
                for t in h['time_commitment'].split()
            )]
        
        return results

    @staticmethod
    def get_hustle_recommendations(user_id):
        """Get AI-matched hustle recommendations"""
        # Use AI service to match
        matches = AIService.match_side_hustle()
        
        enriched_matches = []
        for match in matches:
            # Find matching hustle
            hustle = next((h for h in HustleService.HUSTLES if h['title'] == match['title']), None)
            if hustle:
                enriched_matches.append({
                    **hustle,
                    'ai_match': match['match_score']
                })
        
        return enriched_matches

    @staticmethod
    def get_earning_potential_by_time(time_hours_per_week):
        """Calculate potential earnings based on time commitment"""
        potential = {
            'by_hustle': [],
            'total_potential_low': 0,
            'total_potential_high': 0
        }
        
        for hustle in HustleService.HUSTLES:
            # Extract min and max from earnings string
            earnings_str = hustle['earnings']
            
            # Simple parsing (in production, use regex)
            if '₹' in earnings_str:
                try:
                    parts = earnings_str.split('₹')[1].split('-')
                    min_val = int(parts[0].strip().split('/')[0].replace(',', ''))
                    max_val = int(parts[1].split('/')[0].replace(',', ''))
                    
                    # Estimate weekly
                    if 'hour' in earnings_str:
                        min_weekly = min_val * time_hours_per_week
                        max_weekly = max_val * time_hours_per_week
                    elif 'week' in earnings_str:
                        min_weekly = min_val
                        max_weekly = max_val
                    else:
                        min_weekly = min_val / 4
                        max_weekly = max_val / 4
                    
                    potential['by_hustle'].append({
                        'title': hustle['title'],
                        'weekly_min': round(min_weekly, 0),
                        'weekly_max': round(max_weekly, 0),
                        'monthly_min': round(min_weekly * 4.33, 0),
                        'monthly_max': round(max_weekly * 4.33, 0),
                        'annual_min': round(min_weekly * 52, 0),
                        'annual_max': round(max_weekly * 52, 0)
                    })
                    
                    potential['total_potential_low'] += min_weekly
                    potential['total_potential_high'] += max_weekly
                except:
                    continue
        
        potential['total_potential_low'] = round(potential['total_potential_low'], 0)
        potential['total_potential_high'] = round(potential['total_potential_high'], 0)
        
        return potential

    @staticmethod
    def get_hustle_success_guide(hustle_id):
        """Get success guide for specific hustle"""
        hustle = HustleService.get_hustle_by_id(hustle_id)
        if not hustle:
            return None
        
        guides = {
            1: {  # Web Development
                'steps': [
                    'Build a strong portfolio with 3-5 projects',
                    'Start on Fiverr with competitive pricing',
                    'Get first 5 positive reviews',
                    'Increase prices and move to higher-value platforms',
                    'Build recurring clients for stable income'
                ],
                'tips': [
                    'Learn latest frameworks (React, Vue)',
                    'Focus on responsive design',
                    'Quick turnaround time boosts ratings',
                    'Offer free consultation calls'
                ]
            },
            2: {  # Content Writing
                'steps': [
                    'Start with Medium or personal blog',
                    'Write 10 quality articles',
                    'Apply to writing platforms',
                    'Build client relationships',
                    'Pitch to publications'
                ],
                'tips': [
                    'Research thoroughly before writing',
                    'Focus on SEO optimization',
                    'Engage with readers',
                    'Build email list'
                ]
            }
        }
        
        return {
            'hustle': hustle,
            'guide': guides.get(hustle_id, {'steps': [], 'tips': []}),
            'time_to_first_earning': '1-2 weeks',
            'time_to_consistent_income': '2-3 months'
        }
