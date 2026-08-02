# Security Company Management System - Setup Guide

## Project Overview
This is a comprehensive Django application for managing security company operations, human resources, and finance departments.

## Current Status
✅ Database models created and migrated
✅ Django Admin interface configured
✅ All relationships defined

## Quick Start

### 1. Run the Development Server
```bash
cd c:\Users\User\OneDrive\Desktop\COMP
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000/`

### 2. Access Django Admin
Navigate to: `http://127.0.0.1:8000/admin/`

Default credentials (if you have superuser):
- Create a superuser if not already done:
```bash
python manage.py createsuperuser
```

### 3. Dashboard Sections in Admin

#### Operations Management
- **Clients** - Manage security company clients
- **Sites** - Manage client locations
- **Deployments** - Assign guards to sites
- **Shifts** - Create and manage work shifts
- **Assets** - Track equipment and vehicles
- **Incidents** - Record security incidents
- **Patrol Logs** - Track patrol activities

#### Human Resources
- **Employees** - Central employee database
- **Guards** - Guard qualifications and status
- **Supervisors** - Supervisor authority levels
- **Roles** - Job roles and positions
- **Training** - Employee training records
- **Attendance** - Track work attendance
- **Leaves** - Manage leave requests
- **Disciplinary Actions** - Record disciplinary events
- **Performance Evaluations** - Employee performance ratings
- **Documents** - Store employee documents (licenses, certificates)

#### Finance Management
- **Salaries** - Employee salary information
- **Advances** - Salary advance requests
- **Invoices** - Client invoices
- **Payments** - Record payments
- **Budgets** - Track department budgets
- **Expenses** - Record expenses

## Model Structure

The system is organized into three main departments:

### Operations Department (7 Models)
- Client, Site, Shift, Asset, Incident, Patrol_Log, Deployment

### Human Resources Department (11 Models)
- Employee, Role, Guard, Supervisor, Position, Training, Attendance, Leave, Disciplinary_Action, Performance_Evaluation, Document

### Finance Department (7 Models)
- Salary, Advance, Invoice, Paymee, Payment, Budget, Expense

**Total: 25 models with complete relationships**

## Key Features

### Comprehensive Field Choices
All models use Django choice fields with predefined options:
- Status fields (active, inactive, pending, etc.)
- Level fields (high, medium, low, critical)
- Type fields (various based on model)

### Automatic Timestamps
All models include:
- `created_at` - Record creation time
- `updated_at` - Last modification time

### Relationships
- One-to-Many relationships (1:M)
- One-to-One relationships (1:1)
- Foreign key constraints with cascading deletes

### Admin Features
- Search capabilities on key fields
- Filtering by status, date, department, etc.
- Inline editing for related records
- Read-only timestamps

## Sample Data Entry

### To Add a Client:
1. Go to Admin > Clients > Add Client
2. Fill in:
   - Client Name
   - Contact Person
   - Phone/Email
   - Address
   - Contract dates
   - Contract Status (active/expired/pending/terminated)

### To Add an Employee:
1. Go to Admin > Employees > Add Employee
2. Fill in:
   - Name (First & Last)
   - Date of Birth
   - Gender
   - Contact Information
   - National ID (must be unique)
   - Role
   - Hire Date
   - Status

### To Create a Guard:
1. First, create an Employee
2. Go to Admin > Guards > Add Guard
3. Select the employee
4. Set qualification and armed status

### To Deploy a Guard:
1. Go to Admin > Deployments > Add Deployment
2. Select Site and Shift
3. Set start date, end date, and status

## Common Management Tasks

### Managing Client Contracts
1. Navigate to Clients
2. Edit contract dates and status as needed
3. All related sites will be accessible from each client

### Tracking Deployments
1. Go to Deployments
2. View all active deployments
3. Update status from "active" to "completed"

### Processing Leave Requests
1. Go to Leaves
2. Filter by "Pending" status
3. Review and update approval_status
4. Select approver (Employee)

### Financial Management
- Track salary advances and approvals
- Record client invoices and payments
- Monitor budget spending by department
- Log expenses by category

## Database Schema
See `MODELS_DOCUMENTATION.md` for complete database schema documentation.

## Future Enhancements

### Views & Templates
- Create web-based dashboard
- Staff management interface
- Reporting system

### API Development
- REST API for mobile apps
- GraphQL endpoints
- Third-party integrations

### Advanced Features
- Automated email notifications
- Document management system
- Advanced reporting & analytics
- Payroll automation
- Mobile app support

### Security
- Role-based access control (RBAC)
- Permission management
- Audit logging
- Two-factor authentication

## Troubleshooting

### Migration Issues
```bash
# Reset migrations (USE WITH CAUTION)
python manage.py migrate webCom zero
python manage.py makemigrations webCom
python manage.py migrate webCom
```

### Superuser Access Issues
```bash
# Create new superuser
python manage.py createsuperuser
```

### Database Issues
```bash
# Reset database (WARNING: will delete all data)
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

## Next Steps

1. **View the Database Schema**
   - Read `MODELS_DOCUMENTATION.md` for detailed model descriptions

2. **Create Test Data**
   - Use Django Admin to add sample clients, employees, and sites

3. **Develop Views & Templates**
   - Create web-based management interface
   - Build reporting dashboards

4. **Build API Endpoints**
   - Create REST API for mobile/external integrations
   - Implement proper authentication

5. **Add Custom Business Logic**
   - Implement workflow approvals
   - Add salary calculations
   - Create automated reports

## Support Files

- `MODELS_DOCUMENTATION.md` - Detailed model and relationship documentation
- `SecurityCompany/settings.py` - Django configuration
- `webCom/models.py` - All model definitions
- `webCom/admin.py` - Admin interface configuration
- `manage.py` - Django management script

## Tips

✅ Always use the Django Admin interface for data management
✅ Use search and filter features to find records quickly
✅ Review `MODELS_DOCUMENTATION.md` before creating custom views
✅ Test your data workflow in Admin before building custom interfaces
✅ Keep timestamps accurate for audit trails


## ISO Readiness And Production Security

The project now includes a baseline for ISO 27001-style technical controls:

- Staff ERP routes require authenticated staff users.
- Write actions by authenticated users are captured in immutable audit logs.
- Production configuration is environment-driven for secret key, debug mode, allowed hosts, HTTPS redirects, secure cookies, HSTS, upload limits, and email settings.
- Payroll is the parent finance module for salary records and salary advances.

Before any certification audit, review `ISO_READINESS.md`, configure production using `.env.example`, run migrations, and keep operational evidence for access reviews, backups, incident handling, payroll approvals, change management, and management reviews.

Production startup requires at minimum:

```bash
set DJANGO_DEBUG=false
set DJANGO_SECRET_KEY=<strong unique secret>
set DJANGO_ALLOWED_HOSTS=<your production hostnames>
set DATABASE_URL=<hosted postgres connection string>
python manage.py migrate
python manage.py check --deploy
```

For Vercel, add these in Project Settings > Environment Variables before redeploying:

```text
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=<strong unique secret>
DJANGO_ALLOWED_HOSTS=turyans-security.vercel.app,securitycompany2-mvt4.vercel.app
DATABASE_URL=<hosted postgres connection string>
DATABASE_SSL_REQUIRE=true
```

Vercel deployments must use a hosted database such as Vercel Postgres, Neon, Supabase, or another PostgreSQL provider. SQLite is only for local development.
