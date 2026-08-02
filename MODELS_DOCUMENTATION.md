# Security Company Management System - Models Documentation

This document outlines the complete database schema for the Security Company Management System built with Django, following the ERD provided.

---

## Table of Contents
1. [Operations Department](#operations-department)
2. [Human Resources Department](#human-resources-department)
3. [Finance Department](#finance-department)
4. [Relationships Overview](#relationships-overview)

---

## OPERATIONS DEPARTMENT

### Client
Manages security company clients and their contracts.
- **Fields:**
  - client_id (Primary Key - AutoField)
  - client_name (CharField)
  - contact_person (CharField)
  - phone_number (CharField)
  - email (EmailField)
  - address (TextField)
  - contract_start_date (DateField)
  - contract_end_date (DateField)
  - contract_status (Choices: active, expired, pending, terminated)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - One-to-Many with Site
  - One-to-Many with Invoice
  - One-to-Many with Deployment (indirect through Site)

### Site
Manages individual client locations/sites.
- **Fields:**
  - site_id (Primary Key - AutoField)
  - client (ForeignKey to Client)
  - site_name (CharField)
  - site_address (TextField)
  - state (CharField)
  - security_level (Choices: low, medium, high, critical)
  - notes (TextField, optional)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Client
  - One-to-Many with Shift
  - One-to-Many with Asset
  - One-to-Many with Incident
  - One-to-Many with Patrol_Log
  - One-to-Many with Deployment

### Shift
Manages work shifts at sites.
- **Fields:**
  - shift_id (Primary Key - AutoField)
  - site (ForeignKey to Site)
  - shift_date (DateField)
  - start_time (TimeField)
  - end_time (TimeField)
  - hours_per_shift (DecimalField)
  - shift_type (Choices: morning, afternoon, night)
  - description (TextField, optional)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Site
  - One-to-Many with Deployment

### Deployment
Manages deployment of guards to sites.
- **Fields:**
  - deployment_id (Primary Key - AutoField)
  - site (ForeignKey to Site)
  - shift (ForeignKey to Shift, nullable)
  - start_date (DateField)
  - end_date (DateField, optional)
  - status (Choices: active, completed, cancelled)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Site
  - Many-to-One with Shift

### Asset
Manages assets at sites (vehicles, equipment, weapons, uniforms).
- **Fields:**
  - asset_id (Primary Key - AutoField)
  - site (ForeignKey to Site)
  - asset_type (Choices: vehicle, equipment, uniform, weapon, other)
  - asset_number (CharField)
  - quantity (IntegerField)
  - notes (TextField, optional)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Site

### Incident
Manages incidents at sites.
- **Fields:**
  - incident_id (Primary Key - AutoField)
  - site (ForeignKey to Site)
  - incident_type (Choices: theft, breach, vandalism, injury, other)
  - description (TextField)
  - date_time (DateTimeField)
  - location (CharField)
  - severity_level (Choices: low, medium, high, critical)
  - reported_by (CharField)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Site

### Patrol_Log
Manages patrol records.
- **Fields:**
  - patrol_id (Primary Key - AutoField)
  - site (ForeignKey to Site)
  - patrol_date (DateField)
  - patrol_route (CharField)
  - quantity (IntegerField)
  - duration (DecimalField - in hours)
  - issue_date (DateField)
  - return_date (DateField, optional)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Site

---

## HUMAN RESOURCES DEPARTMENT

### Role
Manages employee roles.
- **Fields:**
  - role_id (Primary Key - AutoField)
  - role_name (CharField)
  - department (Choices: operations, hr, finance, admin)
  - description (TextField, optional)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - One-to-Many with Employee

### Position
Manages employee positions and salary grades.
- **Fields:**
  - position_id (Primary Key - AutoField)
  - position_title (CharField)
  - department (Choices: operations, hr, finance, admin)
  - grade_level (CharField)
  - salary_range_min (DecimalField)
  - salary_range_max (DecimalField)
  - description (TextField, optional)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - No direct foreign keys, but used for reference

### Employee
Main employee records.
- **Fields:**
  - employee_id (Primary Key - AutoField)
  - first_name (CharField)
  - last_name (CharField)
  - date_of_birth (DateField)
  - gender (Choices: M, F, O)
  - phone_number (CharField)
  - email (EmailField)
  - address (TextField)
  - national_id (CharField, unique)
  - role (ForeignKey to Role, nullable)
  - hire_date (DateField)
  - status (Choices: active, inactive, on_leave, terminated)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Role
  - One-to-One with Guard (optional)
  - One-to-One with Supervisor (optional)
  - One-to-One with Salary
  - One-to-Many with Training
  - One-to-Many with Attendance
  - One-to-Many with Leave (as employee)
  - One-to-Many with Leave (as approver)
  - One-to-Many with Disciplinary_Action
  - One-to-Many with Performance_Evaluation (as evaluated)
  - One-to-Many with Performance_Evaluation (as evaluator)
  - One-to-Many with Document
  - One-to-Many with Advance (as employee)
  - One-to-Many with Advance (as approver)
  - One-to-Many with Expense

### Guard
Guard-specific information (extends Employee).
- **Fields:**
  - employee (OneToOneField to Employee - Primary Key)
  - qualification (Choices: basic, advanced, specialized)
  - armed_status (Choices: armed, unarmed)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - One-to-One with Employee

### Supervisor
Supervisor-specific information (extends Employee).
- **Fields:**
  - supervisor_id (Primary Key - AutoField)
  - employee (OneToOneField to Employee)
  - authority_level (Choices: site, regional, national)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - One-to-One with Employee

### Training
Employee training records.
- **Fields:**
  - training_id (Primary Key - AutoField)
  - employee (ForeignKey to Employee)
  - training_name (CharField)
  - provider (CharField)
  - start_date (DateField)
  - end_date (DateField)
  - certificate_no (CharField, optional)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Employee

### Attendance
Employee attendance records.
- **Fields:**
  - attendance_id (Primary Key - AutoField)
  - employee (ForeignKey to Employee)
  - date (DateField)
  - time_in (TimeField)
  - time_out (TimeField, optional)
  - remarks (TextField, optional)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Employee

### Leave
Employee leave requests.
- **Fields:**
  - leave_id (Primary Key - AutoField)
  - employee (ForeignKey to Employee)
  - leave_type (Choices: annual, medical, unpaid, maternity, paternity)
  - start_date (DateField)
  - end_date (DateField)
  - reason (TextField)
  - approval_status (Choices: pending, approved, rejected)
  - approved_by (ForeignKey to Employee, nullable)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Employee (as requester)
  - Many-to-One with Employee (as approver)

### Disciplinary_Action
Employee disciplinary records.
- **Fields:**
  - action_id (Primary Key - AutoField)
  - employee (ForeignKey to Employee)
  - description (TextField)
  - action_date (DateField)
  - reason (TextField)
  - approval_status (Choices: pending, approved, rejected)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Employee

### Performance_Evaluation
Employee performance evaluations.
- **Fields:**
  - eval_id (Primary Key - AutoField)
  - employee (ForeignKey to Employee)
  - date (DateField)
  - rating (Choices: 1-5 scale)
  - comments (TextField)
  - evaluated_by (ForeignKey to Employee, nullable)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Employee (as subject)
  - Many-to-One with Employee (as evaluator)

### Document
Employee documents (licenses, certificates, etc.).
- **Fields:**
  - doc_id (Primary Key - AutoField)
  - employee (ForeignKey to Employee)
  - doc_type (Choices: license, certificate, passport, contract, other)
  - file_path (FileField)
  - expiry_date (DateField, optional)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Employee

---

## FINANCE DEPARTMENT

### Salary
Employee salary information.
- **Fields:**
  - salary_id (Primary Key - AutoField)
  - employee (OneToOneField to Employee)
  - basic_salary (DecimalField)
  - allowances (DecimalField)
  - deductions (DecimalField)
  - overtime_pay (DecimalField)
  - bonus (DecimalField)
  - pay_period (Choices: monthly, weekly, biweekly)
  - created_at, updated_at (Auto-timestamps)

- **Computed Property:**
  - total_salary = basic_salary + allowances - deductions + overtime_pay + bonus

- **Relationships:**
  - One-to-One with Employee

### Advance
Salary advance requests.
- **Fields:**
  - advance_id (Primary Key - AutoField)
  - employee (ForeignKey to Employee)
  - amount_requested (DecimalField)
  - approval_status (Choices: pending, approved, rejected)
  - approved_by (ForeignKey to Employee, nullable)
  - disbursement_date (DateField, optional)
  - status (Choices: pending, disbursed, recovered)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Employee (as requester)
  - Many-to-One with Employee (as approver)

### Invoice
Client invoices.
- **Fields:**
  - invoice_id (Primary Key - AutoField)
  - client (ForeignKey to Client)
  - invoice_date (DateField)
  - due_date (DateField)
  - description (TextField)
  - status (Choices: draft, sent, paid, overdue, cancelled)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Client
  - One-to-One with Paymee
  - One-to-Many with Payment

### Paymee
Invoice payment record (tracks overall payment status).
- **Fields:**
  - invoice (OneToOneField to Invoice - Primary Key)
  - total_amount (DecimalField)
  - amount_paid (DecimalField)
  - status (Choices: pending, partial, completed)
  - created_at, updated_at (Auto-timestamps)

- **Computed Property:**
  - balance_amount = total_amount - amount_paid

- **Relationships:**
  - One-to-One with Invoice

### Payment
Individual payment transactions.
- **Fields:**
  - payment_id (Primary Key - AutoField)
  - invoice (ForeignKey to Invoice)
  - payment_date (DateField)
  - amount (DecimalField)
  - payment_method (Choices: cash, check, bank_transfer, credit_card, other)
  - transaction_ref (CharField, optional)
  - remarks (TextField, optional)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Invoice

### Budget
Departmental budgets.
- **Fields:**
  - budget_id (Primary Key - AutoField)
  - department (Choices: operations, hr, finance, admin)
  - year (IntegerField)
  - allocated_amount (DecimalField)
  - spent_amount (DecimalField)
  - created_at, updated_at (Auto-timestamps)

- **Computed Property:**
  - remaining_amount = allocated_amount - spent_amount

- **Unique Constraint:**
  - (department, year)

- **Relationships:**
  - No direct foreign keys

### Expense
Expense records.
- **Fields:**
  - expense_id (Primary Key - AutoField)
  - category (Choices: payroll, operations, training, equipment, admin, other)
  - amount (DecimalField)
  - expense_date (DateField)
  - description (TextField)
  - spent_by (ForeignKey to Employee, nullable)
  - created_at, updated_at (Auto-timestamps)

- **Relationships:**
  - Many-to-One with Employee

---

## Relationships Overview

### One-to-Many Relationships
- Client → Sites
- Client → Invoices
- Site → Shifts
- Site → Assets
- Site → Incidents
- Site → Patrol_Logs
- Site → Deployments
- Role → Employees
- Employee → Training
- Employee → Attendance
- Employee → Leaves (as requester)
- Employee → Disciplinary_Actions
- Employee → Performance_Evaluations (as subject)
- Employee → Documents
- Employee → Advances
- Employee → Expenses
- Invoice → Payments
- Shift → Deployments

### One-to-One Relationships
- Employee ↔ Guard
- Employee ↔ Supervisor
- Employee ↔ Salary
- Invoice ↔ Paymee

### Many-to-One Relationships
- Shift → Site
- Asset → Site
- Incident → Site
- Patrol_Log → Site
- Deployment → Site
- Deployment → Shift
- Employee → Role
- Training → Employee
- Attendance → Employee
- Leave → Employee (both requester and approver)
- Disciplinary_Action → Employee
- Performance_Evaluation → Employee (both subject and evaluator)
- Document → Employee
- Advance → Employee (both requester and approver)
- Payment → Invoice
- Expense → Employee

---

## Next Steps

1. **Create Views and Serializers** - For API endpoints
2. **Create Forms** - For CRUD operations
3. **Develop Admin Customizations** - Enhanced admin interface
4. **Create Reports** - For analytics and reporting
5. **Implement Permissions** - Role-based access control
6. **Create Tests** - Unit and integration tests

---

## Usage Tips

- All models use auto-incrementing primary keys
- All models include `created_at` and `updated_at` timestamps
- Use Django Admin to manage data: `/admin/`
- The app supports filtering, searching, and inline editing in Admin


## Governance And Audit

### AuditLog
Immutable audit records used as technical evidence for staff write activity.

Fields:
- `audit_id` - Primary key
- `user` - Linked Django user where available
- `username` - Username snapshot retained for evidence continuity
- `action` - Classified action such as create, update, delete, or post
- `path` - Request path
- `method` - HTTP method
- `status_code` - Response status code
- `ip_address` - Client IP address when available
- `user_agent` - Browser/client user agent snapshot
- `created_at` - Timestamp when the audit record was written

Audit records cannot be edited or deleted through the model API or admin interface.

## Payroll Module Structure

Payroll is the parent finance module for salary records and salary advances:

- `Salary` stores employee salary calculations, payslip figures, statutory deductions, overtime, and net pay.
- `Advance` stores salary advance requests, approval status, disbursement status, and recovery balances.
- `AdvanceRecovery` records deductions posted against salary periods.