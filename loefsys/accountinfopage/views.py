"""Module defining the views for accountinfopage."""

from django.shortcuts import render
from users.models import MemberDetails, Membership, NameMixin, User


def accountinfo(request):
    """View for loading the accountinformation page."""
    information = (
        {
            "name": NameMixin.display_name,
            "birthday": MemberDetails.birthday,
            "email": User.email,
            "phone_number": User.phone_number,
            "picture": "",
            "member_since": Membership.start,
            "year_of_joining": Membership.start.year,
            "activities": "",
            "groups": User.groups,
        },
    )
    return render(request, "accountinfopage.html", {"information": information})
