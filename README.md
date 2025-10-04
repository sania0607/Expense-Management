# 🌟 Expenseflow

### 📌 **Smart User Management**
- **Auto-Company Setup**: Automatically create company profiles in local currency
- **Role-Based Access**: Assign roles and manage team permissions with ease
- **Team Management**: Streamlined onboarding and user administration
- **Multi-Level Hierarchy**: Support for complex organizational structures

### 🧾 **Effortless Expense Submission**
- **Multi-Currency Support**: Submit claims in any currency with real-time conversion
- **OCR Receipt Processing**: Upload receipts with intelligent text extraction
- **Real-Time Tracking**: Monitor approval status and reimbursement progress
- **Mobile-First Design**: On-the-go expense reporting capabilities

### ✅ **Flexible Approval Workflows**
- **Customizable Rules**: Percentage-based, specific approver, or hybrid workflows
- **Multi-Level Approvals**: Configure complex approval chains
- **Policy Compliance**: Automatic policy checking and enforcement
- **Delegation Support**: Temporary approval delegation during absence

### 🌍 **Global Currency & Transparency**
- **Live Currency Conversion**: Real-time exchange rates for accurate reporting
- **Clear Dashboards**: Full expense visibility with comprehensive analytics
- **Advanced Reporting**: Track spending patterns and budget compliance
- **Financial Integration**: Seamless connection with accounting systems

### 🔒 **User Authentication**
- Secure login and registration system
- Password hashing with Werkzeug security
- Session management for personalized experienceExpenseFlow** is a comprehensive expense management platform designed for modern businesses. It streamlines expense tracking, automates approval workflows, and provides real-time financial insights with multi-currency support and intelligent automation.

## 💼 ExpenseFlow - Modern Expense Management System

**ExpenseFlow** is a comprehensive expense management platform designed for modern businesses. It streamlines expense tracking, automates approval workflows, and provides real-time financial insights with multi-currency support and intelligent automation.

## 🌟 Features

### 👥 **Role-Based User Management**
- **Multi-Role Support**: Admin, Manager, and Employee roles with specific permissions
- **Company-Based Organization**: Auto-company setup with country-based currency configuration
- **Team Hierarchy**: Manager-employee relationships with approval delegation
- **Secure Authentication**: Password hashing with session management

### 💰 **Comprehensive Expense Management**
- **Multi-Currency Support**: Submit expenses in any currency with real-time conversion
- **Receipt Upload**: Upload and manage receipt attachments
- **Smart Categorization**: Pre-defined expense categories (Travel, Meals, Office Supplies, etc.)
- **Status Tracking**: Draft → Submitted → Approved/Rejected workflow

### ✅ **Advanced Approval Workflows**
- **Manager Dashboard**: Dedicated interface for reviewing and approving expenses
- **Bulk Actions**: Approve or reject multiple expenses at once
- **Approval History**: Track all approval actions with comments and timestamps
- **Real-time Statistics**: Pending, approved, and rejected expense counts

### 📊 **Employee Dashboard**
- **Expense Creation**: Easy-to-use expense submission form
- **Visual Workflow**: Step-by-step expense process visualization
- **Statistics Overview**: Personal expense tracking and analytics
- **Receipt Management**: Upload and preview receipt images

### 🌍 **Global Currency Support**
- **Live Exchange Rates**: Real-time currency conversion using ExchangeRate API
- **Multi-Currency Display**: Show original amount and converted base currency
- **Country-Based Setup**: Automatic currency assignment based on user's country
- **Base Currency Reporting**: Standardized reporting in company's base currency

### 📧 **Email Integration**
- **Password Reset**: Automated password reset emails with secure tokens
- **SMTP Configuration**: Gmail SMTP integration with app passwords
- **Professional Templates**: HTML email templates for better user experience
- **Email Service**: Centralized email handling with error management

## 🏗️ **System Architecture**

### User Roles & Permissions
```
├── Admin
│   ├── User Management (Create, Edit, Delete users)
│   ├── Company Settings
│   ├── System Configuration
│   └── Full Access to All Features
│
├── Manager
│   ├── Approve/Reject Expenses
│   ├── View Team Expenses
│   ├── Bulk Approval Actions
│   └── Approval Analytics
│
└── Employee
    ├── Create & Submit Expenses
    ├── Upload Receipts
    ├── Track Personal Expenses
    └── View Approval Status
```

