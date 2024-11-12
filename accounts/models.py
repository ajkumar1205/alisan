from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _
import uuid
from django.core.exceptions import ValidationError


def validate_pdf(file):
    if not file.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('Either email or phone number must be provided')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone_number, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('sale_manager', 'Sale Manager'),
        ('sales_executive', 'Sales Executive'),
        ('technical_manager', 'Technical Manager'),
        ('technician_executive', 'Technician Executive'),
        ('accounts', 'Accounts'),
        ('admin', 'Admin')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    franchise = models.ForeignKey(_('accounts.Franchise'), on_delete=models.CASCADE, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email or self.phone_number

class Franchise(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(_('accounts.MyUser'), on_delete=models.CASCADE, blank=True, related_name="franchise_owner")
    dob = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    type = models.CharField(max_length=100)
    gst_number = models.FileField(upload_to='franchise/gst', validators=[validate_pdf])
    registration_number = models.CharField(max_length=100, null=True, blank=True)
    interests = models.ManyToManyField('core.Product', related_name="franchise_interests")
    website = models.URLField(null=True, blank=True)
    sales_region = models.CharField(max_length=100)
    tnc = models.TextField()
    referral_code = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Neighbours(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=100)
    first_phone = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    second_phone = models.CharField(max_length=100)
    third_name = models.CharField(max_length=100)
    third_phone = models.CharField(max_length=100) 


class Employee(models.Model):

    MARRIED_STATUS = [
        ('married', 'Married'),
        ('unmarried', 'Unmarried')
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    doj = models.DateField()
    maritial_status = models.CharField(max_length=100, choices=MARRIED_STATUS)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    permanent_address = models.TextField()
    current_address = models.TextField()
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="employee_user")
    guardian_or_spouse_name = models.CharField(max_length=100)
    guardian_relation = models.CharField(max_length=100)
    guardian_or_spouse_number = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100, null=True, blank=True)
    neighbours = models.OneToOneField(Neighbours, on_delete=models.CASCADE, related_name="neighbours", null=True, blank=True)

    aadhar_front = models.ImageField(upload_to='employee/aadhar/front')
    aadhar_back = models.ImageField(upload_to='employee/aadhar/back')

    pan_card = models.ImageField(upload_to='employee/pan_card')
    driving_license_front = models.ImageField(upload_to='employee/driving_license/front')


    docs_drive_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="employee_created_by", null=True, blank=True)


