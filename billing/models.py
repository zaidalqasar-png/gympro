import uuid
from django.db import models
from django.utils import timezone
from members.models import Member, Subscription

class Invoice(models.Model):
    STATUS = [("UNPAID","Unpaid"), ("PARTIAL","Partial"), ("PAID","Paid")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="invoices")
    subscription = models.OneToOneField(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    issue_date = models.DateField(default=timezone.now)

    total_iqd = models.PositiveIntegerField(default=0)
    paid_iqd = models.PositiveIntegerField(default=0)
    balance_iqd = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default="UNPAID")

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["balance_iqd"]),
            models.Index(fields=["issue_date"]),
        ]

    def recalc(self):
        self.balance_iqd = max(0, self.total_iqd - self.paid_iqd)
        if self.paid_iqd == 0:
            self.status = "UNPAID"
        elif self.balance_iqd > 0:
            self.status = "PARTIAL"
        else:
            self.status = "PAID"

class Payment(models.Model):
    METHOD = [("CASH","Cash"), ("CARD","Card"), ("TRANSFER","Transfer")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    pay_date = models.DateField(default=timezone.now, db_index=True)
    amount_iqd = models.PositiveIntegerField()
    method = models.CharField(max_length=20, choices=METHOD, default="CASH")
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        indexes = [models.Index(fields=["pay_date"])]

class Expense(models.Model):
    METHOD = [("CASH","Cash"), ("CARD","Card"), ("TRANSFER","Transfer")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense_date = models.DateField(default=timezone.now, db_index=True)
    category = models.CharField(max_length=80, db_index=True)
    amount_iqd = models.PositiveIntegerField()
    method = models.CharField(max_length=20, choices=METHOD, default="CASH")
    description = models.CharField(max_length=200, blank=True)
