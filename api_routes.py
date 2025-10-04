"""
Additional API routes for expense management system
"""

from flask import Blueprint, request, jsonify, session
from database import db
from models import Company, User, ApprovalRule, RuleStep, ExpenseApproval, Expense
from werkzeug.security import generate_password_hash
from email_service import email_service
import requests

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Company Management APIs
@api_bp.route('/companies', methods=['GET', 'POST'])
def manage_companies():
    if request.method == 'POST':
        # Only admin can create companies
        if session.get('user_role') != 'Admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Get currency from REST Countries API to validate
        try:
            response = requests.get('https://restcountries.com/v3.1/all?fields=currencies')
            countries_data = response.json()
            
            valid_currencies = set()
            for country in countries_data:
                country_currencies = country.get('currencies', {})
                valid_currencies.update(country_currencies.keys())
            
            if data['base_currency_code'] not in valid_currencies:
                return jsonify({'error': 'Invalid currency code'}), 400
        except:
            pass  # Skip validation if API is down
        
        company = Company(
            name=data['name'],
            base_currency_code=data['base_currency_code']
        )
        
        db.session.add(company)
        db.session.commit()
        
        return jsonify({
            'message': 'Company created successfully',
            'id': company.id
        }), 201
    
    else:
        companies = Company.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'base_currency_code': c.base_currency_code
        } for c in companies])

# User Management APIs
@api_bp.route('/users', methods=['GET', 'POST'])
def manage_users():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        # Only admin and managers can create users
        if session.get('user_role') not in ['Admin', 'Manager']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(
            company_id=data['company_id'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role=data.get('role', 'Employee'),
            manager_id=data.get('manager_id')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'id': user.id
        }), 201
    
    else:
        # Get users based on role
        current_user = User.query.get(session['user_id'])
        
        if current_user.role == 'Admin':
            users = User.query.filter_by(company_id=current_user.company_id).all()
        elif current_user.role == 'Manager':
            users = User.query.filter_by(manager_id=current_user.id).all()
            users.append(current_user)  # Include self
        else:
            users = [current_user]  # Only self
        
        return jsonify([{
            'id': u.id,
            'email': u.email,
            'role': u.role,
            'manager_id': u.manager_id
        } for u in users])

# Approval Rules Management
@api_bp.route('/approval-rules', methods=['GET', 'POST'])
def manage_approval_rules():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        # Only admin can create approval rules
        if session.get('user_role') != 'Admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        rule = ApprovalRule(
            name=data['name'],
            applies_to_category=data.get('applies_to_category'),
            is_manager_first=data.get('is_manager_first', False),
            is_sequential=data.get('is_sequential', False),
            min_approval_percentage=data.get('min_approval_percentage', 100.0)
        )
        
        db.session.add(rule)
        db.session.flush()  # Get the ID
        
        # Add rule steps
        for step_data in data.get('steps', []):
            step = RuleStep(
                rule_id=rule.id,
                user_id=step_data.get('user_id'),
                role_type=step_data.get('role_type'),
                is_required_approver=step_data.get('is_required_approver', False),
                sequence_order=step_data.get('sequence_order', 1)
            )
            db.session.add(step)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Approval rule created successfully',
            'id': rule.id
        }), 201
    
    else:
        rules = ApprovalRule.query.all()
        result = []
        
        for rule in rules:
            steps = [{
                'id': s.id,
                'user_id': s.user_id,
                'role_type': s.role_type,
                'is_required_approver': s.is_required_approver,
                'sequence_order': s.sequence_order
            } for s in rule.rule_steps]
            
            result.append({
                'id': rule.id,
                'name': rule.name,
                'applies_to_category': rule.applies_to_category,
                'is_manager_first': rule.is_manager_first,
                'is_sequential': rule.is_sequential,
                'min_approval_percentage': float(rule.min_approval_percentage),
                'steps': steps
            })
        
        return result

# Expense Categories API
@api_bp.route('/expense-categories', methods=['GET'])
def get_expense_categories():
    """Get list of expense categories"""
    categories = [
        'Travel',
        'Meals & Entertainment',
        'Office Supplies',
        'Equipment',
        'Software & Subscriptions',
        'Training & Development',
        'Marketing',
        'Utilities',
        'Other'
    ]
    return jsonify(categories)