### Expense Workflow
```
1. Employee Creates Expense (Draft)
2. Employee Submits for Approval
3. Manager Reviews Expense
4. Manager Approves/Rejects with Comments
5. Employee Receives Notification
6. Expense Marked as Final Status
```

## 🚀 **Technology Stack**

- **Backend**: Flask 2.3+ (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, jQuery
- **Authentication**: Werkzeug security, Flask sessions
- **Email**: Flask-Mail with Gmail SMTP
- **APIs**: ExchangeRate API for currency conversion
- **Environment**: Python-dotenv for configuration

## 🛠️ **Installation & Setup**

### Prerequisites
1. **Python 3.8 or higher**
2. **PostgreSQL** installed and running
3. **Gmail account** for email functionality (optional)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sania0607/Expense-Management.git
   cd Expense-Management
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file:
   ```env
   # Database Configuration
   DATABASE_URL=postgresql://username:password@localhost/expense_management
   SECRET_KEY=your-secret-key-change-this-in-production
   
   # Email Configuration (Optional)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

4. **Set up the database:**
   ```bash
   python -c "from app import app; from database import db; app.app_context().push(); db.create_all()"
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the application:**
   Open your browser and go to `http://localhost:5000`

## 📁 **Project Structure**

```
ExpenseFlow/
├── app.py                    # Main Flask application
├── models.py                 # Database models (User, Company, Expense, etc.)
├── database.py               # Database configuration
├── api_routes.py            # API endpoints for expense management
├── email_service.py         # Email service for notifications
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── README.md               # Project documentation
├── LICENSE                 # MIT License
├── .gitignore              # Git ignore rules
├── templates/              # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── landing.html        # Landing page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── employee_dashboard.html  # Employee expense interface
│   ├── manager_dashboard.html   # Manager approval interface
│   └── admin_dashboard.html     # Admin user management
└── static/                 # Static assets
    ├── css/                # Custom stylesheets
    ├── js/                 # JavaScript files
    ├── images/             # Image assets
    ├── fonts/              # Font files
    └── vendor/             # Third-party libraries (Bootstrap, jQuery)
```

## 🗄️ **Database Schema**

### Core Tables

#### Companies
- `id` (Primary Key)
- `name` (Company name)
- `base_currency_code` (e.g., USD, EUR, INR)
- `created_at`

#### Users
- `id` (Primary Key)
- `name` (Full name)
- `email` (Unique)
- `password_hash` (Hashed password)
- `role` (Admin, Manager, Employee)
- `company_id` (Foreign Key → companies.id)
- `manager_id` (Foreign Key → users.id, self-referential)
- `created_at`

#### Expenses
- `id` (Primary Key)
- `user_id` (Foreign Key → users.id)
- `category` (Expense category)
- `description` (Expense details)
- `date` (Expense date)
- `amount_spent` (Original amount)
- `currency_spent` (Original currency)
- `final_amount_base_currency` (Converted amount)
- `status` (Draft, Submitted, Approved, Rejected)
- `receipt_url` (Receipt file path)
- `created_at`, `updated_at`

#### ExpenseApprovals
- `id` (Primary Key)
- `expense_id` (Foreign Key → expenses.id)
- `approver_user_id` (Foreign Key → users.id)
- `action` (Approved, Rejected)
- `comments` (Approval comments)
- `approval_date`
- `created_at`

## 🌐 **API Endpoints**

### Authentication
- `GET /` - Landing page
- `GET,POST /login` - User authentication
- `GET,POST /register` - User registration
- `GET /logout` - User logout

### Dashboards
- `GET /dashboard` - Role-based dashboard routing
- `GET /admin` - Admin dashboard (Admin only)

### Expense Management APIs
- `GET,POST /api/expenses` - List/Create expenses
- `GET,PUT,DELETE /api/expenses/<id>` - Expense CRUD operations
- `POST /api/expenses/<id>/submit` - Submit expense for approval
- `POST /api/expenses/<id>/approve` - Approve/Reject expense
- `GET /api/currencies` - Available currencies
- `GET /api/exchange-rate` - Currency conversion rates

### Admin APIs
- `GET,POST /api/admin/users` - User management
- `PUT,DELETE /api/admin/users/<id>` - User CRUD operations
- `POST /api/admin/users/<id>/reset-password` - Password reset
- `GET /api/admin/managers` - List potential managers

## 🎯 **Default User Accounts**

After setup, you can create users through the registration page or use the admin interface.

### Sample Company Structure:
- **Company**: Sample Corp (USD)
- **Admin**: Full system access
- **Manager**: Expense approval rights
- **Employee**: Expense submission rights

## 🔧 **Configuration**

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | Flask secret key | Yes |
| `MAIL_SERVER` | SMTP server (gmail: smtp.gmail.com) | No |
| `MAIL_PORT` | SMTP port (gmail: 587) | No |
| `MAIL_USE_TLS` | Enable TLS (gmail: True) | No |
| `MAIL_USERNAME` | Email username | No |
| `MAIL_PASSWORD` | Email password/app password | No |

### Currency Configuration
- Uses ExchangeRate API for real-time conversion
- Supports 160+ currencies
- Automatic fallback to 1:1 conversion if API fails
- Country-based currency auto-detection

## 🐛 **Troubleshooting**

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check PostgreSQL is running
   # Verify DATABASE_URL in .env
   # Ensure database exists
   ```

2. **Email Not Working**
   ```bash
   # Check Gmail app password (not regular password)
   # Verify MAIL_* settings in .env
   # Test with email service manually
   ```

3. **Currency Conversion Issues**
   ```bash
   # Check internet connection
   # Verify ExchangeRate API accessibility
   # Check for API rate limits
   ```

### Debug Mode
Set `FLASK_DEBUG=1` for detailed error messages in development.

## 🚀 **Deployment**

### Production Considerations
- Use a production WSGI server (e.g., Gunicorn)
- Set up reverse proxy (e.g., Nginx)
- Use environment variables for secrets
- Enable HTTPS
- Set up database backups
- Configure logging and monitoring

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Flask framework and community
- Bootstrap for responsive UI components
- ExchangeRate API for currency conversion
- PostgreSQL for robust data storage

---

**ExpenseFlow** - Streamlining expense management for modern businesses 💼

### 🗺️ **Smart Route Planning**
- **SafePath Route**: Prioritizes safety with advanced algorithms
- **Quick Route**: Fastest path with minimum safety threshold
- **Real-time Safety Calculation**: Uses community reports and multiple safety factors
- **Interactive Map**: Powered by Leaflet.js with OpenStreetMap integration

### � **Community Safety Platform**
- **Incident Reporting**: Users can report scams, harassment, theft, and other safety concerns
- **Community Validation**: Helpful voting system for report verification
- **Real-time Alerts**: Stay informed about safety issues in your area
- **Filtering & Search**: Filter reports by type, location, and date

### 🔒 **User Authentication**
- Secure login and registration system
- Session management for personalized experience

## 🧠 **ExpenseFlow Workflow**

Our intelligent expense processing system automates the entire lifecycle:

```
Expense Lifecycle = Submission → Validation → Approval → Processing → Reimbursement
```

### Workflow Components:
- **Smart Categorization (25%)**: AI-powered expense classification
- **Policy Validation (30%)**: Automatic compliance checking
- **Approval Routing (25%)**: Dynamic workflow assignment
- **Financial Processing (20%)**: Integration with accounting systems

## 🚀 **Technology Stack**

- **Backend**: Flask 2.3.3 (Python)
- **Database**: PostgreSQL with psycopg2-binary
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Authentication**: Werkzeug security, Flask sessions
- **Environment**: Python-dotenv for configuration
- **File Processing**: OCR capabilities for receipt scanning
- **Currency API**: Real-time exchange rate integration

## Demo Credentials

- **Username:** admin, **Password:** password123
- **Username:** user, **Password:** mypassword

## Prerequisites

1. **Python 3.7 or higher**
2. **PostgreSQL** installed and running
3. **PostgreSQL user** with database creation privileges

## Installation

1. **Clone or download the project**

2. **Install Python dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL:**
   - Install PostgreSQL if not already installed
   - Create a PostgreSQL user (or use existing one)
   - Note down your database credentials

4. **Configure environment variables:**
   ```
   copy .env.example .env
   ```
   Edit `.env` file with your PostgreSQL credentials:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/expenseflow_db
   SECRET_KEY=your-secret-key-change-this-in-production
   
   # Or use individual components:
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=expenseflow_db
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

5. **Set up the database:**
   ```
   python setup_db.py
   ```

## Running the Application

1. **Navigate to the project directory**
2. **Run the Flask application:**
   ```
   python app.py
   ```
3. **Open your browser and go to** `http://localhost:5000`

## Project Structure

```
expenseflow/
├── app.py                    # Main Flask application with routing
├── database.py               # Database connection and operations
├── setup_db.py               # Database setup script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .env                      # Your environment variables
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── landing.html         # Landing page
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── home.html            # Main dashboard
│   ├── community_reports.html # Expense reports feed
│   └── submit_report.html   # Expense submission form
└── static/                  # Static files
    ├── css/                 # Stylesheets
    ├── js/                  # JavaScript files
    ├── images/              # Image assets
    ├── fonts/               # Font files
    └── vendor/              # Third-party libraries
```

## Database Schema

### Users Table
- `id` (Primary Key, Serial)
- `username` (Unique, VARCHAR(50))
- `email` (Unique, VARCHAR(100))
- `password_hash` (VARCHAR(255))
- `created_at` (Timestamp)
- `last_login` (Timestamp)

### Reports Table (Expense Reports)
- `id` (Primary Key, Serial)
- `user_id` (Foreign Key → users.id)
- `type` (VARCHAR(50)) # expense category
- `title` (VARCHAR(200))
- `description` (TEXT)
- `location` (VARCHAR(300))
- `severity` (VARCHAR(20)) # expense amount tier
- `time_of_day` (VARCHAR(20))
- `is_anonymous` (BOOLEAN)
- `notify_authorities` (BOOLEAN) # notify finance team
- `helpful_count` (INTEGER) # approval votes
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Reports_Helpful Table (Approval Tracking)
- `id` (Primary Key, Serial)
- `report_id` (Foreign Key → reports.id)
- `user_id` (Foreign Key → users.id)
- `created_at` (Timestamp)
- Unique constraint: (report_id, user_id)

## API Endpoints

### Authentication
- `GET /` - Landing page
- `GET,POST /login` - User login
- `GET,POST /register` - User registration
- `GET /logout` - User logout

### Main Application
- `GET /home` - Main dashboard with expense overview (protected)
- `GET /reports` - Expense reports feed (protected)
- `GET /submit_report` - Expense submission form (protected)
- `POST /submit_report` - Submit new expense report (protected)
- `POST /mark_helpful/<report_id>` - Approve expense report (protected)

### API Routes
- `POST /api/nearby-reports` - Get reports for expense analytics

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Complete PostgreSQL connection string | `postgresql://user:pass@localhost:5432/expenseflow_db` |
| `SECRET_KEY` | Flask secret key for sessions | `your-secret-key` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_NAME` | Database name | `expenseflow_db` |
| `DB_USER` | PostgreSQL username | `your_username` |
| `DB_PASSWORD` | PostgreSQL password | `your_password` |

## Troubleshooting

### Database Connection Issues
1. **Check PostgreSQL is running:**
   ```
   # Windows (if using service)
   services.msc
   
   # Check if PostgreSQL service is running
   ```

2. **Verify credentials in .env file**

3. **Test connection manually:**
   ```
   psql -h localhost -U your_username -d postgres
   ```

### Common Errors
- **"database does not exist"** - Run `python setup_db.py`
- **"authentication failed"** - Check username/password in `.env`
- **"could not connect to server"** - Ensure PostgreSQL is running

## 🎯 **Key ExpenseFlow Features**

### Expense Management
- Submit expenses with receipt upload and OCR processing
- Multi-currency support with real-time conversion
- Automated expense categorization and policy compliance
- Real-time approval tracking and notifications

### Approval Workflows
- Configure multi-level approval chains
- Percentage-based or specific approver routing
- Delegation support for temporary approval transfers
- Policy enforcement with automatic compliance checking

### Analytics & Reporting
- Comprehensive expense dashboards and insights
- Budget tracking and spending pattern analysis
- Real-time financial reporting and export capabilities
- Integration with accounting systems and HR platforms

## 🌍 **Demo Setup**

Currently configured with sample expense data and workflows.
**Demo Company**: ExpenseFlow Demo Corp
**Currency**: INR (Indian Rupees) with multi-currency support

## Security Notes

- Change the secret key in production
- Use environment variables for sensitive data
- Implement additional security measures like CSRF protection
- Use HTTPS in production
- Consider implementing password complexity requirements
- Add rate limiting for login attempts
- Implement proper logging and monitoring
