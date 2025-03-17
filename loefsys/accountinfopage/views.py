"""Module defining the views for accountinfopage."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from loefsys.users.models import MemberDetails, Membership


@login_required(login_url="signup_page")
def accountinfo(request):
    """View for loading the accountinformation page."""
    user_info = {
        "name": request.user.display_name,
        "email": request.user.email,
        "phone_number": request.user.phone_number,
        "picture": "",
        "activities": "",
        "groups": request.user.groups,
    }

    member_info = []
    qs_member = MemberDetails.objects.filter(user=request.user)
    if len(qs_member) > 1:
        raise Exception("User has multiple members")
    elif len(qs_member) == 1:
        member = qs_member[0]
        qs_membership = Membership.objects.filter(member=member)
        if len(qs_membership) == 1:
            membership = qs_membership[0]
            member_info = {
                "birthday": member.birthday,
                "picture": "",
                "member_since": membership.start,
                "year_of_joining": membership.start.year,
                "activities": "",
            }
        else:
            raise Exception("Member has no or more than one membership")

    return render(
        request,
        "accountinfopage.html",
        {"user_info": user_info},
        {"member_info": member_info},
    )