# Countries and Currency API
@api_bp.route('/countries', methods=['GET'])
def get_countries_with_currencies():
    """Get list of countries with their currencies"""
    try:
        response = requests.get('https://restcountries.com/v3.1/all?fields=name,currencies')
        data = response.json()
        
        countries = []
        for country in data:
            country_name = country.get('name', {}).get('common', '')
            country_currencies = country.get('currencies', {})
            
            currency_list = []
            for currency_code, currency_data in country_currencies.items():
                currency_list.append({
                    'code': currency_code,
                    'name': currency_data.get('name', ''),
                    'symbol': currency_data.get('symbol', '')
                })
            
            if country_name and currency_list:
                countries.append({
                    'name': country_name,
                    'currencies': currency_list
                })
        
        # Sort by country name
        countries.sort(key=lambda x: x['name'])
        return jsonify(countries)
    except Exception as e:
        return jsonify({'error': f'Failed to fetch countries data: {str(e)}'}), 500

# Currency API
@api_bp.route('/currencies', methods=['GET'])
def get_currencies():
    """Get list of supported currencies from REST Countries API"""
    try:
        response = requests.get('https://restcountries.com/v3.1/all?fields=name,currencies')
        data = response.json()
        
        currencies = set()
        currency_info = []
        
        for country in data:
            country_name = country.get('name', {}).get('common', '')
            country_currencies = country.get('currencies', {})
            
            for currency_code, currency_data in country_currencies.items():
                if currency_code not in currencies:
                    currencies.add(currency_code)
                    currency_info.append({
                        'code': currency_code,
                        'name': currency_data.get('name', ''),
                        'symbol': currency_data.get('symbol', ''),
                        'country_example': country_name
                    })
        
        # Sort by currency code
        currency_info.sort(key=lambda x: x['code'])
        return jsonify(currency_info)
    except Exception as e:
        # Fallback list of common currencies with basic info
        fallback_currencies = [
            {'code': 'USD', 'name': 'United States Dollar', 'symbol': '$', 'country_example': 'United States'},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'country_example': 'European Union'},
            {'code': 'GBP', 'name': 'British Pound Sterling', 'symbol': '£', 'country_example': 'United Kingdom'},
            {'code': 'JPY', 'name': 'Japanese Yen', 'symbol': '¥', 'country_example': 'Japan'},
            {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': 'A$', 'country_example': 'Australia'},
            {'code': 'CAD', 'name': 'Canadian Dollar', 'symbol': 'C$', 'country_example': 'Canada'},
            {'code': 'CHF', 'name': 'Swiss Franc', 'symbol': 'Fr', 'country_example': 'Switzerland'},
            {'code': 'CNY', 'name': 'Chinese Yuan', 'symbol': '¥', 'country_example': 'China'},
            {'code': 'INR', 'name': 'Indian Rupee', 'symbol': '₹', 'country_example': 'India'},
            {'code': 'SGD', 'name': 'Singapore Dollar', 'symbol': 'S$', 'country_example': 'Singapore'}
        ]
        return jsonify(fallback_currencies)

# Exchange Rate API
@api_bp.route('/exchange-rate', methods=['GET'])
def get_exchange_rate():
    """Get exchange rate between two currencies"""
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    
    if not from_currency or not to_currency:
        return jsonify({'error': 'Missing currency parameters'}), 400
    
    try:
        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{from_currency}')
        data = response.json()
        rate = data['rates'].get(to_currency)
        
        if rate:
            return jsonify({
                'from': from_currency,
                'to': to_currency,
                'rate': rate,
                'date': data['date']
            })
        else:
            return jsonify({'error': 'Currency not found'}), 404
    except:
        return jsonify({'error': 'Unable to fetch exchange rate'}), 500

