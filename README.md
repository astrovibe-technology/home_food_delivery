# home_food_delivery

# 🍴 Food Ordering System (FastAPI)

This project is a backend service for a **Food Ordering System** built using FastAPI.

### 🚀 Features
- User Management (Customer, Merchant, Delivery Partner, Admin, Superadmin)
- Menu, Categories, and Addons
- Orders and Payments
- Ratings and Reviews
- Real-time Delivery Tracking

### 🧱 Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL / MySQL
- **ORM:** SQLAlchemy
- **Version Control:** Git + GitHub

### ⚙️ Setup
```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
