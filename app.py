"""
AutoWealth Backend - Main Application Entry Point
A Flask-based micro-investment platform backend
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app with custom template and static folders
app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# Import routes
from backend.routes import auth, expenses, savings, insights, side_hustles, i18n, alerts

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(expenses.bp)
app.register_blueprint(savings.bp)
app.register_blueprint(insights.bp)
app.register_blueprint(side_hustles.bp)
app.register_blueprint(i18n.bp)
app.register_blueprint(alerts.bp)

# Frontend Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/goals')
def goals():
    return render_template('goals.html')

@app.route('/side-hustles')
def side_hustles_page():
    return render_template('side_hustles.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Resource not found',
        'message': str(error)
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 'Bad request',
        'message': str(error)
    }), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'AutoWealth API'
    }), 200

# Root endpoint
@app.route('/api', methods=['GET'])
def root():
    return jsonify({
        'success': True,
        'name': 'AutoWealth API',
        'version': '1.0.0',
        'description': 'AI Micro-Investment & Income Growth Engine',
        'endpoints': {
            'auth': '/api/auth',
            'expenses': '/api/expenses',
            'savings': '/api/savings',
            'insights': '/api/insights',
            'side_hustles': '/api/side-hustles'
        }
    }), 200

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, port=port, host='0.0.0.0')