# Expense Reports API
@api_bp.route('/reports/expenses', methods=['GET'])
def expense_reports():
    """Generate expense reports"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    current_user = User.query.get(session['user_id'])
    
    # Parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    status = request.args.get('status')
    user_id = request.args.get('user_id')
    
    # Build query based on user role
    query = Expense.query
    
    if current_user.role == 'Employee':
        query = query.filter_by(user_id=current_user.id)
    elif current_user.role == 'Manager':
        # Manager can see their expenses and their subordinates'
        subordinate_ids = [u.id for u in current_user.subordinates]
        subordinate_ids.append(current_user.id)
        query = query.filter(Expense.user_id.in_(subordinate_ids))
    # Admin can see all expenses (no additional filter needed)
    
    # Apply filters
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    if status:
        query = query.filter(Expense.status == status)
    if user_id and current_user.role in ['Admin', 'Manager']:
        query = query.filter(Expense.user_id == user_id)
    
    expenses = query.all()
    
    # Calculate totals
    total_amount = sum(float(e.final_amount_base_currency or 0) for e in expenses)
    total_count = len(expenses)
    
    # Group by status
    status_summary = {}
    for expense in expenses:
        status = expense.status
        if status not in status_summary:
            status_summary[status] = {'count': 0, 'amount': 0}
        status_summary[status]['count'] += 1
        status_summary[status]['amount'] += float(expense.final_amount_base_currency or 0)
    
    return jsonify({
        'expenses': [{
            'id': e.id,
            'user_email': e.user.email,
            'category': e.category,
            'description': e.description,
            'date': e.date.isoformat(),
            'amount_spent': float(e.amount_spent),
            'currency_spent': e.currency_spent,
            'status': e.status,
            'final_amount_base_currency': float(e.final_amount_base_currency or 0)
        } for e in expenses],
        'summary': {
            'total_count': total_count,
            'total_amount': total_amount,
            'currency': current_user.company.base_currency_code,
            'status_breakdown': status_summary
        }
    })

# Pending Approvals API
@api_bp.route('/approvals/pending', methods=['GET'])
def pending_approvals():
    """Get pending approvals for current user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    approvals = ExpenseApproval.query.filter_by(
        approver_user_id=session['user_id'],
        status='Pending'
    ).all()
    
    result = []
    for approval in approvals:
        expense = approval.expense
        result.append({
            'approval_id': approval.id,
            'expense_id': expense.id,
            'submitter': expense.user.email,
            'category': expense.category,
            'description': expense.description,
            'date': expense.date.isoformat(),
            'amount': float(expense.final_amount_base_currency),
            'currency': expense.user.company.base_currency_code,
            'submitted_date': expense.created_at.isoformat()
        })
    
    return jsonify(result)

# Approval Rules Management APIs
@api_bp.route('/admin/approval-rules', methods=['GET', 'POST'])
def admin_manage_approval_rules():
    # Check admin access
    if session.get('user_role') != 'Admin':
        return jsonify({'error': 'Unauthorized - Admin access required'}), 403
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data.get('user_id') or not data.get('description'):
                return jsonify({'error': 'Missing required fields: user_id, description'}), 400
            
            if not data.get('approvers') or len(data.get('approvers', [])) == 0:
                return jsonify({'error': 'At least one approver is required'}), 400
            
            # Create approval rule
            approval_rule = ApprovalRule(
                name=data.get('description'),
                applies_to_category=data.get('category'),  # Optional
                is_manager_first=data.get('is_manager_first', False),
                is_sequential=data.get('is_sequential', False),
                min_approval_percentage=data.get('min_approval_percentage', 100.0)
            )
            
            db.session.add(approval_rule)
            db.session.flush()  # Get the ID
            
            # Create rule steps for each approver
            for i, approver in enumerate(data.get('approvers', [])):
                rule_step = RuleStep(
                    rule_id=approval_rule.id,
                    user_id=approver.get('id'),
                    sequence_order=approver.get('sequence', i + 1),
                    is_required_approver=True
                )
                db.session.add(rule_step)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Approval rule created successfully',
                'rule_id': approval_rule.id
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create approval rule: {str(e)}'}), 500
    
    else:  # GET request
        try:
            # Get all approval rules with their steps
            rules = db.session.query(ApprovalRule).all()
            
            rules_data = []
            for rule in rules:
                # Get approvers for this rule
                approvers = []
                for step in rule.rule_steps:
                    if step.user:
                        approvers.append({
                            'id': step.user.id,
                            'name': step.user.name,
                            'role': step.user.role,
                            'sequence': step.sequence_order
                        })
                
                # Sort approvers by sequence
                approvers.sort(key=lambda x: x['sequence'])
                
                rules_data.append({
                    'id': rule.id,
                    'name': rule.name,
                    'description': rule.name,
                    'is_manager_first': rule.is_manager_first,
                    'is_sequential': rule.is_sequential,
                    'min_approval_percentage': float(rule.min_approval_percentage),
                    'approvers': approvers,
                    'created_at': rule.created_at.isoformat()
                })
            
            return jsonify({
                'success': True,
                'rules': rules_data
            })
            
        except Exception as e:
            return jsonify({'error': f'Failed to load approval rules: {str(e)}'}), 500

