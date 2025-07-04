from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import (
    Account,
    MinistryChurch1, MinistryChurch2,
    MembershipChurch1, MembershipChurch2,
    JuniorChurchChurch1, JuniorChurchChurch2,
    BirthdayAdvertChurch1, BirthdayAdvertChurch2,
    SocialMediaReportChurch1, SocialMediaReportChurch2,
    MissionTeamSummary,
    SakponbaChurch,
    UseluChurch,
    HillChurch,
    UserVerification,
)

# ─── 1. Base admin that “opens up” all four perms ───
class BaseUnfoldAdmin(UnfoldModelAdmin):
    """
    A ModelAdmin that always returns True for view/add/change/delete,
    but still respects your underlying Django permissions.
    """
    def has_view_permission(self, request, obj=None):
        return request.user.has_perm(f"{self.opts.app_label}.view_{self.opts.model_name}")

    def has_add_permission(self, request):
        return request.user.has_perm(f"{self.opts.app_label}.add_{self.opts.model_name}")

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm(f"{self.opts.app_label}.change_{self.opts.model_name}")

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm(f"{self.opts.app_label}.delete_{self.opts.model_name}")


# ─── 2. Your Account forms ───
class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ("email", "username", "groups", "user_permissions")
        widgets = {
            "groups": FilteredSelectMultiple("Groups", is_stacked=False),
            "user_permissions": FilteredSelectMultiple("User permissions", is_stacked=False),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()
        return user


class AccountChangeForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            "email",
            "username",
            "groups",
            "user_permissions",
            "is_active",
            "is_staff",
            "is_superuser",
            "can_submit_despite_missing_last_week",
        )
        widgets = {
            "groups": FilteredSelectMultiple("Groups", is_stacked=False),
            "user_permissions": FilteredSelectMultiple("User permissions", is_stacked=False),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.save_m2m()
        return user


# ─── 3. Register each model, inheriting BaseUnfoldAdmin ───
@admin.register(Account)
class AccountAdmin(BaseUnfoldAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm

    list_display = ("profile_pic_thumbnail","email", "username","role", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "username")
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("email", "username", "password", "profile_picture")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "can_submit_despite_missing_last_week",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "profile_picture",
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "can_submit_despite_missing_last_week",
                ),
            },
        ),
    )
    
    def profile_pic_thumbnail(self, obj):
        if obj.profile_picture:
            return format_html(f'<img src="{obj.profile_picture.url}" width="50" height="50" style="border-radius:50%;" />')
        return "-"
    profile_pic_thumbnail.short_description = "Profile Pic"

    def get_form(self, request, obj=None, **kwargs):
        kwargs["form"] = self.add_form if obj is None else self.form
        return super().get_form(request, obj, **kwargs)




# MinistryChurch admin
@admin.register(MinistryChurch1)
class MinistryChurch1Admin(UnfoldModelAdmin):
    list_display = ('date', 'sunday_wednesday', 'service', 'male', 'female', 'children', 'total', 'number_of_cars')
    list_filter = ('sunday_wednesday', 'service', 'date')
    search_fields = ('date',)
    readonly_fields = ('total',)

@admin.register(MinistryChurch2)
class MinistryChurch2Admin(UnfoldModelAdmin):
    list_display = ('date', 'sunday_wednesday', 'service', 'male', 'female', 'children', 'total', 'number_of_cars')
    list_filter = ('sunday_wednesday', 'service', 'date')
    search_fields = ('date',)
    readonly_fields = ('total',)

# MembershipChurch admin
@admin.register(MembershipChurch1)
class MembershipChurch1Admin(UnfoldModelAdmin):
    list_display = ('date', 'service', 'first_time_guests', 'second_time_guests', 'number_called', 'number_of_sms', 'membership_interest', 'number_of_converts')
    list_filter = ('service', 'date')
    search_fields = ('date',)

@admin.register(MembershipChurch2)
class MembershipChurch2Admin(UnfoldModelAdmin):
    list_display = ('date', 'service', 'first_time_guests', 'second_time_guests', 'number_called', 'number_of_sms', 'membership_interest', 'number_of_converts')
    list_filter = ('service', 'date')
    search_fields = ('date',)

# JuniorChurch admin
@admin.register(JuniorChurchChurch1)
class JuniorChurchChurch1Admin(UnfoldModelAdmin):
    list_display = ('date', 'service', 'church_type', 'total_children', 'children_offering', 'children_tithe', 'children_total', 'total_teens', 'teens_offering', 'teens_tithe', 'teens_total')
    list_filter = ('service', 'church_type', 'date')
    readonly_fields = ('total_children', 'children_total', 'teens_total')
    search_fields = ('date',)

