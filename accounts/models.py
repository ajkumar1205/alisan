from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Franchise(models.Model):
    name = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by", blank=True)


class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    role = models.CharField(max_length=100)
    address = models.TextField()
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_created_by", blank=True)