@api_bp.route('/admin/approval-rules/<int:rule_id>', methods=['PUT', 'DELETE'])
def manage_approval_rule(rule_id):
    # Check admin access
    if session.get('user_role') != 'Admin':
        return jsonify({'error': 'Unauthorized - Admin access required'}), 403
    
    rule = ApprovalRule.query.get(rule_id)
    if not rule:
        return jsonify({'error': 'Approval rule not found'}), 404
    
    if request.method == 'PUT':
        try:
            data = request.get_json()
            
            # Update rule properties
            rule.name = data.get('description', rule.name)
            rule.is_manager_first = data.get('is_manager_first', rule.is_manager_first)
            rule.is_sequential = data.get('is_sequential', rule.is_sequential)
            rule.min_approval_percentage = data.get('min_approval_percentage', rule.min_approval_percentage)
            
            # Update approvers if provided
            if 'approvers' in data:
                # Remove existing rule steps
                RuleStep.query.filter_by(rule_id=rule.id).delete()
                
                # Add new rule steps
                for i, approver in enumerate(data.get('approvers', [])):
                    rule_step = RuleStep(
                        rule_id=rule.id,
                        user_id=approver.get('id'),
                        sequence_order=approver.get('sequence', i + 1),
                        is_required_approver=True
                    )
                    db.session.add(rule_step)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Approval rule updated successfully'
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update approval rule: {str(e)}'}), 500
    
    else:  # DELETE request
        try:
            # Delete rule steps first (due to foreign key constraint)
            RuleStep.query.filter_by(rule_id=rule.id).delete()
            
            # Delete the rule
            db.session.delete(rule)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Approval rule deleted successfully'
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete approval rule: {str(e)}'}), 500

@api_bp.route('/admin/users/<int:user_id>/send-password', methods=['POST'])
def send_password_reset(user_id):
    """Generate new password and send it to user's email"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Check if current user is admin
    current_user = User.query.get(session['user_id'])
    if not current_user or current_user.role != 'Admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    # Get the user to reset password for
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        # Generate new random password
        new_password = email_service.generate_random_password()
        
        # Update user's password in database
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        # Send email with new password
        success, message = email_service.send_password_reset_email(
            user.email, 
            user.name, 
            new_password
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': f'New password sent to {user.email}'
            })
        else:
            # If email fails, we still keep the password change but inform admin
            return jsonify({
                'success': True,
                'message': f'Password updated but email failed: {message}. New password: {new_password}',
                'password': new_password  # Return password if email fails
            })
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to reset password: {str(e)}'}), 500

@api_bp.route('/admin/test-email', methods=['POST'])
def test_email_configuration():
    """Test email configuration"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Check if current user is admin
    current_user = User.query.get(session['user_id'])
    if not current_user or current_user.role != 'Admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    success, message = email_service.test_email_connection()
    
    return jsonify({
        'success': success,
        'message': message
    })

