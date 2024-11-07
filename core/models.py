from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image_url = models.CharField(max_length=2083, blank=True, null=True)
    gst_number = models.CharField(max_length=100)
    max_discount = models.FloatField()


class Lead(models.Model):
    source = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    interest = models.ManyToManyField(Product, related_name="leads")
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class SiteVisit(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    visit_date = models.DateTimeField(auto_now_add=True)
    visit_notes = models.TextField()
    visit_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    technicians = models.ManyToManyField(User, related_name="technicians", blank=True)

class SiteExpenses(models.Model):
    site_visit = models.ForeignKey(SiteVisit, on_delete=models.CASCADE)
    expense_date = models.DateTimeField(auto_now_add=True)
    expense_amount = models.FloatField()
    expense_notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)