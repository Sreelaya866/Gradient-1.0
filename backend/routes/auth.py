"""
Authentication Routes - User login, signup, and session management
"""

from flask import Blueprint, request, jsonify
from backend.database.csv_handler import CSVHandler
import json

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Check if email already exists
        existing = CSVHandler.get_user_by_email(data['email'])
        if existing:
            return jsonify({'success': False, 'error': 'Email already registered'}), 409
        
        # Add user
        user = CSVHandler.add_user(data['name'], data['email'], data['password'])
        
        if not user:
            return jsonify({'success': False, 'error': 'Failed to create user'}), 500
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': user
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login user with email and password"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        # Get user
        user = CSVHandler.get_user_by_email(data['email'])
        
        if not user or user['password'] != data['password']:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        
        # Remove password from response
        user_data = {k: v for k, v in user.items() if k != 'password'}
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user_data,
            'token': f"token_{user['id']}"  # Mock JWT token
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile"""
    try:
        user = CSVHandler.get_user(user_id)
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Remove sensitive data
        user_data = {k: v for k, v in user.items() if k != 'password'}
        
        return jsonify({
            'success': True,
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200

@bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token"""
    try:
        data = request.get_json()
        
        if not data.get('token'):
            return jsonify({'success': False, 'error': 'Token required'}), 400
        
        # Mock verification
        return jsonify({
            'success': True,
            'message': 'Token valid'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
