# Generated by Django 5.1.3 on 2024-11-09 04:15

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Neighbours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('first_phone', models.CharField(max_length=100)),
                ('second_name', models.CharField(max_length=100)),
                ('second_phone', models.CharField(max_length=100)),
                ('third_name', models.CharField(max_length=100)),
                ('third_phone', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_account', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('gst_number', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('doj', models.DateField()),
                ('maritial_status', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('mother_name', models.CharField(max_length=100)),
                ('permanent_address', models.TextField()),
                ('current_address', models.TextField()),
                ('guardian_or_spouse_name', models.CharField(max_length=100)),
                ('guardian_relation', models.CharField(max_length=100)),
                ('guardian_or_spouse_number', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=100)),
                ('ifsc_code', models.CharField(max_length=100)),
                ('passport_number', models.CharField(blank=True, max_length=100, null=True)),
                ('aadhar_front', models.ImageField(upload_to='employee/aadhar/front')),
                ('aadhar_back', models.ImageField(upload_to='employee/aadhar/back')),
                ('pan_card', models.ImageField(upload_to='employee/pan_card')),
                ('driving_license_front', models.ImageField(upload_to='employee/driving_license/front')),
                ('docs_drive_link', models.URLField(blank=True, null=True)),
                ('role', models.CharField(blank=True, choices=[('sale_manager', 'Sale Manager'), ('sales_executive', 'Sales Executive'), ('technical_manager', 'Technical Manager'), ('technician_executive', 'Technician Executive'), ('accounts', 'Accounts')], max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_created_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_user', to=settings.AUTH_USER_MODEL)),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.franchise')),
                ('neighbours', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='neighbours', to='accounts.neighbours')),
            ],
        ),
    ]
