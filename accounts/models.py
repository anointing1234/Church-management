import json
import locale
import random
import string
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from io import BytesIO
from PIL import Image

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

# Set locale for formatting prices and dates
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'C')  # Fallback to default locale


class AccountManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email address")
        if not phone_number:
            raise ValueError("User must have a phone number")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not username:
            username = f"admin_{email.split('@')[0]}"
        if not phone_number:
            raise ValueError("Superuser must have a phone number")

        return self.create_user(email=email, username=username, phone_number=phone_number, password=password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("ministry_church_1", "Ministry Church 1"),
        ("ministry_church_2", "Ministry Church 2"),
        ("membership_church_1", "Membership Church 1"),
        ("membership_church_2", "Membership Church 2"),
        ("junior_church_1", "Junior Church 1"),
        ("junior_church_2", "Junior Church 2"),
        ("multimedia_church_1", "Multimedia Church 1"),
        ("multimedia_church_2", "Multimedia Church 2"),
        ("social_media_report", "Social Media Report"),
        ("missions_team_summary", "Missions Team Summary"),
        ("sakponba_church", "Sakponba Church"),
        ("uselu_church", "Uselu Church"),
        ("hill_church", "Hill Church"),

    ]

    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    username = models.CharField(max_length=100)
    phone_number = PhoneNumberField(region="NG", unique=True, null=True, blank=True)
    role = models.CharField(max_length=500, choices=ROLE_CHOICES, default='user')
    profile_picture = models.ImageField(
    upload_to='profile_pics/',
    default='profile_pics/profile_pic.webp',
    null=True,
    blank=True
        )
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    can_submit_despite_missing_last_week = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return super().has_module_perms(app_label)



# ---------------- Ministry Models ------------------

