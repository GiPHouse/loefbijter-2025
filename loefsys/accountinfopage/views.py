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
        "groups": request.user.groups.all(),
    }

    member_info = []
    qs_member = MemberDetails.objects.filter(user=request.user)
    if qs_member.count() == 1:
        member = qs_member[0]
        qs_membership = Membership.objects.filter(member=member)
        if qs_membership.count() > 0:
            membership = qs_membership[::-1][0]
            member_info = {
                "birthday": member.birthday.__str__(),
                "member_since": membership.start.__str__(),
                "year_of_joining": membership.start.year.__str__(),
                "activities": "",
            }
        else:
            raise Exception("Member has no membership")

    return render(
        request,
        "accountinfopage.html",
        {"user_info": user_info, "member_info": member_info},
    )
