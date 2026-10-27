# Farmer Plants — Django Marketplace

A beginner-friendly demonstration project with three main pages:
1. Business homepage (`/`)
2. Import / Export enquiry page (`/trade/`)
3. Farmer stock marketplace (`/marketplace/`)

Built with Python, Django, HTML, CSS and SQLite.

## Requirements
- Python 3.10+
- pip

## Setup (Windows PowerShell)

```powershell
# 1. Extract the ZIP and open the project folder in VS Code
cd farmer_plants_project

# 2. Create a virtual environment
py -m venv venv

# 3. Activate it
.\venv\Scripts\Activate.ps1

# If PowerShell blocks activation, use Command Prompt:
# venv\Scripts\activate.bat

# 4. Install Django
python -m pip install -r requirements.txt

# 5. Create the database tables
python manage.py makemigrations marketplace
python manage.py migrate

# 6. Create an admin login
python manage.py createsuperuser

# 7. Start the website
python manage.py runserver
```

Open:
- Business page: http://127.0.0.1:8000/
- Import / Export: http://127.0.0.1:8000/trade/
- Farmer Stock: http://127.0.0.1:8000/marketplace/
- Admin: http://127.0.0.1:8000/admin/

## Add sample products
Log in to `/admin/`, select Products, and add records. Example:
- Name: Mango
- Category: Fruit
- Description: Fresh seasonal mangoes
- Price: 120.00
- Quantity: 25
- Unit: kg
- Farmer name: Ravi Farms
- Location: Chengalpattu
- Is available: checked

Add more products such as Banana, Tomato, Onion, Potato and Spinach.

## Features
- Products stored in SQLite
- Search by product, farmer or location
- Filter by Fruit or Vegetable
- Trade enquiries saved to the database
- Orders saved to the database
- Stock quantity decreases after a successful order
- Django Admin for products, orders and enquiries
- CSRF protection on POST forms

## Important notes
- This is a demo project; it does not take payments or send real emails.
- `DEBUG = True` and the development secret key are for local development only. Do not deploy publicly with these settings.
- For a real deployment, add authentication/authorization for farmers, stronger phone validation, tests, secure production settings and payment integration if required.
