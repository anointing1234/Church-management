from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
import requests 
from decimal import Decimal, InvalidOperation
import logging
import json
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime, timedelta, time
from django.http import Http404
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout,login as auth_login,authenticate
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max
from decimal import Decimal,InvalidOperation
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.core.mail import EmailMultiAlternatives
import pytz
from datetime import datetime, timedelta
from pytz import timezone as pytz_timezone
import logging
from django.db import transaction
from django.db.models import F,Sum
from django.contrib.auth.decorators import login_required
import logging
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .models import Account
from django.contrib.auth import logout
import string
import random
from django.contrib.auth import authenticate, login
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from calendar import monthrange
from .decorators import role_required
from .access_control import role_access_required
from django.contrib.auth.decorators import login_required, user_passes_test
import uuid


User = get_user_model()
from .models import (
    Account,
    HillChurch, 
    SakponbaChurch,
    UseluChurch,
    MinistryChurch1,
    MinistryChurch2,
   MembershipChurch1,
   MembershipChurch2,
   JuniorChurchChurch1,
   JuniorChurchChurch2,
    SocialMediaReportChurch1,
    SocialMediaReportChurch2,
    MissionTeamSummary,
    BirthdayAdvertChurch1,
    BirthdayAdvertChurch2,
    UserVerification,
    PasswordResetCode,
) 


import logging
logger = logging.getLogger(__name__)


