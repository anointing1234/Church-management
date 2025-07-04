"""
Django settings for church_management project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import os
import environ
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR,'file.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x*t@866olky#bvl(i^%$p1d1mlvtt_t!#l!ih=e*&wp$tpq6&j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["miracleassembly.top", "www.miracleassembly.top"]

CSRF_TRUSTED_ORIGINS = ["https://miracleassembly.top"]

# Application definition
AUTH_USER_MODEL = 'accounts.Account'



INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'church_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.user_role',
            ],
        },
    },
]

WSGI_APPLICATION = 'church_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),  
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


# settings.py

STATIC_URL = '/static/'            # leading slash!
MEDIA_URL  = '/media/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',           # your app-level CSS/JS/images
    # BASE_DIR / 'assets',         # optional: if you keep assets outside 'static'
]

# for development you don't need STATIC_ROOT
# if not DEBUG:
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_ROOT = BASE_DIR / 'media'



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_BACKEND      = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST         = 'smtp.zoho.com'     
EMAIL_PORT         = 465
EMAIL_USE_TLS      = False
EMAIL_USE_SSL      = True
EMAIL_HOST_USER    = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD= env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



BASE_SIDEBAR = [
    {
        "title": _("Users"),
        "icon": "group",
        "collapsible": True,
        "items": [
            {
                "title": _("Accounts"),
                "icon": "person",
                "link": lambda request: reverse_lazy("admin:accounts_account_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_account"),
            },
        ],
    },
    {
        "title": _("Ministries"),
        "icon": "apartment",
        "collapsible": True,
        "items": [
            {
                "title": _("Ministry Church 1"),
                "icon": "apartment",
                "link": lambda request: reverse_lazy("admin:accounts_ministrychurch1_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_ministrychurch1"),
            },
            {
                "title": _("Ministry Church 2"),
                "icon": "apartment",
                "link": lambda request: reverse_lazy("admin:accounts_ministrychurch2_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_ministrychurch2"),
            },
        ],
    },
    {
        "title": _("Memberships"),
        "icon": "people",
        "collapsible": True,
        "items": [
            {
                "title": _("Membership Church 1"),
                "icon": "people",
                "link": lambda request: reverse_lazy("admin:accounts_membershipchurch1_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_membershipchurch1"),
            },
            {
                "title": _("Membership Church 2"),
                "icon": "people",
                "link": lambda request: reverse_lazy("admin:accounts_membershipchurch2_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_membershipchurch2"),
            },
        ],
    },
    {
        "title": _("Church Services"),
        "icon": "church",
        "collapsible": True,
        "items": [
            {
                "title": _("Sakponba Church Services"),
                "icon": "church",
                "link": lambda request: reverse_lazy("admin:accounts_sakponbachurch_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_sakponbachurch"),
            },
            {
                "title": _("Uselu Church Services"),
                "icon": "church",
                "link": lambda request: reverse_lazy("admin:accounts_useluchurch_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_useluchurch"),
            },
            {
                "title": _("Hill Church"),
                "icon": "terrain",
                "link": lambda request: reverse_lazy("admin:accounts_hillchurch_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_hillchurch"),
            },
        ],
    },
    {
        "title": _("Junior Church"),
        "icon": "child_care",
        "collapsible": True,
        "items": [
            {
                "title": _("Junior Church Church 1"),
                "icon": "child_care",
                "link": lambda request: reverse_lazy("admin:accounts_juniorchurchchurch1_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_juniorchurchchurch1"),
            },
            {
                "title": _("Junior Church Church 2"),
                "icon": "child_care",
                "link": lambda request: reverse_lazy("admin:accounts_juniorchurchchurch2_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_juniorchurchchurch2"),
            },
        ],
    },
    {
        "title": _("Reports"),
        "icon": "bar_chart",
        "collapsible": True,
        "items": [
            {
                "title": _("Mission Team Summary"),
                "icon": "group",
                "link": lambda request: reverse_lazy("admin:accounts_missionteamsummary_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_missionteamsummary"),
            },
            {
                "title": _("Birthday Advert Church 1"),
                "icon": "cake",
                "link": lambda request: reverse_lazy("admin:accounts_birthdayadvertchurch1_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_birthdayadvertchurch1"),
            },
            {
                "title": _("Birthday Advert Church 2"),
                "icon": "cake",
                "link": lambda request: reverse_lazy("admin:accounts_birthdayadvertchurch2_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_birthdayadvertchurch2"),
            },
            {
                "title": _("Social Media Report Church 1"),
                "icon": "share",
                "link": lambda request: reverse_lazy("admin:accounts_socialmediareportchurch1_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_socialmediareportchurch1"),
            },
              {
                "title": _("Social Media Report Church 2"),
                "icon": "share",
                "link": lambda request: reverse_lazy("admin:accounts_socialmediareportchurch2_changelist"),
                "permission": lambda request: request.user.has_perm("accounts.view_socialmediareportchurch2"),
            },
        ],
    },
]

def get_filtered_sidebar(request):
    """
    Filters BASE_SIDEBAR by checking each item's permission callable
    and resolves each link for the given request.
    """
    filtered = []
    for group in BASE_SIDEBAR:
        allowed_items = []
        for item in group["items"]:
            # permission is now a callable
            if item["permission"](request):
                item_copy = item.copy()
                # resolve URL
                item_copy["link"] = item_copy["link"](request)
                allowed_items.append(item_copy)
        if allowed_items:
            group_copy = group.copy()
            group_copy["items"] = allowed_items
            filtered.append(group_copy)
    return filtered

# UNFOLD configuration
UNFOLD = {
    "SITE_TITLE": "MIRACLE ASSEMBLY",
    "SITE_HEADER": "MIRACLE ASSEMBLY MANAGEMENT PANEL",
    "SHOW_SIDEBAR": True,
    "SITE_SUBHEADER": "Miracle Assembly Management Panel",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("logo/cropped-logo.png"),
        "dark": lambda request: static("logo/cropped-logo.png"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("logo/cropped-logo.png"),
        "dark": lambda request: static("logo/cropped-logo.png"),
    },
    "DASHBOARD": {
        "show_search": True,
        "show_all_applications": True,
        "cards": [
            {
                "title": _("Users"),
                "icon": "group",
                "link": lambda request: reverse_lazy("admin:accounts_account_changelist"),
                "description": _("Manage registered users."),
            },
             {
                "title": "User Verifications",
                "icon": "verified",
                "link": lambda request: reverse_lazy("admin:accounts_userverification_changelist"),
                 "description": _("verification codes."),
            },
            {
                "title": _("Ministries"),
                "icon": "apartment",
                "link": lambda request: reverse_lazy("admin:accounts_ministry_changelist"),
                "description": _("Manage ministries."),
            },
            {
                "title": _("Memberships"),
                "icon": "people",
                "link": lambda request: reverse_lazy("admin:accounts_membership_changelist"),
                "description": _("Manage church memberships."),
            },
            {
                "title": _("Junior Church"),
                "icon": "child_care",
                "link": lambda request: reverse_lazy("admin:accounts_juniorchurch_changelist"),
                "description": _("Manage Junior Church attendance and offerings."),
            },
            {
                "title": _("Reports"),
                "icon": "bar_chart",
                "link": lambda request: reverse_lazy("admin:accounts_socialmediareport_changelist"),
                "description": _("View various reports."),
            },
        ],
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": lambda request: get_filtered_sidebar(request),
    },
}
