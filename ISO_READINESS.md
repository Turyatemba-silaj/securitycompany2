# ISO Readiness Baseline

This project has been hardened toward an ISO 27001-style information security baseline for an ERP/security-management system. Passing an ISO audit still requires organizational evidence, policies, risk treatment records, internal audits, staff training, vendor reviews, and management approval. The software can support those controls, but it cannot by itself certify the organization.

## Implemented Technical Controls

| Control area | Project baseline |
| --- | --- |
| Access control | Staff ERP routes require authenticated `is_staff` users. Public pages remain available without login. |
| Auditability | Authenticated write requests are recorded in immutable `AuditLog` records with user, action, path, status, IP, and user agent. |
| Secure configuration | Production mode requires `DJANGO_SECRET_KEY` and explicit `DJANGO_ALLOWED_HOSTS`. Debug mode is environment-controlled. |
| Web hardening | Security middleware, secure cookie flags, HSTS controls, content sniffing protection, clickjacking protection, and referrer policy are configured. |
| Data protection | Upload memory limits are configured. Employee documents and job applications remain under controlled media storage. |
| Payroll governance | Salary is handled inside Payroll, alongside salary advances and recovery records. |
| Evidence exports | Existing CSV exports and reports support management review and operational evidence. |

## Production Deployment Requirements

Set these variables before deployment:

```text
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=<strong unique secret>
DJANGO_ALLOWED_HOSTS=<domain1,domain2>
DJANGO_SECURE_SSL_REDIRECT=true
DJANGO_SESSION_COOKIE_SECURE=true
DJANGO_CSRF_COOKIE_SECURE=true
DJANGO_AUDIT_LOG_ENABLED=true
```

Use PostgreSQL or another managed database for production. SQLite is acceptable for local development only.

## Auditor Evidence To Maintain

| Evidence | Owner | Frequency |
| --- | --- | --- |
| Information security policy | Management | Annual review |
| Risk register and treatment plan | Security/Management | Quarterly or after major change |
| Access review for staff users | System admin | Monthly |
| Backup and restore test record | IT | Monthly |
| Incident register review | Operations/Security | Monthly |
| Payroll approval and reconciliation evidence | Finance | Each pay cycle |
| Supplier/vendor review | Procurement/Management | Annual review |
| Internal audit report | Appointed internal auditor | Before certification audit |
| Corrective action register | Management representative | Ongoing |

## Remaining Certification Gaps

- Role-based permissions should be mapped to job duties, for example HR, Finance, Operations, and Administrator roles.
- Database backups, retention, encryption, and restore testing must be implemented in the hosting environment.
- Media files containing employee documents should be stored in encrypted private storage, not served directly from public media URLs in production.
- Formal change management, code review, release approval, and vulnerability management workflows must be documented and followed.
- Disaster recovery objectives, logging retention, and incident response escalation times must be approved by management.
- A certification body will require interviews and sampled evidence from actual operations.

## Suggested ISO Scope Statement

The information security management system covers the design, operation, support, and maintenance of the Security Company ERP platform used for operations, human resources, payroll, finance, incidents, contracts, documents, public recruitment, and management reporting.