@role_access_required
@login_required(login_url='auth_login') 
def home_view(request):
    today = timezone.now().date()
    start_date = today - relativedelta(months=1)
    
    
    if not request.user.is_superuser:
        role = getattr(request.user, 'role', None)

        if role == 'missions_team_summary':
            return redirect('missions_summary')
        elif role == 'hill_church':
            return redirect('hill_church')
        elif role == 'sakponba_church':
            return redirect('sakponba_church')
        elif role == 'uselu_church':
            return redirect('uselu_church')
        elif role == 'ministry_church_1':
            return redirect('ministry', category='church1')
        elif role == 'ministry_church_2':
            return redirect('ministry', category='church2')
        elif role == 'membership_church_1':
            return redirect('membership', category='church1')
        elif role == 'membership_church_2':
            return redirect('membership', category='church2')
        elif role == 'junior_church_1':
            return redirect('junior_church', category='church1')
        elif role == 'junior_church_2':
            return redirect('junior_church', category='church2')
        elif role == 'multimedia_church_1':
            return redirect('ministry', category='multimedia1')
        elif role == 'multimedia_church_2':
            return redirect('ministry', category='multimedia2')
        elif role == 'social_media_report':
            return redirect('social-media', category='church1')
        elif role == 'birthday_advert_church_1':
            return redirect('birthday_adverts', category='church1')
        elif role == 'birthday_advert_church_2':
            return redirect('birthday_adverts', category='church2')
        else:
            return redirect('no_permission')  # fallback for unknown roles

    # Get counts for each queryset
    count1 = MissionTeamSummary.objects.filter(date__gte=start_date).count()
    count2 = HillChurch.objects.filter(date__gte=start_date).count()
    count3 = SakponbaChurch.objects.filter(date__gte=start_date).count()
    count4 = UseluChurch.objects.filter(date__gte=start_date).count()
    count5 = MinistryChurch1.objects.filter(date__gte=start_date).count()
    count6 = MembershipChurch2.objects.filter(date__gte=start_date).count()
    count7 = MembershipChurch1.objects.filter(date__gte=start_date).count()
    count8 = JuniorChurchChurch1.objects.filter(date__gte=start_date).count()
    count9 = JuniorChurchChurch2.objects.filter(date__gte=start_date).count()
    count10 = SocialMediaReportChurch1.objects.filter(date__gte=start_date).count()
    count11 = SocialMediaReportChurch2.objects.filter(date__gte=start_date).count()
    count12 = BirthdayAdvertChurch1.objects.filter(date__gte=start_date).count()
    count13 = BirthdayAdvertChurch2.objects.filter(date__gte=start_date).count()

    total_count = (
        count1 + count2 + count3 + count4 + count5 + count6 + count7 + count8 + 
        count9 + count10 + count11 + count12 + count13
    )
    
    team_models = [
        ('Ministry Church 1', MinistryChurch1),
        ('Ministry Church 2', MinistryChurch2),  # Add if exists
        ('Membership Church 1', MembershipChurch1),
        ('Membership Church 2', MembershipChurch2),
        ('Junior Church 1', JuniorChurchChurch1),
        ('Junior Church 2', JuniorChurchChurch2),
        ('Birthday Advert 1', BirthdayAdvertChurch1),
        ('Birthday Advert 2', BirthdayAdvertChurch2),
        ('Social Media Report 1', SocialMediaReportChurch1),
        ('Social Media Report 2', SocialMediaReportChurch2),
        ('Mission Team Summary', MissionTeamSummary),
        ('Sakponba Church', SakponbaChurch),
        ('Uselu Church', UseluChurch),
        ('Hill Church', HillChurch),
    ]
    
        # Get the start of the week for the start_date (assume Monday as start of week)
    start_of_period = start_date - timedelta(days=start_date.weekday())
    end_of_period = today

    team_weekly_counts = []

    # Loop through each model
    for name, model in team_models:
        # Track number of unique weeks that have at least one report
        reported_weeks = 0
        current = start_of_period

        while current <= end_of_period:
            week_start = datetime.combine(current, datetime.min.time())
            week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)

            # Check if any record exists for this team in this week
            if model.objects.filter(date__range=(week_start, week_end)).exists():
                reported_weeks += 1

            # Move to the next week
            current += timedelta(weeks=1)

        team_weekly_counts.append({
            'name': name,
            'count': reported_weeks,  # Weeks with report submitted
        })

    # Sort by most active weeks
    team_weekly_counts.sort(key=lambda x: x['count'], reverse=True)

    # Top 4 teams with most weekly submissions
    top_teams = team_weekly_counts[:4]

    # Best team = first one in the sorted list
    best_team = top_teams[0] if top_teams else None
        
    weekly_models = [
    MissionTeamSummary,
    HillChurch,
    SakponbaChurch,
    UseluChurch,
    MinistryChurch1,
    MinistryChurch2,
    MembershipChurch1,
    MembershipChurch2,
    JuniorChurchChurch1,
    JuniorChurchChurch2,
    SocialMediaReportChurch1,
    SocialMediaReportChurch2,
    BirthdayAdvertChurch1,
    BirthdayAdvertChurch2,
]


    # Calculate the total registered users
    total_registered_users = User.objects.count()
        
    # Get the current date
    current_date = datetime.now()

    # Calculate the start of the month
    first_day_of_month = current_date.replace(day=1)

    # Calculate the last day of the month
    _, num_days_in_month = monthrange(current_date.year, current_date.month)
    last_day_of_month = current_date.replace(day=num_days_in_month)

    # Prepare a list of week start dates in the month (Monday-based)
    week_starts = []
    current = first_day_of_month
    while current <= last_day_of_month:
        week_starts.append(current)
        current += timedelta(days=7)

    daily_progress = {}

    for idx, week_start in enumerate(week_starts):
        week_end = week_start + timedelta(days=6)
        week_end = min(week_end, last_day_of_month)

        week_start_dt = datetime.combine(week_start, time.min)
        week_end_dt = datetime.combine(week_end, time.max)

        weekly_record_count = 0  # Count total records from all models

        for model in weekly_models:
            count = model.objects.filter(date__range=(week_start_dt, week_end_dt)).count()
            weekly_record_count += count

        label = f"Week {idx + 1} ({week_start.strftime('%b %d')} - {week_end.strftime('%b %d')})"
        daily_progress[label] = weekly_record_count

   

    
    

            # Get count of records in a model
    def get_count(model):
        return model.objects.count()

    ministry1_total = get_count(MinistryChurch1)
    ministry2_total = get_count(MinistryChurch2)

    membership1_total = get_count(MembershipChurch1)
    membership2_total = get_count(MembershipChurch2)

    junior1_total = get_count(JuniorChurchChurch1)
    junior2_total = get_count(JuniorChurchChurch2)

    social_media_1_total = get_count(SocialMediaReportChurch1)
    social_media_2_total = get_count(SocialMediaReportChurch2)

        # MissionTeamSummary - count records instead of grand_total
    mission_team_total = get_count(MissionTeamSummary)

    sakponba_total = get_count(SakponbaChurch)
    uselu_total = get_count(UseluChurch)
    hill_total = get_count(HillChurch)
    Birthday_Advert_Church_1_total = get_count(BirthdayAdvertChurch1)
    Birthday_Advert_Church_2_total = get_count(BirthdayAdvertChurch2)


    # Prepare weekly, monthly, yearly data arrays for dataComparisonOptions.series
    weekly_data_comp = [
        {'x': "Sakponba Church", 'y': sakponba_total},
        {'x': "Uselu Church", 'y': uselu_total},
        {'x': "Hill Church", 'y': hill_total},
        {'x': "Membership Church 1", 'y': membership1_total},
        {'x': "Membership Church 2", 'y': membership2_total},
        {'x': "Ministry Church 1", 'y': ministry1_total},
        {'x': "Ministry Church 2", 'y': ministry2_total},
        {'x': "Junior Church 1", 'y': junior1_total},
        {'x': "Junior Church 2", 'y': junior2_total},
        {'x': "Social Media Report", 'y': social_media_1_total},
        {'x': "Social Media Report", 'y': social_media_2_total},
        {'x': "Missions Team Summary", 'y': mission_team_total},
        {'x': "Birthday Advert 1", 'y': Birthday_Advert_Church_1_total},
        {'x': "Birthday Advert 2", 'y': Birthday_Advert_Church_2_total},


    ]

    # Calculate monthly counts
    monthly_data_comp = []
    for item in weekly_data_comp:
        model_name = item['x']
        if model_name == "Sakponba Church":
            monthly_count = SakponbaChurch.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Uselu Church":
            monthly_count = UseluChurch.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Hill Church":
            monthly_count = HillChurch.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Membership Church 1":
            monthly_count = MembershipChurch1.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Membership Church 2":
            monthly_count = MembershipChurch2.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Ministry Church 1":
            monthly_count = MinistryChurch1.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Ministry Church 2":
            monthly_count = MinistryChurch2.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Junior Church 1":
            monthly_count = JuniorChurchChurch1.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Junior Church 2":
            monthly_count = JuniorChurchChurch2.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Social Media Report":
            monthly_count = SocialMediaReportChurch1.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Missions Team Summary":
            monthly_count = MissionTeamSummary.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Birthday Advert 1":
            monthly_count = BirthdayAdvertChurch1.objects.filter(date__gte=start_date, date__lte=today).count()
        elif model_name == "Birthday Advert 2":
            monthly_count = BirthdayAdvertChurch2.objects.filter(date__gte=start_date, date__lte=today).count()
        monthly_data_comp.append({'x': item['x'], 'y': monthly_count})

     # Calculate yearly counts
    yearly_data_comp = []
    for item in weekly_data_comp:
        model_name = item['x']
        if model_name == "Sakponba Church":
            yearly_count = SakponbaChurch.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Uselu Church":
            yearly_count = UseluChurch.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Hill Church":
            yearly_count = HillChurch.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Membership Church 1":
            yearly_count = MembershipChurch1.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Membership Church 2":
            yearly_count = MembershipChurch2.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Ministry Church 1":
            yearly_count = MinistryChurch1.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Ministry Church 2":
            yearly_count = MinistryChurch2.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Junior Church 1":
            yearly_count = JuniorChurchChurch1.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Junior Church 2":
            yearly_count = JuniorChurchChurch2.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Social Media Report":
            yearly_count = SocialMediaReportChurch1.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Missions Team Summary":
            yearly_count = MissionTeamSummary.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Birthday Advert 1":
            yearly_count = BirthdayAdvertChurch1.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        elif model_name == "Birthday Advert 2":
            yearly_count = BirthdayAdvertChurch2.objects.filter(date__gte=start_date - relativedelta(years=1), date__lte=today).count()
        
        # Add the result to the data list
        yearly_data_comp.append({
            'x': model_name,
            'y': yearly_count
        })
      
 

    data_comparison_series = [
        {'name': 'Weekly', 'data': weekly_data_comp},
        {'name': 'Monthly', 'data': monthly_data_comp},
        {'name': 'Yearly', 'data': yearly_data_comp},
    ]

    weeklyData = [
        {'team': "Ministry Church 1", 'values': [round(ministry1_total * 0.95)]},
        {'team': "Ministry Church 2", 'values': [round(ministry2_total * 0.87)]},
        {'team': "Membership Church 1", 'values': [round(membership1_total * 0.94)]},
        {'team': "Membership Church 2", 'values': [round(membership2_total * 0.93)]},
        {'team': "Junior Church 1", 'values': [round(junior1_total * 0.92)]},
        {'team': "Junior Church 2", 'values': [round(junior2_total * 0.90)]},
        {'team': "Social Media Report 1", 'values': [round(social_media_1_total * 0.93)]},
        {'team': "Social Media Report 2", 'values': [round(social_media_2_total * 0.92)]},
        {'team': "Missions Team Summary", 'values': [round(mission_team_total * 0.95)]},
        {'team': "Sakponba Church", 'values': [round(sakponba_total * 0.96)]},
        {'team': "Uselu Church", 'values': [round(uselu_total * 0.94)]},
        {'team': "Hill Church", 'values': [round(hill_total * 0.93)]},
        {'team': "Birthday Advert 1", 'values': [round(Birthday_Advert_Church_1_total * 0.90)]},
        {'team': "Birthday Advert 2", 'values': [round(Birthday_Advert_Church_2_total * 0.92)]},
    ]


    
    user_verifications = UserVerification.objects.select_related('user').all()
    users = Account.objects.all()
    context = {
        'total_count': total_count,
        'total_registered_users': total_registered_users,
        'daily_progress_labels': list(daily_progress.keys()),
        'daily_progress_counts': list(daily_progress.values()),
        'top_teams': top_teams,
        'best_team': best_team,
        'data_comparison_series': json.dumps(data_comparison_series),
        'weekly_data': json.dumps(weeklyData),
        'users': users,
        'user_verifications': user_verifications,
    }

    return render(request, 'home/index.html', context)










#------------------register/login templates

def register_view(request):
    return render(request,'auth/signup.html') 

def login_view(request):
    return render(request,'auth/login.html')


def stake_register_view(request):
    return render(request,'auth/stake_holders/stake_register.html') 



# -------authentication----start



