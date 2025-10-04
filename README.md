# 💼 ExpenseFlow - Modern Expense Management System

A comprehensive expense management platform designed for modern businesses with role-based dashboards, real-time approval workflows, and multi-currency support.

## 🚀 Quick Start

1. **Clone & Install:**
   ```bash
   git clone https://github.com/sania0607/Expense-Management.git
   cd Expense-Management
   pip install -r requirements.txt
   ```

2. **Configure:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Run:**
   ```bash
   python -c "from app import app; from database import db; app.app_context().push(); db.create_all()"
   python app.py
   ```

4. **Access:** Open `http://localhost:5000`

## 🌟 Key Features

### 👥 **Role-Based System**
- **Admin**: User management, company settings, system configuration
- **Manager**: Expense approval dashboard with bulk actions and analytics
- **Employee**: Expense submission with visual workflow tracking

### 💰 **Expense Management**
- Multi-currency support with real-time conversion (ExchangeRate API)
- Receipt uploads and smart categorization
- Draft → Submitted → Approved/Rejected workflow
- Comprehensive expense tracking and reporting

### ✅ **Approval Workflow**
- Manager dashboard matching your workflow requirements
- Bulk approve/reject with comments and history
- Real-time statistics and filtering capabilities
- Email notifications with professional templates

## 🛠️ **Technology Stack**

- **Backend**: Flask 2.3+ (Python), PostgreSQL, SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, jQuery
- **Authentication**: Werkzeug security with session management
- **Email**: Flask-Mail with Gmail SMTP integration
- **APIs**: ExchangeRate API for currency conversion

## 📁 **Project Structure**

```
ExpenseFlow/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── api_routes.py              # API endpoints
├── email_service.py           # Email functionality
├── templates/                 # HTML templates
│   ├── employee_dashboard.html # Employee interface
│   ├── manager_dashboard.html  # Manager approval interface
│   └── admin_dashboard.html    # Admin user management
└── static/                    # CSS, JS, images
```

## 🗄️ **Database Schema**

| Table | Key Fields | Purpose |
|-------|------------|---------|
| **Companies** | name, base_currency_code | Organization setup |
| **Users** | name, email, role, company_id, manager_id | User management |
| **Expenses** | category, amount_spent, currency_spent, status | Expense tracking |
| **ExpenseApprovals** | expense_id, approver_user_id, action, comments | Approval workflow |

## 🔧 **Configuration**

### Required Environment Variables
```env
DATABASE_URL=postgresql://username:password@localhost/expense_management
SECRET_KEY=your-secret-key-change-this-in-production
```

### Optional Email Configuration
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 🌐 **API Endpoints**

### Core Routes
- `GET /dashboard` - Role-based dashboard routing
- `GET,POST /api/expenses` - Expense CRUD operations
- `POST /api/expenses/<id>/approve` - Approval workflow
- `GET,POST /api/admin/users` - User management (Admin only)

### Authentication
- `GET,POST /login` - User authentication
- `GET,POST /register` - User registration

## 🐛 **Troubleshooting**

| Issue | Solution |
|-------|----------|
| Database connection error | Check PostgreSQL is running, verify DATABASE_URL |
| Email not working | Use Gmail app password, verify MAIL_* settings |
| Currency conversion issues | Check internet connection, API accessibility |

## 🚀 **Deployment**

For production:
- Use Gunicorn/uWSGI instead of Flask dev server
- Set up Nginx reverse proxy
- Enable HTTPS
- Configure database backups
- Set up logging and monitoring

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

---

**ExpenseFlow** - Streamlining expense management for modern businesses 💼
