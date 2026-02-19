import uuid
from django.db import models
from django.utils import timezone

class Employee(models.Model):
    ROLE = [("RECEPTION","Reception"), ("COACH","Coach"), ("ACCOUNTANT","Accountant"), ("MANAGER","Manager")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=120, db_index=True)
    phone = models.CharField(max_length=40, blank=True, db_index=True)
    role = models.CharField(max_length=30, choices=ROLE)
    hire_date = models.DateField(default=timezone.now)
    base_salary_iqd = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

class SalaryPayout(models.Model):
    METHOD = [("CASH","Cash"), ("CARD","Card"), ("TRANSFER","Transfer")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payouts")
    payout_date = models.DateField(default=timezone.now, db_index=True)
    amount_iqd = models.PositiveIntegerField()
    method = models.CharField(max_length=20, choices=METHOD, default="CASH")
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        indexes = [models.Index(fields=["payout_date"])]
