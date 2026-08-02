from django.contrib import admin
from .models import (
    # Operations Department
    AuditLog, Client, Contract, ContractDeliverable, Region, Site, Shift, Asset, AssetAssignment, Incident, IncidentNotification, Patrol_Log, Deployment, DeploymentArea,
    # Human Resources Department
    Role, Position, Employee, Guard, Supervisor, Training, Attendance, Leave, 
    Disciplinary_Action, DisciplinaryNotification, Performance_Evaluation, Document,
    # Finance Department
    Salary, PayrollDeduction, Advance, AdvanceRecovery, Invoice, InvoiceBillableItem, InvoiceBillableItemPrice, Paymee, Payment, Supplier, ProcurementRequisition, ProcurementApproval, SupplierProformaInvoice, SupplierProformaItemPrice, SupplierProformaInvoiceItem, PurchaseOrder, GoodsReceivedNote, SupplierInvoice, SupplierPayment, ProcurementNotification, Budget, Expense, ExpenseNotification, BudgetNotification,
    WebsiteAdvertisement, CompanyEvent, WebsiteResource, AssociatedLink, JobPosting, JobApplication
)


# ==================== GOVERNANCE AND AUDIT ====================

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('audit_id', 'created_at', 'username', 'action', 'method', 'status_code', 'path', 'ip_address')
    list_filter = ('action', 'method', 'status_code', 'created_at')
    search_fields = ('username', 'path', 'ip_address', 'user_agent')
    readonly_fields = ('user', 'username', 'action', 'path', 'method', 'status_code', 'ip_address', 'user_agent', 'created_at')
    ordering = ('-created_at', '-audit_id')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# ==================== OPERATIONS DEPARTMENT ====================

class SiteInline(admin.TabularInline):
    model = Site
    extra = 1


class ContractInline(admin.TabularInline):
    model = Contract
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'client_name', 'contact_person', 'phone_number')
    list_filter = ('created_at',)
    search_fields = ('client_name', 'contact_person', 'email')
    inlines = [SiteInline, ContractInline]


class ContractDeliverableInline(admin.TabularInline):
    model = ContractDeliverable
    extra = 1
    readonly_fields = ('amount',)

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_id', 'contract_number', 'client', 'day_shift_guards', 'night_shift_guards', 'number_of_guards', 'rate_per_guard', 'contract_value', 'contract_status')
    list_filter = ('contract_status', 'contract_start_date', 'contract_end_date', 'client')
    search_fields = ('contract_number', 'client__client_name', 'client__contact_person', 'client__email')
    readonly_fields = ('contract_number', 'number_of_guards', 'contract_value')
    inlines = [ContractDeliverableInline]



@admin.register(ContractDeliverable)
class ContractDeliverableAdmin(admin.ModelAdmin):
    list_display = ('deliverable_id', 'contract', 'item_name', 'quantity', 'unit_price', 'amount')
    list_filter = ('contract', 'created_at')
    search_fields = ('item_name', 'contract__client__client_name')
    readonly_fields = ('amount',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_id', 'region_name', 'description')
    search_fields = ('region_name', 'description')
@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('site_id', 'region', 'site_name', 'site_address', 'day_shift_guards', 'night_shift_guards', 'number_of_guards', 'assigned_guards')
    list_filter = ('region', 'client', 'contract', 'created_at')
    search_fields = ('site_name', 'site_address', 'region__region_name', 'guards__first_name', 'guards__last_name', 'guards__employee_number')
    filter_horizontal = ('guards',)


class DeploymentInline(admin.TabularInline):
    model = Deployment
    extra = 1


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('shift_id', 'shift_type', 'start_time', 'end_time', 'hours_per_shift')
    list_filter = ('shift_type',)
    inlines = [DeploymentInline]


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'asset_type', 'asset_name', 'asset_number', 'quantity')
    list_filter = ('asset_type', 'created_at')
    search_fields = ('asset_name', 'asset_number')