class MinistryChurch1(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    SERVICE_DAY_CHOICES = [
        ('sunday_wednesday', 'Sunday & Wednesday'),
        ('sunday', 'Sunday'),
        ('wednesday', 'Wednesday'),
    ]

    SERVICE_CHOICES = [
        ('1', '1st Service'),
        ('2', '2nd Service'),
        ('3', '3rd Service'),
    ]

    sunday_wednesday = models.CharField(max_length=20, choices=SERVICE_DAY_CHOICES)
    service = models.CharField(max_length=1, choices=SERVICE_CHOICES)

    male = models.PositiveIntegerField(default=0)
    female = models.PositiveIntegerField(default=0)
    children = models.PositiveIntegerField(default=0)

    total = models.PositiveIntegerField(blank=True, null=True)
    number_of_cars = models.PositiveIntegerField(default=0)

    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total = self.male + self.female + self.children
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Church 1 - {self.get_service_display()}  on {self.date}"


class MinistryChurch2(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    SERVICE_DAY_CHOICES = [
        ('sunday_wednesday', 'Sunday & Wednesday'),
        ('sunday', 'Sunday'),
        ('wednesday', 'Wednesday'),
    ]

    SERVICE_CHOICES = [
        ('1', '1st Service'),
        ('2', '2nd Service'),
        ('3', '3rd Service'),
    ]

    sunday_wednesday = models.CharField(max_length=20, choices=SERVICE_DAY_CHOICES)
    service = models.CharField(max_length=1, choices=SERVICE_CHOICES)

    male = models.PositiveIntegerField(default=0)
    female = models.PositiveIntegerField(default=0)
    children = models.PositiveIntegerField(default=0)

    total = models.PositiveIntegerField(blank=True, null=True)
    number_of_cars = models.PositiveIntegerField(default=0)

    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total = self.male + self.female + self.children
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Church 2 - {self.get_service_display()}  on {self.date}"


# ---------------- Membership Models ------------------

class MembershipChurch1(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    SERVICE_CHOICES = [
        ('1', '1st Service'),
        ('2', '2nd Service'),
        ('3', '3rd Service'),
    ]

    service = models.CharField(max_length=1, choices=SERVICE_CHOICES)

    first_time_guests = models.PositiveIntegerField(default=0)
    second_time_guests = models.PositiveIntegerField(default=0)

    number_called = models.PositiveIntegerField(default=0)
    number_of_sms = models.PositiveIntegerField(default=0)

    membership_interest = models.PositiveIntegerField(default=0)
    number_of_converts = models.PositiveIntegerField(default=0)

    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Church 1 - Service {self.service} on {self.date}"


class MembershipChurch2(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    SERVICE_CHOICES = [
        ('1', '1st Service'),
        ('2', '2nd Service'),
        ('3', '3rd Service'),
    ]

    service = models.CharField(max_length=1, choices=SERVICE_CHOICES)

    first_time_guests = models.PositiveIntegerField(default=0)
    second_time_guests = models.PositiveIntegerField(default=0)

    number_called = models.PositiveIntegerField(default=0)
    number_of_sms = models.PositiveIntegerField(default=0)

    membership_interest = models.PositiveIntegerField(default=0)
    number_of_converts = models.PositiveIntegerField(default=0)

    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Church 2 - Service {self.service} on {self.date}"



# ---------------- JuniorChurch Models ------------------

class JuniorChurchChurch1(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    SERVICE_CHOICES = [
        ('1', 'Service 1'),
        ('2', 'Service 2'),
    ]

    CHURCH_TYPE_CHOICES = [
       ('both', 'Children & Teens Church')
    ]

    service = models.CharField(max_length=1, choices=SERVICE_CHOICES)
    church_type = models.CharField(max_length=10, choices=CHURCH_TYPE_CHOICES)

    # Fields for Children Church
    creche = models.PositiveIntegerField(default=0)
    adorable = models.PositiveIntegerField(default=0)
    angels = models.PositiveIntegerField(default=0)
    shining_stars = models.PositiveIntegerField(default=0)
    great_minds = models.PositiveIntegerField(default=0)
    sparkles = models.PositiveIntegerField(default=0)
    total_children = models.PositiveIntegerField(blank=True, null=True)
    children_offering = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    children_tithe = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    children_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Fields for Teens Church
    total_teens = models.PositiveIntegerField(default=0)
    teens_offering = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    teens_tithe = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    teens_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_children = self.creche + self.adorable + self.angels + self.shining_stars + self.great_minds + self.sparkles
        self.children_total = self.children_offering + self.children_tithe
        self.teens_total = self.teens_offering + self.teens_tithe
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Church 1 - {self.get_church_type_display()} - Service {self.service} on {self.date}"


class JuniorChurchChurch2(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    SERVICE_CHOICES = [
        ('1', 'Service 1'),
        ('2', 'Service 2'),
    ]
     
    CHURCH_TYPE_CHOICES = [
       ('both', 'Children & Teens Church')
    ]


    service = models.CharField(max_length=1, choices=SERVICE_CHOICES)
    church_type = models.CharField(max_length=10, choices=CHURCH_TYPE_CHOICES)

    # Fields for Children Church
    creche = models.PositiveIntegerField(default=0)
    adorable = models.PositiveIntegerField(default=0)
    angels = models.PositiveIntegerField(default=0)
    shining_stars = models.PositiveIntegerField(default=0)
    great_minds = models.PositiveIntegerField(default=0)
    sparkles = models.PositiveIntegerField(default=0)
    total_children = models.PositiveIntegerField(blank=True, null=True)
    children_offering = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    children_tithe = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    children_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Fields for Teens Church
    total_teens = models.PositiveIntegerField(default=0)
    teens_offering = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    teens_tithe = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    teens_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_children = self.creche + self.adorable + self.angels + self.shining_stars + self.great_minds + self.sparkles
        self.children_total = self.children_offering + self.children_tithe
        self.teens_total = self.teens_offering + self.teens_tithe
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Church 2 - {self.get_church_type_display()} - Service {self.service} on {self.date}"


# ---------------- BirthdayAdvert Models ------------------

class BirthdayAdvertChurch1(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    total = models.PositiveIntegerField(default=0, help_text="Total number of birthday adverts")
    date = models.DateField(auto_now_add=True, help_text="Date this record was created")

    class Meta:
        verbose_name = "Birthday Advert Church 1"
        verbose_name_plural = "Birthday Adverts Church 1"

    def __str__(self):
        return f"Church 1 — {self.total} advert(s) on {self.date}"


class BirthdayAdvertChurch2(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    total = models.PositiveIntegerField(default=0, help_text="Total number of birthday adverts")
    date = models.DateField(auto_now_add=True, help_text="Date this record was created")

    class Meta:
        verbose_name = "Birthday Advert Church 2"
        verbose_name_plural = "Birthday Adverts Church 2"

    def __str__(self):
        return f"Church 2 — {self.total} advert(s) on {self.date}"


# ---------------- SocialMediaReport Models ------------------

# Choices defined once
SOTW_CHOICES = [
    ('facebook', 'Facebook'),
    ('youtube', 'YouTube'),
]

SERVICE_CHOICES = [
    ('1', 'Service 1'),
    ('2', 'Service 2'),
    ('3', 'Service 3'),
]

class SocialMediaReportChurch1(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    sotw = models.CharField(max_length=100, choices=SOTW_CHOICES, verbose_name="Platform")
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, verbose_name="Service")
    
    facebook_count = models.PositiveIntegerField(
        default=0,
        help_text="Metric (e.g. likes/views) on Facebook"
    )
    youtube_count = models.PositiveIntegerField(
        default=0,
        help_text="Metric (e.g. likes/views) on YouTube"
    )
 
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Church 1 - {self.sotw} - Service {self.service} on {self.date}"


class SocialMediaReportChurch2(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    sotw = models.CharField(max_length=100, choices=SOTW_CHOICES, verbose_name="Platform")
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, verbose_name="Service")
    
    facebook_count = models.PositiveIntegerField(
        default=0,
        help_text="Metric (e.g. likes/views) on Facebook"
    )
    youtube_count = models.PositiveIntegerField(
        default=0,
        help_text="Metric (e.g. likes/views) on YouTube"
    )
 
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Church 2 - {self.sotw} - Service {self.service} on {self.date}"



class MissionTeamSummary(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    evbuotubu = models.PositiveIntegerField(default=0, help_text="Count at Evbuotubu")
    gra       = models.PositiveIntegerField(default=0, help_text="Count at GRA")

    # — split metrics —
    total_first_time_guests_evbuotubu = models.PositiveIntegerField(default=0)
    total_first_time_guests_gra       = models.PositiveIntegerField(default=0)

    reached_first_time_guests_evbuotubu = models.PositiveIntegerField(default=0)
    reached_first_time_guests_gra       = models.PositiveIntegerField(default=0)

    not_reachable_first_time_guests_evbuotubu = models.PositiveIntegerField(default=0)
    not_reachable_first_time_guests_gra       = models.PositiveIntegerField(default=0)

    visitors_and_outsiders_evbuotubu = models.PositiveIntegerField(default=0)
    visitors_and_outsiders_gra       = models.PositiveIntegerField(default=0)

    committed_to_second_visit_evbuotubu = models.PositiveIntegerField(default=0)
    committed_to_second_visit_gra       = models.PositiveIntegerField(default=0)

    committed_to_believers_academy_evbuotubu = models.PositiveIntegerField(default=0)
    committed_to_believers_academy_gra       = models.PositiveIntegerField(default=0)

    attended_cell_meeting_same_day_evbuotubu = models.PositiveIntegerField(default=0)
    attended_cell_meeting_same_day_gra       = models.PositiveIntegerField(default=0)

    committed_to_cell_meeting_next_week_evbuotubu = models.PositiveIntegerField(default=0)
    committed_to_cell_meeting_next_week_gra       = models.PositiveIntegerField(default=0)

    second_time_visitors_previous_week_evbuotubu = models.PositiveIntegerField(default=0)
    second_time_visitors_previous_week_gra       = models.PositiveIntegerField(default=0)

    # Grand total (evbuotubu + gra)
    grand_total = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-calculate Evbuotubu total
        self.evbuotubu = sum([
            self.total_first_time_guests_evbuotubu,
            self.reached_first_time_guests_evbuotubu,
            self.not_reachable_first_time_guests_evbuotubu,
            self.visitors_and_outsiders_evbuotubu,
            self.committed_to_second_visit_evbuotubu,
            self.committed_to_believers_academy_evbuotubu,
            self.attended_cell_meeting_same_day_evbuotubu,
            self.committed_to_cell_meeting_next_week_evbuotubu,
            self.second_time_visitors_previous_week_evbuotubu,
        ])

        # Auto-calculate GRA total
        self.gra = sum([
            self.total_first_time_guests_gra,
            self.reached_first_time_guests_gra,
            self.not_reachable_first_time_guests_gra,
            self.visitors_and_outsiders_gra,
            self.committed_to_second_visit_gra,
            self.committed_to_believers_academy_gra,
            self.attended_cell_meeting_same_day_gra,
            self.committed_to_cell_meeting_next_week_gra,
            self.second_time_visitors_previous_week_gra,
        ])
        
   

        # Set the grand total
        self.grand_total = self.evbuotubu + self.gra

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Mission Summary on {self.date}"



class SakponbaChurchServiceBase(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    SERVICE_DAY_CHOICES = [
        ('sunday', 'Sunday'),
        ('wednesday', 'Wednesday'),
    ]
    SERVICE_NO_CHOICES = [
        ('1', '1st Service'),
        ('2', '2nd Service'),
    ]

    service_day = models.CharField(max_length=9, choices=SERVICE_DAY_CHOICES, verbose_name="Service Day")
    service_no = models.CharField(max_length=1, choices=SERVICE_NO_CHOICES, verbose_name="Service Number")

    male = models.PositiveIntegerField(default=0)
    female = models.PositiveIntegerField(default=0)
    children = models.PositiveIntegerField(default=0)
    attendance_total = models.PositiveIntegerField(blank=True, null=True, editable=False)

    number_of_cars = models.PositiveIntegerField(default=0)

    offering = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tithe = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transfer = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    financial_total = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=2, editable=False)

    date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True  # This base is still abstract to avoid table creation for it

    def save(self, *args, **kwargs):
        self.attendance_total = self.male + self.female + self.children
        self.financial_total = self.offering + self.tithe + self.transfer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_service_day_display()} {self.get_service_no_display()} on {self.date}"

# Now, your actual models inheriting from their own base

class SakponbaChurch(SakponbaChurchServiceBase):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    class Meta:
        verbose_name = "Sakponba Church Service"
        verbose_name_plural = "Sakponba Church Services"




class UseluChurchServiceBase(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    SERVICE_DAY_CHOICES = [
        ('sunday', 'Sunday'),
        ('wednesday', 'Wednesday'),
    ]
    SERVICE_NO_CHOICES = [
        ('1', '1st Service'),
        ('2', '2nd Service'),
    ]

    service_day = models.CharField(max_length=9, choices=SERVICE_DAY_CHOICES, verbose_name="Service Day")
    service_no = models.CharField(max_length=1, choices=SERVICE_NO_CHOICES, verbose_name="Service Number")

    male = models.PositiveIntegerField(default=0)
    female = models.PositiveIntegerField(default=0)
    children = models.PositiveIntegerField(default=0)
    attendance_total = models.PositiveIntegerField(blank=True, null=True, editable=False)

    number_of_cars = models.PositiveIntegerField(default=0)

    offering = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tithe = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transfer = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    financial_total = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=2, editable=False)

    date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.attendance_total = self.male + self.female + self.children
        self.financial_total = self.offering + self.tithe + self.transfer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_service_day_display()} {self.get_service_no_display()} on {self.date}"

class UseluChurch(UseluChurchServiceBase):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    class Meta:
        verbose_name = "Uselu Church Service"
        verbose_name_plural = "Uselu Church Services"




class HillChurchServiceBase(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    SERVICE_DAY_CHOICES = [
        ('sunday', 'Sunday'),
        ('wednesday', 'Wednesday'),
    ]
    SERVICE_NO_CHOICES = [
        ('1', '1st Service'),
        ('2', '2nd Service'),
    ]

    service_day = models.CharField(max_length=9, choices=SERVICE_DAY_CHOICES, verbose_name="Service Day")
    service_no = models.CharField(max_length=1, choices=SERVICE_NO_CHOICES, verbose_name="Service Number")

    male = models.PositiveIntegerField(default=0)
    female = models.PositiveIntegerField(default=0)
    children = models.PositiveIntegerField(default=0)
    attendance_total = models.PositiveIntegerField(blank=True, null=True, editable=False)

    number_of_cars = models.PositiveIntegerField(default=0)

    offering = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tithe = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transfer = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    financial_total = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=2, editable=False)

    date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.attendance_total = self.male + self.female + self.children
        self.financial_total = self.offering + self.tithe + self.transfer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_service_day_display()} {self.get_service_no_display()} on {self.date}"

class HillChurch(HillChurchServiceBase):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    default=1  # or any valid user ID from your User table
)

    class Meta:
        verbose_name = "Hill Church Service"
        verbose_name_plural = "Hill Church Services"
        
        
        

class ReportSubmission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    
    
    
    




class UserVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    def generate_code(self):
        self.code = str(random.randint(100000, 999999))
        self.save()

    def __str__(self):
        return f"{self.user.username} - Verified: {self.is_verified}"    
    
    
    


class PasswordResetCode(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=8, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=20)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        return ''.join(random.choices(string.digits, k=6))  # 6-digit numeric code    