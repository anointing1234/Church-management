from django.utils import timezone
import datetime
from django.shortcuts import redirect
from functools import wraps
from .models import (
    HillChurch, SakponbaChurch, UseluChurch,
    MinistryChurch1, MinistryChurch2,
    MembershipChurch1, MembershipChurch2,
    JuniorChurchChurch1, JuniorChurchChurch2,
    SocialMediaReportChurch1, SocialMediaReportChurch2,
    MissionTeamSummary,
    BirthdayAdvertChurch1, BirthdayAdvertChurch2
)

ROLE_MODEL_MAP = {
    "hill_church": HillChurch,
    "sakponba_church": SakponbaChurch,
    "uselu_church": UseluChurch,
    "ministry_church_1": MinistryChurch1,
    "ministry_church_2": MinistryChurch2,
    "membership_church_1": MembershipChurch1,
    "membership_church_2": MembershipChurch2,
    "junior_church_1": JuniorChurchChurch1,
    "junior_church_2": JuniorChurchChurch2,
    "social_media_report": SocialMediaReportChurch1,
    "missions_team_summary": MissionTeamSummary,
    "multimedia_church_1": BirthdayAdvertChurch1,
    "multimedia_church_2": BirthdayAdvertChurch2,
    "birthday_advert_church_1": BirthdayAdvertChurch1,
    "birthday_advert_church_2": BirthdayAdvertChurch2,
}

def get_last_week_thursday_to_friday_noon(now):
    weekday = now.weekday()  # Monday = 0, Sunday = 6
    days_to_current_thursday = (weekday - 3) % 7  # Days to current Thursday
    current_thursday = now - datetime.timedelta(days=days_to_current_thursday)
    # Subtract 7 days to get the previous Thursday
    last_thursday = current_thursday - datetime.timedelta(days=7)
    start = last_thursday.replace(hour=13, minute=0, second=0, microsecond=0)  # Thursday 1:00 PM
    end = current_thursday.replace(hour=12, minute=0, second=0, microsecond=0)  # Current Thursday 12:00 PM
    print(f"DEBUG: Submission window - Start={start}, End={end}, Timezone={start.tzinfo}")
    return start, end

def role_access_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            print("DEBUG: ⛔ User not authenticated, redirecting to login")
            request.restriction_message = "Please log in to access this page."
            return redirect("login_view")

        request.access_denied = False
        print(f"DEBUG: Initial access_denied set to {request.access_denied}, User: {user.username}")

        if user.is_superuser:
            print("DEBUG: ✅ Superuser bypassed check, access_denied=False")
            return view_func(request, *args, **kwargs)

        role = getattr(user, "role", None)
        model = ROLE_MODEL_MAP.get(role)

        if not model:
            print(f"DEBUG: ⛔ No model found for role: {role}, setting access_denied=True")
            request.access_denied = True
            request.restriction_message = "Invalid user role."
            return view_func(request, *args, **kwargs)

        USE_DUMMY_TIME = True  # Use real time for production
        if USE_DUMMY_TIME:
            dummy_now = datetime.datetime(2025, 7, 3, 14, 0, 0)
            now = timezone.make_aware(dummy_now)
            print(f"DEBUG: Using dummy time: {now}")
        else:
            now = timezone.now()
            print(f"DEBUG: Using current time: {now}, Timezone={now.tzinfo}")

        weekday = now.weekday()
        hour = now.hour
        queryset = model.objects.all()  # Check all records in the model
        total_records = queryset.count()
        record_dates = queryset.values('created_at', 'date', 'user__username')

        print(f"DEBUG: User Role: {role}, Username: {user.username}")
        print(f"DEBUG: Total Records in {model.__name__}: {total_records}")
        print(f"DEBUG: Record Details: {list(record_dates)}")
        print(f"DEBUG: Current Weekday: {weekday} (0=Monday, 3=Thursday, 4=Friday)")
        print(f"DEBUG: Current Hour: {hour} (UTC)")

        start, end = get_last_week_thursday_to_friday_noon(now)
        # Filter on 'date' field instead of 'created_at'
        has_recent_record = queryset.filter(date__range=(start.date(), end.date())).exists()
        recent_records = queryset.filter(date__range=(start.date(), end.date())).values('created_at', 'date', 'user__username')
        can_submit_override = getattr(user, "can_submit_despite_missing_last_week", False)
        print(f"DEBUG: Has recent record in window ({start} to {end}): {has_recent_record}")
        print(f"DEBUG: Recent Records: {list(recent_records)}")
        print(f"DEBUG: Can submit despite missing last week: {can_submit_override}")

        if total_records == 0:
            print("DEBUG: ✅ No records in model, access_denied=False")
            return view_func(request, *args, **kwargs)

        if total_records == 1:
            print("DEBUG: ✅ Only one record in model, access_denied=False")
            return view_func(request, *args, **kwargs)

        if weekday < 3:
            print("DEBUG: ⛔ Before Thursday, setting access_denied=True")
            request.access_denied = True
            request.restriction_message = "Submissions are only allowed from Thursday 1:00 PM to Friday 12:00 PM."
            return view_func(request, *args, **kwargs)

        if weekday == 3 or (weekday == 4 and hour < 12):
            if has_recent_record or can_submit_override:
                print("DEBUG: ✅ Within allowed window and has recent record or override, access_denied=False")
                return view_func(request, *args, **kwargs)
            else:
                print("DEBUG: ⛔ Within window but no recent record or override, setting access_denied=True")
                request.access_denied = True
                request.restriction_message = "No submission found for the previous week."
                return view_func(request, *args, **kwargs)

        print("DEBUG: ⛔ Outside allowed window, setting access_denied=True")
        request.access_denied = True
        request.restriction_message = "Submissions are only allowed from Thursday 1:00 PM to Friday 12:00 PM."
        return view_func(request, *args, **kwargs)

    return wrapper