@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_id', 'asset', 'quantity', 'assigned_to', 'site', 'deployment', 'status')
    list_filter = ('status', 'asset__asset_type', 'site', 'assigned_date')
    search_fields = ('asset__asset_name', 'asset__asset_number', 'guard__first_name', 'guard__last_name', 'driver__first_name', 'driver__last_name', 'site__site_name')


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('incident_id', 'incident_type', 'site', 'severity_level', 'status', 'date_time', 'reported_by')
    list_filter = ('incident_type', 'severity_level', 'status', 'date_time', 'site')
    search_fields = ('site__site_name', 'reported_by', 'reported_to', 'description', 'occurrence_summary', 'conclusion')

@admin.register(IncidentNotification)
class IncidentNotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'incident', 'recipient', 'authority_group', 'status', 'notified_at')
    list_filter = ('authority_group', 'status', 'notified_at')
    search_fields = ('incident__site__site_name', 'recipient__first_name', 'recipient__last_name', 'recipient__email')

@admin.register(Patrol_Log)
class Patrol_LogAdmin(admin.ModelAdmin):
    list_display = ('patrol_id', 'site', 'patrol_date', 'patrol_route', 'duration')
    list_filter = ('patrol_date', 'site')
    search_fields = ('patrol_route', 'site__site_name')


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = ('deployment_id', 'client', 'site', 'shift_summary', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'shift_coverage', 'client', 'start_date', 'site')
    search_fields = ('client__client_name', 'site__site_name')