@admin.register(JuniorChurchChurch2)
class JuniorChurchChurch2Admin(UnfoldModelAdmin):
    list_display = ('date', 'service', 'church_type', 'total_children', 'children_offering', 'children_tithe', 'children_total', 'total_teens', 'teens_offering', 'teens_tithe', 'teens_total')
    list_filter = ('service', 'church_type', 'date')
    readonly_fields = ('total_children', 'children_total', 'teens_total')
    search_fields = ('date',)

# BirthdayAdvert admin
@admin.register(BirthdayAdvertChurch1)
class BirthdayAdvertChurch1Admin(UnfoldModelAdmin):
    list_display = ('date', 'total')
    readonly_fields = ('date',)
    search_fields = ('date',)

@admin.register(BirthdayAdvertChurch2)
class BirthdayAdvertChurch2Admin(UnfoldModelAdmin):
    list_display = ('date', 'total')
    readonly_fields = ('date',)
    search_fields = ('date',)

@admin.register(SocialMediaReportChurch1)
class SocialMediaReportChurch1Admin(UnfoldModelAdmin):
    list_display = ('date', 'sotw', 'service', 'facebook_count', 'youtube_count')
    list_filter = ('sotw', 'service', 'date')
    search_fields = ('date',)

@admin.register(SocialMediaReportChurch2)
class SocialMediaReportChurch2Admin(UnfoldModelAdmin):
    list_display = ('date', 'sotw', 'service', 'facebook_count', 'youtube_count')
    list_filter = ('sotw', 'service', 'date')
    search_fields = ('date',)



@admin.register(MissionTeamSummary)
class MissionTeamSummaryAdmin(BaseUnfoldAdmin):
    readonly_fields = ("date", "evbuotubu", "gra", "grand_total")
    list_display    = ("date", "evbuotubu", "gra", "grand_total")
    list_filter     = ("date",)

    fieldsets = (
        ("Date & Totals", {
            "fields": ("date", "evbuotubu", "gra", "grand_total"),
        }),
        ("Evbuotubu Metrics", {
            "fields": (
                "total_first_time_guests_evbuotubu",
                "reached_first_time_guests_evbuotubu",
                "not_reachable_first_time_guests_evbuotubu",
                "visitors_and_outsiders_evbuotubu",
                "committed_to_second_visit_evbuotubu",
                "committed_to_believers_academy_evbuotubu",
                "attended_cell_meeting_same_day_evbuotubu",
                "committed_to_cell_meeting_next_week_evbuotubu",
                "second_time_visitors_previous_week_evbuotubu",
            )
        }),
        ("GRA Metrics", {
            "fields": (
                "total_first_time_guests_gra",
                "reached_first_time_guests_gra",
                "not_reachable_first_time_guests_gra",
                "visitors_and_outsiders_gra",
                "committed_to_second_visit_gra",
                "committed_to_believers_academy_gra",
                "attended_cell_meeting_same_day_gra",
                "committed_to_cell_meeting_next_week_gra",
                "second_time_visitors_previous_week_gra",
            )
        }),
    )




@admin.register(SakponbaChurch)
class SakponbaChurchAdmin(BaseUnfoldAdmin):
    list_display = (
        "service_day",
        "service_no",
        "male",
        "female",
        "children",
        "attendance_total",
        "number_of_cars",
        "offering",
        "tithe",
        "transfer",
        "financial_total",
        "date",
    )
    list_filter = ("service_day", "service_no", "date")
    readonly_fields = ("attendance_total", "financial_total")


@admin.register(UseluChurch)
class UseluChurchAdmin(BaseUnfoldAdmin):
    list_display = (
        "service_day",
        "service_no",
        "male",
        "female",
        "children",
        "attendance_total",
        "number_of_cars",
        "offering",
        "tithe",
        "transfer",
        "financial_total",
        "date",
    )
    list_filter = ("service_day", "service_no", "date")
    readonly_fields = ("attendance_total", "financial_total")


@admin.register(HillChurch)
class HillChurchAdmin(BaseUnfoldAdmin):
    list_display = (
        "service_day",
        "service_no",
        "male",
        "female",
        "children",
        "attendance_total",
        "number_of_cars",
        "offering",
        "tithe",
        "transfer",
        "financial_total",
        "date",
    )
    list_filter = ("service_day", "service_no", "date")
    readonly_fields = ("attendance_total", "financial_total")



@admin.register(UserVerification)
class UserVerificationAdmin(BaseUnfoldAdmin):
    list_display = ('user', 'code', 'is_verified')
    search_fields = ('user__username', 'user__email')
    list_filter = ('is_verified',)
    readonly_fields = ('code',)

    def has_add_permission(self, request):
        # Prevent manual additions through the admin panel
        return False

    def has_change_permission(self, request, obj=None):
        # Allow changing is_verified (if needed), but not code
        return True