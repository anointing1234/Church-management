def user_role(request):
    print("Context processor called")  # Debugging line
    
    # Define role groups matching your model ROLE_CHOICES keys
    ministry_roles = [
        "ministry_church_1",
        "ministry_church_2",
    ]

    membership_roles = [
        "membership_church_1",
        "membership_church_2",
    ]

    junior_church_roles = [
        "junior_church_1",
        "junior_church_2",
    ]

    multimedia_roles = [
        "multimedia_church_1",
        "multimedia_church_2",
    ]

    other_roles = [
        "social_media_report",
        "missions_team_summary",
        "sakponba_church",
        "uselu_church",
        "hill_church",
    ]

    if request.user.is_authenticated:
        user_role = request.user.role  # user's role string
        perms = request.user.get_all_permissions()
        return {
            'user_role': user_role,
            'user_permissions': perms,
            'ministry_roles': ministry_roles,
            'membership_roles': membership_roles,
            'junior_church_roles': junior_church_roles,
            'multimedia_roles': multimedia_roles,
            'other_roles': other_roles,
        }
    return {
        'user_role': None,
        'user_permissions': set(),
        'ministry_roles': ministry_roles,
        'membership_roles': membership_roles,
        'junior_church_roles': junior_church_roles,
        'multimedia_roles': multimedia_roles,
        'other_roles': other_roles,
    }
    
    
    
    


    
