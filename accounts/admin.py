from django.contrib import admin
from .models import Franchise, Employee, Neighbours, MyUser

# Register your models here.
admin.site.register(Franchise)
admin.site.register(Employee)
admin.site.register(Neighbours)
admin.site.register(MyUser)