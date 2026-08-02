from decimal import Decimal

from django.db import migrations
from django.utils import timezone


def refresh_paymee_receivables(apps, schema_editor):
    Paymee = apps.get_model("webCom", "Paymee")
    Payment = apps.get_model("webCom", "Payment")

    for record in Paymee.objects.select_related("invoice", "invoice__client").all():
        invoice = record.invoice
        amount_paid = sum(
            (payment.amount for payment in Payment.objects.filter(invoice=invoice)),
            Decimal("0.00"),
        )
        if invoice.status == "cancelled":
            status = "cancelled"
        elif invoice.total_amount <= 0:
            status = "pending"
        elif amount_paid > invoice.total_amount:
            status = "overpaid"
        elif amount_paid >= invoice.total_amount:
            status = "paid"
        elif amount_paid > 0:
            status = "partial"
        elif invoice.due_date and invoice.due_date < timezone.localdate():
            status = "overdue"
        else:
            status = "pending"

        latest_payment = Payment.objects.filter(invoice=invoice).order_by("-payment_date", "-payment_id").first()
        record.client = invoice.client
        record.total_amount = invoice.total_amount
        record.amount_paid = amount_paid
        record.due_date = invoice.due_date
        record.last_payment_date = latest_payment.payment_date if latest_payment else None
        record.status = status
        record.save(update_fields=["client", "total_amount", "amount_paid", "due_date", "last_payment_date", "status", "updated_at"])


class Migration(migrations.Migration):

    dependencies = [
        ("webCom", "0048_alter_paymee_options_paymee_client_paymee_currency_and_more"),
    ]

    operations = [
        migrations.RunPython(refresh_paymee_receivables, migrations.RunPython.noop),
    ]
