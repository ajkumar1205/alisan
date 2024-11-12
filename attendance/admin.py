from django.contrib import admin
from .models import Attendance, Leave, Holiday

admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Holiday)
