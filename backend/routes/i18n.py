"""
i18n Routes - Local language support endpoints
"""

from flask import Blueprint, request, jsonify
from backend.services.i18n_service import I18nService

bp = Blueprint('i18n', __name__, url_prefix='/api/i18n')

@bp.route('/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    return jsonify({
        'success': True,
        'languages': I18nService.get_supported_languages()
    }), 200

@bp.route('/translations', methods=['GET'])
def get_translations():
    """Get all translations for a language"""
    lang = request.args.get('lang', default='en')
    translations = I18nService.get_all_keys(lang)
    
    return jsonify({
        'success': True,
        'language': lang,
        'translations': translations
    }), 200

@bp.route('/translate', methods=['POST'])
def translate_key():
    """Translate a specific key"""
    data = request.get_json()
    lang = data.get('lang', 'en')
    key = data.get('key')
    params = data.get('params', [])
    
    if not key:
        return jsonify({'success': False, 'error': 'Key required'}), 400
        
    translation = I18nService.get_translation(lang, key, *params)
    
    return jsonify({
        'success': True,
        'translation': translation
    }), 200
