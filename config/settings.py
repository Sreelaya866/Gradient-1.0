"""
AutoWealth Backend - Configuration Settings
Loads all configuration from environment variables
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'production'
    SECRET_KEY = os.getenv('SECRET_KEY')  # Must be set in production

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Database paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
USERS_CSV = os.path.join(DATA_DIR, 'users.csv')
EXPENSES_CSV = os.path.join(DATA_DIR, 'expenses.csv')
GOALS_CSV = os.path.join(DATA_DIR, 'goals.csv')
INVESTMENTS_CSV = os.path.join(DATA_DIR, 'investments.csv')

# API Configuration
API_PREFIX = '/api'
API_VERSION = 'v1'

# Get config based on environment
ENV = os.getenv('FLASK_ENV', 'development')
if ENV == 'production':
    config = ProductionConfig()
elif ENV == 'testing':
    config = TestingConfig()
else:
    config = DevelopmentConfig()
