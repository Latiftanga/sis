from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from core.utils import generate_unique_token

class School(models.Model):
    """Schools in the system"""
    name = models.CharField(max_length=255, unique=True)
    registered_no = models.CharField(
        max_length=255, unique=True
    )
    motto = models.CharField(
        max_length=255, blank=True, default=''
    )
    address = models.CharField(
        max_length=255, blank=True, default=''
    )
    email = models.EmailField(
        max_length=255, blank=True, default=''
    )
    website = models.CharField(
        max_length=255,
        blank=True, default=''
    )

    def __str__(self) -> str:
        return self.name


class Person(models.Model):
    """Person abstract model"""
    GENDER = (('m', 'Male'), ('f', 'Female'))
    RELIGIONS = (
        ('christianity', 'Christianity'),
        ('islam', 'Islam'),
        ('traditional african religion', 'Traditional African Religion')
    )
    first_name = models.CharField(max_length=32)
    other_names = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=GENDER)
    date_of_birth = models.DateField()
    religion = models.CharField(
        max_length=32, blank=True, default='',
        choices=RELIGIONS
    )
    religious_denomination = models.CharField(
        max_length=32, blank=True, default=''
    )
    nationality = models.CharField(max_length=128)
    national_id = models.CharField(
        max_length=32, blank=True, default=''
    )
    social_security_no = models.CharField(
        max_length=32, blank=True, default=''
    )
    health_insurance_no = models.CharField(
        max_length=32, blank=True, default=''
    )
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """"Manage for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_adminuser(self, email, password):
        """Create and return a new admin user"""
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_teacheruser(self, email, password):
        """Create and return a new teacher user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_studentuser(self, email, password):
        """Create and return a new student user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_guardianuser(self, email, password):
        """Create and return a new guardian user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user


class SignupToken(models.Model):
    TOKEN_TYPES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('guardian', 'Guardian')
    )
    token_type = models.CharField(
        max_length=32, choices=TOKEN_TYPES
    )
    token = models.CharField(
        default=generate_unique_token(),
        editable=False, unique=True
    )
    email = models.EmailField(unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_guardian = models.BooleanField(default=False)
    token = models.OneToOneField(
        SignupToken, blank=True, null=True,
        related_name='user', on_delete=models.CASCADE
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Address(models.Model):
    """Address for teachers and students"""
    house_number = models.CharField(max_length=50, blank=True, default='')
    street_name = models.CharField(max_length=255, blank=True, default='')
    landmark = models.CharField(max_length=255, blank=True, default='')
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    email = models.EmailField(max_length=244, blank=True, null=True)
    gps_address = models.CharField(max_length=15, blank=True,default='')
    postal_code = models.CharField(max_length=10, blank=True, default='')
    mobile_no = models.CharField(max_length=32, blank=True, default='')
    telephone = models.CharField(max_length=32, blank=True, default='')

    def __str__(self):
        address_parts = [
            self.house_number if self.house_number else '',
            self.street_name if self.street_name else '',
            self.city, self.district, self.region
        ]
        # Filter out empty parts and join the rest with a comma
        return ', '.join(part for part in address_parts if part) 


class Teacher(Person):
    """Teaching Teacher in the system"""
    TITLES = (
        (
            ("Dr.", "Dr."), ("Dr.", "Dr."), ("Hon", "Hon"),
            ("Hon.", "Hon."), ("Lord", "Lord"), ("Md.", "Md."),
            ("Ms", "Ms"), ("Mr.", "Mr."), ("Mrs.", "Mrs."),
            ("Prof", "Prof"), ("Prof", "Prof"), ("Rev", "Rev"),
            ("Rev.", "Rev."), ("Sir", "Sir"),
        )
    )
    title = models.CharField(max_length=32, choices=TITLES)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='teacher_profile'
    )
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE,
        related_name='teacher_address', blank=True, null=True
    )
    def __str__(self):
        return f'{self.first_name} {self.other_names}'

    def get_full_name(self):
        return self.__str__()


class Qualification(models.Model):
    """Teacher academic & Professional qualification"""
    QUALIFICATION_TYPES = (
        ('academic', 'Academic'),
        ('professional', 'Professional'),
    )
    title = models.CharField(max_length=255)
    institution = models.CharField(
        max_length=255, blank=True, default=''
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        blank=True, null=True, related_name='qualifications'
    )

    def __str__(self):
        return f'{self.title} {self.start_date}-{self.end_date}'


class Promotion(models.Model):
    """Teacher Promotion History"""
    title = models.CharField(max_length=255)
    notional_date = models.DateField(null=True, blank=True)
    substantive_date = models.DateField()
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        blank=True, null=True, related_name='promotions'
    )
    def __str__(self) -> str:
        return f'{self.title} {self.substantive_date}'
