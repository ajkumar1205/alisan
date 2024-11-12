from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Employee
import uuid

# Create your models here.

class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image_url = models.CharField(max_length=2083, blank=True, null=True)
    gst_number = models.CharField(max_length=100)
    max_discount = models.FloatField()


class Lead(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    interest = models.ManyToManyField(Product, related_name="leads")
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="lead_created_by")

    def __str__(self) -> str:
        return self.name

class SiteVisit(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    visit_date = models.DateTimeField(auto_now_add=True)
    visit_notes = models.TextField()
    visit_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    technicians = models.ManyToManyField(Employee, related_name="technicians", blank=True)

    def __str__(self) -> str:
        return self.lead.name

class SiteExpenses(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    site_visit = models.ForeignKey(SiteVisit, on_delete=models.CASCADE)
    expense_date = models.DateTimeField(auto_now_add=True)
    expense_amount = models.FloatField()
    expense_notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.expense_amount


class Payment(models.Model):

    PAYMENT_MODE = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('cheque', 'Cheque'),
        ('bank', 'Bank Transfer')
    ]



    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=100, choices=PAYMENT_MODE)
    payment_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    recieved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="recieved_by")

    def __str__(self) -> str:
        return self.amount