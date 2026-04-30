# AutoWealth Backend

A comprehensive Flask backend for the AutoWealth micro-investment and income growth platform.

## Features

- **User Authentication** - Signup, login, and session management
- **Expense Tracking** - Add, categorize, and analyze expenses with round-up savings
- **Savings Goals** - Create and track financial goals
- **Investment Recommendations** - AI-powered investment suggestions based on risk profile
- **AI Insights** - Personalized savings tips, spending analysis, and financial forecasting
- **Side Hustle Matcher** - Discover income opportunities matched to your skills
- **CSV Data Management** - Leverage existing CSV files for data storage

## Project Structure

```
backend/
├── database/
│   └── csv_handler.py       # CSV read/write operations
├── routes/
│   ├── auth.py             # Authentication endpoints
│   ├── expenses.py         # Expense tracking endpoints
│   ├── savings.py          # Savings goals endpoints
│   ├── insights.py         # AI insights endpoints
│   └── side_hustles.py     # Side hustle endpoints
├── services/
│   ├── expense_service.py  # Expense business logic
│   ├── savings_service.py  # Savings business logic
│   ├── investment_service.py # Investment recommendations
│   ├── ai_service.py       # AI/ML logic
│   └── hustle_service.py   # Side hustle recommendations
config/
├── settings.py             # Configuration management
app.py                       # Flask application entry point
requirements.txt            # Python dependencies
.env.example               # Environment variables template
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env .env.local
# Edit .env.local with your settings
```

3. **Create data directory:**
```bash
mkdir -p data
# Copy CSV files to data/ directory
```

## Running the Server

### Development Mode

```bash
python app.py
```

Server will start on `http://localhost:5000`

### Production Mode

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication Endpoints

#### Register User
```
POST /api/auth/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure_password"
}

Response:
{
  "success": true,
  "message": "Login successful",
  "user": { ... },
  "token": "token_1"
}
```

### Expense Endpoints

#### Get All Expenses
```
GET /api/expenses?user_id=1
```

#### Add Expense
```
POST /api/expenses/add
Content-Type: application/json

{
  "user_id": 1,
  "date": "2024-01-15",
  "category": "Food",
  "merchant": "Restaurant ABC",
  "amount": 450.50
}
```

#### Get Expense Summary
```
GET /api/expenses/summary?user_id=1
```

#### Get Expenses by Category
```
GET /api/expenses/by-category?user_id=1
```

### Savings Endpoints

#### Get Round-up Savings Total
```
GET /api/savings/roundup-total?user_id=1
```

#### Get Emergency Fund Plan
```
GET /api/savings/emergency-fund-plan?user_id=1&monthly_income=50000
```

#### Get All Goals
```
GET /api/savings/goals?user_id=1
```

#### Create Goal
```
POST /api/savings/goals/add
Content-Type: application/json

{
  "user_id": 1,
  "goal_name": "Laptop Fund",
  "target_amount": 75000,
  "deadline": "2025-12-31"
}
```

### Insights Endpoints

#### Get Savings Tips
```
GET /api/insights/savings-tips?user_id=1
```

#### Get Investment Recommendations
```
GET /api/insights/investment-recommendations?user_id=1&risk_profile=Medium&budget=5000
```

#### Get Portfolio Analysis
```
GET /api/insights/portfolio-analysis?user_id=1
```

### Side Hustles Endpoints

#### Get All Hustles
```
GET /api/side-hustles
```

#### Search Hustles
```
GET /api/side-hustles/search?q=web+development
```

#### Filter Hustles
```
GET /api/side-hustles/filter?difficulty=intermediate&max_time=10
```

#### Get AI Recommendations
```
GET /api/side-hustles/recommendations?user_id=1
```

#### Get Earning Potential
```
GET /api/side-hustles/earning-potential?hours_per_week=10
```

## Database (CSV Files)

The backend uses CSV files for data storage:

- `users.csv` - User accounts and profiles
- `expenses.csv` - Transaction history
- `goals.csv` - Savings goals
- `investments.csv` - Investment portfolio

## Services Architecture

### Expense Service
- Add and retrieve expenses
- Calculate round-up savings
- Analyze spending by category
- Budget tracking
- Date range queries

### Savings Service
- Track round-up savings
- Emergency fund planning
- Monthly savings comparison
- Auto-savings distribution

### Investment Service
- Investment recommendations
- Portfolio analysis
- Diversification checking
- Returns calculation

### AI Service
- Personalized savings tips
- Spending cut suggestions
- Trend prediction
- Side hustle matching

### Hustle Service
- Opportunity catalog
- Search and filtering
- Earning potential calculation
- Success guides

## Error Handling

All responses follow this format:

**Success Response:**
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message",
  "message": "Detailed error description"
}
```

## Testing Endpoints

Use the following test credentials:

```
Email: aisha.yadav1@gmail.com
Password: pass001
```

Or signup with new credentials through the `/api/auth/signup` endpoint.

## Future Enhancements

- [ ] JWT token authentication
- [ ] Rate limiting
- [ ] Logging and monitoring
- [ ] Real database (PostgreSQL)
- [ ] WebSocket for real-time updates
- [ ] Payment gateway integration
- [ ] Advanced analytics
- [ ] Machine learning models

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Submit a pull request

## License

MIT License

## Support

For issues and support, please contact: support@autowealth.io
