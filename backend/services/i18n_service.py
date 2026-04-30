"""
i18n Service - Internationalization and local language support
Provides translations for common phrases and tips
"""

class I18nService:
    """Service for handling multiple languages"""

    TRANSLATIONS = {
        'en': {
            'greeting_morning': 'Good morning! Here\'s your financial snapshot for today.',
            'greeting_afternoon': 'Good afternoon! Keep tracking your progress.',
            'greeting_evening': 'Good evening! Review your daily spending and goals.',
            'total_spent': 'Total Spent',
            'roundup_saved': 'Round-up Saved',
            'active_goals': 'Active Goals',
            'investment_portfolio': 'Investment Portfolio',
            'emergency_fund': 'Emergency Fund',
            'hustle_tip': 'Tip: You can earn up to ₹{} more this week with side hustles!',
            'saving_badge': 'Savings Streak: {} days! 🚀'
        },
        'hi': {  # Hindi
            'greeting_morning': 'शुभ प्रभात! आज का आपका वित्तीय विवरण यहाँ है।',
            'greeting_afternoon': 'शुभ दोपहर! अपनी प्रगति पर नज़र रखते रहें।',
            'greeting_evening': 'शुभ संध्या! अपने दैनिक खर्च और लक्ष्यों की समीक्षा करें।',
            'total_spent': 'कुल खर्च',
            'roundup_saved': 'राउंड-अप बचत',
            'active_goals': 'सक्रिय लक्ष्य',
            'investment_portfolio': 'निवेश पोर्टफोलियो',
            'emergency_fund': 'आपातकालीन निधि',
            'hustle_tip': 'सुझाव: आप इस सप्ताह साइड हसल के साथ ₹{} तक अधिक कमा सकते हैं!',
            'saving_badge': 'बचत सिलसिला: {} दिन! 🚀'
        },
        'ml': {  # Malayalam
            'greeting_morning': 'സുപ്രഭാതം! ഇന്നത്തെ നിങ്ങളുടെ സാമ്പത്തിക ചിത്രം ഇതാ.',
            'greeting_afternoon': 'ശുഭ ഉച്ചതിരിഞ്ഞ്! നിങ്ങളുടെ പുരോഗതി ട്രാക്ക് ചെയ്യുന്നത് തുടരുക.',
            'greeting_evening': 'ശുഭ സായാഹ്നം! നിങ്ങളുടെ ദൈനംദിന ചിലവുകളും ലക്ഷ്യങ്ങളും അവലോകനം ചെയ്യുക.',
            'total_spent': 'ആകെ ചിലവ്',
            'roundup_saved': 'റൗണ്ട്-അപ്പ് സേവിംഗ്സ്',
            'active_goals': 'സജീവ ലക്ഷ്യങ്ങൾ',
            'investment_portfolio': 'ഇൻവെസ്റ്റ്‌മെന്റ് പോർട്ട്‌ഫോളിയോ',
            'emergency_fund': 'അടിയന്തര ഫണ്ട്',
            'hustle_tip': 'അറിവ്: സൈഡ് ഹസിലുകളിലൂടെ ഈ ആഴ്ച നിങ്ങൾക്ക് ₹{} വരെ കൂടുതൽ നേടാം!',
            'saving_badge': 'സേവിംഗ്സ് സ്ട്രീക്ക്: {} ദിവസങ്ങൾ! 🚀'
        },
        'ta': {  # Tamil
            'greeting_morning': 'காலை வணக்கம்! இன்றைய உங்கள் நிதி நிலவரம் இதோ.',
            'greeting_afternoon': 'மதிய வணக்கம்! உங்கள் முன்னேற்றத்தைத் தொடர்ந்து கண்காணியுங்கள்.',
            'greeting_evening': 'மாலை வணக்கம்! உங்கள் தினசரி செலவுகள் மற்றும் இலக்குகளை மதிப்பாய்வு செய்யுங்கள்.',
            'total_spent': 'மொத்த செலவு',
            'roundup_saved': 'ரவுண்ட்-அப் சேமிப்பு',
            'active_goals': 'செயலில் உள்ள இலக்குகள்',
            'investment_portfolio': 'முதலீட்டு தொகுப்பு',
            'emergency_fund': 'அவசர கால நிதி',
            'hustle_tip': 'குறிப்பு: இந்த வாரம் சைடு ஹசல்கள் மூலம் ₹{} வரை கூடுதலாக சம்பாதிக்கலாம்!',
            'saving_badge': 'சேமிப்புத் தொடர்: {} நாட்கள்! 🚀'
        }
    }

    @staticmethod
    def get_translation(lang, key, *args):
        """Get translated text for a key"""
        lang_dict = I18nService.TRANSLATIONS.get(lang, I18nService.TRANSLATIONS['en'])
        text = lang_dict.get(key, I18nService.TRANSLATIONS['en'].get(key, key))
        
        if args:
            return text.format(*args)
        return text

    @staticmethod
    def get_all_keys(lang):
        """Get all translations for a language"""
        return I18nService.TRANSLATIONS.get(lang, I18nService.TRANSLATIONS['en'])

    @staticmethod
    def get_supported_languages():
        """Get list of supported languages"""
        return [
            {'code': 'en', 'name': 'English'},
            {'code': 'hi', 'name': 'Hindi (हिन्दी)'},
            {'code': 'ml', 'name': 'Malayalam (മലയാളം)'},
            {'code': 'ta', 'name': 'Tamil (தமிழ்)'}
        ]
