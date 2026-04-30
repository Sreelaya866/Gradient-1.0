# 🚀 AutoWealth: AI Micro-Investment & Income Growth Engine

**AutoWealth** is an AI-powered financial mobility platform designed to bridge the wealth gap for students, gig workers, and low-income individuals. By turning daily "spare change" into long-term capital and using AI to discover hyper-local earning opportunities, AutoWealth moves users from a payday-to-payday cycle toward sustainable financial growth.

---

## 🌟 Social Impact
*   **Democratizing Investment**: Makes wealth-building accessible to those who feel they "don't have enough to save".
*   **Income Generation**: Uses AI to match user skills with real-world micro-gigs, creating new revenue streams.
*   **Financial Literacy**: Simplifies complex financial jargon into actionable, plain-language insights.
*   **Emergency Security**: Automatically builds a liquid safety net to reduce dependence on high-interest predatory loans.

---

## ✨ Key Features
*   **Smart Round-Ups**: Automatically calculates spare change from `expenses.csv` and redirects it to a virtual wealth pot.
*   **AI Side-Hustle Finder**: A Gemini-powered engine that analyzes user skills to suggest hyper-local, high-probability earning opportunities.
*   **Wealth Projection**: Data-driven visualizations showing the long-term growth potential of small, consistent habits.
*   **Neon Dashboard**: A glassmorphic UI designed in Charcoal Black and Neon Pink for a futuristic, engaging user experience.

---

## 🏗 System Architecture
The platform is built on a modular AI-SaaS architecture:
*   **Frontend**: Next.js with Tailwind CSS (Glassmorphism & Neon Aesthetics).
*   **Backend**: Python Flask/FastAPI for high-performance AI processing and financial logic.
*   **AI Engine**: Google Gemini 1.5 Flash for personalized financial coaching and gig matching.
*   **Database**: CSV-based storage for rapid hackathon deployment and data portability.

---

## 📂 Project Structure
```text
AutoWealth/
├── backend/
│   ├── routes/          # API Endpoints (Auth, Insights, Hustles)
│   ├── services/        # AI Service (Gemini) & Savings Logic
│   └── database/        # CSV Handler (Data Persistence)
├── frontend/
│   ├── templates/       # Glassmorphic HTML layouts
│   └── static/          # Neon Pink styling (CSS) & Interactivity (JS)
├── data/                # CSV Datasets (Expenses, Goals, Users, Investments)
├── app.py               # Main Flask Entry Point
└── requirements.txt     # Dependency List
