# � ## 🌟 Features

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

## 🌟 Features

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
