import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone

class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=120, db_index=True)
    phone = models.CharField(max_length=40, blank=True, db_index=True)
    email = models.EmailField(blank=True, db_index=True)
    join_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

class Plan(models.Model):
    DURATION_CHOICES = [
        ("DAILY", "Daily (1 day)"),
        ("WEEKLY", "Weekly (7 days)"),
        ("D10", "10 days"),
        ("D15", "15 days"),
        ("MONTHLY", "Monthly (30 days)"),
    ]
    code = models.CharField(max_length=20, choices=DURATION_CHOICES, unique=True)
    name_ar = models.CharField(max_length=80)
    name_en = models.CharField(max_length=80)
    days = models.PositiveIntegerField()
    price_iqd = models.PositiveIntegerField()  # د.ع (بدون كسور)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name_en} - {self.price_iqd} IQD"

class Subscription(models.Model):
    STATUS = [("ACTIVE", "Active"), ("EXPIRED", "Expired"), ("FROZEN", "Frozen"), ("CANCELLED", "Cancelled")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default="ACTIVE")

    class Meta:
        indexes = [
            models.Index(fields=["status", "end_date"]),
            models.Index(fields=["member", "status"]),
        ]

    @staticmethod
    def calc_end_date(start, days: int):
        return start + timedelta(days=days)

    def __str__(self):
        return f"{self.member} - {self.plan.code}"