# ----admin registeration
def Registeration(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone', '').strip()
        role = request.POST.get('role', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Basic validation
        if not all([username, email, phone_number, role, password, confirm_password]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

        if password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'})

        if Account.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists.'})

        if Account.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists.'})

        if Account.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'status': 'error', 'message': 'Phone number already exists.'})

        try:
            user = Account.objects.create_superuser(
                email=email,
                username=username,
                phone_number=phone_number,
                password=password,
                role='admin',
                is_active=True,
                is_staff=True,
                is_admin=True,
                is_superuser=True,
            )
            
            return JsonResponse({'status': 'success', 'message': 'Super admin registered successfully. Please login.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Error occurred: {str(e)}"})

    # For GET requests, render the registration page
    return render(request, 'auth/stake_holders/stake_register.html')





def generate_verification_code():
    return str(random.randint(100000, 999999))





# ------user registration
def user_registration(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone', '').strip()
        role = request.POST.get('role', '').strip().lower()
        password = request.POST.get('password1', '')
        confirm_password = request.POST.get('password2', '')

        if not all([username, email, phone_number, role, password, confirm_password]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

        if password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'})

        if Account.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists.'})

        if Account.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists.'})

        if Account.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'status': 'error', 'message': 'Phone number already exists.'})

        if Account.objects.filter(role=role).exists():
            return JsonResponse({'status': 'error', 'message': f"The role '{role}' is already assigned to another user."})

        try:
            user = Account.objects.create_user(
                email=email,
                username=username,
                phone_number=phone_number,
                password=password,
                role=role,
                is_active=True,
                is_staff=False,
                is_admin=False,
                is_superuser=False,
            )
            request.session['verification_email'] = user.email
            verification_code = generate_verification_code()
            UserVerification.objects.create(user=user, code=verification_code)

            # (Optional) Send the code via email or SMS here

            return JsonResponse({'status': 'success', 'message': 'User registered successfully. Please verify your account to continue.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Error occurred: {str(e)}"})

    return render(request, 'auth/signup.html')







def send_verification_code(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

    if not request.user.is_authenticated or not request.user.is_superuser:
        logger.warning(f"Unauthorized attempt to send verification code by user: {request.user.username}")
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        user = Account.objects.get(id=user_id)

        # Check if user is already verified
        user_verification = UserVerification.objects.filter(user=user).first()
        if user_verification and user_verification.is_verified:
            logger.warning(f"Verification code not sent: User {user.username} already verified.")
            return JsonResponse({'status': 'error', 'message': 'User is already verified.'})

        # Generate a 6-character verification code
        verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Save or update verification code
        if user_verification:
            user_verification.code = verification_code
            user_verification.is_verified = False
            user_verification.save()
        else:
            UserVerification.objects.create(user=user, code=verification_code, is_verified=False)

        # Send email
        subject = 'Your Verification Code'
        message = f'Hello {user.username},\n\nYour verification code is: {verification_code}\n\nPlease use this code to verify your account.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        logger.info(f"Verification code sent to user: {user.username}, email: {user.email}")
        return JsonResponse({'status': 'success', 'message': 'Verification code sent successfully.'})

    except Account.DoesNotExist:
        logger.error(f"User not found for ID: {user_id}")
        return JsonResponse({'status': 'error', 'message': 'User not found.'})
    except Exception as e:
        logger.error(f"Error sending verification code for user ID {user_id}: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'An error occurred while sending the verification code.'})



def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            return JsonResponse({'status': 'error', 'message': 'Email and password are required.'})

        user = authenticate(request, username=email, password=password)
        if user is not None:
            if not user.is_active:
                return JsonResponse({'status': 'error', 'message': 'Account disabled. Please contact support.'})

            if not user.is_superuser:
                try:
                    verification = UserVerification.objects.get(user=user)
                    if not verification.is_verified:
                        request.session['verification_email'] = user.email
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Account not verified. Redirecting to verification...',
                            'redirect_url': '/verify-registration/'
                        })
                    else:
                        # Already verified, cleanup
                        verification.delete()
                except UserVerification.DoesNotExist:
                    # ✅ No verification record found — assume verified
                    pass

            # Superuser or verified user can login
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful! Redirecting...'})

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid email or password.'})

    return render(request, 'auth/login.html')





def LogoutView(request):
    logout(request)
    return redirect('auth_login')

# -------authentication----end

def handle_church_service(request, model_class, template_name):
    filter_type = request.GET.get('filter', 'month')
    view_mode = request.GET.get('view')
    today = timezone.now().date()

    if filter_type == 'week':
        start_date = today - timedelta(days=7)
    elif filter_type == 'year':
        start_date = today - relativedelta(years=1)
    else:
        start_date = today - relativedelta(months=1)

    all_records = model_class.objects.filter(date__gte=start_date).order_by('-date')
    records = all_records if view_mode == 'all' else all_records[:1]

    if request.method == 'POST':
        if 'service_day' in request.POST and '_' not in next(iter(request.POST.keys()), ''):
            try:
                model_class.objects.create(
                    service_day=request.POST['service_day'],
                    service_no=request.POST['service_no'],
                    male=int(request.POST.get('male', 0)),
                    female=int(request.POST.get('female', 0)),
                    children=int(request.POST.get('children', 0)),
                    number_of_cars=int(request.POST.get('number_of_cars', 0)),
                    offering=Decimal(request.POST.get('offering', '0')),
                    tithe=Decimal(request.POST.get('tithe', '0')),
                    transfer=Decimal(request.POST.get('transfer', '0')),
                )
                return JsonResponse({'status': 'success', 'message': 'Record added'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Failed to add record: {e}'}, status=400)

        # Update existing records
        errors = False
        for key, value in request.POST.items():
            if '_' in key:
                field, rec_id = key.rsplit('_', 1)
                try:
                    rec = model_class.objects.get(id=int(rec_id))
                    if field in ['male', 'female', 'children', 'number_of_cars']:
                        setattr(rec, field, int(value or 0))
                    elif field in ['offering', 'tithe', 'transfer']:
                        setattr(rec, field, Decimal(value or '0'))
                    elif field in ['service_day', 'service_no', 'service']:
                        setattr(rec, field, value)
                    rec.save()
                except Exception:
                    errors = True              
        return JsonResponse({'status': 'error' if errors else 'success', 'message': 'Update completed'})

    return render(request, template_name, {
        'records': records,
        'total_count': all_records.count(),
        'filter_type': filter_type,
        'view_mode': view_mode,
    })
    
    
    
@login_required(login_url='auth_login') 
@role_access_required    
@role_required("hill_church")    
def hill(request):
    return handle_church_service(request, HillChurch, 'home/Hill_church.html')


@login_required(login_url='auth_login') 
@role_access_required
@role_required("sakponba_church")
def sakponba_view(request):
    return handle_church_service(request, SakponbaChurch, 'home/Sakponba_church.html')


@login_required(login_url='auth_login') 
@role_access_required
@role_required("uselu_church")
def uselu_view(request):
    return handle_church_service(request, UseluChurch, 'home/Uselu_church.html')



@login_required(login_url='auth_login')
@role_access_required
@role_required("ministry_church_1", "ministry_church_2")
def ministry_view(request, category):
    filter_type = request.GET.get('filter', 'month')
    view_mode = request.GET.get('view')
    today = timezone.now().date()

    category_models = {
        'church1': ("ministry_church_1", MinistryChurch1),
        'church2': ("ministry_church_2", MinistryChurch2),
    }

    category_key = category.lower()
    if category_key not in category_models:
        raise Http404("Invalid church category.")

    required_role, Model = category_models[category_key]

    if not request.user.is_superuser and request.user.role != required_role:
        return redirect('no_permission')

    if filter_type == 'week':
        start_date = today - timedelta(days=7)
    elif filter_type == 'year':
        start_date = today - relativedelta(years=1)
    else:
        start_date = today - relativedelta(months=1)

    queryset = Model.objects.filter(date__gte=start_date).order_by('-date')
    total_count = queryset.count()
    records = queryset if view_mode == 'all' else queryset[:1]

    total_male = queryset.aggregate(total=Sum('male'))['total'] or 0
    total_female = queryset.aggregate(total=Sum('female'))['total'] or 0
    total_cars = queryset.aggregate(total=Sum('number_of_cars'))['total'] or 0

    def get_differences(model_class, church_name):
        latest_date = model_class.objects.aggregate(Max('date'))['date__max']
        if not latest_date:
            return None
        latest_report = model_class.objects.filter(date=latest_date).first()
        if not latest_report:
            return None
        previous_report = model_class.objects.filter(date__lt=latest_date).order_by('-date').first()
        if not previous_report:
            return None
        previous_date = previous_report.date

        differences = {
            'church': church_name,
            'date': latest_date,
            'prev_date': previous_date,
            'male_diff': latest_report.male - previous_report.male,
            'female_diff': latest_report.female - previous_report.female,
            'children_diff': latest_report.children - previous_report.children,
            'cars_diff': latest_report.number_of_cars - previous_report.number_of_cars,
            'current_male': latest_report.male,
            'current_female': latest_report.female,
            'current_children': latest_report.children,
            'current_cars': latest_report.number_of_cars,
            'prev_male': previous_report.male,
            'prev_female': previous_report.female,
            'prev_children': previous_report.children,
            'prev_cars': previous_report.number_of_cars,
        }
        return differences

    church_name = "Church 1" if category_key == 'church1' else "Church 2"
    analysis_data = get_differences(Model, church_name)
    report_differences = [analysis_data] if analysis_data else []

    if request.method == 'POST':
        if getattr(request, 'access_denied', False):
            return JsonResponse({'status': 'error', 'message': 'Access denied: You have missed last week\'s report. Contact admin to pay fine.'}, status=403)
        if 'service_day' in request.POST:
            try:
                male = int(request.POST.get('male', 0))
                female = int(request.POST.get('female', 0))
                children = int(request.POST.get('children', 0))
                number_of_cars = int(request.POST.get('number_of_cars', 0))
                service_day = request.POST['service_day']
                service_no = request.POST.get('service', '')

                Model.objects.create(
                    user=request.user,
                    sunday_wednesday=service_day,
                    service=service_no,
                    male=male,
                    female=female,
                    children=children,
                    number_of_cars=number_of_cars,
                    date=timezone.now().date(),
                )
                return JsonResponse({'status': 'success', 'message': 'Record added'})
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid input for numeric fields.'}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Failed to add record: {e}'}, status=400)

    print(f"Passing to template: access_denied={getattr(request, 'access_denied', False)}")
    context = {
        'records': records,
        'category': category,
        'filter_type': filter_type,
        'total_count': total_count,
        'view_mode': view_mode or 'default',
        'total_male': total_male,
        'total_female': total_female,
        'total_cars': total_cars,
        'report_differences': report_differences,
        'access_denied': getattr(request, 'access_denied', False),
    }
    return render(request, 'home/Ministry_church.html', context)



@login_required(login_url='auth_login')
@role_access_required
@role_required("membership_church_1", "membership_church_2")
def membership_view(request, category):
    filter_type = request.GET.get('filter', 'month')
    view_mode = request.GET.get('view')
    today = timezone.now().date()

    # Map category to model and required role
    category_models = {
        'church1': ("membership_church_1", MembershipChurch1),
        'church2': ("membership_church_2", MembershipChurch2),
    }

    category_key = category.lower()
    if category_key not in category_models:
        raise Http404("Invalid church category.")

    required_role, Model = category_models[category_key]

    # Restrict access if role doesn't match (unless superuser)
    if not request.user.is_superuser and request.user.role != required_role:
        return redirect('no_permission')  # Or raise Http404 or render a custom page

    # Calculate start_date based on filter
    if filter_type == 'week':
        start_date = today - timedelta(days=7)
    elif filter_type == 'year':
        start_date = today - relativedelta(years=1)
    else:  # default to month
        start_date = today - relativedelta(months=1)

    # Get queryset for filtered records
    queryset = Model.objects.filter(date__gte=start_date).order_by('-date')
    total_count = queryset.count()
    records = queryset if view_mode == 'all' else queryset[:1]

    # Analysis: Calculate differences and totals for latest and previous reports
    def get_differences(model_class, church_name):
        # Get the latest report date
        latest_date = model_class.objects.aggregate(Max('date'))['date__max']
        if not latest_date:
            return None
        
        # Commented out Thursday validation and specific date logic for testing
        """
        # Ensure the latest date is a Thursday
        if latest_date.weekday() != 3:  # Thursday is 3 (0=Monday, 6=Sunday)
            return None

        # Get the latest Thursday report
        latest_report = model_class.objects.filter(date=latest_date).first()
        if not latest_report:
            return None
            
        # Get the previous Thursday report (one week before)
        previous_date = latest_date - timedelta(days=7)
        previous_report = model_class.objects.filter(date=previous_date).first()
        
        if not previous_report:
            return None
        """
        
        # For testing: Get the latest and second-latest reports regardless of day
        latest_report = model_class.objects.filter(date=latest_date).first()
        if not latest_report:
            return None
        
        previous_report = model_class.objects.filter(date__lt=latest_date).order_by('-date').first()
        if not previous_report:
            return None
        previous_date = previous_report.date

        # Calculate differences and collect totals
        differences = {
            'church': church_name,
            'date': latest_date,
            'prev_date': previous_date,
            'first_time_guests_diff': latest_report.first_time_guests - previous_report.first_time_guests,
            'second_time_guests_diff': latest_report.second_time_guests - previous_report.second_time_guests,
            'number_called_diff': latest_report.number_called - previous_report.number_called,
            'number_of_sms_diff': latest_report.number_of_sms - previous_report.number_of_sms,
            'number_of_converts_diff': latest_report.number_of_converts - previous_report.number_of_converts,
            'membership_interest_diff':latest_report.membership_interest - previous_report.membership_interest,
            'current_first_time_guests': latest_report.first_time_guests,
            'current_second_time_guests': latest_report.second_time_guests,
            'current_number_called': latest_report.number_called,
            'current_number_of_sms': latest_report.number_of_sms,
            'current_number_of_converts': latest_report.number_of_converts,
            'current_membership_interest': latest_report.membership_interest,
            'prev_first_time_guests': previous_report.first_time_guests,
            'prev_second_time_guests': previous_report.second_time_guests,
            'prev_number_called': previous_report.number_called,
            'prev_number_of_sms': previous_report.number_of_sms,
            'prev_number_of_converts': previous_report.number_of_converts,
            'prev_membership_interest': previous_report.membership_interest,
        }
        return differences

    # Get analysis data for the selected church
    church_name = "Church 1" if category_key == 'church1' else "Church 2"
    analysis_data = get_differences(Model, church_name)
    report_differences = [analysis_data] if analysis_data else []

    # Handle POST request
    if request.method == 'POST':
        try:
            first_time_guests = int(request.POST.get('first_time_guests', 0))
            second_time_guests = int(request.POST.get('second_time_guests', 0))
            number_called = int(request.POST.get('number_called', 0))
            number_of_sms = int(request.POST.get('number_of_sms', 0))
            membership_interest = int(request.POST.get('membership_interest', '0'))
            number_of_converts = int(request.POST.get('number_of_converts', 0))
            service_no = request.POST.get('service', '')

            Model.objects.create(
                first_time_guests=first_time_guests,
                service=service_no,
                second_time_guests=second_time_guests,
                number_called=number_called,
                number_of_sms=number_of_sms,
                membership_interest=membership_interest,
                number_of_converts=number_of_converts,
                date=timezone.now().date(),
            )
            return JsonResponse({'status': 'success', 'message': 'Record added'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid input for numeric fields.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to add record: {e}'}, status=400)

    # Render template
    context = {
        'records': records,
        'category': category,
        'filter_type': filter_type,
        'total_count': total_count,
        'view_mode': view_mode or 'default',
        'report_differences': report_differences,
    }
    return render(request, 'home/membership_church.html', context)





@login_required(login_url='auth_login')
@role_access_required
@role_required("junior_church_1", "junior_church_2")
def junior_church_view(request, category):
    filter_type = request.GET.get('filter', 'month')
    view_mode = request.GET.get('view')
    today = timezone.now().date()

    # Map category to model and required role
    category_models = {
        'church1': ("junior_church_1", JuniorChurchChurch1),
        'church2': ("junior_church_2", JuniorChurchChurch2),
    }

    category_key = category.lower()
    if category_key not in category_models:
        raise Http404("Invalid church category.")

    required_role, Model = category_models[category_key]

    # Restrict access if role doesn't match (unless superuser)
    if not request.user.is_superuser and request.user.role != required_role:
        return redirect('no_permission')  # Or raise Http404 or render a custom page

    # Determine the filter date range
    if filter_type == 'week':
        start_date = today - timedelta(days=7)
    elif filter_type == 'year':
        start_date = today - relativedelta(years=1)
    else:
        start_date = today - relativedelta(months=1)

    # Get queryset for filtered records
    queryset = Model.objects.filter(date__gte=start_date).order_by('-date')
    total_count = queryset.count()
    records = queryset if view_mode == 'all' else queryset[:1]

    # Analysis: Calculate differences and totals for latest and previous reports
    def get_differences(model_class, church_name):
        # Get the latest report date
        latest_date = model_class.objects.aggregate(Max('date'))['date__max']
        if not latest_date:
            return None
        
        # Commented out Thursday validation and specific date logic for testing
        """
        # Ensure the latest date is a Thursday
        if latest_date.weekday() != 3:  # Thursday is 3 (0=Monday, 6=Sunday)
            return None

        # Get the latest Thursday report
        latest_report = model_class.objects.filter(date=latest_date).first()
        if not latest_report:
            return None
            
        # Get the previous Thursday report (one week before)
        previous_date = latest_date - timedelta(days=7)
        previous_report = model_class.objects.filter(date=previous_date).first()
        
        if not previous_report:
            return None
        """
        
        # For testing: Get the latest and second-latest reports regardless of day
        latest_report = model_class.objects.filter(date=latest_date).first()
        if not latest_report:
            return None
        
        previous_report = model_class.objects.filter(date__lt=latest_date).order_by('-date').first()
        if not previous_report:
            return None
        previous_date = previous_report.date

        # Calculate differences and collect totals
        differences = {
            'church': church_name,
            'date': latest_date,
            'prev_date': previous_date,
            'creche_diff': latest_report.creche - previous_report.creche,
            'adorable_diff': latest_report.adorable - previous_report.adorable,
            'angels_diff': latest_report.angels - previous_report.angels,
            'shining_stars_diff': latest_report.shining_stars - previous_report.shining_stars,
            'great_minds_diff': latest_report.great_minds - previous_report.great_minds,
            'sparkles_diff': latest_report.sparkles - previous_report.sparkles,
            'children_offering_diff': latest_report.children_offering - previous_report.children_offering,
            'children_tithe_diff': latest_report.children_tithe - previous_report.children_tithe,
            'total_teens_diff': latest_report.total_teens - previous_report.total_teens,
            'teens_offering_diff': latest_report.teens_offering - previous_report.teens_offering,
            'teens_tithe_diff': latest_report.teens_tithe - previous_report.teens_tithe,
            'current_creche': latest_report.creche,
            'current_adorable': latest_report.adorable,
            'current_angels': latest_report.angels,
            'current_shining_stars': latest_report.shining_stars,
            'current_great_minds': latest_report.great_minds,
            'current_sparkles': latest_report.sparkles,
            'current_children_offering': latest_report.children_offering,
            'current_children_tithe': latest_report.children_tithe,
            'current_total_teens': latest_report.total_teens,
            'current_teens_offering': latest_report.teens_offering,
            'current_teens_tithe': latest_report.teens_tithe,
            'prev_creche': previous_report.creche,
            'prev_adorable': previous_report.adorable,
            'prev_angels': previous_report.angels,
            'prev_shining_stars': previous_report.shining_stars,
            'prev_great_minds': previous_report.great_minds,
            'prev_sparkles': previous_report.sparkles,
            'prev_children_offering': previous_report.children_offering,
            'prev_children_tithe': previous_report.children_tithe,
            'prev_total_teens': previous_report.total_teens,
            'prev_teens_offering': previous_report.teens_offering,
            'prev_teens_tithe': previous_report.teens_tithe,
        }
        return differences

    # Get analysis data for the selected church
    church_name = "Church 1" if category_key == 'church1' else "Church 2"
    analysis_data = get_differences(Model, church_name)
    report_differences = [analysis_data] if analysis_data else []

    if request.method == 'POST':
        service_no = request.POST.get('service')

        try:
            # Collect all numeric fields from POST (convert as needed)
            creche = int(request.POST.get('creche', 0))
            adorable = int(request.POST.get('adorable', 0))
            angels = int(request.POST.get('angels', 0))
            shining_stars = int(request.POST.get('shining_stars', 0))
            great_minds = int(request.POST.get('great_minds', 0))
            sparkles = int(request.POST.get('sparkles', 0))
            children_offering = float(request.POST.get('children_offering', 0))
            children_tithe = float(request.POST.get('children_tithe', 0))
            total_teens = int(request.POST.get('total_teens', 0))
            teens_offering = float(request.POST.get('teens_offering', 0))
            teens_tithe = float(request.POST.get('teens_tithe', 0))

            # Create new record without church_type field
            Model.objects.create(
                church_type='both',
                service=service_no,
                creche=creche,
                adorable=adorable,
                angels=angels,
                shining_stars=shining_stars,
                great_minds=great_minds,
                sparkles=sparkles,
                children_offering=children_offering,
                children_tithe=children_tithe,
                total_teens=total_teens,
                teens_offering=teens_offering,
                teens_tithe=teens_tithe,
                date=today,
            )

            return JsonResponse({'status': 'success', 'message': 'Record added successfully'})

        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid input in numeric fields.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to save record: {e}'}, status=400)

    context = {
        'records': records,
        'category': category,
        'filter_type': filter_type,
        'total_count': total_count,
        'view_mode': view_mode or 'default',
        'report_differences': report_differences,
    }
    return render(request, 'home/junior_church.html', context)

    

@login_required(login_url='auth_login')     
@role_access_required    
@role_required("social_media_report")
def social_media_report(request,category):
    filter_type = request.GET.get('filter', 'month')
    view_mode = request.GET.get('view')
    today = timezone.now().date()

    # Calculate start_date based on filter
    if filter_type == 'week':
        start_date = today - timedelta(days=7)
    elif filter_type == 'year':
        start_date = today - relativedelta(years=1)
    else:  # default to month
        start_date = today - relativedelta(months=1)

    # Map category to the corresponding model
    category_models = {
        'church1':  SocialMediaReportChurch1,
        'church2':  SocialMediaReportChurch2,
    }

    Model = category_models.get(category.lower())
    if not Model:
        raise Http404("Invalid church category.")

    queryset = Model.objects.filter(date__gte=start_date).order_by('-date')
    total_count = queryset.count()
    records = queryset if view_mode == 'all' else queryset[:1]

    # Handle POST request
    if request.method == 'POST':
        try:
            sotw = request.POST.get('sotw','')
            service = request.POST.get('service','')
            facebook_count = int(request.POST.get('facebook_count',0))
            youtube_count = int(request.POST.get('youtube_count',0))
            Model.objects.create(
                sotw=sotw,
                service=service,
                facebook_count=facebook_count,
                youtube_count=youtube_count,
                date=timezone.now().date(),
            )
            return JsonResponse({'status': 'success', 'message': 'Record added'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid input for numeric fields.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to add record: {e}'}, status=400)

    # Render template
    context = {
        'records': records,
        'category': category,
        'filter_type': filter_type,
        'total_count': total_count,
        'view_mode': view_mode or 'default',
    }
    return render(request, 'home/social_media_Report.html', context)
    
    
    
    
@login_required(login_url='auth_login')     
@role_access_required    
@role_required("multimedia_church_1", "multimedia_church_2")
def birthday_adverts_view(request, category):
    filter_type = request.GET.get('filter', 'month')
    view_mode = request.GET.get('view')
    today = timezone.now().date()
    
    
      
     # Map category to model and required role
    category_models = {
        'church1': ("multimedia_church_1",BirthdayAdvertChurch1),
        'church2': ("multimedia_church_2",BirthdayAdvertChurch2),
    }

    category_key = category.lower()
    if category_key not in category_models:
        raise Http404("Invalid church category.")

    required_role, Model = category_models[category_key]

    # Restrict access if role doesn't match (unless superuser)
    if not request.user.is_superuser and request.user.role != required_role:
        return redirect('no_permission')  # Or raise Http404 or render a custom page

    

    
    # Calculate start_date based on filter
    if filter_type == 'week':
        start_date = today - timedelta(days=7)
    elif filter_type == 'year':
        start_date = today - relativedelta(years=1)
    else:  # default to month
        start_date = today - relativedelta(months=1)

    # Map category to the corresponding model
    category_models = {
        'church1': BirthdayAdvertChurch1,
        'church2': BirthdayAdvertChurch2,
    }

    Model = category_models.get(category.lower())
    if not Model:
        raise Http404("Invalid church category.")

    queryset = Model.objects.filter(date__gte=start_date).order_by('-date')
    total_count = queryset.count()
    records = queryset if view_mode == 'all' else queryset[:1]

    # Handle POST request
    if request.method == 'POST':
        try:
            total = int(request.POST.get('total', 0))

            Model.objects.create(
                total=total,
                date=timezone.now().date(),
            )
            return JsonResponse({'status': 'success', 'message': 'Record added'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid input for numeric fields.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to add record: {e}'}, status=400)

    # Render template
    context = {
        'records': records,
        'category': category,
        'filter_type': filter_type,
        'total_count': total_count,
        'view_mode': view_mode or 'default',
    }
    return render(request, 'home/Multimedia.html', context)




@login_required(login_url='auth_login') 
@role_access_required
@role_required("missions_team_summary")
def missions_summary(request):
    filter_type = request.GET.get('filter', 'month')
    view_mode = request.GET.get('view')
    today = timezone.now().date()

    # Date filtering
    if filter_type == 'week':
        start_date = today - timedelta(days=7)
    elif filter_type == 'year':
        start_date = today - relativedelta(years=1)
    else:  # default to month
        start_date = today - relativedelta(months=1)

    queryset = MissionTeamSummary.objects.filter(date__gte=start_date).order_by('-date')
    total_count = queryset.count()
    records = queryset if view_mode == 'all' else queryset[:1]

    if request.method == 'POST':
        try:
            # All expected integer input fields except auto-calculated ones
            expected_fields = [
                'total_first_time_guests_evbuotubu',
                'total_first_time_guests_gra',
                'reached_first_time_guests_evbuotubu',
                'reached_first_time_guests_gra',
                'not_reachable_first_time_guests_evbuotubu',
                'not_reachable_first_time_guests_gra',
                'visitors_and_outsiders_evbuotubu',
                'visitors_and_outsiders_gra',
                'committed_to_second_visit_evbuotubu',
                'committed_to_second_visit_gra',
                'committed_to_believers_academy_evbuotubu',
                'committed_to_believers_academy_gra',
                'attended_cell_meeting_same_day_evbuotubu',
                'attended_cell_meeting_same_day_gra',
                'committed_to_cell_meeting_next_week_evbuotubu',
                'committed_to_cell_meeting_next_week_gra',
                'second_time_visitors_previous_week_evbuotubu',
                'second_time_visitors_previous_week_gra',
            ]

            data = {}
            for field in expected_fields:
                raw_val = request.POST.get(field)
                # Convert to int, default to 0 if missing or empty
                data[field] = int(raw_val) if raw_val and raw_val.isdigit() else 0

            # Create the summary record; evbuotubu, gra, grand_total calculated on save()
            summary = MissionTeamSummary.objects.create(**data)
            return JsonResponse({'status': 'success', 'message': 'Record added successfully'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to add record: {str(e)}'}, status=400)

    context = {
        'records': records,
        'filter_type': filter_type,
        'total_count': total_count,
        'view_mode': view_mode or 'default',
    }
    return render(request, 'home/missions_team_summary.html', context)


@login_required(login_url='auth_login') 
@role_access_required
def profile_views(request):
    return render(request,'home/profile.html')



def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        request.user.profile_picture = request.FILES['profile_picture']
        request.user.save()
        return render(request,'home/profile.html')
    return render(request,'home/profile.html')


def update_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Check for duplicate email and phone number
        if Account.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'Email is already in use by another account.')
            return redirect('profile')

        if Account.objects.filter(phone_number=phone_number).exclude(id=user.id).exists():
            messages.error(request, 'Phone number is already in use by another account.')
            return redirect('profile')

        # Update and save
        user.username = username
        user.email = email
        user.phone_number = phone_number
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')  # redirect after POST

    return render(request, 'home/profile.html')



def no_permission(request):
    return render(request,'home/eror404.html')


def locked_until_thursday(request):
    return render(request, 'home/locked_until_thursday.html')

def locked_need_to_pay_fine(request):
    return render(request, 'home/locked_need_to_pay_fine.html')

def locked(request):
    return render(request, 'home/locked.html')





def admin_check(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(admin_check)
def update_can_submit_permissions(request):
    if request.method == 'POST':
        users = Account.objects.all()
        for user in users:
            checkbox_name = f'can_submit_{user.id}'
            # Checkbox is checked if its name is in POST keys
            has_permission = checkbox_name in request.POST
            if user.can_submit_despite_missing_last_week != has_permission:
                user.can_submit_despite_missing_last_week = has_permission
                user.save()
        return redirect('update_can_submit_permissions')

    # GET request: show the form
    return redirect('home')


MODEL_MAP = {
    'church1': MinistryChurch1,
    'church2': MinistryChurch2,
    'membershipchurch1': MembershipChurch1,
    'membershipchurch2': MembershipChurch2,
    'juniorchurch1': JuniorChurchChurch1,
    'juniorchurch2': JuniorChurchChurch2,
    'birthdayadvert1': BirthdayAdvertChurch1,
    'birthdayadvert2': BirthdayAdvertChurch2,
    'socialmediareport1': SocialMediaReportChurch1,
    'socialmediareport2': SocialMediaReportChurch2,
    'missionteamsummary': MissionTeamSummary,
    'sakponbachurch': SakponbaChurch,
    'useluchurch': UseluChurch,
    'hillchurch': HillChurch,
}

def update_ministry_records(request, category):
    if request.method == 'POST':
        model_class = MODEL_MAP.get(category)
        if not model_class:
            print("❌ Invalid category")
            return HttpResponseBadRequest('Invalid category')

        update_ids = request.POST.getlist('update_ids')
        print(f"🔄 Updating records for model: {model_class.__name__}")
        print(f"🆔 Record IDs to update: {update_ids}")

        for record_id in update_ids:
            record = get_object_or_404(model_class, id=record_id)

            # ✅ Convert all inputs to integers before saving
            male = int(request.POST.get(f'male_{record_id}', 0))
            female = int(request.POST.get(f'female_{record_id}', 0))
            children = int(request.POST.get(f'children_{record_id}', 0))
            number_of_cars = int(request.POST.get(f'cars_{record_id}', 0))

            record.sunday_wednesday = request.POST.get(f'service_day_{record_id}')
            record.service = request.POST.get(f'service_{record_id}')
            record.male = male
            record.female = female
            record.children = children
            record.number_of_cars = number_of_cars

            # ✅ This triggers the save() in your model which calculates the total
            record.save()

            print(f"✅ Saved record ID: {record.id}")
            print(f"   - Male: {male}, Female: {female}, Children: {children}")
            print(f"   - Total (calculated in model): {record.total}")
            print(f"   - Cars: {number_of_cars}")

        print("✅ All records updated successfully.")
        return redirect('/')
    else:
        print("❌ Invalid request method")
        return HttpResponseBadRequest('Invalid request method')





def update_membership_records(request, category):
    if request.method == 'POST':
        model_class = MODEL_MAP.get(category)
        if not model_class:
            print("❌ Invalid category")
            return HttpResponseBadRequest('Invalid category')

        update_ids = request.POST.getlist('update_ids')
        print(f"🔄 Updating records for model: {model_class.__name__}")
        print(f"🆔 Record IDs to update: {update_ids}")

        for record_id in update_ids:
            record = get_object_or_404(model_class, id=record_id)

            # ✅ Convert all inputs to integers before saving
            first_time_guests = int(request.POST.get(f'first_time_guests_{record_id}', 0))
            second_time_guests = int(request.POST.get(f'second_time_guests_{record_id}', 0))
            number_called = int(request.POST.get(f'number_called_{record_id}', 0))
            number_of_sms = int(request.POST.get(f'number_of_sm_{record_id}', 0))
            membership_interest = int(request.POST.get(f'membership_interest_{record_id}', 0))
            number_of_converts = int(request.POST.get(f'number_of_converts_{record_id}', 0))

            record.service = request.POST.get(f'service_{record_id}')
            record.first_time_guests =  first_time_guests
            record.second_time_guests =  second_time_guests
            record.number_called =   number_called
            record.number_of_sms =   number_of_sms 
            record.membership_interest = membership_interest
            record.number_of_converts =  number_of_converts

            # ✅ This triggers the save() in your model which calculates the total
            record.save()

            print(f"✅ Saved record ID: {record.id}")
          
        print("✅ All records updated successfully.")
        return redirect('/')
    else:
        print("❌ Invalid request method")
        return HttpResponseBadRequest('Invalid request method')






def update_Junior_records(request, category):
    if request.method == 'POST':
        model_class = MODEL_MAP.get(category)
        if not model_class:
            return JsonResponse({'status': 'error', 'message': 'Invalid category'})

        update_ids = request.POST.getlist('update_ids')
        print(f"🔄 Updating records for model: {model_class.__name__}")
        print(f"🆔 Record IDs to update: {update_ids}")

        for record_id in update_ids:
            record = get_object_or_404(model_class, id=record_id)

            # Debugging: Print all POST data
            print(request.POST)

            service_value = request.POST.get(f'service_{record_id}')
            if not service_value:
                return JsonResponse({
                    'status': 'error', 
                    'message': f'Missing service value for record ID {record_id}'
                })
            record.service = int(service_value)

            # Children Department (integers)
            record.creche = int(request.POST.get(f'creche_{record_id}', 0))
            record.adorable = int(request.POST.get(f'adorable_{record_id}', 0))
            record.angels = int(request.POST.get(f'angels_{record_id}', 0))
            record.shining_stars = int(request.POST.get(f'shining_stars_{record_id}', 0))
            record.great_minds = int(request.POST.get(f'great_minds_{record_id}', 0))
            record.sparkles = int(request.POST.get(f'sparkles_{record_id}', 0))

            # Children Department (decimals)
            record.children_offering = Decimal(request.POST.get(f'children_offering_{record_id}', '0.00'))
            record.children_tithe = Decimal(request.POST.get(f'children_tithe_{record_id}', '0.00'))

            # Teens Department (integers and decimals)
            record.total_teens = int(request.POST.get(f'total_teens_{record_id}', 0))
            record.teens_offering = Decimal(request.POST.get(f'teens_offering_{record_id}', '0.00'))
            record.teens_tithe = Decimal(request.POST.get(f'teens_tithe_{record_id}', '0.00'))

            try:
                record.save()
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Failed to save record: {str(e)}'})

        return JsonResponse({'status': 'success', 'message': 'Records updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    




def  update_multimedia_records(request, category):
    if request.method == 'POST':
        model_class = MODEL_MAP.get(category)
        if not model_class:
            return JsonResponse({'status': 'error', 'message': 'Invalid category'})

        update_ids = request.POST.getlist('update_ids')
        print(f"🔄 Updating records for model: {model_class.__name__}")
        print(f"🆔 Record IDs to update: {update_ids}")

        for record_id in update_ids:
            record = get_object_or_404(model_class, id=record_id)

            print(request.POST)


            record.total = int(request.POST.get(f'total_number_birthday_adverts_{ record.total }', 0))
            try:
                record.save()
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Failed to save record: {str(e)}'})

        return JsonResponse({'status': 'success', 'message': 'Records updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})





def update_social_media_Report(request, category):
    if request.method == 'POST':
        model_class = MODEL_MAP.get(category)
        if not model_class:
            return JsonResponse({'status': 'error', 'message': 'Invalid category'})

        update_ids = request.POST.getlist('update_ids')
        print(f"🔄 Updating records for model: {model_class.__name__}")
        print(f"🆔 Record IDs to update: {update_ids}")

        for record_id in update_ids:
            record = get_object_or_404(model_class, id=record_id)

            print(request.POST)
            
            record.sotw = request.POST.get(f'sotw_{ record.id }',0)
            record.service = request.POST.get(f'service_{ record.id }',0)
            record.facebook_count = int(request.POST.get(f'facebook_count_{ record.id }',0))
            record.youtube_count = int(request.POST.get(f'youtube_count_{ record.id }',0))
            try:
                record.save()
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Failed to save record: {str(e)}'})

        return JsonResponse({'status': 'success', 'message': 'Records updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    







def Sakponba_update_view(request, category):
    if request.method == 'POST':
        model_class = MODEL_MAP.get(category)
        if not model_class:
            print("❌ Invalid category")
            return HttpResponseBadRequest('Invalid category')

        update_ids = request.POST.getlist('update_ids')
        print(f"🔄 Updating records for model: {model_class.__name__}")
        print(f"🆔 Record IDs to update: {update_ids}")

        for record_id in update_ids:
            record = get_object_or_404(model_class, id=record_id)

            # ✅ Convert all inputs to integers before saving
            male = int(request.POST.get(f'male_{ record.id }', 0))
            female = int(request.POST.get(f'female_{ record.id }', 0))
            children = int(request.POST.get(f'children_{ record.id }', 0))
            number_of_cars = int(request.POST.get(f'number_of_cars_{ record.id }', 0))
            offering = Decimal(request.POST.get(f'offering_{ record.id }', '0.00'))
            tithe = Decimal(request.POST.get(f'tithe_{ record.id }', '0.00'))
            transfer = Decimal(request.POST.get(f'transfer_{ record.id }', '0.00'))
         

            record.service_day = request.POST.get(f'service_day_{ record.id }')
            record.service_no = request.POST.get(f'service_{record_id}')
            record.male =  male
            record.female = female
            record.children = children
            record.number_of_cars = number_of_cars 
            record.offering = offering
            record.tithe =  tithe
            record.transfer = transfer

            # ✅ This triggers the save() in your model which calculates the total
            record.save()

            print(f"✅ Saved record ID: {record.id}")
          
        print("✅ All records updated successfully.")
        return redirect('/')
    else:
        print("❌ Invalid request method")
        return HttpResponseBadRequest('Invalid request method')








def Uselu_update_view(request, category):
    if request.method == 'POST':
        model_class = MODEL_MAP.get(category)
        if not model_class:
            print("❌ Invalid category")
            return HttpResponseBadRequest('Invalid category')

        update_ids = request.POST.getlist('update_ids')
        print(f"🔄 Updating records for model: {model_class.__name__}")
        print(f"🆔 Record IDs to update: {update_ids}")

        for record_id in update_ids:
            record = get_object_or_404(model_class, id=record_id)

            # ✅ Convert all inputs to integers before saving
            male = int(request.POST.get(f'male_{ record.id }', 0))
            female = int(request.POST.get(f'female_{ record.id }', 0))
            children = int(request.POST.get(f'children_{ record.id }', 0))
            number_of_cars = int(request.POST.get(f'number_of_cars_{ record.id }', 0))
            offering = Decimal(request.POST.get(f'offering_{ record.id }', '0.00'))
            tithe = Decimal(request.POST.get(f'tithe_{ record.id }', '0.00'))
            transfer = Decimal(request.POST.get(f'transfer_{ record.id }', '0.00'))
         

            record.service_day = request.POST.get(f'service_day_{ record.id }')
            record.service_no = request.POST.get(f'service_{record_id}')
            record.male =  male
            record.female = female
            record.children = children
            record.number_of_cars = number_of_cars 
            record.offering = offering
            record.tithe =  tithe
            record.transfer = transfer

            # ✅ This triggers the save() in your model which calculates the total
            record.save()

            print(f"✅ Saved record ID: {record.id}")
          
        print("✅ All records updated successfully.")
        return redirect('/')
    else:
        print("❌ Invalid request method")
        return HttpResponseBadRequest('Invalid request method')






def Hill_update_view(request, category):
    if request.method == 'POST':
        model_class = MODEL_MAP.get(category)
        if not model_class:
            print("❌ Invalid category")
            return HttpResponseBadRequest('Invalid category')

        update_ids = request.POST.getlist('update_ids')
        print(f"🔄 Updating records for model: {model_class.__name__}")
        print(f"🆔 Record IDs to update: {update_ids}")

        for record_id in update_ids:
            record = get_object_or_404(model_class, id=record_id)

            # ✅ Convert all inputs to integers before saving
            male = int(request.POST.get(f'male_{ record.id }', 0))
            female = int(request.POST.get(f'female_{ record.id }', 0))
            children = int(request.POST.get(f'children_{ record.id }', 0))
            number_of_cars = int(request.POST.get(f'number_of_cars_{ record.id }', 0))
            offering = Decimal(request.POST.get(f'offering_{ record.id }', '0.00'))
            tithe = Decimal(request.POST.get(f'tithe_{ record.id }', '0.00'))
            transfer = Decimal(request.POST.get(f'transfer_{ record.id }', '0.00'))
         

            record.service_day = request.POST.get(f'service_day_{ record.id }')
            record.service_no = request.POST.get(f'service_{record_id}')
            record.male =  male
            record.female = female
            record.children = children
            record.number_of_cars = number_of_cars 
            record.offering = offering
            record.tithe =  tithe
            record.transfer = transfer

            # ✅ This triggers the save() in your model which calculates the total
            record.save()

            print(f"✅ Saved record ID: {record.id}")
          
        print("✅ All records updated successfully.")
        return redirect('/')
    else:
        print("❌ Invalid request method")
        return HttpResponseBadRequest('Invalid request method')




def mission_edit_inline(request, pk):
    summary = get_object_or_404(MissionTeamSummary, pk=pk)

    fields = [
        'total_first_time_guests_evbuotubu',
        'reached_first_time_guests_evbuotubu',
        'not_reachable_first_time_guests_evbuotubu',
        'visitors_and_outsiders_evbuotubu',
        'committed_to_second_visit_evbuotubu',
        'committed_to_believers_academy_evbuotubu',
        'total_first_time_guests_gra',
        'reached_first_time_guests_gra',
        'not_reachable_first_time_guests_gra',
        'visitors_and_outsiders_gra',
        'committed_to_second_visit_gra',
        'committed_to_believers_academy_gra',
    ]

    try:
        for field in fields:
            if field in request.POST:
                value_str = request.POST.get(field)
                value_int = int(value_str) if value_str.isdigit() else 0
                setattr(summary, field, value_int)

        # Recalculate totals (assuming your model does not do this automatically)
        summary.evbuotubu = (
            summary.total_first_time_guests_evbuotubu +
            summary.reached_first_time_guests_evbuotubu +
            summary.not_reachable_first_time_guests_evbuotubu +
            summary.visitors_and_outsiders_evbuotubu +
            summary.committed_to_second_visit_evbuotubu +
            summary.committed_to_believers_academy_evbuotubu
        )

        summary.gra = (
            summary.total_first_time_guests_gra +
            summary.reached_first_time_guests_gra +
            summary.not_reachable_first_time_guests_gra +
            summary.visitors_and_outsiders_gra +
            summary.committed_to_second_visit_gra +
            summary.committed_to_believers_academy_gra
        )

        summary.grand_total = summary.evbuotubu + summary.gra

        summary.save()
        messages.success(request, "Mission summary updated successfully.")

    except ValueError:
        messages.error(request, "Please enter valid numbers in all fields.")
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('missions_summary') 





def verication_views(request):
    return render(request,'auth/verification.html')




def resend_verification_code(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    email = request.session.get('verification_email')
    if not email:
        return redirect('signup')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return redirect('signup')

    # Delete any existing UserVerification for this user
    UserVerification.objects.filter(user=user).delete()

    # Create a new verification record with a new code
    user_verification = UserVerification.objects.create(user=user)
    user_verification.generate_code()  

    return redirect('verify_registration')






def verify_registration(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        code = request.POST.get('verification_code', '').strip()
        email = request.session.get('verification_email')

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Session expired. Please signup again.'})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'})

        try:
            user_verification = UserVerification.objects.get(user=user)
        except UserVerification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Verification record not found. Please resend the code.'})

        if user_verification.code == code:
            user.is_active = True  # or user.is_verified = True if you use a custom field
            user.save()

            user_verification.is_verified = True
            user_verification.save()

            request.session.pop('verification_email', None)

            return JsonResponse({'status': 'success', 'message': 'Account verified successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid verification code.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})



def send_reset_code_view(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email is required.'}, status=400)

        try:
            user = Account.objects.get(email=email)
            code = str(uuid.uuid4()).replace("-", "")[:6]
            PasswordResetCode.objects.create(user=user, code=code)

            send_mail(
                subject="Your Reset Code",
                message=f"Your reset code is: {code}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )

            return JsonResponse({'status': 'success', 'message': 'A reset code has been sent to your email.'})
        except Account.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Email address not found.'}, status=404)

    return render(request, "auth/send_reset_pass.html")



def reset_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        code = request.POST.get("code")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Basic validation
        if not all([email, code, new_password, confirm_password]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

        if new_password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'}, status=400)

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Email address not found.'}, status=404)

        try:
            reset_entry = PasswordResetCode.objects.get(user=user, code=code)
            if reset_entry.is_expired():
                reset_entry.delete()
                return JsonResponse({'status': 'error', 'message': 'Reset code expired. Please request a new one.'}, status=400)

            # Update password
            user.password = make_password(new_password)
            user.save()
            reset_entry.delete()

            return JsonResponse({'status': 'success', 'message': 'Password reset successfully. You can now log in.'})

        except PasswordResetCode.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid reset code for this email.'}, status=404)

    # GET request - render reset form
    return render(request, "auth/reset_password.html")