from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

ROLE_GROUPS = {
    "Supervisor": {
        "models": {"attendance"},
        "views": set(),
    },
    "Human Resources": {
        "models": {
            "employees",
            "guards",
            "supervisors",
            "training",
            "leaves",
            "disciplinary-actions",
            "performance-evaluations",
            "documents",
            "payroll",
            "salaries",
            "advances",
            "payroll-deductions",
        },
        "views": {"payroll"},
    },
    "Operations Manager": {
        "models": {
            "clients",
            "contracts",
            "regions",
            "sites",
            "shifts",
            "assets",
            "asset-assignments",
            "incidents",
            "deployments",
            "deployment-areas",
            "attendance",
        },
        "views": {
            "asset_assignment_report",
            "asset_store_report",
            "contract_report",
            "duty_roster_export",
            "duty_roster_upload",
            "incident_notifications",
            "incident_notify",
            "incident_report",
        },
    },
    "Finance Officer": {
        "models": {
            "procurement",
            "suppliers",
            "procurement-requisitions",
            "procurement-approvals",
            "proforma-item-prices",
            "supplier-proformas",
            "purchase-orders",
            "goods-received-notes",
            "supplier-invoices",
            "supplier-payments",
            "procurement-notifications",
            "invoices",
            "paymees",
            "payments",
            "budgets",
            "expenses",
        },
        "views": {
            "aging_report",
            "budget_notifications",
            "budget_report",
            "expense_notifications",
            "expense_report",
            "invoice_document",
            "payment_receipt",
            "payment_reconciliation",
            "payout_api_batch",
            "payout_api_index",
            "procurement",
            "procurement_api_detail",
            "procurement_api_index",
            "procurement_api_list",
            "procurement_contact_supplier",
        },
    },
}

DEFAULT_USERS = {
    "supervisor": "Supervisor",
    "hr": "Human Resources",
    "operation_manager": "Operations Manager",
    "finance_officer": "Finance Officer",
    "head_of_finance": "Head of Finance",
}

DEFAULT_PASSWORD = "ChangeMe123!"


def user_group_names(user):
    if not getattr(user, "is_authenticated", False):
        return set()
    return set(user.groups.values_list("name", flat=True))


def user_allowed_models(user):
    if not getattr(user, "is_authenticated", False):
        return set()
    group_names = user_group_names(user)
    if user.is_superuser or "Head of Finance" in group_names:
        return None
    restricted_groups = group_names.intersection(ROLE_GROUPS)
    if not restricted_groups:
        return None
    allowed = set()
    for group_name in restricted_groups:
        allowed.update(ROLE_GROUPS[group_name].get("models", set()))
    return allowed


def user_allowed_views(user):
    if not getattr(user, "is_authenticated", False):
        return set()
    group_names = user_group_names(user)
    if user.is_superuser or "Head of Finance" in group_names:
        return None
    restricted_groups = group_names.intersection(ROLE_GROUPS)
    if not restricted_groups:
        return None
    allowed = set()
    for group_name in restricted_groups:
        allowed.update(ROLE_GROUPS[group_name].get("views", set()))
    return allowed


def can_access_model(user, model_name):
    allowed = user_allowed_models(user)
    return allowed is None or model_name in allowed


def can_access_view(user, view_name):
    allowed = user_allowed_views(user)
    return allowed is None or view_name in allowed


def require_model_access(request, model_name):
    if not can_access_model(request.user, model_name):
        raise PermissionDenied("You do not have permission to open this module.")


def require_view_access(request, view_name):
    if not can_access_view(request.user, view_name):
        raise PermissionDenied("You do not have permission to open this page.")


def first_allowed_model(user):
    allowed = user_allowed_models(user)
    if allowed is None:
        return None
    preferred = [
        "attendance",
        "employees",
        "payroll",
        "clients",
        "procurement",
        "invoices",
        "payments",
        "budgets",
    ]
    for model_name in preferred:
        if model_name in allowed:
            return model_name
    return next(iter(sorted(allowed)), None)


def redirect_to_first_allowed_module(user):
    model_name = first_allowed_model(user)
    if model_name:
        return redirect("webcom:list", model_name=model_name)
    raise PermissionDenied("No modules are assigned to this account.")


def sync_default_role_accounts(password=DEFAULT_PASSWORD):
    User = get_user_model()
    created = []
    updated = []
    for username, group_name in DEFAULT_USERS.items():
        group, _group_created = Group.objects.get_or_create(name=group_name)
        user, was_created = User.objects.get_or_create(username=username)
        user.is_staff = True
        if group_name == "Head of Finance":
            user.is_superuser = True
        if was_created or not user.has_usable_password():
            user.set_password(password)
        user.save()
        user.groups.add(group)
        if was_created:
            created.append(username)
        else:
            updated.append(username)
    return created, updated