@admin.register(DeploymentArea)
class DeploymentAreaAdmin(admin.ModelAdmin):
    list_display = ('deployment_area_id', 'employee', 'region', 'start_date', 'end_date', 'status', 'transferred_by_hr_manager')
    list_filter = ('status', 'region', 'start_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'region__region_name', 'transferred_by_hr_manager__first_name', 'transferred_by_hr_manager__last_name')
# ==================== HUMAN RESOURCES DEPARTMENT ====================

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name', 'department')
    list_filter = ('department',)
    search_fields = ('role_name',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_id', 'position_title', 'department', 'grade_level')
    list_filter = ('department', 'grade_level')
    search_fields = ('position_title',)


class GuardInline(admin.TabularInline):
    model = Guard
    extra = 0


class SupervisorInline(admin.TabularInline):
    model = Supervisor
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'employee_number', 'first_name', 'last_name', 'role', 'position', 'department', 'daily_rate', 'is_reliever', 'email', 'nssf_number', 'status', 'hire_date')
    list_filter = ('status', 'role', 'is_reliever', 'position', 'department', 'hire_date', 'gender')
    search_fields = ('employee_number', 'first_name', 'last_name', 'email', 'national_id', 'nssf_number')
    readonly_fields = ('employee_number', 'salary_scale', 'daily_rate', 'created_at', 'updated_at')
    ordering = ('employee_id',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(employee_number__iexact=search_term)
        return queryset, use_distinct

@admin.register(Guard)
class GuardAdmin(admin.ModelAdmin):
    list_display = ('employee', 'qualification', 'armed_status')
    list_filter = ('qualification', 'armed_status')
    search_fields = ('employee__first_name', 'employee__last_name')


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('supervisor_id', 'employee', 'authority_level')
    list_filter = ('authority_level',)
    search_fields = ('employee__first_name', 'employee__last_name')


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('training_id', 'training_type', 'trainee', 'training_name', 'provider', 'start_date', 'end_date')
    list_filter = ('training_type', 'start_date', 'end_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'recruit', 'training_name', 'provider')
    exclude = ('certificate_no',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_id', 'site', 'shift', 'scheduled_guard', 'present', 'attended_guard', 'date')
    list_filter = ('date', 'site', 'shift', 'present')
    search_fields = ('employee__first_name', 'employee__last_name', 'scheduled_guard__first_name', 'scheduled_guard__last_name', 'attended_guard__first_name', 'attended_guard__last_name')


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('leave_id', 'employee', 'leave_type', 'start_date', 'end_date', 'operations_verification_status', 'approval_status', 'verified_by', 'approved_by')
    list_filter = ('leave_type', 'operations_verification_status', 'approval_status', 'start_date')
    search_fields = ('employee__first_name', 'employee__last_name')


@admin.register(Disciplinary_Action)
class Disciplinary_ActionAdmin(admin.ModelAdmin):
    list_display = ('action_id', 'employee', 'offence_committed', 'offence_date', 'status', 'outcome', 'approval_status')
    list_filter = ('status', 'outcome', 'approval_status', 'offence_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'offence_committed', 'description', 'steps_taken', 'conclusion')



@admin.register(DisciplinaryNotification)
class DisciplinaryNotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'disciplinary_action', 'recipient', 'status', 'notified_at')
    list_filter = ('status', 'notified_at')
    search_fields = ('disciplinary_action__offence_committed', 'recipient__first_name', 'recipient__last_name', 'recipient__email', 'message')

@admin.register(Performance_Evaluation)
class Performance_EvaluationAdmin(admin.ModelAdmin):
    list_display = ('eval_id', 'employee', 'review_period_start', 'review_period_end', 'overall_score', 'rating', 'status', 'evaluated_by')
    list_filter = ('rating', 'status', 'review_period_start', 'review_period_end')
    search_fields = ('employee__first_name', 'employee__last_name', 'strengths', 'areas_for_improvement', 'goals')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_id', 'employee', 'doc_type', 'expiry_date')
    list_filter = ('doc_type', 'expiry_date')
    search_fields = ('employee__first_name', 'employee__last_name')


# ==================== FINANCE DEPARTMENT ====================

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('salary_id', 'employee', 'shifts_worked', 'daily_rate', 'basic_salary', 'loan_deduction', 'medical_deduction', 'total_deductions', 'total_salary', 'pay_period')
    list_filter = ('pay_period',)
    search_fields = ('employee__first_name', 'employee__last_name')
    readonly_fields = ('shifts_worked', 'daily_rate', 'basic_salary', 'overtime_pay', 'gross_pay', 'loan_deduction', 'medical_deduction', 'other_payroll_deductions', 'ledger_installment_amount', 'total_deductions', 'total_salary', 'created_at', 'updated_at')


@admin.register(PayrollDeduction)
class PayrollDeductionAdmin(admin.ModelAdmin):
    list_display = ('deduction_id', 'employee', 'category', 'amount', 'start_date', 'end_date', 'status')
    list_filter = ('category', 'status', 'start_date', 'end_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__employee_number', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Advance)
class AdvanceAdmin(admin.ModelAdmin):
    list_display = ('advance_id', 'employee', 'amount_requested', 'installment_amount', 'balance', 'approval_status', 'status')
    list_filter = ('approval_status', 'status', 'created_at')
    search_fields = ('employee__first_name', 'employee__last_name', 'strengths', 'areas_for_improvement', 'goals')


@admin.register(AdvanceRecovery)
class AdvanceRecoveryAdmin(admin.ModelAdmin):
    list_display = ('recovery_id', 'employee', 'advance', 'salary', 'amount', 'installment_amount', 'balance', 'period_start_date', 'period_end_date')
    list_filter = ('period_start_date', 'period_end_date', 'created_at')
    search_fields = ('employee__first_name', 'employee__last_name', 'strengths', 'areas_for_improvement', 'goals')
    readonly_fields = ('created_at',)


@admin.register(InvoiceBillableItemPrice)
class InvoiceBillableItemPriceAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'unit_price', 'taxable', 'active', 'updated_at')
    list_filter = ('active', 'taxable')
    search_fields = ('item_name',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1


class InvoiceBillableItemInline(admin.TabularInline):
    model = InvoiceBillableItem
    extra = 3
    readonly_fields = ('amount',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'contract', 'client', 'invoice_date', 'due_date', 'deployed_guards', 'contract_amount', 'tax_amount', 'total_amount', 'status')
    list_filter = ('status', 'invoice_date', 'client', 'contract')
    search_fields = ('invoice_number', 'client__client_name', 'contract__contract_number')
    readonly_fields = ('invoice_number', 'deployed_guards', 'rate_per_guard', 'contract_amount', 'tax_amount', 'total_amount')
    inlines = [InvoiceBillableItemInline, PaymentInline]


@admin.register(Paymee)
class PaymeeAdmin(admin.ModelAdmin):
    readonly_fields = ('client', 'total_amount', 'amount_paid', 'balance_amount', 'overpaid_amount', 'due_date', 'last_payment_date', 'aging_days', 'status')
    list_display = ('invoice', 'client', 'total_amount', 'amount_paid', 'balance_amount', 'due_date', 'aging_days', 'status')
    list_filter = ('status', 'due_date', 'currency')
    search_fields = ('invoice__client__client_name', 'invoice__contract__contract_number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'invoice', 'amount', 'payment_date', 'payment_method')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('invoice__client__client_name', 'transaction_ref')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_code', 'supplier_name', 'contact_person', 'phone_number', 'email', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('supplier_code', 'supplier_name', 'contact_person', 'phone_number', 'email', 'tax_identification_number')
    readonly_fields = ('supplier_code', 'created_at', 'updated_at')


@admin.register(ProcurementRequisition)
class ProcurementRequisitionAdmin(admin.ModelAdmin):
    list_display = ('requisition_number', 'title', 'department', 'budget', 'required_date', 'estimated_amount', 'requested_by', 'status')
    list_filter = ('department', 'category', 'status', 'required_date')
    search_fields = ('requisition_number', 'title', 'description', 'requested_by__first_name', 'requested_by__last_name')
    readonly_fields = ('requisition_number', 'approved_amount', 'created_at', 'updated_at')


@admin.register(ProcurementApproval)
class ProcurementApprovalAdmin(admin.ModelAdmin):
    list_display = ('approval_id', 'requisition', 'approved_by', 'decision', 'approved_amount', 'decided_at')
    list_filter = ('decision', 'decided_at')
    search_fields = ('requisition__requisition_number', 'requisition__title', 'approved_by__first_name', 'approved_by__last_name')
    readonly_fields = ('decided_at', 'created_at', 'updated_at')


@admin.register(SupplierProformaItemPrice)
class SupplierProformaItemPriceAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'unit_price', 'tax_rate', 'discount_allowed', 'max_discount_rate', 'active', 'updated_at')
    list_filter = ('active', 'discount_allowed')
    search_fields = ('item_name',)


class SupplierProformaInvoiceItemInline(admin.TabularInline):
    model = SupplierProformaInvoiceItem
    extra = 3
    readonly_fields = ('description', 'unit_price', 'tax_rate', 'line_total', 'tax_amount', 'total_amount')


@admin.register(SupplierProformaInvoice)
class SupplierProformaInvoiceAdmin(admin.ModelAdmin):
    list_display = ('proforma_number', 'supplier_reference', 'requisition', 'supplier', 'proforma_date', 'total_amount', 'status', 'purchase_order')
    list_filter = ('status', 'proforma_date', 'supplier')
    search_fields = ('proforma_number', 'supplier_reference', 'supplier__supplier_name', 'requisition__requisition_number')
    readonly_fields = ('proforma_number', 'subtotal_amount', 'tax_amount', 'total_amount', 'purchase_order', 'created_at', 'updated_at')
    inlines = [SupplierProformaInvoiceItemInline]


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'requisition', 'supplier', 'order_date', 'expected_delivery_date', 'total_amount', 'status')
    list_filter = ('status', 'order_date', 'expected_delivery_date', 'supplier')
    search_fields = ('po_number', 'requisition__requisition_number', 'supplier__supplier_name')
    readonly_fields = ('po_number', 'total_amount', 'created_at', 'updated_at')


@admin.register(GoodsReceivedNote)
class GoodsReceivedNoteAdmin(admin.ModelAdmin):
    list_display = ('grn_number', 'purchase_order', 'received_date', 'received_by', 'quantity_summary', 'status')
    list_filter = ('status', 'received_date')
    search_fields = ('grn_number', 'purchase_order__po_number', 'delivery_note_number', 'quantity_summary')
    readonly_fields = ('grn_number', 'created_at', 'updated_at')


@admin.register(SupplierInvoice)
class SupplierInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'supplier', 'purchase_order', 'due_date', 'total_amount', 'amount_paid', 'balance_amount', 'status')
    list_filter = ('status', 'invoice_date', 'due_date', 'supplier')
    search_fields = ('invoice_number', 'supplier__supplier_name', 'purchase_order__po_number')
    readonly_fields = ('total_amount', 'amount_paid', 'balance_amount', 'created_at', 'updated_at')


@admin.register(SupplierPayment)
class SupplierPaymentAdmin(admin.ModelAdmin):
    list_display = ('supplier_payment_id', 'supplier_invoice', 'payment_date', 'amount', 'payment_method', 'approval_status', 'payment_status', 'paid_by')
    list_filter = ('payment_method', 'approval_status', 'payment_status', 'payment_date')
    search_fields = ('supplier_invoice__invoice_number', 'supplier_invoice__supplier__supplier_name', 'transaction_ref')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('budget_code', 'budget_title', 'department', 'fiscal_year', 'requested_amount', 'allocated_amount', 'spent_amount', 'remaining_amount', 'approval_status')
    list_filter = ('department', 'budget_category', 'fiscal_year', 'approval_status')
    search_fields = ('budget_code', 'budget_title', 'department', 'requisition_reason')
    readonly_fields = ('budget_code', 'spent_amount', 'approved_at', 'created_at', 'updated_at')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_code', 'requisition_title', 'budget', 'requested_amount', 'amount', 'variance_amount', 'expense_date', 'approval_status', 'accountability_status')
    list_filter = ('category', 'verification_status', 'approval_status', 'accountability_status', 'status', 'expense_date')
    search_fields = ('expense_code', 'requisition_title', 'category', 'description', 'receipt_reference', 'requested_by__first_name', 'requested_by__last_name', 'spent_by__first_name', 'spent_by__last_name')
    readonly_fields = ('expense_code', 'accountability_status', 'approved_at', 'accounted_at', 'recorded_at', 'created_at', 'updated_at')












































@admin.register(ProcurementNotification)
class ProcurementNotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'recipient', 'recipient_group', 'notification_type', 'status', 'notified_at')
    list_filter = ('recipient_group', 'notification_type', 'status', 'notified_at')
    search_fields = ('recipient__first_name', 'recipient__last_name', 'message', 'related_model')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BudgetNotification)
class BudgetNotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'budget', 'recipient', 'recipient_group', 'notification_type', 'status', 'notified_at')
    list_filter = ('recipient_group', 'notification_type', 'status', 'notified_at')
    search_fields = ('budget__budget_code', 'budget__budget_title', 'recipient__first_name', 'recipient__last_name', 'message')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ExpenseNotification)
class ExpenseNotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'expense', 'recipient', 'recipient_group', 'notification_type', 'status', 'notified_at')
    list_filter = ('recipient_group', 'notification_type', 'status', 'notified_at')
    search_fields = ('expense__expense_code', 'expense__requisition_title', 'recipient__first_name', 'recipient__last_name', 'message')
    readonly_fields = ('created_at', 'updated_at')


# ==================== PUBLIC WEBSITE ====================

@admin.register(WebsiteAdvertisement)
class WebsiteAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'placement', 'starts_on', 'ends_on', 'is_active')
    list_filter = ('placement', 'is_active', 'starts_on')
    search_fields = ('title', 'message')


@admin.register(CompanyEvent)
class CompanyEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'is_public')
    list_filter = ('is_public', 'event_date')
    search_fields = ('title', 'location', 'summary')


@admin.register(WebsiteResource)
class WebsiteResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'is_public')
    list_filter = ('resource_type', 'is_public')
    search_fields = ('title', 'summary')


@admin.register(AssociatedLink)
class AssociatedLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'is_public')
    list_filter = ('category', 'is_public')
    search_fields = ('title', 'description', 'url')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'employment_type', 'deadline', 'is_online', 'is_active')
    list_filter = ('department', 'employment_type', 'is_online', 'is_active')
    search_fields = ('title', 'summary', 'requirements')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'job', 'application_mode', 'phone_number', 'status', 'submitted_at')
    list_filter = ('application_mode', 'status', 'job')
    search_fields = ('applicant_name', 'phone_number', 'email', 'job__title')






