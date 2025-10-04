from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, init_db
from models import User, Company, Expense, ApprovalRule, RuleStep, ExpenseApproval
from api_routes import api_bp
import os
from datetime import datetime
import requests
from decimal import Decimal
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 
    'postgresql://username:password@localhost/expense_management')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Register API blueprint
app.register_blueprint(api_bp)

# Helper decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Unauthorized - Please login'}), 401
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Unauthorized - Please login'}), 401
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'Admin':
            if request.is_json:
                return jsonify({'error': 'Unauthorized - Admin access required'}), 403
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

# Security middleware for admin routes
@app.before_request
def check_admin_access():
    # Skip security checks for static files and certain routes
    if request.endpoint and (
        request.endpoint.startswith('static') or 
        request.endpoint in ['landing', 'login', 'register', 'logout']
    ):
        return
    
    # Check if accessing admin routes
    if request.path.startswith('/admin') or request.path.startswith('/api/admin'):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Unauthorized - Please login'}), 401
            flash('Please log in to access admin features.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'Admin':
            if request.is_json:
                return jsonify({'error': 'Unauthorized - Admin access required'}), 403
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        print(f"🔐 Login attempt - Email: {username}")  # Debug log
        
        user = User.query.filter_by(email=username).first()
        
        if user:
            print(f"👤 User found: {user.name} ({user.role})")  # Debug log
            password_valid = check_password_hash(user.password_hash, password)
            print(f"🔑 Password valid: {password_valid}")  # Debug log
            
            if password_valid:
                session['user_id'] = user.id
                session['user_role'] = user.role
                flash('Login successful!', 'success')
                print(f"✅ Login successful for {user.email}")  # Debug log
                
                # Redirect based on user role
                if user.role == 'Admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    # Redirect Employees and Managers to regular dashboard
                    return redirect(url_for('dashboard'))
            else:
                print(f"❌ Invalid password for {username}")  # Debug log
                flash('Invalid username or password', 'error')
        else:
            print(f"❌ User not found: {username}")  # Debug log
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        country = request.form['country']
        role = request.form.get('role', 'Employee')
        
        # Validate password confirmation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Validate password strength
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Get or create company based on country
        company = get_or_create_company_for_country(country)
        
        # Create new user
        password_hash = generate_password_hash(password)
        new_user = User(
            name=name,
            company_id=company.id,
            email=email,
            password_hash=password_hash,
            role=role,
            manager_id=None  # Can be set later by admin
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    # Redirect admins to their specific dashboard
    if user.role == 'Admin':
        return redirect(url_for('admin_dashboard'))
    
    # Show employee dashboard for Employees and Managers
    expenses = Expense.query.filter_by(user_id=session['user_id']).order_by(Expense.created_at.desc()).all()
    return render_template('employee_dashboard.html', user=user, expenses=expenses)

@app.route('/debug-session')
def debug_session():
    return jsonify({
        'session_data': dict(session),
        'user_id': session.get('user_id'),
        'user_role': session.get('user_role'),
        'logged_in': 'user_id' in session
    })

@app.route('/admin')
@admin_required
def admin_dashboard():
    user = User.query.get(session['user_id'])
    return render_template('admin_dashboard.html', user=user)

@app.route('/admin/approval-rules')
@admin_required
def approval_rules():
    user = User.query.get(session['user_id'])
    return render_template('approval_rules.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('landing'))

# API Routes for expense management
@app.route('/api/expenses', methods=['GET', 'POST'])
def api_expenses():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Get exchange rate for currency conversion
        base_currency = User.query.get(session['user_id']).company.base_currency_code
        spent_currency = data['currency_spent']
        
        if base_currency != spent_currency:
            final_amount = convert_currency(
                data['amount_spent'], 
                spent_currency, 
                base_currency
            )
        else:
            final_amount = data['amount_spent']
        
        expense = Expense(
            user_id=session['user_id'],
            category=data['category'],
            description=data['description'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            amount_spent=Decimal(str(data['amount_spent'])),
            currency_spent=spent_currency,
            status='Draft',
            final_amount_base_currency=Decimal(str(final_amount))
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({'message': 'Expense created successfully', 'id': expense.id}), 201
    
    else:
        expenses = Expense.query.filter_by(user_id=session['user_id']).all()
        return jsonify([{
            'id': e.id,
            'category': e.category,
            'description': e.description,
            'date': e.date.isoformat(),
            'amount_spent': float(e.amount_spent),
            'currency_spent': e.currency_spent,
            'status': e.status,
            'final_amount_base_currency': float(e.final_amount_base_currency)
        } for e in expenses])

@app.route('/api/expenses/<int:expense_id>/submit', methods=['POST'])
def submit_expense(expense_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    expense = Expense.query.get_or_404(expense_id)
    
    if expense.user_id != session['user_id']:
        return jsonify({'error': 'Forbidden'}), 403
    
    expense.status = 'Submitted'
    db.session.commit()
    
    # Create approval workflow
    create_approval_workflow(expense)
    
    return jsonify({'message': 'Expense submitted for approval'})

@app.route('/api/expenses/<int:expense_id>/approve', methods=['POST'])
def approve_expense(expense_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    action = data.get('action', 'Approved')  # Default to 'Approved'
    comments = data.get('comments', '')
    
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if user is authorized to approve this expense
    approval = ExpenseApproval.query.filter_by(
        expense_id=expense_id,
        approver_user_id=session['user_id'],
        status='Pending'
    ).first()
    
    if not approval:
        return jsonify({'error': 'Not authorized to approve this expense'}), 403
    
    # Update approval status
    approval.status = action
    approval.comments = comments
    approval.approval_date = datetime.utcnow()
    
    # Check if all required approvals are complete or if any rejection occurred
    if action == 'Rejected':
        expense.status = 'Rejected'
    else:
        pending_approvals = ExpenseApproval.query.filter_by(
            expense_id=expense_id,
            status='Pending'
        ).count()
        
        if pending_approvals == 0:
            expense.status = 'Approved'
    
    db.session.commit()
    
    return jsonify({'message': f'Expense {action.lower()} successfully'})

def convert_currency(amount, from_currency, to_currency):
    """Convert currency using ExchangeRate API"""
    try:
        # Using the specified ExchangeRate API
        response = requests.get(
            f'https://api.exchangerate-api.com/v4/latest/{from_currency}'
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        if to_currency in data['rates']:
            rate = data['rates'][to_currency]
            converted_amount = float(amount) * rate
            return converted_amount
        else:
            # Currency not found in rates
            print(f"Warning: Currency {to_currency} not found in exchange rates")
            return float(amount)  # Return original amount as fallback
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return float(amount)  # Fallback to 1:1 conversion if API fails
    except (KeyError, ValueError) as e:
        print(f"Error processing exchange rate data: {e}")
        return float(amount)  # Fallback to 1:1 conversion if data is invalid

def get_country_currency(country_name):
    """Get the primary currency for a country"""
    try:
        response = requests.get('https://restcountries.com/v3.1/all?fields=name,currencies')
        countries_data = response.json()
        
        for country in countries_data:
            if country.get('name', {}).get('common', '').lower() == country_name.lower():
                currencies = country.get('currencies', {})
                if currencies:
                    # Return the first currency code
                    return list(currencies.keys())[0]
        
        # Fallback to USD if country not found
        return 'USD'
    except:
        return 'USD'

def get_or_create_company_for_country(country_name):
    """Get or create a company for the specified country"""
    # Check if a company already exists for this country
    company = Company.query.filter_by(name=f"{country_name} Office").first()
    
    if not company:
        # Get the primary currency for this country
        currency_code = get_country_currency(country_name)
        
        # Create a new company
        company = Company(
            name=f"{country_name} Office",
            base_currency_code=currency_code
        )
        db.session.add(company)
        db.session.commit()
    
    return company

def create_approval_workflow(expense):
    """Create approval workflow based on rules"""
    # Find applicable approval rules
    rules = ApprovalRule.query.filter_by(applies_to_category=expense.category).all()
    
    if not rules:
        # No specific rules, default to manager approval
        user = User.query.get(expense.user_id)
        if user.manager_id:
            approval = ExpenseApproval(
                expense_id=expense.id,
                approver_user_id=user.manager_id,
                status='Pending'
            )
            db.session.add(approval)
    else:
        # Apply rules
        for rule in rules:
            steps = RuleStep.query.filter_by(rule_id=rule.id).order_by(RuleStep.sequence_order).all()
            for step in steps:
                approval = ExpenseApproval(
                    expense_id=expense.id,
                    approver_user_id=step.user_id,
                    status='Pending'
                )
                db.session.add(approval)
    
    db.session.commit()

# Admin User Management API Endpoints
@app.route('/api/admin/users', methods=['GET', 'POST'])
@admin_required
def admin_manage_users():
    current_user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        data = request.get_json()
        print(f"DEBUG: Received data: {data}")  # Debug logging
        
        # Check if data is None or missing required fields
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400
        
        if not data.get('name') or not data.get('email'):
            return jsonify({'success': False, 'error': 'Name and email are required'}), 400
        
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
        # Create new user with proper company_id
        password_hash = generate_password_hash(data.get('password', 'TempPass123!'))
        new_user = User(
            name=data['name'],
            company_id=current_user.company_id,  # Use admin's company
            email=data['email'],
            password_hash=password_hash,
            role=data.get('role', 'Employee'),
            manager_id=data.get('manager_id') if data.get('manager_id') else None
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user_id': new_user.id
        }), 201
    
    else:
        # Get all users in the same company as admin
        users = User.query.filter_by(company_id=current_user.company_id).all()
        
        users_data = []
        for user in users:
            manager_name = None
            if user.manager_id:
                manager = User.query.get(user.manager_id)
                manager_name = manager.name if manager else None
            
            users_data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'manager_id': user.manager_id,
                'manager_name': manager_name,
                'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') else None,
                'status': 'Active'  # You can add a status field to User model later
            })
        
        return jsonify({
            'success': True,
            'users': users_data
        })

@app.route('/api/admin/users/<int:user_id>', methods=['PUT', 'DELETE'])
@admin_required
def admin_manage_single_user(user_id):
    current_user = User.query.get(session['user_id'])
    user = User.query.get(user_id)
    
    if not user or user.company_id != current_user.company_id:
        return jsonify({'error': 'User not found'}), 404
    
    if request.method == 'PUT':
        data = request.get_json()
        
        # Update user details
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            # Check if email is unique
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({'success': False, 'error': 'Email already exists'}), 400
            user.email = data['email']
        if 'role' in data:
            user.role = data['role']
        if 'manager_id' in data:
            user.manager_id = data['manager_id'] if data['manager_id'] else None
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'User updated successfully'})
    
    elif request.method == 'DELETE':
        # Don't allow deleting yourself
        if user_id == session['user_id']:
            return jsonify({'success': False, 'error': 'Cannot delete yourself'}), 400
        
        # Soft delete or deactivate user (you can add a status field later)
        # For now, we'll just remove them
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'User deleted successfully'})

@app.route('/api/admin/users/<int:user_id>/reset-password', methods=['POST'])
@admin_required
def admin_reset_user_password(user_id):
    current_user = User.query.get(session['user_id'])
    user = User.query.get(user_id)
    
    if not user or user.company_id != current_user.company_id:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    data = request.get_json() or {}  # Handle case where no JSON is sent
    temp_password = data.get('temp_password', 'TempPass123!')
    
    # Set new temporary password
    user.password_hash = generate_password_hash(temp_password)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Password reset successfully',
        'new_password': temp_password
    })

@app.route('/api/admin/managers', methods=['GET'])
@admin_required
def get_potential_managers():
    current_user = User.query.get(session['user_id'])
    if not current_user or current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized - Admin access required'}), 403
    
    current_user = User.query.get(session['user_id'])
    
    # Get all users who can be managers (Admin or Manager role) in same company
    managers = User.query.filter_by(company_id=current_user.company_id).filter(
        User.role.in_(['Admin', 'Manager'])
    ).all()
    
    managers_data = []
    for manager in managers:
        managers_data.append({
            'id': manager.id,
            'name': manager.name,
            'email': manager.email,
            'role': manager.role
        })
    
    return jsonify({
        'success': True,
        'managers': managers_data
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)