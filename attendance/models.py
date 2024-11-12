from django.db import models
from datetime import date
from accounts.models import Employee

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Leave'),
        ('H', 'Holiday'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    remarks = models.TextField(blank=True, null=True) 

    class Meta:
        unique_together = ('employee', 'date') 

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.get_status_display()}"


class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('S', 'Sick Leave'),
        ('C', 'Casual Leave'),
        ('E', 'Emergency Leave'),
        ('V', 'Vacation Leave'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=1, choices=LEAVE_TYPE_CHOICES)
    approved = models.BooleanField(default=False)
    reason = models.TextField()

    def __str__(self):
        return f"{self.employee.name} - {self.get_leave_type_display()} from {self.start_date} to {self.end_date}"
    

class Holiday(models.Model):
    date = models.DateField(unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.description or 'Holiday'} on {self.date}"
    
    class Meta:
        ordering = ['date']
        verbose_name = "Holiday"
        verbose_name_plural = "Holidays"


