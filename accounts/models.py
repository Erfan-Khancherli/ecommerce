from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager ,AbstractBaseUser , PermissionsMixin
from django.utils import timezone
from django_countries.fields import CountryField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User



class CustomUserManager(BaseUserManager):
    def create_user(self , email , first_name , last_name,password = None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        
        user = self.model(email = self.normalize_email(email))
        user.first_name = first_name
        user.last_name  = last_name
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.save()
        return user
    def create_superuser(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # change password to hash
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user
    
class CustomUser(AbstractBaseUser):
    ADMIN = 'admin'
    STAFF = 'staff'
    STAUS = [
        (ADMIN , ('Admin User')),
        (STAFF, ('Staff user')),
    ]
    email = models.EmailField(('email address') , unique =True)
    first_name = models.CharField(('first name'), max_length=30)
    last_name = models.CharField(('last name'), max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    @staticmethod
    def has_perm(perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return "{}".format(self.email)

def validate_phone_number(value) : 
    if len(value) != 13:
        raise ValidationError(
            (f'{value} is not a correct phone number.'),
            params={'value': value},
        )
    if value[0] != "+" or value[1] != "2" or value[2] != "5" or value[3] != "4":
        raise ValidationError(
            (f'{value} is not a correct Kenyan phone number.'),
            params={'value': value},
        )
    
B = 'B'
S = 'S'

ADDRESS_CHOICES = (
    (B, "Billing"),
    (S, "Shipping"),
)
User = get_user_model()
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=13 )#validators=[validate_phone_number])
    country = CountryField(multiple=False)
    time_added = models.DateTimeField(auto_now_add=True)
    time_last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
        