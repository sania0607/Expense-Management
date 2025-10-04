from database import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    base_currency_code = Column(String(3), nullable=False)  # e.g., USD, EUR, GBP
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship('User', backref='company', lazy=True)
    
    def __repr__(self):
        return f'<Company {self.name}>'

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # Added name field
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default='Employee')  # Admin, Manager, Employee
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Self-referential
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    manager = relationship('User', remote_side=[id], backref='subordinates')
    expenses = relationship('Expense', backref='user', lazy=True)
    rule_steps = relationship('RuleStep', backref='user', lazy=True)
    my_approvals = relationship('ExpenseApproval', foreign_keys='ExpenseApproval.approver_user_id', back_populates='approver', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(Date, nullable=False)
    amount_spent = Column(Numeric(10, 2), nullable=False)
    currency_spent = Column(String(3), nullable=False)  # Currency code
    status = Column(String(50), nullable=False, default='Draft')  # Draft, Submitted, Approved, Rejected
    final_amount_base_currency = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    approvals = relationship('ExpenseApproval', back_populates='expense', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Expense {self.id}: {self.description}>'

class ApprovalRule(db.Model):
    __tablename__ = 'approval_rules'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    applies_to_category = Column(String(100), nullable=True)  # Null means applies to all categories
    is_manager_first = Column(Boolean, default=False)  # If manager approval is required first
    is_sequential = Column(Boolean, default=False)  # If approvals must be in sequence
    min_approval_percentage = Column(Numeric(5, 2), default=100.00)  # Minimum percentage of approvers needed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    rule_steps = relationship('RuleStep', backref='rule', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ApprovalRule {self.name}>'

class RuleStep(db.Model):
    __tablename__ = 'rule_steps'
    
    id = Column(Integer, primary_key=True)
    rule_id = Column(Integer, ForeignKey('approval_rules.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Specific user
    role_type = Column(String(50), nullable=True)  # Role-based approval (e.g., Finance, HR)
    is_required_approver = Column(Boolean, default=False)  # For Specific Approver Rule
    sequence_order = Column(Integer, nullable=False, default=1)  # Order in sequence
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RuleStep {self.id}>'

class ExpenseApproval(db.Model):
    __tablename__ = 'expense_approvals'
    
    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey('expenses.id'), nullable=False)
    approver_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String(50), nullable=False)  # 'Approved', 'Rejected'
    comments = Column(Text, nullable=True)
    approval_date = Column(DateTime, nullable=True)  # When the action was taken
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    approver = relationship('User', foreign_keys=[approver_user_id], back_populates='my_approvals')
    expense = relationship('Expense', back_populates='approvals')
    
    def __repr__(self):
        return f'<ExpenseApproval {self.id}: {self.action}>'

# Create database tables
def create_tables():
    """Create all database tables"""
    db.create_all()

# Sample data creation functions
def create_sample_data():
    """Create sample data for testing"""
    
    # Create a sample company
    company = Company(
        name='Sample Corp',
        base_currency_code='USD'
    )
    db.session.add(company)
    db.session.commit()
    
    # Create sample users
    from werkzeug.security import generate_password_hash
    
    admin = User(
        name='System Administrator',
        company_id=company.id,
        email='admin@company.com',
        password_hash=generate_password_hash('admin123'),
        role='Admin'
    )
    db.session.add(admin)
    
    manager = User(
        name='John Manager',
        company_id=company.id,
        email='manager@company.com',
        password_hash=generate_password_hash('manager123'),
        role='Manager'
    )
    db.session.add(manager)
    
    employee = User(
        name='Jane Employee',
        company_id=company.id,
        email='employee@company.com',
        password_hash=generate_password_hash('employee123'),
        role='Employee',
        manager_id=manager.id
    )
    db.session.add(employee)
    
    db.session.commit()
    
    # Create sample approval rule
    rule = ApprovalRule(
        name='Standard Travel Expense Approval',
        applies_to_category='Travel',
        is_manager_first=True,
        is_sequential=True,
        min_approval_percentage=100.00
    )
    db.session.add(rule)
    db.session.commit()
    
    # Create rule steps
    step1 = RuleStep(
        rule_id=rule.id,
        user_id=manager.id,
        is_required_approver=True,
        sequence_order=1
    )
    db.session.add(step1)
    
    step2 = RuleStep(
        rule_id=rule.id,
        role_type='Finance',
        sequence_order=2
    )
    db.session.add(step2)
    
    db.session.commit()
    
    print("Sample data created successfully!")

if __name__ == '__main__':
    create_tables()
    create_sample_data()