# Employee Expense Management APIs
@api_bp.route('/expenses', methods=['GET', 'POST'])
def manage_expenses():
    """Get user's expenses or create new expense"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if request.method == 'GET':
        # Get user's expenses
        expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.created_at.desc()).all()
        
        expense_data = []
        for expense in expenses:
            expense_data.append({
                'id': expense.id,
                'category': expense.category,
                'description': expense.description,
                'amount_spent': float(expense.amount_spent),
                'currency_spent': expense.currency_spent,
                'final_amount_base_currency': float(expense.final_amount_base_currency),
                'date': expense.date.isoformat(),
                'status': expense.status,
                'receipt_url': expense.receipt_url,
                'created_at': expense.created_at.isoformat() if expense.created_at else None,
                'comments': expense.comments
            })
        
        return jsonify(expense_data)
    
    elif request.method == 'POST':
        # Create new expense
        try:
            if request.is_json:
                data = request.get_json()
            else:
                # Handle form data (with potential file upload)
                data = request.form.to_dict()
            
            # Validate required fields
            required_fields = ['category', 'description', 'amount_spent', 'currency_spent', 'date']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Get exchange rate if currency is different from base currency
            exchange_rate = 1.0
            base_currency = user.company.base_currency_code
            spent_currency = data['currency_spent']
            
            if spent_currency != base_currency:
                try:
                    # Use the exchange rate API
                    rate_response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{spent_currency}')
                    if rate_response.status_code == 200:
                        rates = rate_response.json()['rates']
                        exchange_rate = rates.get(base_currency, 1.0)
                except:
                    # Fallback to 1.0 if API fails
                    exchange_rate = 1.0
            
            # Calculate final amount in base currency
            amount_spent = float(data['amount_spent'])
            final_amount = amount_spent * exchange_rate
            
            # Create expense
            expense = Expense(
                user_id=user.id,
                category=data['category'],
                description=data['description'],
                amount_spent=amount_spent,
                currency_spent=spent_currency,
                final_amount_base_currency=final_amount,
                date=data['date'],
                status=data.get('status', 'Draft')
            )
            
            db.session.add(expense)
            db.session.commit()
            
            # Handle receipt upload if provided
            if 'receipt' in request.files:
                receipt_file = request.files['receipt']
                if receipt_file and receipt_file.filename:
                    # Simple file handling - in production, use proper file storage
                    filename = f"receipt_{expense.id}_{receipt_file.filename}"
                    receipt_path = f"/static/receipts/{filename}"
                    # Note: In production, save to proper file storage
                    expense.receipt_url = receipt_path
                    db.session.commit()
            
            return jsonify({
                'message': 'Expense created successfully',
                'id': expense.id,
                'status': expense.status
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create expense: {str(e)}'}), 500

@api_bp.route('/expenses/<int:expense_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_expense(expense_id):
    """Get, update, or delete a specific expense"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if user owns this expense or is admin
    if expense.user_id != user.id and user.role != 'Admin':
        return jsonify({'error': 'Access denied'}), 403
    
    if request.method == 'GET':
        # Get latest approval for this expense
        latest_approval = ExpenseApproval.query.filter_by(expense_id=expense.id).order_by(ExpenseApproval.created_at.desc()).first()
        
        return jsonify({
            'id': expense.id,
            'category': expense.category,
            'description': expense.description,
            'amount_spent': float(expense.amount_spent),
            'currency_spent': expense.currency_spent,
            'final_amount_base_currency': float(expense.final_amount_base_currency),
            'date': expense.date.isoformat(),
            'status': expense.status,
            'receipt_url': expense.receipt_url,
            'created_at': expense.created_at.isoformat() if expense.created_at else None,
            'comments': latest_approval.comments if latest_approval else None,
            'approver_name': latest_approval.approver.name if latest_approval else None,
            'approved_at': latest_approval.created_at.isoformat() if latest_approval else None
        })
    
    elif request.method == 'PUT':
        # Update expense (only if draft)
        if expense.status != 'Draft':
            return jsonify({'error': 'Can only edit draft expenses'}), 400
        
        try:
            data = request.get_json()
            
            # Update fields
            if 'category' in data:
                expense.category = data['category']
            if 'description' in data:
                expense.description = data['description']
            if 'amount_spent' in data:
                expense.amount_spent = float(data['amount_spent'])
            if 'date' in data:
                expense.date = data['date']
            
            # Recalculate exchange rate if needed
            if 'currency_spent' in data or 'amount_spent' in data:
                base_currency = user.company.base_currency_code
                spent_currency = data.get('currency_spent', expense.currency_spent)
                
                exchange_rate = 1.0
                if spent_currency != base_currency:
                    try:
                        rate_response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{spent_currency}')
                        if rate_response.status_code == 200:
                            rates = rate_response.json()['rates']
                            exchange_rate = rates.get(base_currency, 1.0)
                    except:
                        exchange_rate = 1.0
                
                expense.currency_spent = spent_currency
                expense.final_amount_base_currency = expense.amount_spent * exchange_rate
            
            db.session.commit()
            
            return jsonify({'message': 'Expense updated successfully'})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update expense: {str(e)}'}), 500
    
    elif request.method == 'DELETE':
        # Delete expense (only if draft)
        if expense.status != 'Draft':
            return jsonify({'error': 'Can only delete draft expenses'}), 400
        
        try:
            db.session.delete(expense)
            db.session.commit()
            
            return jsonify({'message': 'Expense deleted successfully'})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete expense: {str(e)}'}), 500

@api_bp.route('/expenses/<int:expense_id>/submit', methods=['POST'])
def submit_expense(expense_id):
    """Submit expense for approval"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if user owns this expense
    if expense.user_id != user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    # Check if expense is in draft status
    if expense.status != 'Draft':
        return jsonify({'error': 'Can only submit draft expenses'}), 400
    
    try:
        # Update status to submitted
        expense.status = 'Submitted'
        db.session.commit()
        
        return jsonify({'message': 'Expense submitted for approval'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to submit expense: {str(e)}'}), 500

@api_bp.route('/expenses/<int:expense_id>/approve', methods=['POST'])
def approve_expense(expense_id):
    """Approve or reject expense (for managers)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if user is manager or admin
    if user.role not in ['Manager', 'Admin']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        data = request.get_json()
        action = data.get('action')  # 'Approved' or 'Rejected'
        comments = data.get('comments', '')
        
        if action not in ['Approved', 'Rejected']:
            return jsonify({'error': 'Invalid action'}), 400
        
        # Update expense
        expense.status = action
        # Create approval record
        approval = ExpenseApproval(
            expense_id=expense.id,
            approver_user_id=user.id,
            action=action,
            comments=comments
        )
        db.session.add(approval)
        db.session.commit()
        
        return jsonify({'message': f'Expense {action.lower()} successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to process approval: {str(e)}'}), 500