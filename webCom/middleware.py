from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.db import OperationalError, ProgrammingError
from django.http import HttpResponse

from .models import AuditLog

class VercelConfigurationMiddleware:
    """Handles Vercel-specific startup configuration before views touch the DB."""

    _sqlite_fallback_ready = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        errors = getattr(settings, "VERCEL_CONFIGURATION_ERRORS", [])
        if errors:
            body = "Deployment configuration required:\n\n" + "\n".join(f"- {error}" for error in errors)
            return HttpResponse(body, status=503, content_type="text/plain; charset=utf-8")
        fallback_error = self.prepare_vercel_sqlite_fallback()
        if fallback_error:
            return HttpResponse(fallback_error, status=503, content_type="text/plain; charset=utf-8")
        return self.get_response(request)

    @classmethod
    def prepare_vercel_sqlite_fallback(cls):
        if not getattr(settings, "VERCEL_SQLITE_FALLBACK", False) or cls._sqlite_fallback_ready:
            return ""
        marker = Path(settings.SQLITE_DATABASE_PATH).with_name(".securitycompany_sqlite_ready")
        if marker.exists():
            cls._sqlite_fallback_ready = True
            return ""
        try:
            call_command("migrate", interactive=False, verbosity=0)
            marker.write_text("ready", encoding="utf-8")
            cls._sqlite_fallback_ready = True
        except Exception as exc:
            return f"Temporary Vercel SQLite setup failed: {exc}"
        return ""


class RequestAuditMiddleware:
    """Records authenticated staff write activity for compliance traceability."""

    WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
    IGNORED_PREFIXES = ("/static/", "/media/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if self.should_audit(request):
            self.write_audit_log(request, response)
        return response

    def should_audit(self, request):
        if not getattr(settings, "AUDIT_LOG_ENABLED", True):
            return False
        if request.method not in self.WRITE_METHODS:
            return False
        if any(request.path.startswith(prefix) for prefix in self.IGNORED_PREFIXES):
            return False
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated)

    def write_audit_log(self, request, response):
        user = request.user
        ip_address = self.client_ip(request)
        try:
            AuditLog.objects.create(
                user=user,
                username=user.get_username(),
                action=self.classify_action(request),
                path=request.path[:500],
                method=request.method,
                status_code=getattr(response, "status_code", 0) or 0,
                ip_address=ip_address,
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
            )
        except (OperationalError, ProgrammingError):
            pass

    @staticmethod
    def classify_action(request):
        if request.method == "POST" and request.path.endswith("/delete/"):
            return "delete"
        if request.method == "POST" and request.path.endswith("/add/"):
            return "create"
        if request.method == "POST" and request.path.endswith("/edit/"):
            return "update"
        if request.method == "DELETE":
            return "delete"
        return request.method.lower()

    @staticmethod
    def client_ip(request):
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip() or None
        return request.META.get("REMOTE_ADDR") or None

