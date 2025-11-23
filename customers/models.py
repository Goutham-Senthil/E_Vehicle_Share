# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.utils import timezone


# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)  # This will hash the password
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(username, email, password, **extra_fields)

# class User(AbstractBaseUser):
#     username = models.CharField(max_length=150, unique=True, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     surname = models.CharField(max_length=50)
#     email = models.EmailField(max_length=255, unique=True)
#     password = models.CharField(max_length=128)  # Explicitly add password field for hashing
#     is_customer = models.BooleanField(default=False)
#     is_manager = models.BooleanField(default=False)
#     is_operator = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     balance = models.FloatField(default=0.0)  # New balance field with default value 0.0

#     objects = UserManager()

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email', 'first_name', 'surname']

#     def __str__(self):
#         return self.username

#     def has_perm(self, perm, obj=None):
#         return self.is_superuser

#     def has_module_perms(self, app_label):
#         return self.is_superuser

# class Vehicle(models.Model):
#     vehicle_id = models.AutoField(primary_key=True)
#     vehicle_type = models.CharField(max_length=100)
#     vehicle_name = models.CharField(max_length=100)
#     vehicle_model = models.CharField(max_length=100)
#     registration_number = models.CharField(max_length=100, unique=True)
#     battery = models.FloatField()
#     is_available = models.BooleanField(default=True)
#     is_defective = models.BooleanField(default=False)
#     hourly_rate = models.FloatField()
#     longitude = models.FloatField()
#     latitude = models.FloatField()

# class Reservation(models.Model):
#     reservation_id = models.AutoField(primary_key=True)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField(null=True, blank=True)
#     status = models.CharField(max_length=50)  # 'In use' or 'Completed'

# class Payment(models.Model):
#     transaction_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.FloatField()
#     status = models.CharField(max_length=50)  # 'Pending' or 'Completed'
#     reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)
#     created_at = models.DateTimeField(default=timezone.now)  # This sets a default timestamp


# class Report(models.Model):
#     report_id = models.AutoField(primary_key=True)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     reason = models.CharField(max_length=255)
#     comment = models.TextField(null=True, blank=True)
#previous above

# Imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# UserManager: Handles user and superuser creation
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        # Ensure the email is provided
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # Set default fields for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

# User model: Custom user implementation with various roles
class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, primary_key=True)  # Unique username as primary key
    first_name = models.CharField(max_length=50)  # First name of the user
    surname = models.CharField(max_length=50)  # Surname of the user
    email = models.EmailField(max_length=255, unique=True)  # Unique email for user identification
    password = models.CharField(max_length=128)  # Explicitly add password field for hashing
    is_customer = models.BooleanField(default=False)  # User role: Customer
    is_manager = models.BooleanField(default=False)  # User role: Manager
    is_operator = models.BooleanField(default=False)  # User role: Operator
    date_joined = models.DateTimeField(auto_now_add=True)  # Date when user joined
    is_active = models.BooleanField(default=True)  # User activation status
    is_staff = models.BooleanField(default=False)  # Staff status for admin access
    is_superuser = models.BooleanField(default=False)  # Superuser status for full permissions
    balance = models.FloatField(default=0.0)  # User balance with default value 0.0

    objects = UserManager()  # Link the custom user manager

    USERNAME_FIELD = 'username'  # Use username for authentication
    REQUIRED_FIELDS = ['email', 'first_name', 'surname']  # Required fields for user creation

    def __str__(self):
        return self.username

    # Permissions for admin panel
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

# Vehicle model: Stores vehicle information
class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)  # Unique vehicle ID
    vehicle_type = models.CharField(max_length=100)  # Type of vehicle
    vehicle_name = models.CharField(max_length=100)  # Vehicle name
    vehicle_model = models.CharField(max_length=100)  # Vehicle model
    registration_number = models.CharField(max_length=100, unique=True)  # Unique registration number
    battery = models.FloatField()  # Battery percentage/level
    is_available = models.BooleanField(default=True)  # Availability status
    is_defective = models.BooleanField(default=False)  # Defect status
    hourly_rate = models.FloatField()  # Rate per hour of vehicle usage
    longitude = models.FloatField()  # Vehicle location longitude
    latitude = models.FloatField()  # Vehicle location latitude

# Reservation model: Stores reservation details
class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)  # Unique reservation ID
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)  # Associated vehicle
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associated user
    start_time = models.DateTimeField()  # Reservation start time
    end_time = models.DateTimeField(null=True, blank=True)  # Reservation end time
    status = models.CharField(max_length=50)  # Reservation status ('In use' or 'Completed')

# Payment model: Stores payment information
class Payment(models.Model):
    transaction_id = models.AutoField(primary_key=True)  # Unique transaction ID
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associated user
    amount = models.FloatField()  # Payment amount
    status = models.CharField(max_length=50)  # Payment status ('Pending' or 'Completed')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)  # Associated reservation
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp for payment creation

# Report model: Stores reports filed by users
class Report(models.Model):
    report_id = models.AutoField(primary_key=True)  # Unique report ID
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)  # Associated vehicle
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associated user
    reason = models.CharField(max_length=255)  # Reason for report
    comment = models.TextField(null=True, blank=True)  # Additional comments for the report
