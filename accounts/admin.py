from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Franchise, Employee, Neighbours, MyUser

# Register your models here.
admin.site.register(Franchise)
admin.site.register(Neighbours)

class MyUserChangeForm(forms.ModelForm):
    """Form for updating existing user instances."""
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank if you don't want to change the password."
    )

    class Meta:
        model = MyUser
        fields = ('email', 'phone_number', 'password', 'role', 'franchise', 'is_staff', 'is_active')

    def clean_password(self):
        # Return the existing password if it's not being changed
        return self.initial["password"]

class MyUserCreationForm(forms.ModelForm):
    """Form for creating a new user."""
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = MyUser
        fields = ('email', 'phone_number', 'password', 'role', 'franchise')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user
    

@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    list_display = ('email', 'phone_number', 'role', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'phone_number')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        (_('Personal Info'), {'fields': ('role', 'franchise')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password', 'password_confirm', 'role', 'franchise', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Customize form to handle password hashing."""
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['password'].widget = forms.PasswordInput(render_value=False)
        return form
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == 'admin' and request.user.franchise:
            # filter on the basis of the franchise only
            return qs.filter(franchise=request.user.franchise)
        return qs.none()
    

class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Capture the request object
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Restrict 'user' field based on franchise of logged-in admin
        if request and not request.user.is_superuser:
            self.fields['user'].queryset = MyUser.objects.filter(franchise=request.user.franchise)
        elif request and request.user.is_superuser:
            self.fields['user'].queryset = MyUser.objects.all()


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm
    list_display = ['name', 'dob', 'doj', 'maritial_status']
    search_fields = ['name', 'phone_number']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Pass the request object to the form
        form.request = request
        return form
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superuser sees all employees
        elif request.user.role == 'admin' and request.user.franchise:
            # Employee Doesnot have franchise field only user have so write the filter accordingly

            return qs.filter(user__franchise=request.user.franchise)
        return qs.none()  # For others, return no results

    list_display = ['name', 'dob', 'doj', 'maritial_status']
    search_fields = ['name', 'phone_number']
